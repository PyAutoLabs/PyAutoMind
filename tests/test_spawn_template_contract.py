"""Contract between spawn's output and the workflows the template itself ships.

The template is not inert: it carries `.github/workflows/lifecycle_drift.yml`,
whose self-heal (PyAutoMind#116) regenerates `complete/index.md` on every push
to the template's own `main`. So spawn must produce every file those workflows
produce, or each sync is followed within seconds by a bot commit creating a file
the next `--check` calls drift — permanently red.

That is exactly what happened on 2026-08-04: sync `51f5ae58` at 17:28:51Z, bot
commit `79864dde` at 17:29:12Z, and the very next dispatch failed on
`only in published: complete/index.md`.

The same file also pins the **fresh-repo invariant** (spec rule 9, issue #121):
a workflow shipped into a template must be able to succeed on a freshly-spawned
repo with no secrets and no sibling repos. The published template had 13 failing
runs from inherited instance automation, and owner substitution does not help —
`YOURORG` is a literal placeholder, so its own `spawn_drift` run failed
`repository 'https://github.com/YOURORG/PyAutoMind/' not found`.

Both halves are the same idea: the template is a live repo with running
workflows, so spawn owns what those workflows do on arrival.
"""

import importlib.util
import re
import subprocess
from pathlib import Path

import pytest
import yaml

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

# A .github mirroring the real one: two self-contained/generic workflows and
# three pieces of instance automation (sibling repo lists, organ workflow
# names, org secrets, domain vocabulary).
GITHUB_FILES = {
    ".github/workflows/lifecycle_drift.yml": (
        "name: Lifecycle Drift\non:\n  push:\n    branches: [main]\n"
        "jobs:\n  drift:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - run: python3 scripts/lifecycle.py check\n"
    ),
    ".github/workflows/spawn_drift.yml": (
        "name: Spawn Drift\non:\n"
        "  schedule:\n    - cron: \"17 6 * * 1\"\n"
        "  pull_request:\n    paths:\n      - \"scripts/spawn.py\"\n"
        "  workflow_dispatch:\n\n"
        "jobs:\n  drift:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - run: git clone https://github.com/PyAutoLabs/PyAutoMind\n"
    ),
    ".github/workflows/morning_status.yml": (
        "name: digest\non:\n  schedule:\n    - cron: \"0 6 * * *\"\n"
        "jobs:\n  d:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - run: echo PyAutoLabs/PyAutoFit\n"
    ),
    ".github/workflows/morning_health.yml": (
        "name: health\non:\n  schedule:\n    - cron: \"0 7 * * *\"\n"
        "jobs:\n  h:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - run: gh api repos/PyAutoLabs/PyAutoHeart/actions/workflows/x.yml\n"
    ),
    ".github/workflows/arxiv_papers.yml": (
        "name: papers\non:\n  schedule:\n    - cron: \"0 8 * * *\"\n"
        "jobs:\n  p:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - env:\n          HOOK: ${{ secrets.PYAUTO_PAPERS_WEBHOOK_URL }}\n"
        "        run: echo x\n"
    ),
    ".github/scripts/arxiv_fetch.py": "QUERY = 'strong lensing OR lensed quasar'\n",
}

DROPPED_GITHUB = [
    ".github/workflows/morning_status.yml",
    ".github/workflows/morning_health.yml",
    ".github/workflows/arxiv_papers.yml",
    ".github/scripts/arxiv_fetch.py",
]


@pytest.fixture
def mind_with_github(tmp_path):
    mind = tmp_path / "PyAutoMind"
    _fake_repo(mind, {**MINIMAL_MIND, **GITHUB_FILES})
    out = tmp_path / "out"
    spawn.generate_mind(mind, out)
    return out


def _shipped_workflows(out):
    d = out / ".github" / "workflows"
    return sorted(d.glob("*.yml")) if d.exists() else []


