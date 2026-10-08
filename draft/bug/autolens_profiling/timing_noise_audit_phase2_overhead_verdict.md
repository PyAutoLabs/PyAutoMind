# Timing-noise audit phase 2: one shared ABBA overhead verdict for the CI test and the fixed-light numba cell

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
Status: draft
Filed: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
Depends-on: complete/2026/10/timing-noise-audit-p1-inventory.md (fix phase 1 of the audit note)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md
Supersedes: draft/bug/autolens_profiling/call_accounting_ci_timing_threshold.md (the "relax it a bit" request; this phase fixes the guard instead of relaxing it)

## Original request (chat 2026-10-08)

"do the next step" — after phase 1 (autolens_profiling#402) ranked this as fix phase (1).

## What is wrong (audit rows T1 and P1)

The same ABBA instrument has two budgets in two units and no shared code: the CI test
`test_call_accounting_covers_a_real_likelihood_call` uses `CI_OVERHEAD_RATIO = 1.031` with a
Student-t interval whose INCONCLUSIVE is only printed (silent under `pytest -q`) and which can PASS
on a ratio below 1; the production cell `fixed_light_numba.py` gates
`overhead_ms = (ratio − 1) × clean mean` against `MAX_INSTRUMENTATION_OVERHEAD_MS = 12.0` as a
point estimate with no interval, raises on FAIL (losing the row's JSON), and the promotion rule P2
reads its PASS as a qualification.

## Scope (fix phase 1 of the audit note, verbatim intent)

1. One function, e.g. `scripts/misc/likelihood_breakdown/overhead_verdict.py::abba_overhead_verdict(block_ratios, clean_mean_s, budget_ms, ...)`,
   used by BOTH the test and the cell. Budget in the instrument's unit (ms of excess over the clean
   call). The one-sided small-sample Student-t interval of the excess is compared to the budget:
   PASS when the upper bound ≤ budget, FAIL when the lower bound > budget, FAIL_GROSS on a
   catastrophic mean (keep the existing gross guard), INCONCLUSIVE otherwise, including n < 3 and a
   mean ratio resolved below 1 (a host-noise signature, never a measured pass). Non-finite or
   non-positive input raises.
2. The cell writes PASS / FAIL / FAIL_GROSS / INCONCLUSIVE (plus bounds) into the row and raises
   only on FAIL or FAIL_GROSS; INCONCLUSIVE keeps the row and its JSON. The P2 promotion decision
   requires PASS on both arms; INCONCLUSIVE never promotes and is written as such.
3. The CI test calls the same function with the cell's 12 ms budget converted through the fixture's
   own clean mean; INCONCLUSIVE emits a visible `pytest.warns`-style warning (a `warnings.warn`
   surfaced in the summary), never a silent print. The 1.031 ratio constant goes away.
4. Witness (synthetic, no timing): the block sets in the audit note (clear pass, clear fail, the
   #361 blocks → INCONCLUSIVE, boundary zero-variance, n < 3 → INCONCLUSIVE, gross → FAIL_GROSS,
   the below-1 laptop blocks → INCONCLUSIVE, invalid → ValueError, and the three pinned RAL rows
   224 / 400 / 413 ms keeping today's verdicts), plus an assertion that the test and the cell
   import the same function object.
5. Audit note row T1/P1 updated to SOUND-with-caveats and the phase marked shipped; the lister's
   inventory check stays green; the subsumed "relax the threshold" draft is retired.

No budget is raised; no retry-to-green; the gross guard and the coverage/count assertions stay.

## Witness

`pytest scripts/misc/test/test_fixed_light_numba.py` (new parametrised cases), the shared-function
identity assertion, `AUTOLENS_PROFILING_SMOKE=1 python scripts/imaging/pixelized/fixed_light_numba.py`
import smoke, `list_timing_assertions.py --check`, ruff, `build_readme.py --check`.
