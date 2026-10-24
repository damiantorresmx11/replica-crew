import os
import subprocess
import tempfile
import unittest

from _load import ROOT

SCRIPT = os.path.join(ROOT, "faithful-capture", "capture.mjs")
URL = "https://example.com/"


def run(args, cwd):
    return subprocess.run(["node", SCRIPT] + args, cwd=cwd,
                          capture_output=True, text=True)


@unittest.skipIf(not __import__("shutil").which("node"), "node not on PATH")
class Gate(unittest.TestCase):
    def test_refuses_without_authorization(self):
        with tempfile.TemporaryDirectory() as d:
            r = run([URL], d)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("no authorization", (r.stdout + r.stderr).lower())

    def test_flag_grants_authorization(self):
        # authorized but single-file-cli absent -> it must pass the gate and
        # then fail later on the missing tool / chrome, not on authorization.
        with tempfile.TemporaryDirectory() as d:
            r = run([URL, "--i-have-authorization"], d)
            out = (r.stdout + r.stderr).lower()
            self.assertIn("authorization = flag", out)
            self.assertNotIn("no authorization", out)

    def test_scope_file_grants_authorization(self):
        with tempfile.TemporaryDirectory() as d:
            scope = os.path.join(d, "scope.md")
            with open(scope, "w") as fh:
                fh.write("# Scope\nownership: yes\n## Authorization\nI own it.\n")
            r = run([URL, "--scope", scope], d)
            out = (r.stdout + r.stderr).lower()
            self.assertIn("authorization =", out)
            self.assertNotIn("no authorization", out)

    def test_bad_url_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            r = run(["not-a-url", "--i-have-authorization"], d)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("http(s) url", (r.stdout + r.stderr).lower())


if __name__ == "__main__":
    unittest.main()
