"""Exercise the five runner shapes and the complete twelve-consumer fan-out."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import smoke_bootstrap_sync as sync
import propagate_smoke_bootstrap as propagate

MIND = SCRIPTS.parent
SOURCE = (MIND / sync.SOURCE).read_text()
FIXTURES = Path(__file__).parent / "fixtures/smoke_shims"
SHAPES = ["workspace"] * 3 + ["workspace_test"] * 4 + ["howto"] * 3 + ["cti", "pipeline"]


def install_repo(root, name="example", shape="workspace_test"):
    path = root / name / sync.REL
    path.parent.mkdir(parents=True)
    path.write_text((FIXTURES / f"{shape}.txt").read_text())
    return path


def hands(root, body="VALUE = 'local'\n"):
    path = root / "PyAutoHands/autohands/build_util.py"
    path.parent.mkdir(parents=True)
    path.write_text(body)
    return path.parent


def run_shim(path, env_extra=None, main=False):
    env = {k: v for k, v in os.environ.items()
           if k not in ("PYAUTO_ROOT", "PYTHONPATH", "PYAUTO_BRAIN", "PYAUTO_WT_ROOT")}
    env.update(env_extra or {})
    # Capture runner commands without importing the science stack or executing
    # expensive scripts. The actual shim main() and its return handling run.
    code = '''import json, runpy, subprocess, sys
from types import SimpleNamespace
calls=[]
def call(argv, **kwargs):
    calls.append([argv, kwargs['cwd']])
    return SimpleNamespace(returncode=1 if len(calls)==1 else 0)
subprocess.run=call
scope=runpy.run_path(sys.argv[1])
rc=scope['main']() if sys.argv[2]=='main' else None
print(json.dumps({'hands':str(scope['AUTOHANDS']), 'calls':calls, 'rc':rc}))
'''
    return subprocess.run([sys.executable, "-c", code, str(path), "main" if main else "import"],
                          env=env, capture_output=True, text=True)


@pytest.mark.parametrize("shape", sorted(set(SHAPES)))
@pytest.mark.parametrize("nested", [False, True])
def test_runner_behavior_unchanged_in_flat_and_nested_layouts(tmp_path, shape, nested):
    root = tmp_path / "tree"
    root.mkdir()
    (root / ".pyauto-root").touch()
    path = install_repo(root / "family" if nested else root, shape=shape)
    workspace = path.parents[2]
    for name in ("smoke_tests.txt", "smoke_notebooks.txt"):
        (workspace / name).write_text("example.py\n")
    hand = hands(root)
    before = run_shim(path, {"PYTHONPATH": str(hand)}, main=True)
    assert before.returncode == 0, before.stderr
    path.write_text(sync.render(path.read_text(), SOURCE))
    after = run_shim(path, main=True)
    assert after.returncode == 0, after.stderr
    assert json.loads(before.stdout) == json.loads(after.stdout)
    result = json.loads(after.stdout)
    assert result["rc"] == 1
    assert len(result["calls"]) == (2 if shape == "workspace" else 1)
    for argv, cwd in result["calls"]:
        assert "--report-dir" in argv
        assert cwd == str(workspace)


def test_ci_import_wins_even_with_invalid_root(tmp_path):
    path = install_repo(tmp_path)
    path.write_text(sync.render(path.read_text(), SOURCE))
    hand = hands(tmp_path / "ci")
    result = run_shim(path, {"PYTHONPATH": str(hand), "PYAUTO_ROOT": str(tmp_path / "missing")})
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["hands"] == str(hand)


def test_flat_without_marker_or_brain(tmp_path):
    path = install_repo(tmp_path)
    hand = hands(tmp_path)
    path.write_text(sync.render(path.read_text(), SOURCE))
    result = run_shim(path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["hands"] == str(hand)


@pytest.mark.parametrize("resolver", ["foreign", "broken", "exit", "valid"])
def test_bundle_does_not_import_canonical_hands(tmp_path, resolver):
    canonical = tmp_path / "canonical"
    bundle = tmp_path / "bundle"
    canonical.mkdir()
    bundle.mkdir()
    (canonical / ".pyauto-root").touch()
    (bundle / ".pyauto-root").touch()
    hands(canonical)
    local_hands = hands(bundle)
    path = install_repo(bundle / "family")
    agents = canonical / "PyAutoBrain/agents"
    agents.mkdir(parents=True)
    code = {"foreign": f"def workspace_root_reason(): return {str(canonical)!r}, 'stub'",
            "broken": "raise RuntimeError('broken')",
            "exit": "raise SystemExit(7)",
            "valid": f"def workspace_root_reason(): return {str(bundle)!r}, 'stub'"}[resolver]
    (agents / "_pyauto_root.py").write_text(code)
    (bundle / "PyAutoBrain").symlink_to(agents.parent, target_is_directory=True)
    path.write_text(sync.render(path.read_text(), SOURCE))
    result = run_shim(path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["hands"] == str(local_hands)


def test_explicit_root_and_missing_hands_diagnostics(tmp_path):
    path = install_repo(tmp_path / "family")
    path.write_text(sync.render(path.read_text(), SOURCE))
    result = run_shim(path)
    assert result.returncode != 0
    assert "PyAutoHands not found" in result.stderr
    assert str(path.parents[3] / "PyAutoHands/autohands/build_util.py") in result.stderr
    hand = hands(tmp_path / "chosen")
    result = run_shim(path, {"PYAUTO_ROOT": str(tmp_path / "chosen")})
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["hands"] == str(hand)


def test_missing_transitive_dependency_is_not_disguised(tmp_path):
    path = install_repo(tmp_path)
    path.write_text(sync.render(path.read_text(), SOURCE))
    hand = hands(tmp_path, "import deliberately_missing_dependency\n")
    result = run_shim(path, {"PYTHONPATH": str(hand)})
    assert result.returncode != 0
    assert "deliberately_missing_dependency" in result.stderr
    assert "PyAutoHands not found" not in result.stderr


def test_single_edit_reaches_twelve_preserving_every_exterior_byte(tmp_path):
    repos = {}
    originals = {}
    for index, shape in enumerate(SHAPES):
        name = f"example_{index}"
        path = install_repo(tmp_path, name, shape)
        originals[path] = path.read_text()
        repos[name] = {"smoke_bootstrap": True}
    assert sync.write(tmp_path, repos, SOURCE, require_all=True) == 12
    assert sync.check(tmp_path, repos, SOURCE) == []
    assert sync.write(tmp_path, repos, SOURCE) == 0
    edited = SOURCE + "\n# single-edit propagation witness\n"
    assert len(sync.check(tmp_path, repos, edited)) == 12
    assert sync.write(tmp_path, repos, edited) == 12
    for path, original in originals.items():
        before, after = original.split(sync.LEGACY)
        generated = path.read_text()
        assert generated.split(sync.BEGIN)[0] == before
        assert generated.split(sync.END)[1] == after
        assert "single-edit propagation witness" in generated


def test_unknown_legacy_prevents_any_writes(tmp_path):
    first = install_repo(tmp_path, "first")
    other = install_repo(tmp_path, "other")
    original = first.read_bytes()
    other.write_text("print('custom runner')\n")
    repos = {name: {"smoke_bootstrap": True} for name in ("first", "other")}
    with pytest.raises(ValueError, match="unknown legacy"):
        sync.write(tmp_path, repos, SOURCE)
    assert first.read_bytes() == original


@pytest.mark.parametrize("kind", ["repo", "directory", "file"])
def test_symlink_mutations_are_refused(tmp_path, kind):
    tree = tmp_path / "tree"
    tree.mkdir()
    outside = tmp_path / "outside"
    path = install_repo(outside)
    destination = tree / "example"
    if kind == "repo":
        destination.symlink_to(outside / "example", target_is_directory=True)
    elif kind == "directory":
        destination.mkdir()
        (destination / ".github").symlink_to(path.parents[1], target_is_directory=True)
    else:
        target = destination / sync.REL
        target.parent.mkdir(parents=True)
        target.symlink_to(path)
    original = path.read_bytes()
    with pytest.raises(ValueError, match="symlink"):
        sync.write(tree, {"example": {"smoke_bootstrap": True}}, SOURCE)
    assert path.read_bytes() == original


def test_missing_and_ambiguous_checkouts_are_not_success(tmp_path):
    repos = {"example": {"smoke_bootstrap": True}}
    with pytest.raises(ValueError, match="checkout missing"):
        sync.write(tmp_path, repos, SOURCE, require_all=True)
    install_repo(tmp_path)
    install_repo(tmp_path / "family")
    with pytest.raises(ValueError, match="ambiguous"):
        sync.write(tmp_path, repos, SOURCE)


@pytest.mark.parametrize("text", [sync.BEGIN, sync.END, sync.END + sync.BEGIN,
                                  sync.BEGIN + sync.BEGIN + sync.END])
def test_bad_markers_refused(text):
    with pytest.raises(ValueError):
        sync.render(text, SOURCE)


def test_rollout_hold_and_dry_run_are_explicit(tmp_path):
    mind = tmp_path / "mind"
    mind.mkdir()
    (mind / "policy").mkdir()
    (mind / sync.SOURCE).write_text(SOURCE)
    (mind / "repos.yaml").write_text("smoke_bootstrap_rollout: false\nrepos:\n  example:\n    smoke_bootstrap: true\n")
    tree = tmp_path / "tree"
    path = install_repo(tree)
    original = path.read_bytes()
    cmd = [sys.executable, str(SCRIPTS / "smoke_bootstrap_sync.py"),
           "--root", str(tree), "--mind", str(mind), "--require-all"]
    dry = subprocess.run(cmd + ["--dry-run"], capture_output=True, text=True)
    assert dry.returncode == 0, dry.stderr
    assert "would write" in dry.stdout
    assert path.read_bytes() == original
    write = subprocess.run(cmd + ["--write"], capture_output=True, text=True)
    assert write.returncode != 0
    assert "rollout is held" in write.stderr
    assert path.read_bytes() == original


def test_propagation_refuses_hold_before_clone(tmp_path, monkeypatch):
    (tmp_path / "repos.yaml").write_text("smoke_bootstrap_rollout: false\nrepos:\n  example:\n    smoke_bootstrap: true\n    github: example/example\n")
    def unexpected(*args, **kwargs):
        pytest.fail("must not clone while held")
    monkeypatch.setattr(propagate.subprocess, "run", unexpected)
    with pytest.raises(ValueError, match="rollout held"):
        propagate.propagate(tmp_path, tmp_path / "tree", dry_run=False)


def test_disposable_clone_propagation_and_failed_commit(tmp_path, monkeypatch, capsys):
    remote = tmp_path / "remote"
    path = install_repo(remote, "source", "workspace")
    repo = path.parents[2]
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    for key, value in [("user.name", "Test"), ("user.email", "test@example.invalid")]:
        propagate.git(repo, "config", key, value)
    propagate.git(repo, "add", ".")
    propagate.git(repo, "commit", "-m", "fixture")
    mind = tmp_path / "mind"
    (mind / "policy").mkdir(parents=True)
    (mind / sync.SOURCE).write_text(SOURCE)
    (mind / "repos.yaml").write_text("smoke_bootstrap_rollout: true\nrepos:\n  example:\n    smoke_bootstrap: true\n    github: example/example\n")
    original_run = subprocess.run
    def local_clone(argv, **kwargs):
        if argv[:2] == ["git", "clone"]:
            argv = argv[:-2] + [str(repo), argv[-1]]
        return original_run(argv, **kwargs)
    monkeypatch.setattr(propagate.subprocess, "run", local_clone)
    tree = tmp_path / "dry"
    tree.mkdir()
    propagate.propagate(mind, tree, dry_run=True)
    assert sync.BEGIN in (tree / "example" / sync.REL).read_text()
    assert "would push" in capsys.readouterr().out
    assert sync.BEGIN not in path.read_text()

    actual_git = propagate.git
    def fail_commit(repo, *args):
        if args[0] == "commit":
            raise subprocess.CalledProcessError(1, "git commit")
        if args[0] == "push":
            pytest.fail("must not push after commit failure")
        return actual_git(repo, *args)
    monkeypatch.setattr(propagate, "git", fail_commit)
    tree = tmp_path / "fail"
    tree.mkdir()
    with pytest.raises(ValueError, match="propagation failed: example"):
        propagate.propagate(mind, tree, dry_run=False)
    assert "FAILED" in capsys.readouterr().out


def test_bounded_repos_sync_write_only_changes_smoke_block(tmp_path, monkeypatch):
    import repos_sync
    mind = tmp_path / "PyAutoMind"
    mind.mkdir()
    (mind / "policy").mkdir()
    (mind / sync.SOURCE).write_text(SOURCE)
    (mind / "repos.yaml").write_text("categories: {}\nsmoke_bootstrap_rollout: true\nrepos:\n  example:\n    smoke_bootstrap: true\n")
    path = install_repo(tmp_path)
    # Use the real CLI handler but isolate unrelated policy loading. A narrow
    # write must never invoke any unrelated writer, even in an empty workspace.
    monkeypatch.setattr(repos_sync, "__file__", str(mind / "scripts/repos_sync.py"))
    for name in ("load_history_policy", "load_remote_sessions", "load_deliverable_policy",
                 "load_session_hook", "load_deliverable_hook"):
        monkeypatch.setattr(repos_sync, name, lambda *a: "")
    monkeypatch.setattr(repos_sync, "system_map", lambda *a: "")
    for name in ("write_root_marker", "write_block", "write_codex_hooks", "write_session_hooks"):
        monkeypatch.setattr(repos_sync, name, lambda *a, **k: pytest.fail("unrelated writer"))
    monkeypatch.setattr(sys, "argv", ["repos_sync.py", "--root", str(tmp_path),
                                    "--write", "--only", sync.LABEL])
    with pytest.raises(SystemExit) as result:
        repos_sync.main()
    assert result.value.code == 0
    assert sync.BEGIN in path.read_text()
    assert not (tmp_path / ".pyauto-root").exists()


@pytest.mark.parametrize("ancestor", [False, True])
def test_destination_root_and_its_ancestors_cannot_be_symlinks(tmp_path, ancestor):
    real = tmp_path / "real"
    real.mkdir()
    root = real / "tree" if ancestor else real
    path = install_repo(root)
    original = path.read_bytes()
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    destination = link / "tree" if ancestor else link
    with pytest.raises(ValueError, match="symlink"):
        sync.write(destination, {"example": {"smoke_bootstrap": True}}, SOURCE)
    assert path.read_bytes() == original
