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
import sys
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


def test_single_repo_layout_adds_no_second_registration_to_the_repo(tmp_path):
    """Claude Code already found this repo's settings; a second would double-run."""
    repo = tmp_path / "OrganOne"
    hook = _install_hook(repo)
    before = sorted(p.name for p in (repo / ".claude").iterdir())

    r = _run_hook(hook, project_dir=repo)
    assert r.returncode == 0, r.stderr
    assert sorted(p.name for p in (repo / ".claude").iterdir()) == before


def test_a_single_repo_session_seeds_the_workspace_root(tmp_path):
    """The leg used to be unreachable, and this is the session that reaches it.

    Writing the workspace-root fan-out requires the hook to be running. The
    hook runs only where Claude Code registers it — a session whose project dir
    IS a repo, i.e. a SINGLE-repo session. The old early return skipped exactly
    that session as "nothing to add", so the fan-out was never written by
    anyone, and the multi-repo session that needed it never ran the hook to
    write it either. Observed: a container with two single-repo sessions behind
    it still had no `<root>/.claude`, and the next session — three organs,
    project dir at the root — fired no hook at all.

    A single-repo session sees the same sibling layout one directory up, so it
    can seed the root for the next session in the container for free.
    """
    workspace = tmp_path / "workspace"
    repo = workspace / "OrganOne"
    hook = _install_hook(repo)

    r = _run_hook(hook, project_dir=repo)
    assert r.returncode == 0, r.stderr

    fanout = workspace / ".claude" / "hooks" / "session-start.sh"
    settings = workspace / ".claude" / "settings.json"
    assert fanout.is_file() and os.access(fanout, os.X_OK), (
        "a single-repo session left the root unable to register a hook"
    )
    assert settings.is_file()


def test_a_workspace_root_that_is_itself_a_repo_is_left_alone(tmp_path):
    """Then it owns its own hook, and a fan-out above it is not ours to add."""
    root = tmp_path / "Checkout"
    (root / ".git").mkdir(parents=True)
    repo = root / "Nested"
    hook = _install_hook(repo)

    r = _run_hook(hook, project_dir=repo)
    assert r.returncode == 0, r.stderr
    assert not (root / ".claude").exists(), sorted(p.name for p in root.iterdir())


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


# --------------------------------------------------------------------------
# 4. The interpreter a shell finds when no env file was written
#
# A multi-repo session gets no `CLAUDE_ENV_FILE`, so the venv is never
# prepended to PATH and every Bash call resolves whatever the image installed.
# These pin the two names that have to be right on their own — and the two ways
# writing them destroyed the container the first time.
# --------------------------------------------------------------------------

DEFINE_ONLY = {"PYAUTO_SESSION_DEFINE_ONLY": "1"}


def _call_hook_function(body, *, venv, extra_env=None):
    """Run one leg of the hook against a directory the test owns."""
    env = dict(os.environ)
    env.update({"CLAUDE_CODE_REMOTE": "true", "PYAUTO_SESSION_VENV": str(venv)})
    env.update(extra_env or {})
    script = f'source "{CANONICAL_HOOK}"\n{body}\n'
    return subprocess.run(["bash", "-c", script], capture_output=True, text=True,
                          env={**env, **DEFINE_ONLY}, timeout=120)


def _fake_venv(tmp_path):
    """A stand-in for the session venv: its python reports the venv as prefix."""
    venv = tmp_path / "venv"
    (venv / "bin").mkdir(parents=True)
    python = venv / "bin" / "python"
    python.write_text(f'#!/bin/sh\necho "{venv}"\n')
    python.chmod(0o755)
    return venv


