import json
import os
import re
import unittest

from _load import REPO, ROOT

PHASES = ["recon", "architect", "design", "build", "backend", "test", "diff",
          "entrepreneur", "brand", "launch", "deploy"]
SKILLS = ["replica-" + p for p in PHASES]


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


class Repo(unittest.TestCase):
    def test_skill_folders_at_the_root(self):
        found = sorted(d for d in os.listdir(ROOT)
                       if os.path.isfile(os.path.join(ROOT, d, "SKILL.md")))
        for s in SKILLS + ["replica-crew"]:
            self.assertIn(s, found)
        self.assertGreaterEqual(len(found), 27)

    def test_every_skill_name_is_valid_and_unique(self):
        names = []
        for d in os.listdir(ROOT):
            path = os.path.join(ROOT, d, "SKILL.md")
            if not os.path.isfile(path):
                continue
            fm, _ = frontmatter(path)
            m = re.search(r"^name:\s*['\"]?([^'\"\n]+)", fm, re.M)
            self.assertTrue(m, d)
            self.assertRegex(m.group(1).strip(), r"^[a-z0-9][a-z0-9-]*$", d)
            self.assertIn("description:", fm, d)
            names.append(m.group(1).strip())
        self.assertEqual(len(names), len(set(names)))

    def test_bundled_skills_keep_license_and_source(self):
        for d in os.listdir(ROOT):
            if d.startswith("replica-") or not os.path.isdir(os.path.join(ROOT, d)):
                continue
            for f in ("LICENSE.upstream", "UPSTREAM.md"):
                self.assertTrue(os.path.isfile(os.path.join(ROOT, d, f)), "%s/%s" % (d, f))

    def test_skill_frontmatter(self):
        for s in SKILLS + ["replica-crew"]:
            fm, text = frontmatter(os.path.join(ROOT, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertGreater(len(fm), 200, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 60, s)

    def test_one_agent_per_skill_preloading_it(self):
        agents = os.path.join(REPO, "agents")
        self.assertEqual(sorted(os.listdir(agents)), sorted(s + ".md" for s in SKILLS))
        for s in SKILLS:
            fm, _ = frontmatter(os.path.join(agents, s + ".md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertIn("  - %s\n" % s, fm, s)
            self.assertIn("disallowedTools: Agent", fm, s)

    def test_codex_agents_parse(self):
        import tomllib
        agents = os.path.join(REPO, "codex", "agents")
        self.assertEqual(sorted(os.listdir(agents)), sorted(s + ".toml" for s in SKILLS))
        for s in SKILLS:
            with open(os.path.join(agents, s + ".toml"), "rb") as fh:
                d = tomllib.load(fh)
            self.assertEqual(d["name"], s)
            self.assertIn("$%s" % s, d["developer_instructions"])
            self.assertTrue(d["description"])

    def test_orchestrator_mentions_every_phase(self):
        with open(os.path.join(ROOT, "replica-crew", "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        for p in PHASES:
            self.assertIn(p, text, p)

    def test_plugin_manifests(self):
        with open(os.path.join(REPO, ".claude-plugin", "plugin.json")) as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "replica-crew")
        self.assertEqual(plugin["skills"], "./skills/")
        with open(os.path.join(REPO, "plugin.json")) as fh:
            self.assertEqual(json.load(fh)["name"], "replica-crew")
        with open(os.path.join(REPO, ".agents", "plugins", "marketplace.json")) as fh:
            self.assertEqual(json.load(fh)["plugins"][0]["name"], "replica-crew")
        with open(os.path.join(REPO, ".claude-plugin", "marketplace.json")) as fh:
            market = json.load(fh)
        self.assertEqual(market["plugins"][0]["name"], "replica-crew")

    def test_readme_lists_agents_and_credits_upstream(self):
        with open(os.path.join(REPO, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
        self.assertIn("Jakeschincariol/replica-skill", readme)
        for s in SKILLS:
            self.assertIn("`%s`" % s, readme)

    def test_no_em_dashes_anywhere(self):
        bad = []
        for dirpath, dirnames, filenames in os.walk(REPO):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "node_modules")]
            if os.path.isfile(os.path.join(dirpath, "UPSTREAM.md")):
                dirnames[:] = []
                continue
            for fn in filenames:
                if fn.endswith((".md", ".py", ".json", ".ts", ".csv", ".txt")):
                    path = os.path.join(dirpath, fn)
                    with open(path, encoding="utf-8") as fh:
                        if chr(0x2014) in fh.read():
                            bad.append(os.path.relpath(path, REPO))
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
