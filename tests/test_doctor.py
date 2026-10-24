import os
import sys
import unittest

from _load import ROOT

sys.path.insert(0, os.path.join(ROOT, "replica-capabilities"))
import doctor  # noqa: E402


class Doctor(unittest.TestCase):
    def test_every_target_needs_only_known_tools(self):
        known = set(doctor.TOOLS)
        for name, (need_all, need_any, note) in doctor.TARGETS.items():
            for t in need_all:
                self.assertIn(t, known, "%s: %s" % (name, t))
            for grp in need_any:
                for t in grp:
                    self.assertIn(t, known, "%s: %s" % (name, t))
            self.assertTrue(note)

    def test_stub_output_counts_as_absent(self):
        # the probe filters Windows app-alias stubs; simulate by monkeypatching
        import subprocess

        class FakeRun:
            stdout = "Python was not found; run without arguments to install"
            stderr = ""
            returncode = 9009

        orig_which, orig_run = doctor.shutil.which, subprocess.run
        doctor.shutil.which = lambda t: "C:/fake/python3.exe"
        subprocess.run = lambda *a, **k: FakeRun()
        try:
            present, ver = doctor.probe("python3")
        finally:
            doctor.shutil.which, subprocess.run = orig_which, orig_run
        self.assertFalse(present)
        self.assertIsNone(ver)

    def test_scan_shape(self):
        info = doctor.scan()
        for key in ("os", "cpus", "tools", "targets"):
            self.assertIn(key, info)
        self.assertEqual(set(info["targets"]), set(doctor.TARGETS))
        for t in info["targets"].values():
            self.assertIn("ready", t)
            self.assertIsInstance(t["ready"], bool)
            self.assertIsInstance(t["needs"], list)

    def test_json_main_runs(self):
        self.assertEqual(doctor.main(["--json"]), 0)
        self.assertEqual(doctor.main(["--target", "android"]), 0)


if __name__ == "__main__":
    unittest.main()
