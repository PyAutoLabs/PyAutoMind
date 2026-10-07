"""--write must not install `.claude/` into a repo whose own lint rejects it.

`repos_sync.py --write` creates exactly one top-level entry in every
checked-out repo — `.claude/` — and knows nothing about the target beyond
"checked out, has an AGENTS.md". (The `CLAUDE.md` pointer it used to create is
retired, PyAutoMind#482: --write only ever removes it now, and the tests for
that live at the bottom of this file.) A repo that lints its
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


def test_lint_omitting_claude_dir_forbids_it(tmp_path):
    repo = make_repo(tmp_path, lint=FORBIDS_BOTH)
    assert repos_sync.structure_lint_verdict(repo)[1] == [".claude"]


def test_claude_md_is_no_longer_a_generated_entry(tmp_path):
    """--write never creates CLAUDE.md now, so a lint that leaves it off its
    files allowlist forbids nothing; and the files allowlist cannot vouch for
    the `.claude/` directory."""
    repo = make_repo(
        tmp_path,
        lint='ALLOWED_TOP_DIRS = {".claude"}\nALLOWED_TOP_FILES = {"README.md"}\n',
    )
    assert repos_sync.structure_lint_verdict(repo)[1] == []
    repo = make_repo(
        tmp_path, "OrganTwo",
        lint='ALLOWED_TOP_DIRS = {".git"}\nALLOWED_TOP_FILES = {".claude"}\n',
    )
    assert repos_sync.structure_lint_verdict(repo)[1] == [".claude"]


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
    assert unreadable == ["ALLOWED_TOP_DIRS"]
    assert forbidden == []


# --- the writers refuse ---------------------------------------------------


def test_write_installs_into_a_repo_whose_lint_allows_it(tmp_path):
    repo = make_repo(tmp_path, lint=PERMISSIVE)
    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT,
                                  DELIVERABLE_TEXT)
    repos_sync.remove_claude_md_pointers(tmp_path, REPOS)
    assert (repo / repos_sync.SESSION_HOOK_REL).exists()
    assert (repo / repos_sync.DELIVERABLE_HOOK_REL).exists()
    assert (repo / repos_sync.SESSION_SETTINGS_REL).exists()
    assert not (repo / "CLAUDE.md").exists()  # retired: never created


def test_write_refuses_a_repo_whose_lint_disallows_the_entries(tmp_path):
    repo = make_repo(tmp_path, lint=FORBIDS_BOTH)
    repos_sync.write_session_hooks(tmp_path, REPOS, HOOK_TEXT,
                                  DELIVERABLE_TEXT)
    repos_sync.remove_claude_md_pointers(tmp_path, REPOS)
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
    assert len(problems) == 1
    assert ".claude" in problems[0]
    assert "OrganOne" in problems[0]


def test_unreadable_allowlist_is_reported(tmp_path):
    make_repo(tmp_path, lint="ALLOWED_TOP_DIRS = {\n")
    problems = repos_sync.check_structure_lints(tmp_path, REPOS)
    assert len(problems) == 1
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
    problems = repos_sync.check_structure_lints(tmp_path, REPOS)
    assert len(problems) == 1
    assert all("already installed" in p for p in problems)
    assert all("skips" not in p for p in problems)


# --- CLAUDE.md retirement (PyAutoMind#482) --------------------------------
#
# Claude Code reads AGENTS.md natively, and any CLAUDE.md in the cwd or an
# ancestor makes it ignore every AGENTS.md. So a repo with an AGENTS.md must
# have no CLAUDE.md: the check names every survivor, and the removal deletes
# ONLY a content-free pointer — real content is reported, never deleted.

POINTER_COMMENTED = """\
@AGENTS.md

<!-- Guidance is agent-agnostic and lives in AGENTS.md (read natively by Codex,
     Cursor, etc.). Keep it a pointer — put content in AGENTS.md. -->
"""
POINTER_BOILERPLATE = """\
# OrganOne — agent instructions

