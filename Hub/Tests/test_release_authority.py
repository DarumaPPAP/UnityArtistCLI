from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Tools'))
from validate_repository import public_release_workflows

class ReleaseAuthorityTests(unittest.TestCase):
    def test_prerelease_canary_is_observation_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'unity-prerelease-canary.yml').write_text('permissions:\n  contents: read\njobs:\n  observe:\n    steps:\n      - run: python ci/verify/unity_ci.py --canary\n')
            self.assertEqual([],public_release_workflows(root))
            (root/'release.yml').write_text('permissions:\n  contents: read\n')
            self.assertEqual(['release.yml'],public_release_workflows(root))
    def test_release_publish_rejected_even_with_canary_or_unrelated_name(self):
        unsafe=('uses: softprops/action-gh-release@v2','run: gh release create v1.0.0','run: gh release upload v1.0.0 artifact','run: gh api repos/owner/repo/releases --method POST','run: gh api --method POST repos/owner/repo/releases','run: gh api -XPOST repos/owner/repo/releases','run: gh api -X POST repos/owner/repo/releases','run: gh api repos/owner/repo/releases -f tag_name=v1.0.0')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for filename in ('unity-prerelease-canary.yml','publish.yml'):
                for step in unsafe:
                    with self.subTest(filename=filename,step=step):
                        (root/filename).write_text('permissions:\n  contents: read\njobs:\n  publish:\n    steps:\n      - '+step+'\n')
                        self.assertIn(filename,public_release_workflows(root))
                (root/filename).unlink()
            (root/'unity-prerelease-canary.yml').write_text('permissions:\n  contents: write\n')
            self.assertIn('unity-prerelease-canary.yml',public_release_workflows(root))
    def test_invalid_canary_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'unity-prerelease-canary.yml').write_text('bad: [')
            self.assertEqual(['unity-prerelease-canary.yml'],public_release_workflows(root))
if __name__=='__main__':unittest.main()