def test_the_system_default_is_a_wrapper_because_a_symlink_loses_the_venv(tmp_path):
    """The bug this leg exists for, proved in both directions.

    A symlink to the venv's python is resolved by CPython BEFORE it looks for
    `pyvenv.cfg`, so it lands on the base interpreter's prefix and the venv —
    with pytest and PyYAML in it — is gone. The hook must write a wrapper.
    """
    venv = _fake_venv(tmp_path)
    system_bin = tmp_path / "usr-local-bin"
    system_bin.mkdir()

    r = _call_hook_function("point_system_default", venv=venv,
                            extra_env={"PYAUTO_SESSION_SYSTEM_BIN": str(system_bin)})
    assert r.returncode == 0, r.stderr

    default = system_bin / "python3"
    assert not default.is_symlink(), "a symlink here resolves past the venv"
    assert default.read_text().startswith("#!/bin/sh"), default.read_text()
    assert str(venv / "bin" / "python") in default.read_text()


def test_writing_the_default_replaces_a_symlink_instead_of_writing_through_it(tmp_path):
    """The regression that destroyed a container's interpreter.

    `/usr/local/bin/python3` is a SYMLINK to the real interpreter. A redirect
    opens the link's target, so `cat >` there overwrote /usr/bin/python3.12
    itself with the wrapper — and since the venv's python symlinks to that same
    file, the wrapper then exec'd itself. Every `python3` in the container spun
    at 100% CPU and the interpreter was gone.
    """
    venv = _fake_venv(tmp_path)
    system_bin = tmp_path / "usr-local-bin"
    system_bin.mkdir()
    real = tmp_path / "real-python3.12"
    real.write_text("#!/bin/sh\necho REAL-INTERPRETER\n")
    real.chmod(0o755)
    for name in ("python", "python3"):
        (system_bin / name).symlink_to(real)

    r = _call_hook_function("point_system_default", venv=venv,
                            extra_env={"PYAUTO_SESSION_SYSTEM_BIN": str(system_bin)})
    assert r.returncode == 0, r.stderr

    assert real.read_text() == "#!/bin/sh\necho REAL-INTERPRETER\n", (
        "the wrapper was written THROUGH the symlink and clobbered the interpreter"
    )
    assert not (system_bin / "python3").is_symlink()


def test_a_target_that_links_back_through_the_destination_is_refused(tmp_path):
    """The other way to build the same loop, and the reason for the chain walk.

    If the venv was built on the system default, its python links back through
    the path being rewritten — so the wrapper would exec itself. Refuse, and
    leave the destination as it was.
    """
    system_bin = tmp_path / "usr-local-bin"
    system_bin.mkdir()
    real = tmp_path / "real-python3.12"
    real.write_text("#!/bin/sh\necho REAL\n")
    real.chmod(0o755)
    (system_bin / "python3").symlink_to(real)
    (system_bin / "python").symlink_to(real)

    venv = tmp_path / "venv"
    (venv / "bin").mkdir(parents=True)
    (venv / "bin" / "python").symlink_to(system_bin / "python3")

    r = _call_hook_function("point_system_default", venv=venv,
                            extra_env={"PYAUTO_SESSION_SYSTEM_BIN": str(system_bin)})
    assert r.returncode == 0, r.stderr
    assert "links back through" in r.stderr, r.stderr
    assert (system_bin / "python3").is_symlink(), "the destination was rewritten anyway"


def test_pytest_on_path_is_pointed_at_the_venv(tmp_path):
    """`pytest` resolves before `python3` does, and uv's copy is isolated.

    $HOME/.local/bin precedes /usr/local/bin, and it holds uv's tool shims. uv
    installs each tool in its own environment by design, so that pytest cannot
    import PyYAML — which surfaced as four collection ImportErrors that read
    like broken source, in a workspace whose suite was green.
    """
    venv = _fake_venv(tmp_path)
    (venv / "bin" / "pytest").write_text("#!/bin/sh\necho VENV-PYTEST\n")
    (venv / "bin" / "pytest").chmod(0o755)

    home = tmp_path / "home"
    shim_dir = home / ".local" / "bin"
    shim_dir.mkdir(parents=True)
    (shim_dir / "pytest").write_text("#!/bin/sh\necho UV-ISOLATED-PYTEST\n")
    (shim_dir / "pytest").chmod(0o755)

    r = _call_hook_function("point_pytest_at_venv", venv=venv, extra_env={
        "HOME": str(home), "PATH": f"{shim_dir}:{os.environ['PATH']}"})
    assert r.returncode == 0, r.stderr
    assert str(venv / "bin" / "pytest") in (shim_dir / "pytest").read_text()


