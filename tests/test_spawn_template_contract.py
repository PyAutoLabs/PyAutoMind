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
import sys
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
    ".gitignore": "tmp/\n",
    "AI_POLICY.md": "p\n", "CONTRIBUTING.md": "c\n",
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
# The two workflows Mind really ships are read from disk, NOT hand-copied
# miniatures. A stale miniature is how the PAT_PYAUTOLABS reference slipped
# past `test_no_shipped_workflow_needs_a_configured_secret` in #125: the real
# spawn_drift.yml had grown a self-heal step the fixture knew nothing about.
_REAL_WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"


def _real(name):
    return (_REAL_WORKFLOWS / name).read_text()


GITHUB_FILES = {
    ".github/workflows/lifecycle_drift.yml": _real("lifecycle_drift.yml"),
    ".github/workflows/spawn_drift.yml": _real("spawn_drift.yml"),
    ".github/workflows/dashboard_refresh.yml": _real("dashboard_refresh.yml"),
    ".github/workflows/registry_reconcile.yml": _real("registry_reconcile.yml"),
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
    ".github/workflows/firewall_gate.yml": _real("firewall_gate.yml"),
    ".github/workflows/pages_dashboard.yml": _real("pages_dashboard.yml"),
    ".github/scripts/arxiv_fetch.py": "QUERY = 'strong lensing OR lensed quasar'\n",
    ".github/workflows/arxiv_interests.yml": (
        "name: interests\non:\n  schedule:\n    - cron: \"30 2 * * 1-5\"\n"
        "jobs:\n  i:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - env:\n          PAT: ${{ secrets.PAT_PYAUTOLABS }}\n"
        "        run: echo x\n"
    ),
    ".github/scripts/arxiv_interests.py": "CATEGORIES = ('astro-ph.CO',)\n",
}

