"""Contract tests for the tier-`glance` shadow window and its append hook.

The shadow window is a **pre-registered** decision rule. It ran over tier-`notify`
candidates until `notify` auto-merge was granted on 2026-10-02; it now counts
tier-`glance` auto-merges, and 20 clean rows confirm `glance` (any `reverted`
row demotes it). A pre-registered
rule that anyone can quietly reshape is not pre-registered, so two things are
pinned here:

1. **The live ledger's schema** — heading, header row, six cells per row, an
   allowed `human action` on every row the rule actually grades, and a count
   line that agrees with the rows it claims to count. A count line drifting
   from its table is the exact failure that would let the window "reach 20"
   without 20 candidates.
2. **The append itself** — `lifecycle.py shadow-row` on a fixture: dry run
   writes nothing, `--apply` appends exactly one row and moves the count, and
   an action outside the allowed values is refused.

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
              "[/adversary]) | human action | stage | merge actor | read by human |")


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
FIXTURE = """\
# Autonomy calibration log

| date | task | effective level | gates | outcome |
|------|------|-----------------|-------|---------|
| 2026-08-01 | sprocket-calibration (#1) | safe | tests pass | merged-unchanged |

## Shadow window — the tier-`glance` merge decision

Re-scoped **2026-10-02**.

Count toward 20: 1 (stage 1: 1, stage 2: 0) — window re-scoped to tier \
`glance` 2026-10-02; first `glance` row: 2026-10-02

One row per tier-`glance` candidate at close-out.

| date | task | tier | gate (tests/smoke/review/heart/witness[/adversary]) \
| human action | stage |
|------|------|------|---------|--------------|-------|
| 2026-10-02 | flywheel-tuning (Flywheel#1 / PR#2) | glance | tests 3 pass \
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
def test_every_row_carries_six_cells_or_all_eight():
    """A dropped cell shifts `human action` into `stage` and the count silently
    changes meaning. Rows from before 2026-11-12 stop at `stage` (six cells,
    read as merge actor `unknown`); every later row carries all eight, with a
    merge actor from the fixed classes and a dated-or-empty `read by human`."""
    for row in lifecycle.shadow_rows(LIVE):
        assert len(row) in (6, 8), row
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", row[0]), row[0]
        if len(row) == 8:
            assert lifecycle.row_actor(row) in lifecycle.MERGE_ACTORS, row
            assert row[7] == "" or re.fullmatch(r"\d{4}-\d{2}-\d{2}", row[7]), row


@needs_window
def test_every_prm_appended_row_records_one_of_the_allowed_actions():
    """`human action` is a merge outcome, and the decision is a count over
    exactly these.

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

    graded = [r for r in rows if lifecycle.shadow_counts(r)]
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
    r = _run(log, "--date", "2026-10-03", "--task", "widget-press (Widget#3)",
             "--gate", "tests 4 pass", "--action", "merged-unchanged",
             "--stage", "1")
    assert r.returncode == 0, r.stderr
    assert log.read_bytes() == before
    assert "| 2026-10-03 | widget-press (Widget#3) | glance |" in r.stdout
    assert "Count toward 20: 2 (stage 1: 2, stage 2: 0)" in r.stdout


def test_apply_appends_exactly_one_row_and_moves_the_count(tmp_path):
    log = _fixture(tmp_path)
    before = lifecycle.shadow_rows(log.read_text())
    r = _run(log, "--date", "2026-10-03", "--task", "widget-press (Widget#3)",
             "--gate", "tests 4 pass", "--action",
             "merged-after-substantive-change", "--stage", "2", "--apply")
    assert r.returncode == 0, r.stderr

    text = log.read_text()
    after = lifecycle.shadow_rows(text)
    assert len(after) == len(before) + 1
    assert after[:-1] == before, "an existing row was rewritten"
    assert after[-1] == ["2026-10-03", "widget-press (Widget#3)", "glance",
                         "tests 4 pass", "merged-after-substantive-change", "2",
                         "unknown", ""]
    assert ("Count toward 20: 2 (stage 1: 1, stage 2: 1) — window re-scoped "
            "to tier `glance` 2026-10-02; first `glance` row: 2026-10-02") in text
    # the rest of the ledger is untouched
    assert "## Freeze overrides" in text
    assert "| 2026-08-01 | sprocket-calibration (#1) |" in text


def test_an_action_outside_the_allowed_values_is_refused(tmp_path):
    """The window counts a fixed set of outcomes. Another would be
    uncountable, and the rule is pre-registered over exactly these."""
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
    r = _run(log, "--date", "2026-10-03", "--task", "widget | press",
             "--gate", "tests pass | smoke n/a", "--action", "not-merged",
             "--stage", "1", "--apply")
    assert r.returncode == 0, r.stderr
    row = lifecycle.shadow_rows(log.read_text())[-1]
    assert len(row) == 8, row
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
        "Count toward 20: 1 (stage 1: 1, stage 2: 0) — window re-scoped to "
        "tier `glance` 2026-10-02; first `glance` row: 2026-10-02\n\n", "")
    assert lifecycle.SHADOW_COUNT_PREFIX not in body
    log = _fixture(tmp_path, body)
    r = _run(log, "--date", "2026-10-03", "--task", "widget-press",
             "--gate", "tests pass", "--action", "not-merged", "--stage", "1",
             "--apply")
    assert r.returncode == 0, r.stderr
    text = log.read_text()
    count = next(ln for ln in text.splitlines()
                 if ln.startswith(lifecycle.SHADOW_COUNT_PREFIX))
    assert "Count toward 20: 2" in count
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
    r = _run(log, "--date", "2026-10-03", "--task", "widget-press",
             "--gate", "tests pass", "--action", "not-merged", "--stage", "1",
             "--apply")
    assert r.returncode == 0, r.stderr
    text = log.read_text()
    assert "| 2026-08-31 | old-flywheel-run |" in text
    assert "Count toward 20: 2 (stage 1: 2, stage 2: 0)" in text
    assert "and legacy): 1" in text


# --------------------------------------------------------------------------- #
# the merge actor (AUTONOMY.md "Merge actor and random audit — 2026-11-12")
# --------------------------------------------------------------------------- #
def _row(task, actor=None, date="2026-10-05", stage="1"):
    cells = [date, task, "glance", "tests pass", "merged-unchanged", stage]
    if actor is not None:
        cells += [actor, ""]
    return cells


def test_the_count_leaves_out_human_prm_and_human_commanded_rows():
    """Witness (b): a merge the human typed or commanded is not one the
    organism made; `unknown` (a row without the column, or the class itself)
    still counts, as before 2026-11-12."""
    rows = [
        _row("a"),                                              # no column → unknown
        _row("b", "unknown"),
        _row("c", "human-/prm (mergedBy someone)"),
        _row("d", "in-turn-human-commanded"),
        _row("e", "in-turn-autonomous (mergedBy someone)"),
        _row("f", "unattended-watcher"),
    ]
    counted = [r[1] for r in rows if lifecycle.shadow_counts(r)]
    assert counted == ["a", "b", "e", "f"]
    assert lifecycle.row_actor(rows[0]) == "unknown"
    assert lifecycle.row_actor(rows[2]) == "human-/prm"
    line = lifecycle.shadow_count_line(rows)
    assert line.startswith("Count toward 20: 4 (stage 1: 4, stage 2: 0)")
    assert "left out by merge actor (human-/prm / in-turn-human-commanded): 2" in line
    # control: without the actor cells all six count
    assert sum(lifecycle.shadow_counts(r[:6]) for r in rows) == 6


def test_shadow_row_writes_the_actor_and_refuses_an_unknown_class(tmp_path):
    log = _fixture(tmp_path)
    r = _run(log, "--date", "2026-10-03", "--task", "widget-press (Widget#3)",
             "--gate", "tests 4 pass", "--action", "merged-unchanged",
             "--actor", "in-turn-autonomous", "--read-by-human", "2026-10-04",
             "--apply")
    assert r.returncode == 0, r.stderr
    row = lifecycle.shadow_rows(log.read_text())[-1]
    assert row[6:] == ["in-turn-autonomous", "2026-10-04"]
    assert "Count toward 20: 2" in log.read_text()

    before = log.read_bytes()
    r = _run(log, "--task", "t", "--gate", "g", "--action", "not-merged",
             "--actor", "the-cat", "--apply")
    assert r.returncode != 0 and "the-cat" in r.stderr
    assert log.read_bytes() == before


def test_a_human_prm_row_is_appended_but_not_counted(tmp_path):
    log = _fixture(tmp_path)
    r = _run(log, "--date", "2026-10-03", "--task", "widget-press (Widget#3)",
             "--gate", "tests 4 pass", "--action", "merged-unchanged",
             "--actor", "human-/prm", "--apply")
    assert r.returncode == 0, r.stderr
    text = log.read_text()
    assert "| merged-unchanged | 1 | human-/prm |  |" in text
    assert "Count toward 20: 1 (stage 1: 1, stage 2: 0)" in text
    assert "left out by merge actor (human-/prm / in-turn-human-commanded): 1" in text


def test_the_mergedby_evidence_comes_from_the_gh_seam():
    """The class is the caller's; GitHub adds `mergedBy`, never the class."""
    seen = []

    def gh(argv):
        seen.append(argv)
        n = argv[2]
        if n == "3":
            return 0, '{"mergedBy": {"login": "a-human"}, "mergedAt": "x"}', ""
        if n == "4":
            return 0, '{"mergedBy": null, "mergedAt": null}', ""
        return 1, "", "not found"

    refs = lifecycle.task_pr_refs("widget (Widget#3 / Widget#4 / PR#9 / Gear#5)")
    assert refs == [("Widget", 3), ("Widget", 4), ("Gear", 5)]
    cell, warnings = lifecycle.merge_actor_cell("human-/prm", refs, gh=gh)
    assert cell == "human-/prm (mergedBy a-human, 1/3 PRs)"
    assert any("Widget#4: GitHub reports it not merged" in w for w in warnings)
    assert any("Gear#5: GitHub could not say" in w for w in warnings)
    assert seen[0] == ["pr", "view", "3", "-R", "PyAutoLabs/Widget",
                       "--json", "mergedBy,mergedAt"]
    # opted out: no call at all
    seen.clear()
    assert lifecycle.merge_actor_cell("unknown", refs, gh=gh, lookup=False) == ("unknown", [])
    assert seen == []
    with pytest.raises(ValueError):
        lifecycle.merge_actor_cell("robot", refs, gh=gh, lookup=False)


# --------------------------------------------------------------------------- #
# the historical recount — printed, never written
# --------------------------------------------------------------------------- #
def test_the_record_keyword_rule_sorts_records_into_three_classes():
    assert lifecycle.record_merge_class(
        "Merged via human /prm on 2026-10-07.\n") == "human /prm"
    assert lifecycle.record_merge_class(
        "Tier glance: auto-merged on green CI.\n") == "automatic/in-turn"
    assert lifecycle.record_merge_class("Shipped. Tests pass.\n") == "not stated"
    # only the record's own text counts, never the folded prompt
    assert lifecycle.record_merge_class(
        "Shipped.\n\n## Original prompt\nthe human typed /prm\n") == "not stated"


def test_recount_prints_classes_and_writes_nothing(tmp_path, monkeypatch, capsys):
    """Witness (c), offline: the recount prints by actor and by record class."""
    body = FIXTURE.replace(
        "| merged-unchanged | 1 |\n",
        "| merged-unchanged | 1 |\n"
        "| 2026-10-03 | gear-mesh (Gear#4) | glance | tests pass "
        "| merged-unchanged | 1 | human-/prm |  |\n", 1)
    log = _fixture(tmp_path, body)
    bucket = tmp_path / "complete" / "2026" / "10"
    bucket.mkdir(parents=True)
    (bucket / "flywheel-tuning.md").write_text("Merged by the human with /prm.\n")
    monkeypatch.setattr(lifecycle, "_all_records", lambda: [
        ("2026-10-02", "flywheel-tuning", bucket / "flywheel-tuning.md")])
    before = log.read_bytes()
    assert lifecycle.cmd_shadow_recount(
        type("A", (), {"log": str(log), "verbose": True})()) == 0
    out = capsys.readouterr().out
    assert "merge actor (column; a row without it reads `unknown`): human-/prm 1, unknown 1" in out
    assert "counted 1, left out 1" in out
    assert "human /prm 1, automatic/in-turn 0, not stated 0, no record 1" in out
    assert log.read_bytes() == before


# --------------------------------------------------------------------------- #
# the seeded audit sample
# --------------------------------------------------------------------------- #
def _many_rows(n):
    rows = "".join(
        f"| 2026-10-{(i % 25) + 3:02d} | task-{i:02d} (Widget#{i}) | glance | tests pass "
        "| merged-unchanged | 1 |\n" for i in range(n))
    return FIXTURE.replace(
        "| merged-unchanged | 1 |\n", "| merged-unchanged | 1 |\n" + rows, 1)


def test_the_same_seed_draws_the_same_one_in_five_sample(tmp_path):
    """Witness (d): reproducible, 1 in 5, never hand-picked."""
    text = _many_rows(39)                      # 40 counted rows with the fixture's
    pop = lifecycle.audit_population(text)
    assert len(pop) == 40
    a = lifecycle.audit_sample(pop, seed=1104)
    b = lifecycle.audit_sample(lifecycle.audit_population(text), seed=1104)
    assert a == b and len(a) == 8             # ceil(0.2 × 40)
    assert lifecycle.audit_sample(pop, seed=1105) != a   # control: the seed matters
    # and through the CLI, twice
    log = _fixture(tmp_path, text)
    cmd = [sys.executable, str(ROOT / "scripts" / "lifecycle.py"), "audit-sample",
           "--log", str(log), "--seed", "7"]
    one = subprocess.run(cmd, capture_output=True, text=True)
    two = subprocess.run(cmd, capture_output=True, text=True)
    assert one.returncode == 0, one.stderr
    assert one.stdout == two.stdout and "8 of 40 rows" in one.stdout


def test_the_sample_skips_rows_the_count_leaves_out_and_adds_stage2(tmp_path):
    text = _many_rows(4).replace(
        "| task-00 (Widget#0) | glance | tests pass | merged-unchanged | 1 |",
        "| task-00 (Widget#0) | glance | tests pass | merged-unchanged | 1 "
        "| human-/prm |  |")
    text = text.replace("## Freeze overrides", (
        lifecycle.STAGE2_HEADING + " — opened 2026-11-04\n\n"
        "| date | task | brief | gate | human action | merge actor | read by human |\n"
        "|---|---|---|---|---|---|---|\n"
        "| 2026-11-05 | cog (Gear#1) | am | tests pass | merged-unchanged "
        "| unattended-watcher |  |\n\n## Freeze overrides"))
    pop = lifecycle.audit_population(text)
    tasks = [r[1] for _, r in pop]
    assert "task-00 (Widget#0)" not in tasks
    assert ("stage 2", "cog (Gear#1)") in [(t, r[1]) for t, r in pop]
    assert len(pop) == 5                       # fixture + task-01..03 + stage 2
    assert len(lifecycle.audit_sample(pop, seed=3)) == 1
