import json
import os
from pathlib import Path
import tempfile
import unittest
import argparse
import subprocess
from unittest.mock import patch
import unity_ci as ci

class ReleaseResolverTests(unittest.TestCase):
    def release(self, version='6000.7.0a9', url='https://download.unity3d.com/x/editor.tar.xz'):
        return dict(version=version, shortRevision='abc123', downloads=[dict(platform='LINUX',architecture='X86_64',type='TAR_XZ',url=url)])

    def test_latest_numeric_prerelease_next_stream(self):
        rows=[self.release('6000.7.0a9'), self.release('6000.7.0a10'),self.release('6000.6.0b99'),self.release('6000.8.0f1')]
        self.assertEqual(ci.select_release({'results':rows},'6000.6.0f1')['version'],'6000.7.0a10')

    def test_stable_wrong_stream_missing_archive_untrusted_url_rejected(self):
        for row in [self.release('6000.6.0b1'), self.release('6000.7.0f1'), self.release(url='https://evil.test/archive'), self.release(url='http://download.unity3d.com/editor')]:
            with self.subTest(row=row),self.assertRaises(ValueError):
                ci.select_release({'results':[row]},'6000.6.0f1')
        row=self.release();row['downloads'][0]['architecture']='ARM64'
        with self.assertRaises(ValueError):ci.select_release({'results':[row]},'6000.6.0f1')

    def test_pagination_not_first_row_assumption(self):
        pages=[{'results':[self.release('6000.7.0a9')],'total':2},{'results':[self.release('6000.7.0a10')],'total':2}]
        with patch.object(ci,'fetch',side_effect=pages) as fetch:
            self.assertEqual(ci.resolve_release('6000.6.0f1')['version'],'6000.7.0a10')
            self.assertIn('offset=1',fetch.call_args.args[0])

class RegistryTests(unittest.TestCase):
    def test_exact_stream_stable_minimum_patch(self):
        payload={'versions':{'17.6.1':{'unity':'6000.6','unityRelease':'0f1'},
            '17.6.2':{'unity':'6000.6','unityRelease':'1f1'},
            '17.6.3-pre.1':{'unity':'6000.6'},'17.7.0':{'unity':'6000.7'},
            '17.5.9':{'unity':'6000.5'}}}
        self.assertEqual(ci.package_version(payload,'6000.6.0f1'),'17.6.1')
    def test_no_exact_stream_rejected(self):
        with self.assertRaises(ValueError):
            ci.package_version({'versions':{'17.5.0':{'unity':'6000.5'}}},'6000.6.0f1')

class EvidenceTests(unittest.TestCase):
    def evaluate(self,xml):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'results.xml';path.write_text(xml)
            return ci.test_evidence(path)
    def test_nonempty_pass(self):
        self.assertEqual(self.evaluate('<test-run result="Passed" total="1" passed="1"><test-case result="Passed"/></test-run>'),1)
    def test_zero_skipped_failed_inconclusive_bad_totals_rejected(self):
        examples=['<test-run result="Passed" total="0" passed="0"/>',
          '<test-run result="Passed" total="1" passed="1"><test-case result="Skipped"/></test-run>',
          '<test-run result="Passed" total="1" passed="1"><test-case result="Inconclusive"/></test-run>',
          '<test-run result="Failed" total="1" passed="0"><test-case result="Failed"/></test-run>',
          '<test-run result="Passed" total="2" passed="2"><test-case result="Passed"/></test-run>',
          '<test-run result="Passed" total="1" passed="1" skipped="1"><test-case result="Passed"/></test-run>']
        for xml in examples:
            with self.subTest(xml=xml),self.assertRaises(ValueError):self.evaluate(xml)

    def test_missing_license_generates_blocked_artifacts_not_pass(self):
        import argparse
        with tempfile.TemporaryDirectory() as temporary, patch.dict(os.environ,{'UNITY_LICENSE_READY':'false'}):
            args=argparse.Namespace(fixture='minimal-6000.6',output=temporary,canary=False)
            self.assertEqual(ci.run(args),2)
            evidence=json.loads((Path(temporary)/'evidence.json').read_text())
            self.assertEqual(evidence['status'],'BLOCKED_NOT_RUN')
            self.assertEqual(evidence['requested_editor'],'6000.6.0f1')
            self.assertIn('com.unity.pipeline',evidence['packages'])
            self.assertTrue((Path(temporary)/'editor.log').exists())
            self.assertNotIn('tests_passed',evidence)