The canonical, agent-agnostic instructions live in `AGENTS.md`. Claude Code loads them via
the import below; if your tool does not process `@`-imports, open `AGENTS.md` in this
directory and read it directly.

@AGENTS.md
"""
POINTER_BOILERPLATE_REWRAPPED = """\
# OrganOne — agent instructions
The canonical, agent-agnostic instructions live in `AGENTS.md`. Claude Code loads them
via the import below; if your tool does not process `@`-imports, open `AGENTS.md` in
this directory and read it directly.
@AGENTS.md
"""
CONTENT_BEARING = """\
@AGENTS.md

## Claude-specific notes

- Always run the slow tests before shipping.
"""
NO_IMPORT = "# nothing useful\n"
CHECK_LABEL = "CLAUDE.md → AGENTS.md pointers"


def test_check_leg_name_is_byte_identical_for_heart():
    """PyAutoHeart's manifest-drift parser keys on the printed leg name; the
    retirement inverts the rule but must not rename the leg."""
    source = Path(repos_sync.__file__).read_text()
    assert f'"{CHECK_LABEL}":' in source


def test_pointer_shapes_are_content_free():
    for text in (POINTER_COMMENTED, POINTER_BOILERPLATE,
                 POINTER_BOILERPLATE_REWRAPPED, "@AGENTS.md\n"):
        assert repos_sync.claude_md_is_pointer(text), text


def test_content_or_a_missing_import_is_not_a_pointer():
    assert not repos_sync.claude_md_is_pointer(CONTENT_BEARING)
    assert not repos_sync.claude_md_is_pointer(NO_IMPORT)
    # Prose that merely mentions AGENTS.md is not the import.
    assert not repos_sync.claude_md_is_pointer("See @AGENTS.md for details.\n")


def test_check_passes_when_no_claude_md_remains(tmp_path):
    make_repo(tmp_path)
    assert repos_sync.check_claude_md_pointers(tmp_path, REPOS) == []


def test_check_fails_naming_a_repo_that_still_has_a_pointer(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "CLAUDE.md").write_text(POINTER_BOILERPLATE)
    problems = repos_sync.check_claude_md_pointers(tmp_path, REPOS)
    assert len(problems) == 1
    assert "OrganOne" in problems[0] and "retired CLAUDE.md pointer" in problems[0]


def test_check_reports_content_bearing_claude_md_for_a_human(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "CLAUDE.md").write_text(CONTENT_BEARING)
    problems = repos_sync.check_claude_md_pointers(tmp_path, REPOS)
    assert len(problems) == 1
    assert "OrganOne" in problems[0] and "by hand" in problems[0]


def test_check_fires_even_where_a_layout_lint_forbids_claude_md(tmp_path):
    """The old leg exempted lint-forbidden repos because --write skipped them;
    removal needs no allowlist, so nothing is exempt now."""
    repo = make_repo(tmp_path, lint=FORBIDS_BOTH)
    (repo / "CLAUDE.md").write_text(POINTER_COMMENTED)
    assert len(repos_sync.check_claude_md_pointers(tmp_path, REPOS)) == 1


def test_repo_without_agents_md_keeps_its_claude_md(tmp_path):
    """No AGENTS.md: the CLAUDE.md may be the repo's only guidance."""
    repo = tmp_path / "OrganOne"
    repo.mkdir()
    (repo / "CLAUDE.md").write_text(POINTER_COMMENTED)
    assert repos_sync.check_claude_md_pointers(tmp_path, REPOS) == []
    assert repos_sync.remove_claude_md_pointers(tmp_path, REPOS) == []
    assert (repo / "CLAUDE.md").exists()


