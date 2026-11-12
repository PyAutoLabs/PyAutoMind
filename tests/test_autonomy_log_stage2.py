"""The unattended `glance` sub-window (stage 2) of autonomy_log.md.

Opened by the 2026-11-04 ruling and written by the shift watcher (PyAutoBrain
#572) through the one Mind writer; `lifecycle.py shadow-row --stage2` writes the
same row by hand. Fictional fixtures only; the live ledger is only read.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import lifecycle  # noqa: E402

LIVE_LOG = ROOT / "autonomy_log.md"
LIVE = LIVE_LOG.read_text(encoding="utf-8") if LIVE_LOG.is_file() else ""

STAGE2_HEADER = ("| date | task | brief | gate (tests/smoke/review/heart/witness/adversary) "
                 "| human action | merge actor | read by human |")

FIXTURE = f"""\
# Autonomy calibration log

## Shadow window — the tier-`glance` merge decision

| date | task | tier | gate | human action | stage |
|------|------|------|------|--------------|-------|
| 2026-10-06 | sprocket (#1) | glance | tests PASS | merged-unchanged | 1 |

{lifecycle.STAGE2_HEADING} — opened 2026-11-04

{STAGE2_HEADER}
|------|------|-------|------|--------------|-------------|---------------|

## A later section
kept
"""


def _run(log, *extra):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lifecycle.py"), "shadow-row", "--stage2",
         "--log", str(log), "--date", "2026-11-05", "--task", "widget (PyAutoBrain#9)",
         "--gate", "tests PASS / witness PASS / adversary: close-out (opus)",
         "--action", "merged-unchanged", *extra],
        capture_output=True, text=True)


@pytest.mark.skipif(lifecycle.STAGE2_HEADING not in LIVE,
                    reason="no stage-2 sub-window in this ledger")
def test_the_live_ledger_has_the_stage2_table_and_its_amendment():
    rows = lifecycle.stage2_rows(LIVE)
    assert all(len(r) in (5, 7) for r in rows), rows
    assert all(lifecycle.row_actor(r, lifecycle.STAGE2_ACTOR_COL) in lifecycle.MERGE_ACTORS
               for r in rows), rows
    assert STAGE2_HEADER in LIVE
    section = LIVE[LIVE.index(lifecycle.STAGE2_HEADING):]
    assert "Amended 2026-11-04" in section and "Stage-2 adversary amendment" in section


def test_stage2_row_lands_under_its_heading_and_nothing_else_moves(tmp_path):
    log = tmp_path / "autonomy_log.md"
    log.write_text(FIXTURE)
    res = _run(log, "--brief", "2026-11-05-am", "--apply")
    assert res.returncode == 0, res.stderr
    out = log.read_text()
    row = ("| 2026-11-05 | widget (PyAutoBrain#9) | 2026-11-05-am | tests PASS / "
           "witness PASS / adversary: close-out (opus) | merged-unchanged "
           "| unattended-watcher |  |")
    assert out.count(row) == 1
    assert out.index(lifecycle.STAGE2_HEADING) < out.index(row) < out.index("## A later section")
    assert lifecycle.stage2_rows(out) == [lifecycle._md_cells(row)]
    # The stage-1 table and its count are untouched.
    assert lifecycle.shadow_rows(out) == lifecycle.shadow_rows(FIXTURE)


def test_stage2_dry_run_writes_nothing_and_needs_a_brief(tmp_path):
    log = tmp_path / "autonomy_log.md"
    log.write_text(FIXTURE)
    assert _run(log, "--brief", "b").returncode == 0
    assert log.read_text() == FIXTURE
    res = _run(log)
    assert res.returncode == 2 and "--stage2 needs --brief" in res.stderr


def test_stage2_refuses_a_ledger_without_the_sub_window(tmp_path):
    log = tmp_path / "autonomy_log.md"
    log.write_text(FIXTURE.split(lifecycle.STAGE2_HEADING)[0])
    res = _run(log, "--brief", "b", "--apply")
    assert res.returncode == 2 and "no '## Unattended" in res.stderr