class TestStagingTests(unittest.TestCase):
    def test_canonical_discovers_existing_unassembled_tests_in_disposable_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); package = root/'package'; project = root/'project'
            source = package/'Tests/Editor'; source.mkdir(parents=True)
            test = source/'ExistingTests.cs'; test.write_text('class ExistingTests {}')
            inventory = ci.stage_artist_tests(package, project)
            self.assertEqual(len(inventory),1)
            self.assertTrue((project/'Assets/CiArtistPackageTests/CiArtistPackageTests.asmdef').is_file())
            self.assertEqual(test.read_text(),'class ExistingTests {}')
            self.assertFalse((source/'CiArtistPackageTests.asmdef').exists())

class RunnerTests(unittest.TestCase):
    def run_fake(self, mode):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / 'fixture'
            (project / 'Packages').mkdir(parents=True)
            (project / 'ProjectSettings').mkdir()
            (project / 'Packages/manifest.json').write_text('{"dependencies":{"com.unity.test-framework":"1.3.9"}}')
            (project / 'ProjectSettings/ProjectVersion.txt').write_text('m_EditorVersion: 6000.6.0f1')
            matrix = root / 'matrix.yaml'
            matrix.write_text(json.dumps({'canonical_editor':'6000.6.0f1','package_policy':'test',
                'fixtures':[{'id':'fake','project':'fixture','pipeline':'builtin','editor':'6000.6.0f1'}]}))
            output = root / 'artifacts'; output.mkdir()
            # A prior successful result must never satisfy a new run.
            (output / 'results.xml').write_text('<test-run result="Passed" total="1" passed="1"><test-case result="Passed"/></test-run>')
            def execute(command, **kwargs):
                if '-version' in command:
                    return subprocess.CompletedProcess(command,0,'6000.6.0f1','')
                log = Path(command[command.index('-logFile')+1])
                if mode == 'license':
                    log.write_text('No valid license found')
                    return subprocess.CompletedProcess(command,1)
                log.write_text('Editor test execution')
                if mode == 'pass':
                    Path(command[command.index('-testResults')+1]).write_text('<test-run result="Passed" total="1" passed="1"><test-case result="Passed"/></test-run>')
                    copied = Path(command[command.index('-projectPath')+1])
                    (copied / 'Packages/packages-lock.json').write_text('{"dependencies":{"com.unity.test-framework":{"version":"1.3.9"}}}')
                return subprocess.CompletedProcess(command,0)
            with patch.object(ci,'ROOT',root), patch.object(ci,'MATRIX',matrix), patch.object(ci.subprocess,'run',side_effect=execute), patch.dict(os.environ,{'UNITY_EDITOR':'/bin/true','UNITY_LICENSE_READY':'true'}):
                code = ci.run(argparse.Namespace(fixture='fake',output=str(output),canary=False))
            return code, json.loads((output / 'evidence.json').read_text())
    def test_stale_result_is_removed(self):
        code,evidence=self.run_fake('missing-results')
        self.assertEqual(code,1);self.assertEqual(evidence['status'],'FAIL')
    def test_license_fault_is_blocked(self):
        code,evidence=self.run_fake('license')
        self.assertEqual(code,2);self.assertEqual(evidence['status'],'BLOCKED_NOT_RUN')
    def test_observed_pass_requires_results_log_lock_and_exact_editor(self):
        code,evidence=self.run_fake('pass')
        self.assertEqual(code,0);self.assertEqual(evidence['tests_passed'],1)
        self.assertEqual(evidence['observed_editor'],'6000.6.0f1')
        self.assertIn('packages-lock.json',evidence['artifact_hashes'])

class FixtureTests(unittest.TestCase):
    def test_fixtures_have_tests_scene_metadata_and_correct_local_package_path(self):
        config=json.loads(ci.MATRIX.read_text())
        for row in config['fixtures'][1:]:
            project=ci.ROOT/row['project']
            manifest=json.loads((project/'Packages/manifest.json').read_text())
            location=manifest['dependencies']['com.darumappap.artist-subagent'][5:]
            self.assertEqual((project/'Packages'/location).resolve(),ci.ROOT/'Packages/com.darumappap.artist-subagent')
            self.assertIn('[Test]',(project/'Assets/Editor/SmokeTests.cs').read_text())
            for asset in (project/'Assets').rglob('*'):
                if asset.suffix!='.meta':self.assertTrue(Path(str(asset)+'.meta').is_file(),asset)
            if row['scope']=='scene-native-api-smoke':
                scene=(project/'Assets/Scenes/PipelineSmoke.unity').read_text()
                self.assertIn('m_Name: Main Camera',scene)
                self.assertIn('m_Name: FovSubject',scene)
                self.assertIn('m_Name: Key Light',scene)

if __name__=='__main__': unittest.main()
