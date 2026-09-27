"""The where-to-file block is generated — and, like the end-at-deliverable
block, is not allowed to be quietly absent.

`policy/community_surface.md` (PyAutoMind#403) sends users to one org
Discussions hub, but on 2026-09-27 no AGENTS.md in the workspace said so, and
the only filing recipe a collaborator's agent could find was `create_issue`'s
`gh issue create` on the target repo. The rule now rides in every repo's
AGENTS.md, single-sourced from `policy/where_to_file.md` (PyAutoMind#442), and
the drift check reports a repo missing it rather than skipping it.

Conventions, as in the sibling repos_sync tests:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository.
2. **Prove each leg FAILS.** A drift check that cannot fail is decoration.
"""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

MIND = Path(__file__).resolve().parents[1]
CANON = repos_sync.load_filing_policy(MIND)
DELIVERABLE = repos_sync.load_deliverable_policy(MIND)

REPOS = {"OrganCore": {"category": "organ"}, "LibAlpha": {"category": "library"}}


def _repo(root, name, body):
    (root / name).mkdir(parents=True, exist_ok=True)
    (root / name / "AGENTS.md").write_text(body)


def _deliverable_block(text=DELIVERABLE):
    return (
        f"{repos_sync.DELIVERABLE_BEGIN}\n{text}\n{repos_sync.DELIVERABLE_END}\n"
    )


def _filing_block(text):
    return f"{repos_sync.FILING_BEGIN}\n{text}\n{repos_sync.FILING_END}\n"


def _both(text=CANON):
    return f"# OrganCore\n\n{_deliverable_block()}\n{_filing_block(text)}"


# --------------------------------------------------------------------------
# The canonical file
# --------------------------------------------------------------------------

def test_the_canonical_policy_ships():
    assert (MIND / repos_sync.FILING_POLICY_FILE).exists()
    assert CANON.startswith("## Where to file")


def test_the_policy_names_the_hub_and_every_category():
    """An agent about to file must find the exact destination, not a paraphrase."""
    assert "https://github.com/orgs/PyAutoLabs/discussions" in CANON
    for category in ("Help & Questions", "Ideas & Proposals", "Bugs & Errors",
                     "Show and tell", "Announcements"):
        assert category in CANON, f"the policy no longer names {category}"


def test_the_policy_forbids_gh_issue_create_and_keeps_the_dev_flow():
    for needle in ("gh issue create", "/start_dev", "/create_issue",
                   "community_surface.md"):
        assert needle in CANON, needle


def test_the_policy_stays_short_enough_to_ride_in_every_repo():
    """Every line is paid for in every session in every repo."""
    assert len(CANON.splitlines()) <= 12, CANON


# --------------------------------------------------------------------------
# The drift check
# --------------------------------------------------------------------------

def test_a_repo_carrying_the_canonical_text_is_clean(tmp_path):
    _repo(tmp_path, "OrganCore", _both())
    assert repos_sync.check_filing_blocks(tmp_path, REPOS, CANON) == []


def test_a_stale_copy_is_drift(tmp_path):
    stale = CANON.replace("never to this repo's Issues", "or this repo's Issues")
    assert stale != CANON
    _repo(tmp_path, "OrganCore", _both(stale))
    problems = repos_sync.check_filing_blocks(tmp_path, REPOS, CANON)
    assert len(problems) == 1 and "OrganCore" in problems[0]
    assert "stale" in problems[0] and "--write" in problems[0]


def test_a_repo_with_the_deliverable_block_but_no_filing_block_is_reported(tmp_path):
    """Not silence: --write can fix this one itself, and the check says so."""
    _repo(tmp_path, "OrganCore", f"# OrganCore\n\n{_deliverable_block()}")
    problems = repos_sync.check_filing_blocks(tmp_path, REPOS, CANON)
    assert len(problems) == 1 and "no where-to-file block" in problems[0]
    assert "--write" in problems[0] and "deliverable block" in problems[0]


def test_a_repo_with_neither_marker_set_is_reported_as_needing_the_markers(tmp_path):
    _repo(tmp_path, "LibAlpha", "# LibAlpha\n\nno generated blocks at all\n")
    problems = repos_sync.check_filing_blocks(tmp_path, REPOS, CANON)
    assert len(problems) == 1 and "LibAlpha" in problems[0]
    assert "add the markers" in problems[0]
    assert repos_sync.FILING_BEGIN in problems[0]


def test_a_repo_that_is_not_checked_out_is_skipped(tmp_path):
    """A partial/web checkout must not fail on behalf of repos it cannot see."""
    assert repos_sync.check_filing_blocks(tmp_path, REPOS, CANON) == []


def test_the_leg_is_registered_under_its_label(tmp_path, monkeypatch, capsys):
    """`--only`/`--skip` match the printed label; the leg must be reachable by it
    and must fail the run when a copy is missing."""
    _repo(tmp_path, "OrganCore", f"# OrganCore\n\n{_deliverable_block()}")
    monkeypatch.setattr(repos_sync, "load_manifest",
                        lambda _mind: ({}, REPOS))
    monkeypatch.setattr(repos_sync, "system_map", lambda *_: "")
    monkeypatch.setattr(sys, "argv", [
        "repos_sync.py", "--root", str(tmp_path),
        "--only", repos_sync.FILING_BLOCKS,
    ])
    try:
        repos_sync.main()
    except SystemExit as exit_:
        code = exit_.code
    out = capsys.readouterr().out
    assert f"check {repos_sync.FILING_BLOCKS}: 1 mismatch(es)" in out, out
    assert code == 1