def test_instance_automation_is_not_shipped(mind_with_github):
    """The 13 failing runs in the published template all came from these."""
    for rel in DROPPED_GITHUB:
        assert not (mind_with_github / rel).exists(), f"{rel} shipped into the template"


def test_generic_workflows_are_still_shipped(mind_with_github):
    """Guard the other direction — rule 9 must not over-drop."""
    names = {p.name for p in _shipped_workflows(mind_with_github)}
    assert names == {"lifecycle_drift.yml", "spawn_drift.yml"}, names


def test_no_shipped_workflow_runs_on_a_schedule(mind_with_github):
    """The fresh-repo invariant's teeth.

    A scheduled job that cannot succeed on a fresh org fails weekly and emails
    the new owner forever. Nothing shipped may auto-run.
    """
    for wf in _shipped_workflows(mind_with_github):
        spec = yaml.safe_load(wf.read_text())
        triggers = spec[True] if True in spec else spec.get("on", {})
        assert "schedule" not in (triggers or {}), f"{wf.name} still auto-runs"


def test_no_shipped_workflow_needs_a_configured_secret(mind_with_github):
    """`GITHUB_TOKEN` is auto-provided by Actions; anything else is org setup
    a freshly-spawned repo does not have."""
    for wf in _shipped_workflows(mind_with_github):
        for ref in re.findall(r"secrets\.([A-Za-z_][A-Za-z0-9_]*)", wf.read_text()):
            assert ref == "GITHUB_TOKEN", f"{wf.name} needs configured secret {ref}"


def test_a_new_mind_workflow_is_a_human_decision(tmp_path):
    """`.github` has NO catch-all rule, deliberately.

    A catch-all is fail-open: a workflow added to Mind later would ride it into
    the template carrying whatever schedule and secrets it has — the exact
    defect rule 9 exists to fix. This test wrote itself: an earlier draft kept
    a `.github/*` KEEP_SUB fallback and this case caught the schedule sailing
    straight through.

    Unmatched means spawn fails and a human adds an explicit rule 9 entry.
    """
    mind = tmp_path / "PyAutoMind"
    files = {**MINIMAL_MIND, **GITHUB_FILES}
    files[".github/workflows/brand_new_thing.yml"] = (
        "name: new\non:\n  schedule:\n    - cron: \"0 9 * * *\"\n"
        "jobs:\n  n:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - env:\n          K: ${{ secrets.SOME_ORG_SECRET }}\n"
        "        run: echo x\n"
    )
    _fake_repo(mind, files)
    out = tmp_path / "out"

    warns = spawn.generate_mind(mind, out)

    assert ".github/workflows/brand_new_thing.yml" in warns, (
        "a new .github file was classified silently — it must be UNMATCHED"
    )
    assert not (out / ".github" / "workflows" / "brand_new_thing.yml").exists()


def test_unscheduled_transform_fails_loudly_if_it_becomes_a_noop(tmp_path):
    """If spawn_drift ever loses its schedule upstream, the rule silently stops
    doing anything — that is how a guard rots. It must fail instead."""
    src = tmp_path / "spawn_drift.yml"
    src.write_text("name: x\non:\n  workflow_dispatch:\njobs: {}\n")
    with pytest.raises(SystemExit):
        spawn.unscheduled_workflow_body(src)


def test_unscheduled_transform_preserves_everything_else(tmp_path):
    """Structural strip: only the schedule block goes."""
    src = tmp_path / "spawn_drift.yml"
    src.write_text(GITHUB_FILES[".github/workflows/spawn_drift.yml"])

    spec = yaml.safe_load(spawn.unscheduled_workflow_body(src))
    triggers = spec[True] if True in spec else spec["on"]

    assert "schedule" not in triggers
    assert "workflow_dispatch" in triggers
    assert triggers["pull_request"]["paths"] == ["scripts/spawn.py"]
    assert list(spec["jobs"]) == ["drift"]


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
