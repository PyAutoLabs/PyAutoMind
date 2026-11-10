# Boards: draw the unit-test trend, and keep the hygiene counts

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-10
Consequence: glance
Witness: (a) the published Heart board shows a trend chart on every unit-suite card (12 of 12, from 0 of 12 on 2026-11-09), drawn from the main-branch lines of `timings/unit/<repo>.jsonl`, plus one row with the organism's total test count; (b) after two daily runs, a committed PyAutoBrain ledger file holds one line of hygiene counts per day and the Brain board's hygiene block shows a sparkline per row
Review-minutes: 10
Unattended: ready
Lane: any

Human (2026-11-09): "I feel like things like number of unit tests, integration tests, their run time, many of the things we do hygiene runs on are not being fed through to a dashboard so I can track and monitor it."

Source: the ecosystem review of 2026-11-10, findings SIG-2 and SIG-3. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, section B7 with the full signal map. Data: `evidence/signals_flow/signal_map.csv`.

**Unlike the review's other drafts, these two findings were not checked by an independent verifier.** Two source lines behind them were re-read during synthesis and match (below). The first step of this task is to re-measure before changing anything.

**What the reviewer measured.**
- Unit-test counts and runtimes are recorded every day and never drawn. On the published Heart board, 27 of 27 CI-gate cards carry a trend chart while 0 of 12 unit-suite cards and 0 of 12 import cards do. The chart function has one caller, for gates (`heart/timing_display.py:188`; re-read). The ledger already holds 502 lines for 6 libraries and shows tests on `main` (Python 3.12) growing from 6,154 to 9,636 and summed suite time from 534 s to 1,261 s between early September and 2026-11-09.
- The hygiene scan's counts are computed and thrown away. The Brain board has run the pre-scan in the cloud since 2026-08-23 (173 runs, 15 mode rows each), and the board's history is set to an empty list (`board/_board.py:647`; re-read).

**The change.**
1. In `heart/timing_display.py`, pass each repo's history from `timings/unit/<repo>.jsonl` (main-branch lines only) to `chart()` for the suite and import cards, plotting test count and wall-clock. Add one board row with the organism total.
2. In `brain_board.yml`, after the render, append one line of `{date, rows: {mode: count}}` to a committed PyAutoBrain ledger file, with the same commit pattern `heart-health.yml` uses for `timings/`, and draw a sparkline per hygiene row.

Both follow the pattern that already works: an append-only record with one cloud writer. No new board, and a worker never writes to a ledger.

**Next, as separate tasks if this lands well:** shift metrics on the Brain board (today a 4-row Markdown table no board reads); failed, cancelled and rerun counts per gate; smoke and validation counts; coverage.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
