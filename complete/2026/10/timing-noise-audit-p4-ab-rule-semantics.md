Timing-noise audit phase 4 (fix phase 3 of the inventory): the pre-registered A/B go / lever rules gain an INCONCLUSIVE state, and argmax selection becomes a tie set. Issue autolens_profiling#362 stays open for fix phases (4)–(6) and phase 3b.

**Shipped:** autolens_profiling#406 (merged 2026-10-08, 94861700). It adds one shared verdict, `scripts/misc/likelihood_breakdown/ab_verdict.py`, which provides `ab_rule_verdict`, `tie_set` and `paired_block_ratio_interval`.

`ab_rule_verdict` applies these steps in order:
1. A red correctness gate gives NO_GO.
2. Invalid input gives INCONCLUSIVE.
3. Fewer than 5 rounds or blocks gives INCONCLUSIVE.
4. Each criterion is judged on its own interval:
   - GO needs the whole interval and the point estimate to clear the bar.
   - NO_GO needs the whole interval to lie on the bad side.
   - Anything else is INCONCLUSIVE, recorded with the MDI.
5. The criteria are combined as a conjunction.

The verdict is wired into four rules:
- **C7** `pytree_input_ab._phase2b_rule` now also bootstraps the saved milliseconds.
- **C6** `backward_pass_ab._phase2c_rule`.
- **P2** the `fixed_light_numba` promotion uses a paired-by-instance block Student-t interval.
- **C10** `solver_config_sweep._fastest` now returns a tie set.

No pre-registered bar was raised.

**Decision taken (flagged in the PR):** C10's vmap rows and uncapped counts follow the tie set's labelled `point_leader`.

**Re-judgement** (recorded as facts in the audit note; no JSON rewritten):
- No go, no-go or NO_LEVER call changed:
  - C7: 4 rows.
  - C6: 24 rows, 15 GO and 9 NO_GO.
  - P2: the s4b NO_LEVER, with the speedup interval at [−1.31 %, −0.32 %].
- 7 of the 9 committed "best admissible" names are tie sets.
- IP-4a's 2.37x leader is one of five tied configurations.

**Ledger and verdict counts:** the audit note moves to 32 rows, 16 SOUND, 11 FRAGILE and 5 UNSAFE-SILENT. Phase 3b (C1 / C3 / C4 / C5 intervals) and a Holm / Bonferroni policy are recorded as follow-ups.

**Witness:** `scripts/misc/test/test_ab_verdict.py` (37 tests) and the P2 tests in `test_fixed_light_numba.py`. The full suite gave 1210 passed and 6 skipped. The independent Opus review was CLEAN, and its 3 advisories were addressed. Heart was YELLOW, an 8× manifest drift plus no rehearsal, which the human acknowledged on 2026-10-08.

## Original prompt

# Timing-noise audit phase 4: A/B go / lever rules gain INCONCLUSIVE + tie sets (fix phase 3)

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- measurement-tools
Difficulty: moderate
Autonomy: supervised
Priority: high
Consequence: judge
Status: active
Filed: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
Depends-on: complete/2026/10/timing-noise-audit-p3-qualify-drift.md (fix phase 2 of the audit note)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request (chat 2026-10-08)

"do next phase auto and the one after" — fix phase (3) of `results/notes/timing_noise_audit_2026_10.md`,
launched with `--auto` (effective supervised: bug, Consequence judge); plan approved in chat 2026-10-08.

## What is wrong (audit rows C7, C10, P2; C6's rule; C1/C3/C4/C5)

- C7 `pytree_input_ab._phase2b_rule`: GO on the point estimate only; the 90 % CIs are printed, not used.
- C10 `solver_config_sweep._fastest`: `best_admissible` is the argmax of a point speedup over
  configurations whose bootstrap CIs overlap (winner's curse); vmap rows are measured for it.
- P2 `fixed_light_numba` promotion: a point difference of two unpaired row means; anything under
  5 % is written as "a valid measured NO_LEVER".
- C6 `backward_pass_ab._phase2c_rule`: has CIs but no INCONCLUSIVE state (an overlapping CI reads no-go).
- C1/C3/C4/C5: point-estimate rules with no interval at all (need new block-level intervals).

## Scope (fix phase 3; bounded PR)

1. One shared verdict, `scripts/misc/likelihood_breakdown/ab_verdict.py` (beside `overhead_verdict.py`):
   GO when every criterion's whole interval clears its pre-registered bar; NO_GO only when a
   criterion's whole interval is on the bad side; INCONCLUSIVE otherwise, or n below the minimum, or
   invalid inputs. INCONCLUSIVE carries the resolvable effect (MDI, the interval half-width). A red
   correctness gate stays a NO_GO before any timing. `tie_set()` replaces argmax: a single best only
   when the leader's interval is clear of every other candidate's.
2. Wire C7, C6, P2 (go / NO_LEVER) and C10 (tie set) to it. Bars, gross guards and correctness gates
   unchanged; no bar raised. P2 gets a block-level seeded bootstrap of the speedup fraction.
3. Deterministic seeded witnesses (30 % → GO, 0 % → NO_GO, 15 % straddling → INCONCLUSIVE,
   overlapping configurations → tie set, n < min and invalid inputs → INCONCLUSIVE) + each cell
   imports the same function object.
4. Re-judge the committed JSONs those rules produced; record as facts in the note (no JSON rewritten,
   no recorded campaign decision reversed).
5. C1/C3/C4/C5 recorded in the note as **phase 3b** (they need new interval machinery per cell; one
   bounded PR cannot carry them as well). Multiple comparisons: tie sets only; Holm/Bonferroni a
   recorded follow-up.

## Witness

`pytest scripts/misc/test` (new `test_ab_verdict.py`), ruff, every lint.yml `--check`
(`list_timing_assertions`, `build_dashboard`, `build_catalogue --validate-with ../PyAutoPulse`,
`build_readme`, `check_wiki`, `check_results_layout`, `check_submits`), independent review.
