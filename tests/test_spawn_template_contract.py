"""Contract between spawn's output and the workflows the template itself ships.

The template is not inert: it carries `.github/workflows/lifecycle_drift.yml`,
whose self-heal (PyAutoMind#116) regenerates `complete/index.md` on every push
to the template's own `main`. So spawn must produce every file those workflows
produce, or each sync is followed within seconds by a bot commit creating a file
the next `--check` calls drift — permanently red.

That is exactly what happened on 2026-08-04: sync `51f5ae58` at 17:28:51Z, bot
commit `79864dde` at 17:29:12Z, and the very next dispatch failed on
`only in published: complete/index.md`.
"""

import importlib.util
import subprocess
from pathlib import Path

import pytest

SPAWN_PY = Path(__file__).resolve().parents[1] / "scripts" / "spawn.py"

_spec = importlib.util.spec_from_file_location("spawn_contract", SPAWN_PY)
spawn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(spawn)

# A stub standing in for the real lifecycle.py: spawn must INVOKE the generated
# tree's own copy, so a stub that leaves a sentinel proves the wiring without
# depending on the real index format.
STUB_LIFECYCLE = """\
import sys, pathlib
if sys.argv[1:] == ["index", "--apply"]:
    p = pathlib.Path(__file__).resolve().parent.parent / "complete" / "index.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("STAMPED-BY-LIFECYCLE\\n")
"""


def _fake_repo(root, files):
    root.mkdir(parents=True, exist_ok=True)
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e.invalid",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e.invalid",
           "PATH": "/usr/bin:/bin", "HOME": str(root)}
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, env=env)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, env=env)
    subprocess.run(["git", "commit", "-q", "-m", "t"], cwd=root, check=True, env=env)


MINIMAL_MIND = {
    "README.md": "# Mind\n", "AGENTS.md": "# A\n", "CLAUDE.md": "# C\n",
    "REFERENCE.md": "# R\n", "ROUTING.md": "# Ro\n", "LICENSE": "MIT\n",
    ".gitignore": "tmp/\n", "AI_POLICY.md": "p\n", "CONTRIBUTING.md": "c\n",
    "repos.yaml": "repos: {}\n",
    "active.md": "# Active Tasks\n", "planned.md": "# Planned\n",
    "parked.md": "# Parked\n", "condemned.md": "# Condemned\n",
    "ideas.md": "# Ideas\n", "queue.md": "# Queue\n",
    "autonomy_log.md": "| a | b |\n|---|---|\n| x | y |\n",
    "complete/AGENTS.md": "# schema\n",
    "scripts/lifecycle.py": STUB_LIFECYCLE,
}


def test_spawn_stamps_the_templates_complete_index(tmp_path):
    """spawn must run the GENERATED tree's own lifecycle.py, not the live one."""
    mind = tmp_path / "PyAutoMind"
    _fake_repo(mind, MINIMAL_MIND)
    out = tmp_path / "out"

    spawn.generate_mind(mind, out)

    index = out / "complete" / "index.md"
    assert index.exists(), "complete/index.md not stamped — drift loop reopens"
    assert index.read_text() == "STAMPED-BY-LIFECYCLE\n", (
        "index was not produced by the generated tree's own lifecycle.py"
    )


def test_live_complete_index_is_never_copied(tmp_path):
    """Rule 7 still DROPs the live index; 6c stamps a fresh empty one.

    A fresh-slate template must not inherit the live archive's index — that
    would be a wall of instance task slugs.
    """
    mind = tmp_path / "PyAutoMind"
    files = dict(MINIMAL_MIND)
    files["complete/index.md"] = "LIVE-ARCHIVE-INDEX with instance slugs\n"
    files["complete/2026/07/rec.md"] = "a live record\n"
    _fake_repo(mind, files)
    out = tmp_path / "out"

    spawn.generate_mind(mind, out)

    text = (out / "complete" / "index.md").read_text()
    assert "LIVE-ARCHIVE-INDEX" not in text
    assert not (out / "complete" / "2026").exists()


def test_stamping_is_skipped_when_lifecycle_is_not_kept(tmp_path):
    """If the rules ever stop KEEPing lifecycle.py, spawn must not crash."""
    mind = tmp_path / "PyAutoMind"
    files = {k: v for k, v in MINIMAL_MIND.items() if k != "scripts/lifecycle.py"}
    _fake_repo(mind, files)
    out = tmp_path / "out"

    spawn.generate_mind(mind, out)  # must not raise

    assert not (out / "complete" / "index.md").exists()
