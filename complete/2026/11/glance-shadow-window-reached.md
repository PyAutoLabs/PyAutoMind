- summary: already shipped — closed as stale draft. Item 1 (code): commit 679b1319f (2026-10-16) made `shadow_count_line()` append "window reached" once graded rows ≥ SHADOW_TARGET; it now also cites the ruling (SHADOW_RULED). Item 2 (human doctrine call): the human ruled 2026-11-04 — `glance` granted, narrowed; rows keep accumulating, with unattended merges in a stage-2 sub-window (record `complete/2026/11/glance-tier-ruling.md`, PyAutoBrain#567, PyAutoMind#529).
- witness: `tests/test_autonomy_log_shadow.py` passes on main; autonomy_log.md count line reads "…window reached — ruled 2026-11-04: `glance` granted, narrowed…" (2026-11-05).
- found by: queue check-in 2026-11-05.

## Original prompt

# Glance shadow window reached 20/20 clean — count line must say "reached"; record the glance confirmation decision

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: `pytest tests/test_autonomy_log_shadow.py` passes on main; `shadow_count_line()` emits "— window reached; decision due" once graded rows ≥ SHADOW_TARGET; the human's dated glance verdict is recorded in autonomy_log.md / AUTONOMY.md.
Filed: 2026-10-16

## Finding

`tests/test_autonomy_log_shadow.py::test_the_count_line_agrees_with_the_rows_it_counts` fails on main: `autonomy_log.md:458` reads "Count toward 20: 20 (stage 1: 20, stage 2: 0)"; all 20 counted rows are merged-unchanged, 0 reverted. The 20th arrived in 27fc5e22 (prm: close reuse-cholesky-factor, 10-16). The writer `scripts/lifecycle.py shadow_count_line()` (~l.2910) never appends "reached", so a hand edit would be overwritten.

## Needs

1. Code: `shadow_count_line` marks the window reached.
2. **Human doctrine call**: confirm glance at 20 clean rows (pre-registered verdict) and decide whether rows keep accumulating past the window.
