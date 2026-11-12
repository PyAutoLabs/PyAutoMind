"""`prompt_sync_push` commits ONLY the paths it is given, and refuses anything unsafe.

The helper used to run `git add -A`, then commit and push with no guard. In a
shared Mind checkout that swept other sessions' edits into commits, committed
conflict markers, and pushed a `state.json` that no longer parsed. It now takes
explicit paths and refuses, committing nothing, when:

- no paths are given;
- the tree has changes outside the paths (staged, unstaged or untracked),
  including the source side of a staged rename;
- a changed file holds conflict markers (`<<<<<<< ` and `>>>>>>> ` lines; a lone
  `=======` is a Markdown setext underline and never counts);
- a changed `state.json` does not parse.

Like `test_prompt_sync_branch.py`, these drive the real script against a
throwaway repo with a real bare remote, so "nothing committed" and "nothing
pushed" are observed on the refs, not inferred from the source.

Fictional fixtures only, per `test_spawn_privacy.py`.
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
    (repo / "active.md").write_text("# Active\n")
    (repo / "planned.md").write_text("# Planned\n")
    (repo / "state.json").write_text('{"cards": []}\n')
    (repo / "draft").mkdir()
    (repo / "draft" / "an_idea.md").write_text("# An idea\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "seed")
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    return repo, remote


def _run(repo, snippet):
    """Source the real script against `repo` and run `snippet`."""
    return subprocess.run(
        ["bash", "-c", f'export PROMPT_REPO="{repo}"; '
                       f'source "{SYNC}"; {snippet}'],
        capture_output=True, text=True)


def _assert_refused(res, repo, remote, head_before, reason):
    assert res.returncode != 0, "the helper should have refused"
    assert "refusing, nothing committed" in res.stderr
    assert reason in res.stderr, res.stderr
    assert _git(repo, "rev-parse", "HEAD") == head_before, "a commit was made"
    assert _git(remote, "rev-parse", "main") == head_before, "something was pushed"


def _committed_paths(repo):
    return set(_git(repo, "show", "--name-only", "--no-renames",
                    "--format=", "HEAD").splitlines())


def test_no_paths_is_refused(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject"')

    _assert_refused(res, repo, remote, head, "no paths given")


def test_a_dirty_file_outside_the_paths_is_refused(tmp_path):
    """THE defect: another session's unstaged edit must not be swept in."""
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")
    (repo / "planned.md").write_text("# Planned\n\nanother session's edit\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')

    _assert_refused(res, repo, remote, head, "planned.md")
    # Nothing was staged on the way out either.
    assert _git(repo, "diff", "--cached", "--name-only") == ""


def test_a_staged_file_outside_the_paths_is_refused(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")
    (repo / "planned.md").write_text("# Planned\n\nstaged elsewhere\n")
    _git(repo, "add", "planned.md")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')

    _assert_refused(res, repo, remote, head, "planned.md")


def test_an_untracked_file_outside_the_paths_is_refused(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")
    (repo / "draft" / "someone_elses.md").write_text("# Not mine\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')

    _assert_refused(res, repo, remote, head, "draft/someone_elses.md")


def test_an_ignored_file_outside_the_paths_does_not_block(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    (repo / ".gitignore").write_text("scratch/\n")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore scratch")
    _git(repo, "push")
    (repo / "scratch").mkdir()
    (repo / "scratch" / "notes.md").write_text("ignored\n")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')

    assert res.returncode == 0, res.stderr
    assert _committed_paths(repo) == {"active.md"}


def test_a_rename_whose_source_is_outside_the_paths_is_refused(tmp_path):
    """A `git mv` commits a deletion too; its source must be among the paths."""
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "active").mkdir()
    _git(repo, "mv", "draft/an_idea.md", "active/an_idea.md")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active/an_idea.md')

    _assert_refused(res, repo, remote, head, "draft/an_idea.md")


def test_a_rename_with_both_sides_given_commits(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    (repo / "active").mkdir()
    _git(repo, "mv", "draft/an_idea.md", "active/an_idea.md")
    (repo / "active.md").write_text("# Active\n\n## an-idea\n")

    res = _run(repo, 'prompt_sync_push "prompt: issue an idea" '
                     'active.md draft/an_idea.md active/an_idea.md')

    assert res.returncode == 0, res.stderr
    assert _committed_paths(repo) == {
        "active.md", "draft/an_idea.md", "active/an_idea.md"}
    assert _git(remote, "rev-parse", "main") == _git(repo, "rev-parse", "HEAD")


def test_conflict_markers_are_refused(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "active.md").write_text(
        "# Active\n<<<<<<< Updated upstream\n## a-task\n=======\n"
        "## b-task\n>>>>>>> Stashed changes\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')

    _assert_refused(res, repo, remote, head, "conflict markers in 'active.md'")


def test_a_setext_underline_is_not_a_conflict_marker(tmp_path):
    """Mind Markdown underlines headings with `=======`; that alone must pass."""
    repo, remote = _repo_with_remote(tmp_path)
    (repo / "active.md").write_text("Active\n=======\n\n## a-task\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" active.md')

    assert res.returncode == 0, res.stderr
    assert _committed_paths(repo) == {"active.md"}


def test_an_unparseable_state_json_is_refused(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "state.json").write_text('{"cards": [\n')

    res = _run(repo, 'prompt_sync_push "prompt: a subject" state.json')

    _assert_refused(res, repo, remote, head, "'state.json' does not parse")


def test_happy_path_commits_exactly_the_given_paths_and_pushes(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")
    (repo / "state.json").write_text('{"cards": [{"text": "a-task"}]}\n')
    (repo / "complete" / "2026").mkdir(parents=True)
    (repo / "complete" / "2026" / "a_task.md").write_text("# a-task\n")

    # A directory path covers the files under it; absolute and ./ forms work.
    res = _run(repo, f'prompt_sync_push "prompt: ship a-task" '
                     f'./active.md "{repo}/state.json" complete/')

    assert res.returncode == 0, res.stderr
    assert _git(repo, "rev-list", "--count", f"{head}..HEAD") == "1"
    assert _committed_paths(repo) == {
        "active.md", "state.json", "complete/2026/a_task.md"}
    assert _git(repo, "log", "-1", "--format=%s") == "prompt: ship a-task"
    assert _git(remote, "rev-parse", "main") == _git(repo, "rev-parse", "HEAD")
    assert _git(repo, "status", "--porcelain") == ""


def test_a_path_outside_the_repo_is_refused(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    (repo / "active.md").write_text("# Active\n\n## a-task\n")

    res = _run(repo, 'prompt_sync_push "prompt: a subject" ../elsewhere.md')

    _assert_refused(res, repo, remote, head, "not a file or directory inside")


def test_new_prompts_commits_only_the_new_prompt_files(tmp_path):
    """`prompt_sync_new_prompts` keeps its contract: new untracked prompt files
    only. Something another session already staged stays staged, uncommitted."""
    repo, remote = _repo_with_remote(tmp_path)
    (repo / "planned.md").write_text("# Planned\n\nstaged elsewhere\n")
    _git(repo, "add", "planned.md")
    (repo / "draft" / "a new idea.md").write_text("# A new idea\n")

    res = _run(repo, "prompt_sync_new_prompts")

    assert res.returncode == 0, res.stderr
    assert _committed_paths(repo) == {"draft/a new idea.md"}
    assert _git(remote, "rev-parse", "main") == _git(repo, "rev-parse", "HEAD")
    assert _git(repo, "diff", "--cached", "--name-only") == "planned.md"


def test_a_file_staged_just_before_the_commit_does_not_ride_along(tmp_path):
    """A concurrent writer can stage between the final index check and the
    commit. Simulated by shadowing `git` so the `commit` call first stages a
    bystander: the explicit commit pathspec must leave it staged, uncommitted."""
    repo, remote = _repo_with_remote(tmp_path)
    (repo / "active.md").write_text("# Active\n\n## a-task\n")
    racer = (
        'git() { if [ "$3" = commit ]; then '
        'printf "racing edit\\n" >> "$2/planned.md"; '
        'command git -C "$2" add planned.md; fi; command git "$@"; }; '
    )

    res = _run(repo, racer + 'prompt_sync_push "prompt: a subject" active.md')

    assert res.returncode == 0, res.stderr
    assert _committed_paths(repo) == {"active.md"}
    assert _git(repo, "diff", "--cached", "--name-only") == "planned.md"