def test_removal_deletes_content_free_pointers_only(tmp_path):
    repos = {"OrganOne": {"category": "organ"}, "LibTwo": {"category": "library"},
             "ToolThree": {"category": "tool"}}
    one = make_repo(tmp_path, "OrganOne")
    two = make_repo(tmp_path, "LibTwo")
    three = make_repo(tmp_path, "ToolThree")
    (one / "CLAUDE.md").write_text(POINTER_COMMENTED)
    (two / "CLAUDE.md").write_text(POINTER_BOILERPLATE_REWRAPPED)
    (three / "CLAUDE.md").write_text(CONTENT_BEARING)

    removed = repos_sync.remove_claude_md_pointers(tmp_path, repos)

    assert sorted(removed) == sorted([one / "CLAUDE.md", two / "CLAUDE.md"])
    assert not (one / "CLAUDE.md").exists()
    assert not (two / "CLAUDE.md").exists()
    # A content-bearing CLAUDE.md is reported, not deleted — byte for byte.
    assert (three / "CLAUDE.md").read_text() == CONTENT_BEARING
    problems = repos_sync.check_claude_md_pointers(tmp_path, repos)
    assert len(problems) == 1 and "ToolThree" in problems[0]


def test_removal_never_deletes_a_claude_md_without_the_import(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "CLAUDE.md").write_text(NO_IMPORT)
    assert repos_sync.remove_claude_md_pointers(tmp_path, REPOS) == []
    assert (repo / "CLAUDE.md").read_text() == NO_IMPORT


def test_removal_is_idempotent_and_touches_nothing_else(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "CLAUDE.md").write_text(POINTER_COMMENTED)
    repos_sync.remove_claude_md_pointers(tmp_path, REPOS)
    assert sorted(p.name for p in repo.iterdir()) == ["AGENTS.md"]
    assert repos_sync.remove_claude_md_pointers(tmp_path, REPOS) == []
    assert (repo / "AGENTS.md").read_text() == "# guidance\n"


# --- nested CLAUDE.md pointers (PyAutoMind#484) ----------------------------
#
# The same rule below a repo's root: a session started INSIDE a folder whose
# CLAUDE.md sits beside an AGENTS.md loses every ancestor AGENTS.md. Discovery
# is `git ls-files` — untracked and ignored trees are never read — and a nested
# CLAUDE.md with no sibling AGENTS.md is out of scope (neither reported nor
# touched).

import subprocess  # noqa: E402

import yaml  # noqa: E402

GIT = ["git", "-c", "user.email=t@example.invalid", "-c", "user.name=t",
       "-c", "init.defaultBranch=main"]
NESTED_POINTERS = {
    # The nested shapes found in the wild, one per wording.
    "scripts/CLAUDE.md": """\
# scripts — agent instructions

The canonical instructions for this folder live in `AGENTS.md`. Claude Code loads them via
the import below; if your tool does not process `@`-imports, open `AGENTS.md` in this
directory and read it directly.

@AGENTS.md
""",
    "wiki/literature/CLAUDE.md": """\
# wiki/literature — schema and usage rules

The canonical schema and usage rules for this literature sub-wiki live in `AGENTS.md`.
Claude Code loads them via the import below; if your tool does not process `@`-imports, open
`AGENTS.md` in this directory and read it directly.

@AGENTS.md
""",
    "wiki/region/CLAUDE.md": """\
# wiki/region — schema and usage rules

The canonical scope and usage rules for this Euclid sub-wiki live in `AGENTS.md`
(schema shared with `../literature/AGENTS.md`). Claude Code loads them via the import
below; if your tool does not process `@`-imports, open `AGENTS.md` in this directory
and read it directly.

@AGENTS.md
""",
    "wiki/CLAUDE.md": """\
# Claude Code adapter

Shared instructions live in [AGENTS.md](AGENTS.md).

@AGENTS.md
""",
    "wiki/deep/er/CLAUDE.md": "@AGENTS.md\n",
}


def make_git_repo(root, files, name="OrganOne", *, untracked=None):
    """A checked-out git repo (root AGENTS.md included) with `files` tracked
    and committed, plus `untracked` written but never added."""
    repo = make_repo(root, name)
    for rel, text in {**files, **(untracked or {})}.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    subprocess.run(GIT + ["init", "-q", str(repo)], check=True)
    subprocess.run(GIT + ["-C", str(repo), "add", "AGENTS.md", *files],
                   check=True)
    subprocess.run(GIT + ["-C", str(repo), "commit", "-qm", "base"],
                   check=True)
    return repo


