"""`prompt_sync.sh` must push the branch it is ON, never a hardcoded `main`.

Both helpers used to end in `git push origin main` regardless of what was
checked out. `create_issue` step 6 and `start_dev` step 7 both instruct an agent
to call them, so a branch-scoped session — a cloud session with a designated
branch, or any PR-based flow — that followed the documented steps verbatim
pushed Mind straight to `main`, bypassing review entirely.

These tests drive the real script against throwaway git repos with real bare
remotes, because that is the only way to observe *which ref actually moved*. A
test that merely greps the source for the string would pass on a script that
still pushed the wrong branch by another route.

Fictional fixtures only, per `test_spawn_privacy.py` — `tests/**` is KEEP-copied
verbatim into the public template, so nothing here names a real task or prompt.
"""

import subprocess
from pathlib import Path

SYNC = Path(__file__).resolve().parents[1] / "scripts" / "prompt_sync.sh"


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True).stdout.strip()


def _repo_with_remote(tmp_path):
    """A checkout on `main` with one commit, wired to a real bare remote."""
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)],
                   capture_output=True, check=True)
    repo = tmp_path / "mind"
    subprocess.run(["git", "init", "-b", "main", str(repo)],
                   capture_output=True, check=True)
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Test")
    (repo / "seed.md").write_text("# seed\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "seed")
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    return repo, remote


def _run(repo, snippet):
    """Source the real script against `repo` and run `snippet`."""
    return subprocess.run(
        ["bash", "-c", f'set -e; export PROMPT_REPO="{repo}"; '
                       f'source "{SYNC}"; {snippet}'],
        capture_output=True, text=True)


def _remote_branches(remote):
    out = subprocess.run(["git", "-C", str(remote), "for-each-ref",
                          "--format=%(refname:short)", "refs/heads/"],
                         capture_output=True, text=True, check=True).stdout
    return set(out.split())


def test_push_from_a_feature_branch_does_not_touch_main(tmp_path):
    """THE defect. On a branch-scoped checkout the helper must move that
    branch's ref and leave `main` exactly where it was."""
    repo, remote = _repo_with_remote(tmp_path)
    main_before = _git(remote, "rev-parse", "main")

    _git(repo, "checkout", "-b", "claude/some-task")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')
    assert res.returncode == 0, res.stderr

    assert "claude/some-task" in _remote_branches(remote)
    assert _git(remote, "rev-parse", "main") == main_before, (
        "main moved — the helper pushed the wrong branch")


def test_committed_work_actually_reaches_the_remote(tmp_path):
    """The failure the old script hit MOST often, and the quietest one.

    `git push origin main` from a feature branch pushes the local `main` ref —
    not the commit just made. When local `main` already matches the remote (the
    normal case for a session that branched from it) the push is a no-op, exits
    0, and the committed work never leaves the machine. The caller is told the
    sync succeeded. In an ephemeral cloud container that is silent loss.

    Leaking to `main` is the other half of the same bug and needs local `main`
    to be ahead — see `test_a_branch_push_never_advances_main` below. This test
    is the common case: the work must be ON the remote afterwards.
    """
    repo, remote = _repo_with_remote(tmp_path)
    _git(repo, "checkout", "-b", "claude/some-task")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')
    assert res.returncode == 0, res.stderr

    local_head = _git(repo, "rev-parse", "HEAD")
    assert _git(remote, "rev-parse", "claude/some-task") == local_head, (
        "the commit never reached the remote")


def test_a_branch_push_never_advances_main(tmp_path):
    """The other half: an unpushed commit sitting on local `main` must not be
    published as a side effect of syncing a feature branch.

    The old script pushed it — unreviewed work onto `main`, while the branch
    work it was actually asked to sync stayed local.
    """
    repo, remote = _repo_with_remote(tmp_path)
    (repo / "secret.md").write_text("unreviewed local work\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "local main work")
    main_before = _git(remote, "rev-parse", "main")

    _git(repo, "checkout", "-b", "claude/some-task")
    (repo / "active.md").write_text("# Active\n")
    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')
    assert res.returncode == 0, res.stderr

    assert _git(remote, "rev-parse", "main") == main_before, (
        "an unpushed local main commit was published as a side effect")
    assert "claude/some-task" in _remote_branches(remote)


def test_push_on_main_still_pushes_main(tmp_path):
    """The single-branch laptop flow must be unchanged: there the current
    branch IS main, so the fix is a no-op for it."""
    repo, remote = _repo_with_remote(tmp_path)
    main_before = _git(remote, "rev-parse", "main")

    (repo / "active.md").write_text("# Active\n")
    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')
    assert res.returncode == 0, res.stderr

    assert _git(remote, "rev-parse", "main") != main_before
    assert _remote_branches(remote) == {"main"}


def test_push_is_still_a_no_op_when_nothing_is_staged(tmp_path):
    """The documented contract. Guards a regression the branch fix can easily
    introduce: if the early return moves after the push, a caller with no
    changes pushes anyway."""
    repo, remote = _repo_with_remote(tmp_path)
    _git(repo, "checkout", "-b", "claude/some-task")

    res = _run(repo, 'prompt_sync_push "prompt: nothing to do" active.md')
    assert res.returncode == 0, res.stderr

    assert _remote_branches(remote) == {"main"}, (
        "a no-op call created a remote branch")


def test_new_prompts_sweep_also_pushes_the_current_branch(tmp_path):
    """The sibling helper carried the same hardcoded push."""
    repo, remote = _repo_with_remote(tmp_path)
    main_before = _git(remote, "rev-parse", "main")

    _git(repo, "checkout", "-b", "claude/some-task")
    draft = repo / "draft" / "feature" / "widget"
    draft.mkdir(parents=True)
    (draft / "a_new_idea.md").write_text("# A new idea\n")

    res = _run(repo, "prompt_sync_new_prompts")
    assert res.returncode == 0, res.stderr

    assert "claude/some-task" in _remote_branches(remote)
    assert _git(remote, "rev-parse", "main") == main_before


def test_detached_head_is_refused(tmp_path):
    """`push -u origin HEAD` from a detached HEAD is meaningless — say so
    rather than guessing a branch."""
    repo, _ = _repo_with_remote(tmp_path)
    (repo / "active.md").write_text("# Active\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "second")
    _git(repo, "checkout", "--detach", "HEAD")
    (repo / "active.md").write_text("# Active\n\nchanged\n")

    res = _run(repo, 'prompt_sync_push "prompt: from detached" active.md')
    assert res.returncode != 0
    assert "detached HEAD" in res.stderr