DROPPED_GITHUB = [
    ".github/workflows/spawn_drift.yml",     # rule 9b, revised to DROP in #125
    # rule 9c: checks out PyAutoLabs/PyAutoBrain for the dashboard renderer,
    # which a freshly-spawned org does not have.
    ".github/workflows/dashboard_refresh.yml",
    # rule 9c: the online lifecycle leg — scheduled, and reads sibling-repo
    # issue/PR state, so it can neither auto-run nor succeed on a fresh org.
    ".github/workflows/registry_reconcile.yml",
    ".github/workflows/morning_status.yml",
    ".github/workflows/morning_health.yml",
    ".github/workflows/arxiv_papers.yml",
    # rule 9c: checks out three sibling organ repos by name — dashboard_refresh's
    # failure mode three times over. Added 2026-08, first caught by the
    # 2026-08-24 spawn_drift run as UNMATCHED.
    ".github/workflows/firewall_gate.yml",
    # rule 9c: needs a GitHub Pages site the default token cannot create on a
    # fresh repo, and takes pages:write + id-token:write.
    ".github/workflows/pages_dashboard.yml",
    ".github/scripts/arxiv_fetch.py",
    ".github/workflows/arxiv_interests.yml",
    ".github/scripts/arxiv_interests.py",
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


def test_no_tracked_file_is_unmatched_by_mind_rules():
    """Every file in the LIVE Mind tree must have an explicit MIND_RULES entry.

    Every other test here builds a synthetic tree, so it only covers the file
    classes somebody remembered to add to the fixture. That is how
    `firewall_gate.yml`, `pages_dashboard.yml` and `dashboard.html` reached
    main unclassified and sat there until the 2026-08-24 weekly drift run
    failed on them: nothing at PR time ever looked at the real file list.

    This reads the real tracked files instead, so a new file class fails the
    PR that adds it rather than the next Monday cron. It is the same condition
    the drift job reports as UNMATCHED / exit 2, minus the clones — the `drift`
    job is skipped on pull_request, so this hermetic check is the only
    PR-time guard there is.

    MEMORY_RULES cannot be checked from here (PyAutoMemory is not a sibling in
    this checkout); it stays covered by the weekly run.
    """
    repo = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        pytest.skip("not a git checkout")
    tracked = [f for f in proc.stdout.split("\0") if f]
    assert tracked, "git ls-files returned nothing — wrong root?"

    unmatched = [
        f for f in tracked if spawn.match_rule(Path(f), spawn.MIND_RULES)[1] is None
    ]
    assert not unmatched, (
        "these tracked files match no MIND_RULES entry, so spawn cannot decide "
        "whether they travel into the template. Extend the spec's tables "
        "(docs/pyautobrain/spawn_spec.md), then mirror the decision into "
        f"MIND_RULES: {unmatched}"
    )


def test_instance_automation_is_not_shipped(mind_with_github):
    """The 13 failing runs in the published template all came from these."""
    for rel in DROPPED_GITHUB:
        assert not (mind_with_github / rel).exists(), f"{rel} shipped into the template"


def test_generic_workflows_are_still_shipped(mind_with_github):
    """Guard the other direction — rule 9 must not over-drop."""
    names = {p.name for p in _shipped_workflows(mind_with_github)}
    assert names == {"lifecycle_drift.yml"}, names


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


MINIMAL_MEMORY = {
    "README.md": "# Mem\n", "AGENTS.md": "# A\n", "CLAUDE.md": "# C\n",
    "LICENSE": "MIT\n", ".gitignore": "tmp/\n", "Makefile": "all:\n",
    "AI_POLICY.md": "p\n", "CONTRIBUTING.md": "c\n",
    "index.md": "# Index\n", "reading-queue.md": "# Reading queue\n",
    "bibliography/README.md": "# Bib\n",
    "wiki/CLAUDE.md": "# schema\n",
    ".github/workflows/validate.yml": (
        "name: validate\non:\n  push:\n    branches: [main]\n"
        "jobs:\n  v:\n    runs-on: ubuntu-latest\n    steps:\n      - run: make validate\n"
    ),
}


def test_memory_github_is_also_fail_closed(tmp_path):
    """MEMORY_RULES has no `.github` catch-all either.

    Closing one fail-open door and leaving the other is a half-fix, and every
    other workflow test here drives generate_mind — so without this, reverting
    Memory's rule to a catch-all would go unnoticed.
    """
    mem = tmp_path / "PyAutoMemory"
    files = dict(MINIMAL_MEMORY)
    files[".github/workflows/some_new_memory_job.yml"] = (
        'name: new\non:\n  schedule:\n    - cron: "0 9 * * *"\njobs: {}\n'
    )
    _fake_repo(mem, files)
    out = tmp_path / "out"

    warns = spawn.generate_memory(mem, out)

    assert ".github/workflows/some_new_memory_job.yml" in warns
    assert not (out / ".github" / "workflows" / "some_new_memory_job.yml").exists()
    # …and the known-good one still ships.
    assert (out / ".github" / "workflows" / "validate.yml").exists()


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


def _workspace_with_published(tmp_path, mind_files=None, published_edit=None):
    """A CI-shaped layout: live repos plus a `published/` copy of the templates."""
    mind = tmp_path / "PyAutoMind"
    _fake_repo(mind, {**MINIMAL_MIND, **GITHUB_FILES, **(mind_files or {})})
    _fake_repo(tmp_path / "PyAutoMemory", MINIMAL_MEMORY)
    published = tmp_path / "published"
    published.mkdir()
    subprocess.run(
        [sys.executable, str(SPAWN_PY), "--root", str(tmp_path), "--write", str(published)],
        check=False, capture_output=True,
    )
    if published_edit:
        published_edit(published)
    return published


def _check_exit(tmp_path, published):
    return subprocess.run(
        [sys.executable, str(SPAWN_PY), "--root", str(tmp_path), "--check", str(published)],
        capture_output=True, text=True,
    ).returncode


def test_check_exit_codes_are_the_self_heal_contract(tmp_path):
    """`Spawn Drift`'s self-heal branches on these; collapsing them is unsafe.

    0 clean · 1 content drift (safe to propose) · 2 unsafe tree (human decision).
    A canary hit must never reach the PR path — that would automate publishing
    a leak, which is #118 with a robot doing it.
    """
    published = _workspace_with_published(tmp_path)
    assert _check_exit(tmp_path, published) == spawn.EXIT_CLEAN

    # Content drift only.
    (published / "PyAutoMind-template" / "README.md").write_text("drifted\n")
    assert _check_exit(tmp_path, published) == spawn.EXIT_DRIFT


def test_the_workflow_only_proposes_on_the_drift_code():
    """Pin the CONSUMER against the producer, not the producer against itself.

    Every other exit-code test compares a subprocess result with constants
    imported from the same module, so swapping `EXIT_DRIFT` and `EXIT_UNSAFE`
    would leave them all green while the workflow still auto-proposed literal
    exit 1 — now the unsafe one. This reads the real workflow.
    """
    wf = yaml.safe_load(_real("spawn_drift.yml"))
    steps = {s.get("name"): s for s in wf["jobs"]["drift"]["steps"]}
    propose = steps["Propose the sync PR"]

    assert propose["if"] == f"steps.diff.outputs.code == '{spawn.EXIT_DRIFT}'", (
        "the PR step must trigger on EXIT_DRIFT and nothing else — "
        f"got {propose['if']!r} against EXIT_DRIFT={spawn.EXIT_DRIFT}"
    )
    for unsafe in (spawn.EXIT_UNSAFE, spawn.EXIT_CRASH):
        assert f"'{unsafe}'" not in propose["if"], (
            f"exit {unsafe} must never reach the proposal step"
        )


def test_the_workflow_handles_every_exit_code_it_can_see():
    """An unhandled code must hit the catch-all, not fall through silently."""
    diff_step = next(
        s for s in yaml.safe_load(_real("spawn_drift.yml"))["jobs"]["drift"]["steps"]
        if s.get("name") == "Regenerate + diff"
    )
    run = diff_step["run"]
    arms = set(re.findall(r"^\s*([0-9]+|\*)\)", run, re.MULTILINE))
    for code in (spawn.EXIT_CLEAN, spawn.EXIT_DRIFT, spawn.EXIT_UNSAFE):
        assert str(code) in arms, f"exit {code} has no case arm (found {arms})"
    assert "*" in arms, "no catch-all arm for unexpected exit codes"


def test_a_crash_is_not_reported_as_drift(tmp_path):
    """Python exits 1 on an unhandled exception — the same code as EXIT_DRIFT.

    Left alone, the self-heal would read a crash as "the templates are stale"
    and try to open a sync PR from whatever partial tree the crash left behind.
    A real crash of exactly this kind (`stamp_complete_index` on a relative
    path) is what prompted the guard.
    """
    broken = tmp_path / "spawn_broken.py"
    broken.write_text(
        SPAWN_PY.read_text().replace(
            "    results = generate_all(root, out_root)",
            "    raise RuntimeError('simulated crash')",
        )
    )
    r = subprocess.run(
        [sys.executable, str(broken), "--check", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == spawn.EXIT_CRASH, "a crash must not look like drift"
    assert r.returncode != spawn.EXIT_DRIFT
    assert "simulated crash" in r.stderr, "the traceback must still be visible"


def test_a_fail_closed_SystemExit_is_unsafe_not_drift(tmp_path):
    """`SystemExit("message")` also exits 1 — the same code as EXIT_DRIFT.

    The fail-closed generator paths (an unmapped EMPTY file, say) raise exactly
    that. They are human decisions like UNMATCHED, so they must report UNSAFE;
    otherwise the self-heal reads them as ordinary staleness.
    """
    broken = tmp_path / "spawn_failclosed.py"
    broken.write_text(
        SPAWN_PY.read_text().replace(
            "    results = generate_all(root, out_root)",
            "    raise SystemExit('spawn: simulated fail-closed decision')",
        )
    )
    r = subprocess.run(
        [sys.executable, str(broken), "--check", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert r.returncode == spawn.EXIT_UNSAFE, (
        f"fail-closed exit must be UNSAFE, got {r.returncode}"
    )
    assert "simulated fail-closed decision" in r.stderr


def test_canary_hit_reports_unsafe_not_drift(tmp_path):
    """The interlock: a leak must be distinguishable from mechanical drift."""
    token = spawn.CANARY_TOKENS[0]
    published = _workspace_with_published(
        tmp_path, mind_files={"REFERENCE.md": f"# R\nmentions {token}0946\n"}
    )
    assert _check_exit(tmp_path, published) == spawn.EXIT_UNSAFE


def test_unmatched_file_class_reports_unsafe_not_drift(tmp_path):
    published = _workspace_with_published(
        tmp_path, mind_files={"brand_new_thing.md": "unclassified\n"}
    )
    assert _check_exit(tmp_path, published) == spawn.EXIT_UNSAFE


def test_unsafe_outranks_drift(tmp_path):
    """With BOTH problems present, the answer must be UNSAFE.

    If drift won, the self-heal would open a PR from a tree that also carries
    leaked content.
    """
    token = spawn.CANARY_TOKENS[0]
    published = _workspace_with_published(
        tmp_path,
        mind_files={"REFERENCE.md": f"# R\nmentions {token}0946\n"},
        published_edit=lambda p: (p / "PyAutoMind-template" / "README.md").write_text("drifted\n"),
    )
    assert _check_exit(tmp_path, published) == spawn.EXIT_UNSAFE


def test_stamping_works_with_a_RELATIVE_output_dir(tmp_path, monkeypatch):
    """`--write regenerated` must work, not just `--write /abs/path`.

    The child resolves the script path AFTER chdir'ing to `cwd`, so a relative
    out_dir made it unresolvable and the child died with "can't open file".
    Every invocation to date happened to pass an absolute path, so it stayed
    latent until a CI step naturally wrote to a relative dir.
    """
    mind = tmp_path / "PyAutoMind"
    _fake_repo(mind, MINIMAL_MIND)
    monkeypatch.chdir(tmp_path)

    spawn.generate_mind(mind, Path("out_relative"))   # relative, on purpose

    assert (tmp_path / "out_relative" / "complete" / "index.md").exists()


def test_stamping_is_skipped_when_lifecycle_is_not_kept(tmp_path):
    """If the rules ever stop KEEPing lifecycle.py, spawn must not crash."""
    mind = tmp_path / "PyAutoMind"
    files = {k: v for k, v in MINIMAL_MIND.items() if k != "scripts/lifecycle.py"}
    _fake_repo(mind, files)
    out = tmp_path / "out"

    spawn.generate_mind(mind, out)  # must not raise

    assert not (out / "complete" / "index.md").exists()