def test_a_pytest_outside_uvs_shim_dir_is_left_alone(tmp_path):
    """A distro-packaged pytest is not this hook's to overwrite."""
    venv = _fake_venv(tmp_path)
    (venv / "bin" / "pytest").write_text("#!/bin/sh\necho VENV\n")
    (venv / "bin" / "pytest").chmod(0o755)

    home = tmp_path / "home"
    (home / ".local" / "bin").mkdir(parents=True)
    system_dir = tmp_path / "usr-bin"
    system_dir.mkdir()
    (system_dir / "pytest").write_text("#!/bin/sh\necho DISTRO\n")
    (system_dir / "pytest").chmod(0o755)

    r = _call_hook_function("point_pytest_at_venv", venv=venv, extra_env={
        "HOME": str(home), "PATH": f"{system_dir}:{os.environ['PATH']}"})
    assert r.returncode == 0, r.stderr
    assert (system_dir / "pytest").read_text() == "#!/bin/sh\necho DISTRO\n"
    assert "outside uv's shim dir" in r.stderr, r.stderr


# --------------------------------------------------------------------------
# 5. `--check` reports usability, not just version
# --------------------------------------------------------------------------

def test_check_fails_a_pytest_that_has_the_right_version_but_cannot_import(tmp_path):
    """The check answered a question it had not asked.

    It resolved each tool's shebang and asked that interpreter for its version
    — necessary, because a 3.11 mypy judges code against 3.11 rules. But uv
    installs each tool in its OWN environment, so a 3.12 pytest can still be
    unable to import PyYAML. `--check` printed `pytest: 3.12 OK` for exactly
    such a pytest while the suite exited on four collection ImportErrors that
    read like broken source. Version is necessary; it is not sufficient.
    """
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    interp = fake_bin / "fake-python3.12"
    interp.write_text(
        "#!/bin/sh\n"
        "case \"$2\" in\n"
        "  *version_info*) echo '3.12' ;;\n"
        "  *find_spec*) printf 'yaml' ;;\n"
        "esac\n"
    )
    interp.chmod(0o755)
    shim = fake_bin / "pytest"
    shim.write_text(f"#!{interp}\n")
    shim.chmod(0o755)

    env = dict(os.environ)
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    r = subprocess.run(["bash", str(BOOTSTRAP), "--check"], capture_output=True,
                       text=True, env=env, timeout=180)

    assert "pytest: 3.12 OK" not in r.stderr, r.stderr
    assert "cannot import: yaml" in r.stderr, r.stderr
    assert r.returncode != 0


def _import_probe():
    """The probe as the script really spells it, lifted from the script."""
    for line in BOOTSTRAP.read_text().splitlines():
        if line.startswith("IMPORT_PROBE="):
            return line.split("=", 1)[1].strip().strip("'")
    raise AssertionError("session_bootstrap.sh no longer defines IMPORT_PROBE")


