"""The end-at-deliverable block is generated — and, unlike its siblings, is not
allowed to be quietly absent.

The rule it carries (a session ends at its deliverable; never arm anything that
outlives the turn to wait for CI, a review or a merge) was already written down
once, in the batch skill, after five batch members armed hourly check-ins on
2026-08-31. It was still broken on 2026-09-02/03, by a mobile `/prm` that
re-armed a 60-minute `send_later` hourly from 02:39 to 12:11 UTC with no task
active. Prose in one skill did not reach the session that needed it, so the
prose now rides in every repo and the drift check reports a repo that is missing
it rather than skipping it the way the opt-in blocks do.

Conventions, as in the sibling repos_sync tests:

1. **Fictional fixtures only.** `tests/**` is KEEP-copied verbatim into the
   public template, so nothing here names a real repository.
2. **Prove each leg FAILS.** A drift check that cannot fail is decoration.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

MIND = Path(__file__).resolve().parents[1]
CANON = repos_sync.load_deliverable_policy(MIND)
HISTORY = repos_sync.load_history_policy(MIND)

REPOS = {"OrganCore": {"category": "organ"}, "LibAlpha": {"category": "library"}}


def _repo(root, name, body):
    (root / name).mkdir(parents=True, exist_ok=True)
    (root / name / "AGENTS.md").write_text(body)


def _history_block(text=HISTORY):
    return (
        f"{repos_sync.HISTORY_BEGIN}\n{text}\n{repos_sync.HISTORY_END}\n"
    )


def _deliverable_block(text):
    return (
        f"{repos_sync.DELIVERABLE_BEGIN}\n{text}\n{repos_sync.DELIVERABLE_END}\n"
    )


def _both(text=CANON):
    return f"# OrganCore\n\n{_history_block()}\n{_deliverable_block(text)}"


# --------------------------------------------------------------------------
# The canonical file
# --------------------------------------------------------------------------

def test_the_canonical_policy_ships():
    assert (MIND / repos_sync.DELIVERABLE_POLICY_FILE).exists()
    assert CANON.startswith("## Sessions end at their deliverable")


def test_the_policy_names_every_tool_that_outlives_the_turn():
    """The block has to be actionable at the moment of temptation: a session
    reaching for one of these must find its own tool named, not a paraphrase."""
    for needle in ("send_later", "subscribe_pr_activity", "CronCreate",
                   "ScheduleWakeup", "/loop", "RemoteTrigger"):
        assert needle in CANON, f"the policy no longer names {needle}"


def test_the_policy_carries_the_measured_reason_and_the_human_re_run():
    for needle in ("2026-08-31", "2026-09-03", "/prm"):
        assert needle in CANON, f"the policy no longer cites {needle}"


def test_the_policy_stays_short_enough_to_ride_in_every_repo():
    """Every line is paid for in every session in every repo."""
    assert len(CANON.splitlines()) <= 10, CANON


# --------------------------------------------------------------------------
# The drift check
# --------------------------------------------------------------------------

def test_a_repo_carrying_the_canonical_text_is_clean(tmp_path):
    _repo(tmp_path, "OrganCore", _both())
    assert repos_sync.check_deliverable_blocks(tmp_path, REPOS, CANON) == []


def test_a_stale_copy_is_drift(tmp_path):
    stale = CANON.replace("never arm anything", "try not to arm anything")
    assert stale != CANON
    _repo(tmp_path, "OrganCore", _both(stale))
    problems = repos_sync.check_deliverable_blocks(tmp_path, REPOS, CANON)
    assert len(problems) == 1 and "OrganCore" in problems[0]
    assert "stale" in problems[0] and "--write" in problems[0]


def test_a_repo_with_the_history_block_but_no_deliverable_block_is_reported(tmp_path):
    """Not silence: --write can fix this one itself, and the check says so."""
    _repo(tmp_path, "OrganCore", f"# OrganCore\n\n{_history_block()}")
    problems = repos_sync.check_deliverable_blocks(tmp_path, REPOS, CANON)
    assert len(problems) == 1 and "no deliverable block" in problems[0]
    assert "--write" in problems[0]


def test_a_repo_with_neither_marker_set_is_reported_as_needing_the_markers(tmp_path):
    """The five repos the rollout has to hand-fix must be visible, not skipped.

    The other generated blocks treat a marker-less AGENTS.md as an opt-out. That
    is the behaviour that lets a safety rule sit un-adopted in a long tail, so
    this leg names the repo and says what a human has to do."""
    _repo(tmp_path, "LibAlpha", "# LibAlpha\n\nno generated blocks at all\n")
    problems = repos_sync.check_deliverable_blocks(tmp_path, REPOS, CANON)
    assert len(problems) == 1 and "LibAlpha" in problems[0]
    assert "add the markers" in problems[0]
    assert repos_sync.DELIVERABLE_BEGIN in problems[0]


def test_a_repo_that_is_not_checked_out_is_skipped(tmp_path):
    """A partial/web checkout must not fail on behalf of repos it cannot see."""
    assert repos_sync.check_deliverable_blocks(tmp_path, REPOS, CANON) == []


# --------------------------------------------------------------------------
# Auto-insertion on --write
# --------------------------------------------------------------------------

def test_write_inserts_the_block_immediately_after_the_history_block(tmp_path):
    _repo(tmp_path, "OrganCore", f"# OrganCore\n\n{_history_block()}\ntail\n")
    agents = tmp_path / "OrganCore" / "AGENTS.md"

    repos_sync.insert_deliverable_markers(tmp_path, REPOS)
    repos_sync.write_block(agents, CANON, repos_sync.DELIVERABLE_BEGIN,
                           repos_sync.DELIVERABLE_END, required=False)

    assert repos_sync.check_deliverable_blocks(tmp_path, REPOS, CANON) == []
    text = agents.read_text()
    assert (
        f"{repos_sync.HISTORY_END}\n\n{repos_sync.DELIVERABLE_BEGIN}\n"
        in text
    ), text
    assert text.endswith("tail\n")


def test_insertion_is_idempotent(tmp_path):
    _repo(tmp_path, "OrganCore", f"# OrganCore\n\n{_history_block()}")
    repos_sync.insert_deliverable_markers(tmp_path, REPOS)
    once = (tmp_path / "OrganCore" / "AGENTS.md").read_text()
    repos_sync.insert_deliverable_markers(tmp_path, REPOS)
    assert (tmp_path / "OrganCore" / "AGENTS.md").read_text() == once


def test_insertion_leaves_a_marker_less_file_alone(tmp_path):
    """There is no non-arbitrary place to put the block, so --write must not
    guess — the check names the repo for a human instead."""
    body = "# LibAlpha\n\nno generated blocks at all\n"
    _repo(tmp_path, "LibAlpha", body)
    repos_sync.insert_deliverable_markers(tmp_path, REPOS)
    assert (tmp_path / "LibAlpha" / "AGENTS.md").read_text() == body


def test_write_fills_a_stale_block_and_is_idempotent(tmp_path):
    _repo(tmp_path, "OrganCore", _both("stale text"))
    agents = tmp_path / "OrganCore" / "AGENTS.md"

    repos_sync.write_block(agents, CANON, repos_sync.DELIVERABLE_BEGIN,
                           repos_sync.DELIVERABLE_END, required=False)
    assert repos_sync.check_deliverable_blocks(tmp_path, REPOS, CANON) == []
    once = agents.read_text()

    repos_sync.write_block(agents, CANON, repos_sync.DELIVERABLE_BEGIN,
                           repos_sync.DELIVERABLE_END, required=False)
    assert agents.read_text() == once


# --------------------------------------------------------------------------
# This repo's own copy
# --------------------------------------------------------------------------

def test_pyautomind_carries_its_own_block():
    """The generator's home repo is the one --write is never run against from a
    rollout session, so its copy is checked here."""
    text = (MIND / "AGENTS.md").read_text()
    assert repos_sync.extract_block(
        text, repos_sync.DELIVERABLE_BEGIN, repos_sync.DELIVERABLE_END
    ) == CANON


def test_the_canonical_hook_ships_beside_the_prose():
    """Prose for the reasoning, hook for the moment of temptation. The rule was
    already prose once and was still broken twice."""
    hook = MIND / repos_sync.DELIVERABLE_HOOK_FILE
    assert hook.exists()
    assert os.access(hook, os.X_OK)