# --------------------------------------------------------------------------
# Auto-insertion on --write (and the narrow writer the workflow calls)
# --------------------------------------------------------------------------

def test_write_inserts_the_block_immediately_after_the_deliverable_block(tmp_path):
    _repo(tmp_path, "OrganCore",
          f"# OrganCore\n\n{_deliverable_block()}\ntail\n")
    agents = tmp_path / "OrganCore" / "AGENTS.md"

    repos_sync.write_filing_blocks(tmp_path, REPOS, CANON)

    assert repos_sync.check_filing_blocks(tmp_path, REPOS, CANON) == []
    text = agents.read_text()
    assert (
        f"{repos_sync.DELIVERABLE_END}\n\n{repos_sync.FILING_BEGIN}\n" in text
    ), text
    assert text.endswith("tail\n")


def test_insertion_is_idempotent(tmp_path):
    _repo(tmp_path, "OrganCore", f"# OrganCore\n\n{_deliverable_block()}")
    repos_sync.write_filing_blocks(tmp_path, REPOS, CANON)
    once = (tmp_path / "OrganCore" / "AGENTS.md").read_text()
    repos_sync.write_filing_blocks(tmp_path, REPOS, CANON)
    assert (tmp_path / "OrganCore" / "AGENTS.md").read_text() == once


def test_insertion_leaves_a_marker_less_file_alone(tmp_path):
    """No non-arbitrary place to put the block, so --write must not guess."""
    body = "# LibAlpha\n\nno generated blocks at all\n"
    _repo(tmp_path, "LibAlpha", body)
    repos_sync.write_filing_blocks(tmp_path, REPOS, CANON)
    assert (tmp_path / "LibAlpha" / "AGENTS.md").read_text() == body


def test_the_narrow_writer_touches_no_other_block(tmp_path):
    """The propagation job commits whatever this writes, so a stale map or
    deliverable block in a clone must come out exactly as it went in."""
    stale_map = (f"{repos_sync.MAP_BEGIN}\nstale map\n{repos_sync.MAP_END}\n")
    body = (f"# OrganCore\n\n{stale_map}\n"
            f"{_deliverable_block('stale deliverable')}")
    _repo(tmp_path, "OrganCore", body)
    repos_sync.write_filing_blocks(tmp_path, REPOS, CANON)
    text = (tmp_path / "OrganCore" / "AGENTS.md").read_text()
    assert text.startswith(body.rstrip("\n")), text
    assert "stale map" in text and "stale deliverable" in text
    assert repos_sync.extract_block(
        text, repos_sync.FILING_BEGIN, repos_sync.FILING_END) == CANON


def test_write_fills_a_stale_block_and_is_idempotent(tmp_path):
    _repo(tmp_path, "OrganCore", _both("stale text"))
    agents = tmp_path / "OrganCore" / "AGENTS.md"

    repos_sync.write_filing_blocks(tmp_path, REPOS, CANON)
    assert repos_sync.check_filing_blocks(tmp_path, REPOS, CANON) == []
    once = agents.read_text()

    repos_sync.write_filing_blocks(tmp_path, REPOS, CANON)
    assert agents.read_text() == once


# --------------------------------------------------------------------------
# The rollout: the propagation workflow carries this block and only this block
# --------------------------------------------------------------------------

def _workflow():
    path = MIND / ".github/workflows/session_hook_propagate.yml"
    return path.read_text()


def test_the_propagation_workflow_triggers_on_the_policy():
    triggers = yaml.safe_load(_workflow())[True]
    assert repos_sync.FILING_POLICY_FILE in triggers["push"]["paths"]


def test_the_propagation_workflow_writes_and_stages_the_block():
    """A workflow that regenerates a file it never `git add`s reports every
    repo 'already current' and propagates nothing."""
    text = _workflow()
    assert "repos_sync.write_filing_blocks(" in text
    assert "load_filing_policy" in text
    staged = [line for line in text.splitlines()
              if line.strip().startswith("for rel in ")]
    assert len(staged) == 2 and all("AGENTS.md" in line for line in staged)


def test_the_propagation_workflow_never_runs_the_full_writer():
    """The full --write would also regenerate the map blocks, which the bot
    must never commit."""
    code = [line for line in _workflow().splitlines()
            if not line.strip().startswith("#")]
    assert not any("python3" in line and "repos_sync.py" in line
                   for line in code), code
    assert not any("write_block(" in line for line in code)


# --------------------------------------------------------------------------
# This repo's own copy
# --------------------------------------------------------------------------

def test_pyautomind_carries_its_own_block():
    """Propagation never writes to PyAutoMind, so its copy is checked here."""
    text = (MIND / "AGENTS.md").read_text()
    assert repos_sync.extract_block(
        text, repos_sync.FILING_BEGIN, repos_sync.FILING_END
    ) == CANON