def with_sibling_agents(files):
    """Each CLAUDE.md in `files` plus the AGENTS.md beside it."""
    out = dict(files)
    for rel in files:
        out[str(Path(rel).parent / "AGENTS.md")] = "# folder guidance\n"
    return out


def test_every_nested_wording_is_a_content_free_pointer():
    for rel, text in NESTED_POINTERS.items():
        assert repos_sync.claude_md_is_pointer(text), rel


def test_a_near_miss_wording_is_content_not_a_pointer():
    """The boilerplate is matched exactly: a reworded sentence is content."""
    text = NESTED_POINTERS["wiki/CLAUDE.md"].replace(
        "Shared instructions", "Shared and private instructions")
    assert not repos_sync.claude_md_is_pointer(text)


def test_check_names_each_tracked_nested_pointer(tmp_path):
    make_git_repo(tmp_path, with_sibling_agents(NESTED_POINTERS))
    problems = repos_sync.check_claude_md_pointers(tmp_path, REPOS)
    assert len(problems) == len(NESTED_POINTERS), problems
    for rel in NESTED_POINTERS:
        assert any(f"'OrganOne/{rel}'" in p and "retired CLAUDE.md pointer" in p
                   for p in problems), rel


def test_check_reports_a_nested_content_bearing_claude_md(tmp_path):
    make_git_repo(tmp_path, with_sibling_agents(
        {"docs/CLAUDE.md": CONTENT_BEARING}))
    problems = repos_sync.check_claude_md_pointers(tmp_path, REPOS)
    assert len(problems) == 1
    assert "'OrganOne/docs/CLAUDE.md'" in problems[0] and "by hand" in problems[0]


def test_untracked_and_ignored_nested_claude_mds_are_never_read(tmp_path):
    """`tmp/`, `output/`, `.worktrees/` hold copies of other checkouts; only the
    repo's tracked content is in scope."""
    untracked = with_sibling_agents({
        "tmp/CLAUDE.md": "@AGENTS.md\n",
        "output/run/CLAUDE.md": "@AGENTS.md\n",
        ".worktrees/branch/CLAUDE.md": "@AGENTS.md\n",
    })
    untracked[".gitignore"] = "output/\n.worktrees/\n"
    repo = make_git_repo(tmp_path, {}, untracked=untracked)
    assert repos_sync.check_claude_md_pointers(tmp_path, REPOS) == []
    assert repos_sync.remove_claude_md_pointers(tmp_path, REPOS) == []
    assert (repo / "tmp/CLAUDE.md").exists()
    assert (repo / "output/run/CLAUDE.md").exists()


def test_a_nested_claude_md_without_a_sibling_agents_md_is_left_alone(tmp_path):
    repo = make_git_repo(tmp_path, {"lonely/CLAUDE.md": "@AGENTS.md\n"})
    assert repos_sync.check_claude_md_pointers(tmp_path, REPOS) == []
    assert repos_sync.remove_claude_md_pointers(tmp_path, REPOS) == []
    assert (repo / "lonely/CLAUDE.md").read_text() == "@AGENTS.md\n"


def test_a_non_git_checkout_is_scanned_at_its_root_only(tmp_path):
    """Without a .git of its own, `git -C` would climb to an enclosing repo;
    the nested scan stays out and the root check still runs."""
    repo = make_repo(tmp_path)
    (repo / "CLAUDE.md").write_text("@AGENTS.md\n")
    (repo / "sub").mkdir()
    (repo / "sub/AGENTS.md").write_text("# folder\n")
    (repo / "sub/CLAUDE.md").write_text("@AGENTS.md\n")
    problems = repos_sync.check_claude_md_pointers(tmp_path, REPOS)
    assert len(problems) == 1 and "'OrganOne':" in problems[0], problems
    assert repos_sync.remove_claude_md_pointers(tmp_path, REPOS) == \
        [repo / "CLAUDE.md"]
    assert (repo / "sub/CLAUDE.md").exists()


