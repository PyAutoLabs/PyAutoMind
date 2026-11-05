"""The opt-in AGENTS.md blocks share one declaration (`OptInBlock`).

The map, history and remote blocks used to be three hand-copied check
functions plus hand-copied `write_block` calls; they are now one declaration per
surface driving both legs. This pins the shared contract for each declaration,
so a new opt-in surface inherits it rather than re-copying it.

Conventions, as in the sibling repos_sync tests: fictional fixtures only
(`tests/**` is copied into the public template), and every leg is shown to FAIL.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

REPOS = {"OrganCore": {"category": "organ"}, "LibAlpha": {"category": "library"}}
BLOCKS = [repos_sync.MAP_BLOCK, repos_sync.HISTORY_BLOCK, repos_sync.REMOTE_BLOCK]


def _agents(root, name, body):
    (root / name).mkdir(parents=True, exist_ok=True)
    path = root / name / "AGENTS.md"
    path.write_text(body)
    return path


def _with(block, content):
    return f"# Repo\n\n{block.begin}\n{content}\n{block.end}\n"


@pytest.mark.parametrize("block", BLOCKS, ids=lambda b: b.noun)
def test_a_current_block_passes_and_a_stale_one_is_named(tmp_path, block):
    _agents(tmp_path, "OrganCore", _with(block, "canonical"))
    assert block.check(tmp_path, REPOS, "canonical") == []
    _agents(tmp_path, "OrganCore", _with(block, "hand-edited"))
    assert block.check(tmp_path, REPOS, "canonical") == [
        f"'OrganCore': {block.noun} block is stale — run "
        "`python3 PyAutoMind/scripts/repos_sync.py --write`"
    ]


@pytest.mark.parametrize("block", BLOCKS, ids=lambda b: b.noun)
def test_absent_files_and_missing_markers_are_skipped(tmp_path, block):
    assert block.check(tmp_path, REPOS, "canonical") == []
    _agents(tmp_path, "OrganCore", "# Repo\n\nno markers here\n")
    assert block.check(tmp_path, REPOS, "canonical") == []


@pytest.mark.parametrize("block", BLOCKS, ids=lambda b: b.noun)
def test_write_repairs_what_check_flags(tmp_path, block):
    path = _agents(tmp_path, "OrganCore", _with(block, "stale"))
    assert block.check(tmp_path, REPOS, "canonical")
    block.write(path, "canonical")
    assert block.check(tmp_path, REPOS, "canonical") == []


def test_only_the_map_block_is_organs_only(tmp_path):
    for block in BLOCKS:
        _agents(tmp_path, "LibAlpha", _with(block, "stale"))
        flagged = block.check(tmp_path, REPOS, "canonical")
        assert bool(flagged) is (not block.organs_only), block.noun
    assert [b.noun for b in BLOCKS if b.organs_only] == ["organism-map"]
