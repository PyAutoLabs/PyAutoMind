"""Contract tests for the tier-`notify` shadow window and its append hook.

The shadow window is a **pre-registered** decision rule: over a window of at
least 40 tier-`notify` candidates, the human's action at close-out decides
whether an agent may ever merge its own low-consequence work. A pre-registered
rule that anyone can quietly reshape is not pre-registered, so two things are
pinned here:

1. **The live ledger's schema** — heading, header row, six cells per row, an
   allowed `human action` on every row the rule actually grades, and a count
   line that agrees with the rows it claims to count. A count line drifting
   from its table is the exact failure that would let the window "reach 40"
   without 40 candidates.
2. **The append itself** — `lifecycle.py shadow-row` on a fixture: dry run
   writes nothing, `--apply` appends exactly one row and moves the count, and
   an action outside the three allowed values is refused.

Same two rules as the other lifecycle tests: fictional fixtures only (`tests/**`
is KEEP-copied into the public template), and every leg must be shown to fail
on input that should trip it. The live-ledger legs skip where there is no
shadow window — a freshly spawned Mind ships the bare ledger header.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import lifecycle  # noqa: E402

LIVE_LOG = ROOT / "autonomy_log.md"
LIVE = LIVE_LOG.read_text(encoding="utf-8") if LIVE_LOG.is_file() else ""

needs_window = pytest.mark.skipif(
    lifecycle.SHADOW_HEADING not in LIVE,
    reason="no shadow window in this ledger (e.g. a freshly-spawned Mind)",
)

HEADER_ROW = ("| date | task | tier | gate (tests/smoke/review/heart/witness"
              "[/adversary]) | human action | stage |")


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
FIXTURE = """\
# Autonomy calibration log

