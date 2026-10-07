"""The two `required=True` --write targets have a check leg.

`--write` regenerates the workspace-root AGENTS.md routing table and the
PyAutoBrain/skills/WORKFLOW.md owner map, but check mode used to verify
neither: the root table once went two organs and a role line stale while every
check printed OK. These pin the leg that closes that gap.

Conventions, as in the sibling repos_sync tests:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository.
2. **Prove each leg FAILS.** A drift check that cannot fail is decoration.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

CATEGORIES = {"organ": {"label": "Organ", "role": "example"}, "library": None}
REPOS = {
    "OrganCore": {"category": "organ", "path": "organs/OrganCore",
                  "github": "Example/OrganCore", "role": "the core organ"},
    "LibAlpha": {"category": "library", "path": "lib/LibAlpha",
                 "github": "Example/LibAlpha", "role": "a library"},
}


def _blocked(content):
    return (f"# Workspace\n\n{repos_sync.MARK_BEGIN}\n{content}\n"
            f"{repos_sync.MARK_END}\n\ntrailing prose\n")


def _root_agents(root, content):
    (root / "AGENTS.md").write_text(_blocked(content))


def _workflow(root, content):
    path = root / "PyAutoBrain" / "skills" / "WORKFLOW.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_blocked(content))
    return path


def test_in_sync_root_table_and_owner_map_are_clean(tmp_path):
    _root_agents(tmp_path, repos_sync.routing_table(CATEGORIES, REPOS))
    _workflow(tmp_path, repos_sync.owner_map(CATEGORIES, REPOS))
    assert repos_sync.check_routing_table(tmp_path, CATEGORIES, REPOS) == []
    assert repos_sync.check_owner_map(tmp_path, CATEGORIES, REPOS) == []


def test_a_root_table_missing_a_repo_is_drift(tmp_path):
    table = repos_sync.routing_table(CATEGORIES, REPOS)
    stale = "\n".join(line for line in table.splitlines() if "LibAlpha" not in line)
    assert stale != table
    _root_agents(tmp_path, stale)
    problems = repos_sync.check_routing_table(tmp_path, CATEGORIES, REPOS)
    assert len(problems) == 1
    assert problems[0].startswith("AGENTS.md:") and "--write" in problems[0]


def test_a_stale_owner_map_is_drift(tmp_path):
    stale = repos_sync.owner_map(CATEGORIES, REPOS).replace("LibAlpha", "LibGone")
    _workflow(tmp_path, stale)
    problems = repos_sync.check_owner_map(tmp_path, CATEGORIES, REPOS)
    assert len(problems) == 1
    assert problems[0].startswith("PyAutoBrain/skills/WORKFLOW.md:")


def test_absent_files_are_skipped_like_the_write(tmp_path):
    """A partial/web checkout carries neither file; the leg must not fail."""
    assert repos_sync.check_routing_table(tmp_path, CATEGORIES, REPOS) == []
    assert repos_sync.check_owner_map(tmp_path, CATEGORIES, REPOS) == []


def test_a_present_file_without_markers_is_a_problem(tmp_path):
    """--write hard-fails on it (required=True), so check must not pass it."""
    (tmp_path / "AGENTS.md").write_text("# Workspace\n\nno generated block\n")
    problems = repos_sync.check_routing_table(tmp_path, CATEGORIES, REPOS)
    assert len(problems) == 1 and "no " in problems[0]


def test_the_write_output_satisfies_the_check(tmp_path):
    """Round trip: whatever write_block places is exactly what check expects."""
    (tmp_path / "AGENTS.md").write_text(_blocked("old table"))
    table = repos_sync.routing_table(CATEGORIES, REPOS)
    assert repos_sync.check_routing_table(tmp_path, CATEGORIES, REPOS)
    repos_sync.write_block(tmp_path / "AGENTS.md", table, required=True)
    assert repos_sync.check_routing_table(tmp_path, CATEGORIES, REPOS) == []
