#!/usr/bin/env python3
"""Direct-Editor CI; host success never implies Editor evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / 'ci/unity-matrix.yaml'  # JSON is a YAML 1.2 subset.

def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)

def select_release(payload, baseline):
    candidates = []
    for item in payload.get('results', []):
        match = re.fullmatch(r'(6000)\.(\d+)\.(\d+)([ab])(\d+)', item.get('version', ''))
        if not match or int(match[2]) <= int(baseline.split('.')[1]):
            continue
        for download in item.get('downloads', []):
            url = download.get('url', '')
            parsed = urllib.parse.urlparse(url)
            if (download.get('platform') == 'LINUX' and download.get('architecture') == 'X86_64'
                    and download.get('type') == 'TAR_XZ' and parsed.scheme == 'https'
                    and parsed.hostname in {'download.unity3d.com', 'beta.unity3d.com'}
                    and re.fullmatch(r'[a-fA-F0-9]+', item.get('shortRevision', ''))):
                candidates.append(((int(match[2]), int(match[3]), match[4], int(match[5])),
                                   dict(version=item['version'], changeset=item['shortRevision'], editor_url=url)))
    if not candidates:
        raise ValueError('No next-stream prerelease Linux Editor in official archive response')
    return max(candidates, key=lambda pair: pair[0])[1]

def resolve_release(baseline):
    # Iterate all pages: API order is release date, not semantic version order.
    results, offset = [], 0
    while True:
        query = urllib.parse.urlencode({'version': '6000', 'limit': 100, 'offset': offset,
                                       'order': 'RELEASE_DATE_DESC'})
        page = fetch('https://services.api.unity.com/unity/editor/release/v1/releases?' + query)
        rows = page.get('results', [])
        results.extend(rows)
        offset += len(rows)
        if not rows or offset >= page.get('total', offset):
            break
        if offset > 10000:
            raise ValueError('Archive pagination exceeded safety bound')
    return select_release({'results': results}, baseline)

def package_version(payload, editor):
    editor_pair = tuple(map(int, editor.split('.')[:2]))
    candidates = []
    for version, info in payload.get('versions', {}).items():
        if not re.fullmatch(r'17\.\d+\.\d+', version):
            continue
        minimum = info.get('unity', '')
        if not re.fullmatch(r'6000\.\d+', minimum):
            continue
        if tuple(map(int, minimum.split('.'))) != editor_pair:
            continue
        # unityRelease is a patch constraint: conservatively reject unknown forms.
        release = info.get('unityRelease', '0f1')
        match = re.fullmatch(r'(\d+)f(\d+)', release)
        current = re.fullmatch(r'6000\.\d+\.(\d+)f(\d+)', editor)
        if not match or not current:
            continue
        if minimum == '.'.join(editor.split('.')[:2]) and tuple(map(int, match.groups())) > tuple(map(int, current.groups())):
            continue
        candidates.append((tuple(map(int, version.split('.'))), version))
    if not candidates:
        raise ValueError('No stable SRP 17 package with compatible official Unity minimum')
    return max(candidates)[1]

def test_evidence(path):
    root = ET.parse(path).getroot()
    if root.tag != 'test-run' or root.get('result') != 'Passed':
        raise ValueError('Test run did not pass')
    cases = root.findall('.//test-case')
    if not cases or any(case.get('result') != 'Passed' for case in cases):
        raise ValueError('Zero, skipped, inconclusive, or failed test cases')
    if int(root.get('total', '-1')) != len(cases) or int(root.get('passed', '-1')) != len(cases):
        raise ValueError('Test totals disagree with passing test cases')
    for key in ('failed', 'skipped', 'inconclusive'):
        if int(root.get(key, '0')) != 0:
            raise ValueError('Nonpassing test count')
    return len(cases)

def stage_artist_tests(package_root, project):
    """Expose the baseline package's unassembled tests only in the disposable copy."""
    source = package_root / 'Tests/Editor'
    tests = sorted(source.rglob('*.cs'))
    if not tests:
        raise RuntimeError('Canonical full suite has no Artist Editor test sources')
    if list(source.rglob('*.asmdef')):
        return []  # Existing package assemblies are exposed through manifest.testables.
    destination = project / 'Assets/CiArtistPackageTests'
    destination.mkdir(parents=True, exist_ok=False)
    inventory = []
    for test in tests:
        target = destination / test.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(test, target)
        inventory.append({'source': str(test.relative_to(package_root)),
                          'sha256': hashlib.sha256(test.read_bytes()).hexdigest()})
    (destination / 'CiArtistPackageTests.asmdef').write_text(json.dumps({
        'name': 'UnityCi.ArtistPackage.Tests', 'references': ['DarumaPPAP.UnityArtist.Editor'],
        'includePlatforms': ['Editor'], 'optionalUnityReferences': ['TestAssemblies']}))
    return inventory