def test_nested_removal_deletes_pointers_keeps_content_and_is_idempotent(tmp_path):
    files = with_sibling_agents({**NESTED_POINTERS,
                                 "docs/CLAUDE.md": CONTENT_BEARING})
    files["CLAUDE.md"] = POINTER_COMMENTED  # the root shape rides along
    repo = make_git_repo(tmp_path, files)

    removed = repos_sync.remove_claude_md_pointers(tmp_path, REPOS)

    assert sorted(removed) == sorted(
        [repo / "CLAUDE.md"] + [repo / rel for rel in NESTED_POINTERS])
    for rel in NESTED_POINTERS:
        assert not (repo / rel).exists(), rel
        # The sibling AGENTS.md is never touched.
        assert (repo / Path(rel).parent / "AGENTS.md").read_text() == \
            "# folder guidance\n"
    assert (repo / "docs/CLAUDE.md").read_text() == CONTENT_BEARING
    problems = repos_sync.check_claude_md_pointers(tmp_path, REPOS)
    assert len(problems) == 1 and "'OrganOne/docs/CLAUDE.md'" in problems[0]
    # Idempotent while the deletions are still uncommitted: `git ls-files`
    # still lists them, but a file no longer on disk is not re-reported.
    assert repos_sync.remove_claude_md_pointers(tmp_path, REPOS) == []


# --- the propagation job stages every deletion the removal made ------------

def _propagate_run():
    workflow = (Path(__file__).resolve().parents[1]
                / ".github/workflows/session_hook_propagate.yml")
    spec = yaml.safe_load(workflow.read_text())
    return next(step["run"] for step in spec["jobs"]["propagate"]["steps"]
                if "remove_claude_md_pointers" in (step.get("run") or ""))


def _staging_snippet():
    """The CLAUDE.md staging lines of the propagation step, verbatim."""
    lines = _propagate_run().splitlines()
    start = next(i for i, line in enumerate(lines)
                 if "Stage the pointers' deletions" in line)
    end = next(i for i in range(start, len(lines))
               if lines[i].strip() == "done")
    return "\n".join(lines[start:end + 1])


def test_propagation_removal_stays_dispatch_only():
    run = _propagate_run()
    assert 'if os.environ.get("RETIRE_CLAUDE_MD") == "true":' in run
    workflow = (Path(__file__).resolve().parents[1]
                / ".github/workflows/session_hook_propagate.yml").read_text()
    assert "RETIRE_CLAUDE_MD: ${{ github.event_name == 'workflow_dispatch' }}" \
        in workflow


def test_propagation_stages_every_removed_claude_md_and_nothing_else(tmp_path):
    """Execute the job's own staging lines after a real removal: root and
    nested deletions are staged, a KEPT file and every other change are not."""
    files = with_sibling_agents({**NESTED_POINTERS,
                                 "docs/CLAUDE.md": CONTENT_BEARING})
    files["CLAUDE.md"] = POINTER_COMMENTED
    files["notes.md"] = "base\n"
    repo = make_git_repo(tmp_path, files)
    (repo / "notes.md").write_text("an unrelated edit\n")
    repos_sync.remove_claude_md_pointers(tmp_path, REPOS)

    subprocess.run(["bash", "-c", _staging_snippet()], check=True,
                   env={"PATH": "/usr/bin:/bin", "repo": str(repo)})

    staged = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--name-status"],
        check=True, capture_output=True, text=True).stdout.splitlines()
    assert sorted(staged) == sorted(
        f"D\t{rel}" for rel in ["CLAUDE.md", *NESTED_POINTERS])


def test_propagation_staging_is_a_no_op_when_nothing_was_removed(tmp_path):
    """A push run never calls the removal, so nothing may be staged."""
    repo = make_git_repo(tmp_path, with_sibling_agents(NESTED_POINTERS))
    subprocess.run(["bash", "-c", _staging_snippet()], check=True,
                   env={"PATH": "/usr/bin:/bin", "repo": str(repo)})
    assert subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--quiet"]).returncode == 0
