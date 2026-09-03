"""--write must not install `.claude/` into a repo whose own lint rejects it.

`repos_sync.py --write` creates exactly two top-level entries in every
checked-out repo — `.claude/` and the `CLAUDE.md` pointer — and knows nothing
about the target beyond "checked out, has an AGENTS.md". A repo that lints its
own layout has no way to know the write is coming, so the write breaks that
repo's CI and the breakage reads as the repo's fault. The guard asks the
target's own allowlist first; these tests pin that it actually refuses.

Conventions this file follows (see `test_repos_sync_hygiene_coverage.py`):

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository, and the assertions
   are about the guard's logic rather than whatever happens to be checked out.
2. **Prove each leg FAILS.** Every failure mode below is driven with input that
   must trip it — a check that cannot fail is decoration.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

HOOK_TEXT = "#!/usr/bin/env bash\necho canonical\n"
DELIVERABLE_TEXT = "#!/usr/bin/env bash\necho canonical guard\n"
REPOS = {"OrganOne": {"category": "organ"}}

PERMISSIVE = """\
ALLOWED_TOP_DIRS = {".claude", ".git", "scripts"}
ALLOWED_TOP_FILES = {"AGENTS.md", "CLAUDE.md", "README.md"}
"""
FORBIDS_BOTH = """\
ALLOWED_TOP_DIRS = {".git", "scripts"}
ALLOWED_TOP_FILES = {"AGENTS.md", "README.md"}
"""


def make_repo(root, name="OrganOne", *, lint=None):
    """A checked-out repo, optionally carrying its own layout lint."""
    repo = root / name
    repo.mkdir(parents=True)
    (repo / "AGENTS.md").write_text("# guidance\n")
    if lint is not None:
        path = repo / repos_sync.STRUCTURE_LINT_CANDIDATES[0]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(lint)
    return repo


# --- reading the allowlist ------------------------------------------------


def test_repo_without_a_lint_is_unconstrained(tmp_path):
    repo = make_repo(tmp_path)
    assert repos_sync.structure_lint_verdict(repo) == (None, [], [])
    assert not repos_sync.structure_lint_forbids(repo, ".claude")


def test_permissive_lint_forbids_nothing(tmp_path):
    repo = make_repo(tmp_path, lint=PERMISSIVE)
    lint, forbidden, unreadable = repos_sync.structure_lint_verdict(repo)
    assert lint is not None
    assert (forbidden, unreadable) == ([], [])


def test_lint_omitting_both_entries_forbids_both(tmp_path):
    repo = make_repo(tmp_path, lint=FORBIDS_BOTH)
    assert repos_sync.structure_lint_verdict(repo)[1] == [".claude", "CLAUDE.md"]


def test_the_two_entries_are_governed_by_separate_allowlists(tmp_path):
    """A dirs-only allowlist must not vouch for the CLAUDE.md file."""
    repo = make_repo(
        tmp_path,
        lint='ALLOWED_TOP_DIRS = {".claude"}\nALLOWED_TOP_FILES = {"README.md"}\n',
    )
    assert repos_sync.structure_lint_verdict(repo)[1] == ["CLAUDE.md"]


def test_list_and_tuple_allowlists_are_read_too(tmp_path):
    repo = make_repo(
        tmp_path,
        lint='ALLOWED_TOP_DIRS = [".claude"]\nALLOWED_TOP_FILES = ("CLAUDE.md",)\n',
    )
    assert repos_sync.structure_lint_verdict(repo)[1] == []


def test_computed_allowlist_is_unreadable_not_permissive(tmp_path):
    """A lint we cannot read without running it must never read as an all-clear."""
    repo = make_repo(
        tmp_path,
        lint='BASE = {".git"}\nALLOWED_TOP_DIRS = BASE | {".claude"}\n'
             'ALLOWED_TOP_FILES = {"CLAUDE.md"}\n',
    )
    _, forbidden, unreadable = repos_sync.structure_lint_verdict(repo)
    assert unreadable == ["ALLOWED_TOP_DIRS"]
    assert forbidden == []  # "cannot tell" is not "forbids" — it must not block


def test_unparseable_lint_is_unreadable_not_permissive(tmp_path):
    repo = make_repo(tmp_path, lint="ALLOWED_TOP_DIRS = {\n")
    _, forbidden, unreadable = repos_sync.structure_lint_verdict(repo)
    assert unreadable == ["ALLOWED_TOP_DIRS", "ALLOWED_TOP_FILES"]
    assert forbidden == []


# --- the writers refuse ---------------------------------------------------


def test_write_installs_into_a_repo_whose_lint_allows_it(tmp_path):
    repo = make_repo(tmp_path, lint=PERMISSIVE)
    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT,
                                  DELIVERABLE_TEXT)
    repos_sync.write_claude_md_pointers(tmp_path, REPOS)
    assert (repo / repos_sync.SESSION_HOOK_REL).exists()
    assert (repo / repos_sync.DELIVERABLE_HOOK_REL).exists()
    assert (repo / repos_sync.SESSION_SETTINGS_REL).exists()
    assert (repo / "CLAUDE.md").exists()


def test_write_refuses_a_repo_whose_lint_disallows_the_entries(tmp_path):
    repo = make_repo(tmp_path, lint=FORBIDS_BOTH)
    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT,
                                  DELIVERABLE_TEXT)
    repos_sync.write_claude_md_pointers(tmp_path, REPOS)
    assert not (repo / ".claude").exists()
    assert not (repo / "CLAUDE.md").exists()


# --- the checks agree with the writers ------------------------------------


def test_skipped_repo_is_not_also_reported_as_generated_drift(tmp_path):
    """The write side and the drift side must agree, or a deliberately
    unwritten repo reads as permanent drift on every run."""
    make_repo(tmp_path, lint=FORBIDS_BOTH)
    assert repos_sync.check_session_hooks(
        tmp_path, REPOS, HOOK_TEXT, DELIVERABLE_TEXT
    ) == []
    assert repos_sync.check_claude_md_pointers(tmp_path, REPOS) == []


def test_skipped_repo_is_reported_by_its_own_check(tmp_path):
    make_repo(tmp_path, lint=FORBIDS_BOTH)
    problems = repos_sync.check_structure_lints(tmp_path, REPOS)
    assert len(problems) == 2
    assert any(".claude" in p for p in problems)
    assert any("CLAUDE.md" in p for p in problems)
    assert all("OrganOne" in p for p in problems)


def test_unreadable_allowlist_is_reported(tmp_path):
    make_repo(tmp_path, lint="ALLOWED_TOP_DIRS = {\n")
    problems = repos_sync.check_structure_lints(tmp_path, REPOS)
    assert len(problems) == 2
    assert all("cannot tell" in p for p in problems)


def test_permissive_and_lintless_repos_are_silent(tmp_path):
    make_repo(tmp_path, "OrganOne", lint=PERMISSIVE)
    make_repo(tmp_path, "LibTwo")
    repos = {"OrganOne": {"category": "organ"}, "LibTwo": {"category": "library"}}
    assert repos_sync.check_structure_lints(tmp_path, repos) == []


def test_repo_that_is_not_checked_out_is_skipped(tmp_path):
    assert repos_sync.check_structure_lints(tmp_path, REPOS) == []


def test_forbidden_entry_already_on_disk_is_reported_as_currently_failing(tmp_path):
    """The case that actually happened: a --write from before the guard existed
    left `.claude/` behind, so the repo's lint is red now. Skipping the next
    write does not undo that, and the report must not imply it did."""
    repo = make_repo(tmp_path, lint=FORBIDS_BOTH)
    (repo / ".claude").mkdir()
    (repo / "CLAUDE.md").write_text(repos_sync.CLAUDE_MD_POINTER)
    problems = repos_sync.check_structure_lints(tmp_path, REPOS)
    assert len(problems) == 2
    assert all("already installed" in p for p in problems)
    assert all("skips" not in p for p in problems)