def download_editor(release, target):
    target.mkdir(parents=True, exist_ok=True)
    archive = target / 'editor.tar.xz'
    urllib.request.urlretrieve(release['editor_url'], archive)
    with tarfile.open(archive, 'r:xz') as bundle:
        bundle.extractall(target, filter='data')
    archive.unlink()
    editors = list(target.glob('**/Editor/Unity'))
    if len(editors) != 1:
        raise ValueError('Official archive does not contain one Editor/Unity')
    return editors[0]

def run(args):
    config = json.loads(MATRIX.read_text())
    fixture = next(row for row in config['fixtures'] if row['id'] == args.fixture)
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    # Never reuse a previous test result as evidence of this execution.
    for name in ('results.xml', 'editor.log', 'editor-version.txt', 'evidence.json',
                 'packages-lock.json', 'manifest.json', 'requested-manifest.json', 'srp-selection.json'):
        (output / name).unlink(missing_ok=True)
    evidence = dict(status='BLOCKED_NOT_RUN', observation='not_observed', fixture=fixture['id'],
                    project=fixture['project'], pipeline=fixture['pipeline'],
                    requested_editor=fixture['editor'], packages={}, srp_package=fixture.get('srp_package'),
                    package_policy=config['package_policy'], run_id=os.getenv('GITHUB_RUN_ID', 'local'),
                    run_attempt=os.getenv('GITHUB_RUN_ATTEMPT', '1'), reason='Editor not run')
    code = 2
    try:
        release = resolve_release(config['canonical_editor']) if args.canary else None
        version = release['version'] if release else fixture['editor']
        evidence['requested_editor'] = version
        if release:
            evidence['archive_release'] = release
        source = ROOT / fixture['project']
        manifest = json.loads((source / 'Packages/manifest.json').read_text())
        evidence['packages'] = manifest['dependencies'].copy()
        (output / 'requested-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        if os.getenv('UNITY_LICENSE_READY') != 'true':
            raise RuntimeError('Prelicensed runner required: set UNITY_LICENSE_READY=true only after licensing')
        executable = os.getenv('UNITY_EDITOR', '')
        if not executable:
            executable = str(Path(os.getenv('UNITY_EDITOR_ROOT', '/opt/unity')) / version / 'Editor/Unity')
        editor = Path(executable)
        if not editor.is_file() and release and os.getenv('UNITY_ALLOW_EDITOR_DOWNLOAD') == 'true':
            editor = download_editor(release, Path(os.getenv('RUNNER_TEMP', '/tmp')) / ('unity-ci-' + version))
        if not editor.is_file():
            raise RuntimeError('Exact Editor unavailable; configure UNITY_EDITOR_ROOT or direct UNITY_EDITOR')
        measured = subprocess.run([str(editor), '-version'], capture_output=True, text=True, timeout=60)
        (output / 'editor-version.txt').write_text(measured.stdout + measured.stderr)
        if measured.returncode or not re.search(r'(?<![\w.])' + re.escape(version) + r'(?![\w.])', measured.stdout):
            raise RuntimeError('Installed Editor version does not match requested exact version')
        evidence['observed_editor'] = version
        # Separate workspace copies preserve canonical source and leave no stale results.
        project = output / 'project'
        shutil.copytree(source, project, ignore=shutil.ignore_patterns('Library', 'Temp', 'Logs'), dirs_exist_ok=False)
        local_packages = {}
        for package, location in manifest['dependencies'].items():
            if location.startswith('file:'):
                target = (source / 'Packages' / location[5:]).resolve()
                if not target.is_dir():
                    raise RuntimeError('Missing local package: ' + package)
                local_packages[package] = target
                package_metadata = json.loads((target / 'package.json').read_text())
                if package_metadata.get('name') != package or not package_metadata.get('version'):
                    raise RuntimeError('Local package identity/version missing: ' + package)
                evidence.setdefault('local_package_versions', {})[package] = package_metadata['version']
                manifest['dependencies'][package] = 'file:' + str(target)
        if fixture.get('scope') == 'full':
            artist = 'com.darumappap.artist-subagent'
            if artist not in local_packages:
                raise RuntimeError('Canonical full suite requires local Artist package')
            manifest.setdefault('testables', [])
            if artist not in manifest['testables']:
                manifest['testables'].append(artist)
            evidence['staged_package_tests'] = stage_artist_tests(local_packages[artist], project)
        srp = fixture.get('srp_package')
        if srp:
            metadata = fetch('https://packages.unity.com/' + srp)
            selected = package_version(metadata, version)
            manifest['dependencies'][srp] = selected
            evidence['packages'][srp] = selected
            (output / 'srp-selection.json').write_text(json.dumps({'package': srp, 'version': selected,
                'source': 'https://packages.unity.com/' + srp, 'metadata': metadata['versions'][selected]}, indent=2))
        (project / 'Packages/manifest.json').write_text(json.dumps(manifest, indent=2))
        (project / 'ProjectSettings/ProjectVersion.txt').write_text('m_EditorVersion: ' + version + '\n')
        results, log = output / 'results.xml', output / 'editor.log'
        command = [str(editor), '-batchmode', '-nographics', '-projectPath', str(project), '-runTests',
                   '-testPlatform', 'EditMode', '-testResults', str(results), '-logFile', str(log)]
        if fixture.get('test_filter'):
            command.extend(['-testFilter', fixture['test_filter']])
        evidence['status'] = 'FAIL'
        evidence['observation'] = 'observed'
        completed = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3600)
        if completed.returncode:
            # Unity license faults mean no test execution, not an assertion failure.
            contents = log.read_text(errors='replace') if log.exists() else ''
            if not results.exists() and re.search(r'(?i)(no valid license|failed to activate|licensing.*(failed|error))', contents):
                evidence['status'] = 'BLOCKED_NOT_RUN'
                evidence['observation'] = 'not_observed'
                raise RuntimeError('Editor licensing unavailable; see editor.log')
            raise ValueError('Editor returned exit code ' + str(completed.returncode))
        evidence['tests_passed'] = test_evidence(results)
        if not log.is_file() or not log.stat().st_size:
            raise ValueError('Editor log missing')
        lock = project / 'Packages/packages-lock.json'
        if not lock.is_file():
            raise ValueError('Resolved package lock missing')
        shutil.copy2(lock, output / 'packages-lock.json')
        evidence['resolved_packages'] = json.loads(lock.read_text())['dependencies']
        for package, requested in manifest['dependencies'].items():
            resolved = evidence['resolved_packages'].get(package, {}).get('version')
            if not resolved or (not requested.startswith('file:') and resolved != requested):
                raise ValueError('Resolved package lock does not match requested exact dependency: ' + package)
        evidence['status'], evidence['reason'], code = 'PASS', 'Nonempty EditMode tests passed', 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        evidence['reason'] = str(error)
        code = 2 if evidence['status'] == 'BLOCKED_NOT_RUN' else 1
    finally:
        project = output / 'project'
        if project.exists():
            for name in ('manifest.json', 'packages-lock.json'):
                path = project / 'Packages' / name
                if path.exists():
                    shutil.copy2(path, output / name)
            shutil.rmtree(project)
        if not (output / 'editor.log').exists():
            (output / 'editor.log').write_text('BLOCKED_NOT_RUN: ' + evidence['reason'] + '\n')
        evidence['artifact_hashes'] = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                      for path in output.iterdir() if path.is_file()}
        (output / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
        summary = os.getenv('GITHUB_STEP_SUMMARY')
        if summary:
            with open(summary, 'a') as stream:
                stream.write(f"Unity {fixture['id']}: **{evidence['status']}** — {evidence['reason']}\n")
        print(f"{fixture['id']}: {evidence['status']} ({evidence['reason']})")
    return code

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--canary', action='store_true')
    sys.exit(run(parser.parse_args()))