def test_the_import_probe_runs_on_a_real_interpreter():
    """The check above drove a shell script standing in for python.

    A stand-in answers whatever the fixture says, so it can never disagree with
    the snippet — and the snippet was wrong: `import importlib` does not bind
    `importlib.util`, so on every real CPython the probe raised AttributeError,
    the `&&` short-circuited, and `--check` printed `3.12 OK`. Measured in a
    fresh container on 2026-08-27, beside a `python3 -m pytest` that answered
    `No module named pytest`.

    So this one runs the real string on the real interpreter. Sufficiency, not
    plumbing: the fixture cannot be the thing under test.
    """
    import importlib.util
    import sys

    r = subprocess.run([sys.executable, "-c", _import_probe()],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, (
        "the probe cannot run, so --check silently skips it: " + r.stderr)
    expected = {m for m in ("pytest", "yaml", "xdist")
                if not importlib.util.find_spec(m)}
    assert set(r.stdout.split()) == expected


def test_check_fails_when_the_import_probe_cannot_run(tmp_path):
    """"Could not ask" is a failure, not a pass.

    The two outcomes used to be indistinguishable — both fell through to the OK
    line — which is what let a broken probe read as a healthy session.
    """
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    interp = fake_bin / "fake-python3.12"
    interp.write_text(
        "#!/bin/sh\n"
        "case \"$2\" in\n"
        "  *version_info*) echo '3.12' ;;\n"
        "  *find_spec*) exit 1 ;;\n"   # the AttributeError case
        "esac\n"
    )
    interp.chmod(0o755)
    shim = fake_bin / "pytest"
    shim.write_text(f"#!{interp}\n")
    shim.chmod(0o755)

    env = dict(os.environ)
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    r = subprocess.run(["bash", str(BOOTSTRAP), "--check"], capture_output=True,
                       text=True, env=env, timeout=180)

    assert "pytest: 3.12 OK" not in r.stderr, r.stderr
    assert "import probe would not run" in r.stderr, r.stderr
    assert r.returncode != 0


# --------------------------------------------------------------------------
# 6. Everything else the venv owns
#
# `python3` and `pytest` each get their own shim, so both survive a session
# whose PATH never learns about the venv — and a multi-repo session's PATH never
# does, because the env file that would export it is written by Claude Code
# around a hook it does not register. Nothing else in $VENV/bin survived.
#
# Measured on PyAutoHands: with `ipynb-py-convert` installed into the venv, five
# tests still failed with `FileNotFoundError: ipynb-py-convert` — the binary
# present and unreachable — while `--check` called the session healthy.
# --------------------------------------------------------------------------

def test_a_venv_console_script_unreachable_on_path_is_shimmed(tmp_path):
    """A declared dep's console script must be reachable, not merely installed."""
    venv = _fake_venv(tmp_path)
    (venv / "bin" / "widget").write_text("#!/bin/sh\necho VENV-WIDGET\n")
    (venv / "bin" / "widget").chmod(0o755)

    home = tmp_path / "home"
    shim_dir = home / ".local" / "bin"
    shim_dir.mkdir(parents=True)

    r = _call_hook_function("point_venv_scripts_at_venv", venv=venv, extra_env={
        "HOME": str(home), "PATH": f"{shim_dir}:{os.environ['PATH']}"})
    assert r.returncode == 0, r.stderr
    assert (shim_dir / "widget").exists(), "the script stayed unreachable"
    assert str(venv / "bin" / "widget") in (shim_dir / "widget").read_text()
    assert os.access(shim_dir / "widget", os.X_OK)


def test_a_console_script_the_image_owns_is_left_alone(tmp_path):
    """Same claim policy as `pytest`: a name the image owns is not ours."""
    venv = _fake_venv(tmp_path)
    (venv / "bin" / "widget").write_text("#!/bin/sh\necho VENV\n")
    (venv / "bin" / "widget").chmod(0o755)

    home = tmp_path / "home"
    (home / ".local" / "bin").mkdir(parents=True)
    system_dir = tmp_path / "usr-bin"
    system_dir.mkdir()
    (system_dir / "widget").write_text("#!/bin/sh\necho DISTRO\n")
    (system_dir / "widget").chmod(0o755)

    r = _call_hook_function("point_venv_scripts_at_venv", venv=venv, extra_env={
        "HOME": str(home), "PATH": f"{system_dir}:{os.environ['PATH']}"})
    assert r.returncode == 0, r.stderr
    assert (system_dir / "widget").read_text() == "#!/bin/sh\necho DISTRO\n"
    assert "outside uv's shim dir" in r.stderr, r.stderr


def test_the_venvs_own_plumbing_is_not_shimmed(tmp_path):
    """`python` and `pip` belong to legs 2 and to the venv; `activate` is sourced.

    Shimming `pip` would silently redirect every `pip install` in the session,
    and an `activate` shim is an executable copy of a file that only works when
    sourced — a trap, not a fix.
    """
    venv = _fake_venv(tmp_path)
    for name in ("pip", "activate", "python3.12"):
        (venv / "bin" / name).write_text("#!/bin/sh\necho VENV\n")
        (venv / "bin" / name).chmod(0o755)

    home = tmp_path / "home"
    shim_dir = home / ".local" / "bin"
    shim_dir.mkdir(parents=True)

    r = _call_hook_function("point_venv_scripts_at_venv", venv=venv, extra_env={
        "HOME": str(home), "PATH": f"{shim_dir}:{os.environ['PATH']}"})
    assert r.returncode == 0, r.stderr
    assert not list(shim_dir.iterdir()), sorted(p.name for p in shim_dir.iterdir())


# --------------------------------------------------------------------------
# 7. `--check` must be able to read the hook's own shims
# --------------------------------------------------------------------------

def _fake_mind(tmp_path):
    """A stand-in workspace: a repo dir holding this script, with siblings."""
    mind = tmp_path / "FakeMind"
    (mind / "scripts").mkdir(parents=True)
    dest = mind / "scripts" / "session_bootstrap.sh"
    dest.write_text(BOOTSTRAP.read_text())
    dest.chmod(0o755)
    return mind


def test_check_resolves_the_interpreter_behind_an_exec_wrapper(tmp_path):
    """The two halves of the previous fix cancelled each other.

    The hook points `pytest` at the venv with a `#!/bin/sh` + `exec` WRAPPER,
    because a symlink resolves past `pyvenv.cfg` and loses the venv. `--check`
    then sniffed that wrapper's shebang, got `/bin/sh`, and reported
    "interpreter undetermined" — skipping, silently, the import probe added
    precisely because a 3.12 pytest that cannot import PyYAML fails collection
    in a way that reads like broken source.
    """
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    interp = fake_bin / "fake-python3.12"
    interp.write_text(
        "#!/bin/sh\n"
        "case \"$2\" in\n"
        "  *version_info*) echo '3.12' ;;\n"
        "  *find_spec*) printf 'yaml' ;;\n"
        "esac\n"
    )
    interp.chmod(0o755)
    real = fake_bin / "real-pytest"
    real.write_text(f"#!{interp}\n")
    real.chmod(0o755)
    # Exactly what write_venv_shim emits.
    shim = fake_bin / "pytest"
    shim.write_text(f'#!/bin/sh\nexec "{real}" "$@"\n')
    shim.chmod(0o755)

    env = dict(os.environ)
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    r = subprocess.run(["bash", str(BOOTSTRAP), "--check"], capture_output=True,
                       text=True, env=env, timeout=180)

    assert "interpreter undetermined" not in r.stderr, r.stderr
    assert "cannot import: yaml" in r.stderr, r.stderr


def test_check_names_a_compiled_tool_rather_than_leaving_a_blank(tmp_path):
    """`ruff` is a native binary; "undetermined" reads like a fault it is not."""
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    ruff = fake_bin / "ruff"
    ruff.write_bytes(b"\x7fELF\x02\x01\x01\x00not-really-an-elf")
    ruff.chmod(0o755)

    env = dict(os.environ)
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    r = subprocess.run(["bash", str(BOOTSTRAP), "--check"], capture_output=True,
                       text=True, env=env, timeout=180)
    assert "ruff: " in r.stderr
    assert "native binary" in r.stderr, r.stderr


# --------------------------------------------------------------------------
# 8. Declared deps, per repo
#
# The hook reads `.claude/session-python.txt` from the repo whose copy is
# RUNNING. The bootstrap runs the canonical hook, which derives its repo from
# its own path — so one repo's deps installed and no one else's, in exactly the
# multi-repo session that has to use the bootstrap at all.
# --------------------------------------------------------------------------

def test_check_reports_declared_extras_that_never_installed(tmp_path):
    mind = _fake_mind(tmp_path)
    sibling = tmp_path / "FakeHands"
    (sibling / ".claude").mkdir(parents=True)
    (sibling / ".claude" / "session-python.txt").write_text("some-package\n")

    env = dict(os.environ)
    env["PYAUTO_SESSION_VENV"] = str(tmp_path / "venv")
    r = subprocess.run(["bash", str(mind / "scripts" / "session_bootstrap.sh"), "--check"],
                       capture_output=True, text=True, env=env, timeout=180)
    assert "FakeHands extras: declared but NOT installed" in r.stderr, r.stderr
    assert r.returncode != 0


def test_check_is_quiet_once_the_declared_extras_are_installed(tmp_path):
    mind = _fake_mind(tmp_path)
    sibling = tmp_path / "FakeHands"
    (sibling / ".claude").mkdir(parents=True)
    extras = sibling / ".claude" / "session-python.txt"
    extras.write_text("some-package\n")

    venv = tmp_path / "venv"
    venv.mkdir()
    stamp = subprocess.run(f"cksum <{extras} | tr -d ' /'", shell=True,
                           capture_output=True, text=True).stdout.strip()
    (venv / f".extras-{stamp}").touch()

    env = dict(os.environ)
    env["PYAUTO_SESSION_VENV"] = str(venv)
    r = subprocess.run(["bash", str(mind / "scripts" / "session_bootstrap.sh"), "--check"],
                       capture_output=True, text=True, env=env, timeout=180)
    assert "FakeHands extras: installed" in r.stderr, r.stderr


def test_bootstrap_runs_every_sibling_repos_hook(tmp_path):
    """One repo's hook is not the session's environment.

    PyAutoHands declares `ipynb-py-convert` + `Pillow`; a bootstrap that ran
    only PyAutoMind's hook left 14 of its tests failing on a missing module or a
    missing binary, having reported success.
    """
    mind = _fake_mind(tmp_path)
    (mind / "policy").mkdir()
    hook = mind / "policy" / "session_start_hook.sh"
    hook.write_text(CANONICAL_HOOK.read_text())
    hook.chmod(0o755)

    ran = tmp_path / "ran"
    ran.mkdir()
    for name in ("FakeHeart", "FakeHands"):
        sibling = tmp_path / name
        (sibling / ".claude" / "hooks").mkdir(parents=True)
        stub = sibling / ".claude" / "hooks" / "session-start.sh"
        stub.write_text(f'#!/bin/sh\ntouch "{ran}/{name}"\n')
        stub.chmod(0o755)

    env = dict(os.environ)
    env.update({
        "CLAUDE_CODE_REMOTE": "true",
        "PYAUTO_SESSION_SKIP_PYTHON": "1",
        "PYAUTO_SESSION_VENV": str(tmp_path / "venv"),
    })
    env.pop("CLAUDE_ENV_FILE", None)
    r = subprocess.run(["bash", str(mind / "scripts" / "session_bootstrap.sh")],
                       capture_output=True, text=True, env=env, timeout=180)
    assert r.returncode == 0, r.stderr
    assert (ran / "FakeHeart").exists(), r.stderr
    assert (ran / "FakeHands").exists(), r.stderr


# --------------------------------------------------------------------------
# 7. uv's tool environments
#
# The session venv fix has a blast radius nobody costed. uv creates every tool
# env with `bin/python` as a symlink to whatever `python3` was at install time
# — `/usr/local/bin/python3` — and the hook then repoints THAT path at the
# session venv. So each tool env's interpreter resolves its prefix to the venv,
# the tool's own site-packages never reaches `sys.path`, and the console script
# dies on `ModuleNotFoundError` with the package installed two directories away.
#
# Measured 2026-08-27 in a bootstrapped session: mypy, flake8, black, poetry and
# pyright all dead this way, while `--check` reported each as `3.12 OK` — the
# interpreter they reach IS 3.12, it is just not theirs. A session then lints
# clean by not linting, and CI finds out.
# --------------------------------------------------------------------------


def _venv(path):
    subprocess.run([sys.executable, "-m", "venv", str(path)], check=True,
                   capture_output=True, timeout=180)
    return path


def _prefix_of(python):
    r = subprocess.run([str(python), "-c", "import sys; print(sys.prefix)"],
                       capture_output=True, text=True, timeout=60)
    return r.stdout.strip()


def _repair(tools_dir, venv):
    env = dict(os.environ)
    env["PYAUTO_UV_TOOLS_DIR"] = str(tools_dir)
    env["PYAUTO_SESSION_VENV"] = str(venv)
    return subprocess.run(["bash", str(BOOTSTRAP), "--repair-uv-tools"],
                          capture_output=True, text=True, env=env, timeout=300)


def test_a_tool_env_pointed_at_the_session_venv_is_repaired(tmp_path):
    """The exact breakage: a tool env resolving to somebody else's prefix."""
    session_venv = _venv(tmp_path / "session")
    tools = tmp_path / "tools"
    tool = _venv(tools / "widget")

    # The breakage needs the WRAPPER, not a bare symlink. CPython looks for
    # `pyvenv.cfg` beside the executable as invoked, so a tool env whose python
    # merely symlinks elsewhere still finds its own config and is fine. What
    # loses it is `/usr/local/bin/python3` being a shell wrapper that `exec`s
    # the venv (it is a wrapper precisely because a symlink there lost the venv
    # — the other half of this same script): the exec replaces argv, and the
    # tool env is gone.
    hijacked = tmp_path / "usr-local-python3"
    hijacked.write_text(f'#!/bin/sh\nexec "{session_venv}/bin/python" "$@"\n')
    hijacked.chmod(0o755)

    link = tool / "bin" / "python"
    link.unlink()
    link.symlink_to(hijacked)
    assert _prefix_of(link) == str(session_venv), "fixture did not reproduce it"

    r = _repair(tools, session_venv)
    assert "repointed widget" in r.stderr, r.stderr
    assert _prefix_of(link) == str(tool)


def test_a_healthy_tool_env_is_left_alone(tmp_path):
    session_venv = _venv(tmp_path / "session")
    tools = tmp_path / "tools"
    tool = _venv(tools / "widget")
    before = (tool / "bin" / "python").resolve()

    r = _repair(tools, session_venv)
    assert "repointed" not in r.stderr, r.stderr
    assert (tool / "bin" / "python").resolve() == before


def test_check_fails_a_tool_that_has_the_right_version_but_will_not_run(tmp_path):
    """`3.12 OK` was printed for tools that answered ModuleNotFoundError.

    The version probe asks the interpreter; it never asks the tool. A tool that
    cannot run is the same class of finding as one on the wrong interpreter —
    both mean the session is not linting what CI lints.
    """
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    interp = fake_bin / "fake-python3.12"
    interp.write_text(
        "#!/bin/sh\n"
        "case \"$2\" in\n"
        "  *version_info*) echo '3.12' ;;\n"
        "  *find_spec*) printf '' ;;\n"
        "  --version) exit 1 ;;\n"      # ModuleNotFoundError, as measured
        "esac\n"
    )
    interp.chmod(0o755)
    broken = fake_bin / "black"          # a linter, not one of the two probed
    broken.write_text(f"#!{interp}\nimport black\n")
    broken.chmod(0o755)

    env = dict(os.environ)
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    r = subprocess.run(["bash", str(BOOTSTRAP), "--check"], capture_output=True,
                       text=True, env=env, timeout=180)

    assert "black: 3.12 OK" not in r.stderr, r.stderr
    assert "will not run" in r.stderr, r.stderr
    assert r.returncode != 0