| date | task | effective level | gates | outcome |
|------|------|-----------------|-------|---------|
| 2026-08-01 | sprocket-calibration (#1) | safe | tests pass | merged-unchanged |

## Shadow window — the tier-`notify` merge decision

Opened **2026-08-30**.

Count toward 40: 1 (stage 1: 1, stage 2: 0) — window re-opened 2026-09-03; \
first /prm-appended row: 2026-09-07

One row per tier-`notify` candidate at close-out.

| date | task | tier | gate (tests/smoke/review/heart/witness[/adversary]) \
| human action | stage |
|------|------|------|---------|--------------|-------|
| 2026-09-07 | flywheel-tuning (Flywheel#1 / PR#2) | notify | tests 3 pass \
| merged-unchanged | 1 |

## Freeze overrides

| date | task / PR | freeze reason | until | thawed by | why |
"""


def _fixture(tmp_path: Path, body: str = FIXTURE) -> Path:
    log = tmp_path / "autonomy_log.md"
    log.write_text(body, encoding="utf-8")
    return log


def _run(log: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lifecycle.py"), "shadow-row",
         "--log", str(log), *args],
        capture_output=True, text=True)


# --------------------------------------------------------------------------- #
# the live ledger's schema
# --------------------------------------------------------------------------- #
@needs_window
def test_the_window_still_has_its_heading_and_its_header_row():
    """The append hook finds the table by these two strings — if either is
    reworded the hook stops appending and says nothing, which is how a window
    silently stops being fed."""
    start, end = lifecycle.shadow_section(LIVE)
    assert end > start
    header, last = lifecycle.shadow_table(LIVE)
    assert LIVE.splitlines()[header] == HEADER_ROW
    assert last > header + 2, "the shadow table has no data rows"


@needs_window
def test_every_row_carries_all_six_cells():
    """A dropped cell shifts `human action` into `stage` and the count silently
    changes meaning."""
    for row in lifecycle.shadow_rows(LIVE):
        assert len(row) == 6, row
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", row[0]), row[0]


@needs_window
def test_every_prm_appended_row_records_one_of_the_three_allowed_actions():
    """`human action` is a merge outcome, and the decision is a count over
    exactly three of them.

    The boundary is the window's own: rows before the `/prm` epoch were
    appended at **PR-open** by the retired batch protocol, so their action cell
    holds a PR state ("PR-open (#76, ...)") rather than what the human then did
    — which is precisely why the append moved to close-out, and why the header
    re-opens the window from the first `/prm`-appended row. They stay as
    history; from the epoch on, the vocabulary is fixed.
    """
    for row in lifecycle.shadow_rows(LIVE):
        if row[0] >= lifecycle.SHADOW_PRM_EPOCH:
            assert row[4] in lifecycle.SHADOW_ACTIONS, row
            assert row[5] in lifecycle.SHADOW_STAGES, row


@needs_window
def test_the_count_line_agrees_with_the_rows_it_counts():
    """Recomputed from the table, not from the sentence — the whole point is
    that the number cannot be edited independently of the evidence."""
    rows = lifecycle.shadow_rows(LIVE)
    line = next((ln for ln in LIVE.splitlines()
                 if ln.startswith(lifecycle.SHADOW_COUNT_PREFIX)), None)
    assert line is not None, "the shadow window has no count line"

    m = re.match(
        lifecycle.SHADOW_COUNT_PREFIX
        + r" (\d+) \(stage 1: (\d+), stage 2: (\d+)\)", line)
    assert m, f"count line does not parse: {line!r}"
    total, one, two = (int(g) for g in m.groups())

    graded = [r for r in rows if r[5] in lifecycle.SHADOW_STAGES]
    assert (total, one, two) == (
        len(graded),
        sum(1 for r in graded if r[5] == "1"),
        sum(1 for r in graded if r[5] == "2"),
    ), line
    assert total == one + two, line
    assert total < lifecycle.SHADOW_TARGET or "reached" in line.lower(), (
        "the window has reached its pre-registered size — the decision is due, "
        "and this line should say so")


@needs_window
def test_a_dropped_cell_would_be_caught():
    """The schema check above is only worth its runtime if a malformed row
    actually trips it (the positive control)."""
    assert len(lifecycle._md_cells("| a | b | c | d | e |")) == 5


@needs_window
def test_escaped_pipes_do_not_invent_columns():
    """Gate cells quote shell and Python; `\\|delta\\|` must stay one cell."""
    cells = lifecycle._md_cells(r"| 2026-09-07 | t | notify | \|d\| = 1 "
                               r"| merged-unchanged | 1 |")
    assert len(cells) == 6, cells
    assert cells[3] == r"\|d\| = 1"


# --------------------------------------------------------------------------- #
# the append hook
# --------------------------------------------------------------------------- #
def test_a_dry_run_leaves_the_file_byte_identical(tmp_path):
    """The hook is called by a skill that reads the count back to a human
    before committing to it, so the default must not write."""
    log = _fixture(tmp_path)
    before = log.read_bytes()
    r = _run(log, "--date", "2026-09-08", "--task", "widget-press (Widget#3)",
             "--gate", "tests 4 pass", "--action", "merged-unchanged",
             "--stage", "1")
    assert r.returncode == 0, r.stderr
    assert log.read_bytes() == before
    assert "| 2026-09-08 | widget-press (Widget#3) | notify |" in r.stdout
    assert "Count toward 40: 2 (stage 1: 2, stage 2: 0)" in r.stdout


def test_apply_appends_exactly_one_row_and_moves_the_count(tmp_path):
    log = _fixture(tmp_path)
    before = lifecycle.shadow_rows(log.read_text())
    r = _run(log, "--date", "2026-09-08", "--task", "widget-press (Widget#3)",
             "--gate", "tests 4 pass", "--action",
             "merged-after-substantive-change", "--stage", "2", "--apply")
    assert r.returncode == 0, r.stderr

    text = log.read_text()
    after = lifecycle.shadow_rows(text)
    assert len(after) == len(before) + 1
    assert after[:-1] == before, "an existing row was rewritten"
    assert after[-1] == ["2026-09-08", "widget-press (Widget#3)", "notify",
                         "tests 4 pass", "merged-after-substantive-change", "2"]
    assert ("Count toward 40: 2 (stage 1: 1, stage 2: 1) — window re-opened "
            "2026-09-03; first /prm-appended row: 2026-09-07") in text
    # the rest of the ledger is untouched
    assert "## Freeze overrides" in text
    assert "| 2026-08-01 | sprocket-calibration (#1) |" in text


def test_an_action_outside_the_three_values_is_refused(tmp_path):
    """The window counts three outcomes. A fourth would be uncountable, and
    the rule is pre-registered over exactly these."""
    log = _fixture(tmp_path)
    before = log.read_bytes()
    r = _run(log, "--task", "t", "--gate", "g", "--action", "merged-ish",
             "--apply")
    assert r.returncode != 0
    assert "merged-ish" in r.stderr
    assert log.read_bytes() == before


def test_a_stage_outside_one_and_two_is_refused(tmp_path):
    """`stage: 1` and `stage: 2` are never pooled; a third stage would have no
    pre-registered meaning."""
    log = _fixture(tmp_path)
    r = _run(log, "--task", "t", "--gate", "g", "--action", "not-merged",
             "--stage", "3", "--apply")
    assert r.returncode != 0


def test_a_pipe_in_a_cell_cannot_split_the_row(tmp_path):
    """An unescaped pipe in a free-text cell would silently add a column and
    push `stage` off the end of the row."""
    log = _fixture(tmp_path)
    r = _run(log, "--date", "2026-09-08", "--task", "widget | press",
             "--gate", "tests pass | smoke n/a", "--action", "not-merged",
             "--stage", "1", "--apply")
    assert r.returncode == 0, r.stderr
    row = lifecycle.shadow_rows(log.read_text())[-1]
    assert len(row) == 6, row
    assert row[1] == "widget / press"
    assert row[3] == "tests pass / smoke n/a"


def test_a_ledger_with_no_shadow_window_is_an_error_not_a_silent_no_op(tmp_path):
    """Exit 2, not 0: a hook that cannot find its table must stop the caller,
    because the caller's next act is to commit and report a number."""
    log = _fixture(tmp_path, "# Autonomy calibration log\n\n| date |\n|---|\n")
    r = _run(log, "--task", "t", "--gate", "g", "--action", "not-merged",
             "--apply")
    assert r.returncode == 2
    assert lifecycle.SHADOW_HEADING in r.stderr


def test_the_count_line_is_created_when_the_section_has_none(tmp_path):
    """A window that predates the count line still gets one, anchored before
    the paragraph that defines the rows."""
    body = FIXTURE.replace(
        "Count toward 40: 1 (stage 1: 1, stage 2: 0) — window re-opened "
        "2026-09-03; first /prm-appended row: 2026-09-07\n\n", "")
    assert lifecycle.SHADOW_COUNT_PREFIX not in body
    log = _fixture(tmp_path, body)
    r = _run(log, "--date", "2026-09-08", "--task", "widget-press",
             "--gate", "tests pass", "--action", "not-merged", "--stage", "1",
             "--apply")
    assert r.returncode == 0, r.stderr
    text = log.read_text()
    count = next(ln for ln in text.splitlines()
                 if ln.startswith(lifecycle.SHADOW_COUNT_PREFIX))
    assert "Count toward 40: 2" in count
    idx = text.index(count)
    assert idx < text.index(lifecycle.SHADOW_COUNT_ANCHOR)


def test_legacy_rows_are_listed_but_never_counted(tmp_path):
    """Rows whose stage cell is neither 1 nor 2 predate the stage rule. They
    stay in the table — deleting history to tidy a counter is how a
    pre-registered rule stops being one — and are named as uncounted."""
    body = FIXTURE.replace(
        "| merged-unchanged | 1 |\n",
        "| merged-unchanged | 1 |\n"
        "| 2026-08-31 | old-flywheel-run | supervised | tests pass "
        "| PR #9 opened, merged later | shipped |\n")
    log = _fixture(tmp_path, body)
    r = _run(log, "--date", "2026-09-08", "--task", "widget-press",
             "--gate", "tests pass", "--action", "not-merged", "--stage", "1",
             "--apply")
    assert r.returncode == 0, r.stderr
    text = log.read_text()
    assert "| 2026-08-31 | old-flywheel-run |" in text
    assert "Count toward 40: 2 (stage 1: 2, stage 2: 0)" in text
    assert "legacy rows not counted: 1" in text
