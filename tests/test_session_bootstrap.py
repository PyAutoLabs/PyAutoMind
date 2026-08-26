"""What the SessionStart hook DOES at run time, not just whether it is in sync.

`test_session_hook_sync.py` pins that every repo carries the canonical copy.
These tests pin what that copy does when it runs, because two of its legs were
wrong in ways no sync check could see:

1. **It read the wrong directory.** The hook took its repo from
   `$CLAUDE_PROJECT_DIR`. That equals the repo only in a session holding exactly
   ONE repo. A session scoped to several organs clones them side by side *under*
   the project directory, so the project directory is their parent — not a repo,
   with no `.claude/` of its own. Claude Code registers project hooks from that
   directory, so in exactly the sessions holding the most repos, no repo's hook
   was registered and none of this ran. The session came up on the container's
   Python 3.11: below the floor this repo set for itself and below every CI leg,
   with mypy and flake8 reading the interpreter and judging code against 3.11
   rules. Nothing announced it.

2. **It left clones shallow.** A remote session clones shallow, and
   `git merge-base --is-ancestor` then reports "not an ancestor" for a commit
   whose ancestry is merely absent from the clone. The ship and close-out
   procedures act on that answer.

Conventions (see `test_session_hook_sync.py`):

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository.
2. **Prove each leg FAILS.** Every assertion is driven with input that must trip
   it — including running the hook against the layout that used to defeat it.

The hook's interpreter legs are skipped via `PYAUTO_SESSION_SKIP_PYTHON=1`, the
seam the hook documents for exactly this purpose: these tests are about git
history and hook reachability, which the hook now does independently of whether
an interpreter can be built.
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HOOK = ROOT / "policy" / "session_start_hook.sh"
BOOTSTRAP = ROOT / "scripts" / "session_bootstrap.sh"


def _git(*args, cwd):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                          text=True, timeout=60)


def _run_hook(hook, *, project_dir, extra_env=None):
    env = dict(os.environ)
    env.update({
        "CLAUDE_CODE_REMOTE": "true",
        "CLAUDE_PROJECT_DIR": str(project_dir),
        "PYAUTO_SESSION_SKIP_PYTHON": "1",
    })
    env.pop("CLAUDE_ENV_FILE", None)
    env.update(extra_env or {})
    return subprocess.run(["bash", str(hook)], capture_output=True, text=True,
                          env=env, timeout=180)


def _install_hook(repo):
    """A checked-out repo carrying the canonical hook where the harness looks."""
    hooks = repo / ".claude" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    dest = hooks / "session-start.sh"
    dest.write_text(CANONICAL_HOOK.read_text())
    dest.chmod(0o755)
    return dest


# --------------------------------------------------------------------------
# 1. The repo is derived from the hook, not from the project directory
# --------------------------------------------------------------------------

def test_multi_repo_layout_installs_a_workspace_root_hook(tmp_path):
    """The layout that used to defeat the hook entirely.

    Two repos side by side under a workspace root that is not itself a repo —
    a project directory with no `.claude/`, so nothing would have registered
    any hook. Running either repo's hook must leave the root able to register
    one for the next session.
    """
    workspace = tmp_path / "workspace"
    for name in ("OrganOne", "OrganTwo"):
        _install_hook(workspace / name)

    r = _run_hook(workspace / "OrganOne" / ".claude" / "hooks" / "session-start.sh",
                  project_dir=workspace)
    assert r.returncode == 0, r.stderr

    settings = workspace / ".claude" / "settings.json"
    fanout = workspace / ".claude" / "hooks" / "session-start.sh"
    assert settings.is_file(), "workspace root got no settings.json"
    assert fanout.is_file() and os.access(fanout, os.X_OK)

    registered = json.loads(settings.read_text())
    commands = [
        h["command"]
        for group in registered["hooks"]["SessionStart"]
        for h in group["hooks"]
    ]
    assert any("session-start.sh" in c for c in commands), commands


def test_single_repo_layout_installs_nothing_extra(tmp_path):
    """When the project dir IS the repo, Claude Code already found its settings.

    Writing a second registration there would double-run the hook, so the leg
    must be inert in the layout that was never broken.
    """
    repo = tmp_path / "OrganOne"
    hook = _install_hook(repo)
    before = sorted(p.name for p in (repo / ".claude").iterdir())

    r = _run_hook(hook, project_dir=repo)
    assert r.returncode == 0, r.stderr
    assert sorted(p.name for p in (repo / ".claude").iterdir()) == before


def test_generated_fanout_runs_every_sibling_repos_hook(tmp_path):
    """The root hook's whole job: reach each repo's own hook, and say so."""
    workspace = tmp_path / "workspace"
    for name in ("OrganOne", "OrganTwo"):
        _install_hook(workspace / name)
    _run_hook(workspace / "OrganOne" / ".claude" / "hooks" / "session-start.sh",
              project_dir=workspace)

    fanout = workspace / ".claude" / "hooks" / "session-start.sh"
    assert subprocess.run(["bash", "-n", str(fanout)]).returncode == 0

    # Replace each repo's hook with a marker so the fan-out's reach is visible.
    for name in ("OrganOne", "OrganTwo"):
        h = workspace / name / ".claude" / "hooks" / "session-start.sh"
        h.write_text(f"#!/usr/bin/env bash\ntouch '{workspace}/{name}.ran'\n")
        h.chmod(0o755)

    r = subprocess.run(["bash", str(fanout)], capture_output=True, text=True,
                       timeout=60)
    assert r.returncode == 0, r.stderr
    assert (workspace / "OrganOne.ran").exists()
    assert (workspace / "OrganTwo.ran").exists()


# --------------------------------------------------------------------------
# 2. Shallow clones
# --------------------------------------------------------------------------

@pytest.fixture
def shallow_workspace(tmp_path):
    """A workspace whose one repo is a genuine depth-1 clone of a local origin."""
    origin = tmp_path / "origin"
    origin.mkdir()
    _git("init", "-q", "-b", "main", cwd=origin)
    _git("config", "user.email", "t@example.invalid", cwd=origin)
    _git("config", "user.name", "T", cwd=origin)
    for i in range(3):
        (origin / f"f{i}.txt").write_text(str(i))
        _git("add", "-A", cwd=origin)
        _git("commit", "-qm", f"c{i}", cwd=origin)

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    clone = workspace / "OrganOne"
    r = _git("clone", "-q", "--depth=1", f"file://{origin}", str(clone), cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    assert (clone / ".git" / "shallow").exists(), "fixture is not shallow"
    return workspace, clone, origin


def test_shallow_clone_is_unshallowed(shallow_workspace):
    workspace, clone, origin = shallow_workspace
    assert _git("rev-parse", "--is-shallow-repository", cwd=clone).stdout.strip() == "true"

    hook = _install_hook(clone)
    r = _run_hook(hook, project_dir=workspace)
    assert r.returncode == 0, r.stderr

    assert _git("rev-parse", "--is-shallow-repository", cwd=clone).stdout.strip() == "false"
    depth = int(_git("rev-list", "--count", "HEAD", cwd=clone).stdout.strip())
    assert depth == 3, f"history still truncated: {depth} commits"


def test_shallow_clone_defeats_an_ancestry_check_before_the_fix(shallow_workspace):
    """The reason the leg exists, pinned as a fact about git rather than prose.

    `--is-ancestor` answers 'no' for a real ancestor that is merely absent from
    a shallow clone, and answers correctly once the history is there.
    """
    workspace, clone, origin = shallow_workspace
    root_commit = _git("rev-list", "--max-parents=0", "HEAD", cwd=origin).stdout.strip()

    before = _git("merge-base", "--is-ancestor", root_commit, "HEAD", cwd=clone)
    assert before.returncode != 0, "fixture did not reproduce the shallow-clone lie"

    hook = _install_hook(clone)
    assert _run_hook(hook, project_dir=workspace).returncode == 0

    after = _git("merge-base", "--is-ancestor", root_commit, "HEAD", cwd=clone)
    assert after.returncode == 0, "ancestry still wrong after unshallowing"


# --------------------------------------------------------------------------
# 3. The bootstrap door
# --------------------------------------------------------------------------

def test_bootstrap_script_ships_and_is_executable():
    assert BOOTSTRAP.is_file()
    assert os.access(BOOTSTRAP, os.X_OK)
    assert subprocess.run(["bash", "-n", str(BOOTSTRAP)]).returncode == 0


def test_bootstrap_is_inert_outside_a_remote_session(tmp_path):
    """A developer box supplies its own interpreter; the door must not touch it."""
    env = dict(os.environ)
    env.pop("CLAUDE_CODE_REMOTE", None)
    r = subprocess.run(["bash", str(BOOTSTRAP)], capture_output=True, text=True,
                       env=env, timeout=60)
    assert r.returncode == 0
    assert "[session-start]" not in r.stderr


def test_bootstrap_check_reports_rather_than_changes():
    """`--check` is a read-only report; it must never build or fetch anything."""
    r = subprocess.run(["bash", str(BOOTSTRAP), "--check"], capture_output=True,
                       text=True, timeout=60)
    assert r.returncode in (0, 1)
    assert "[bootstrap]" in r.stderr
    assert "unshallowing" not in r.stderr
