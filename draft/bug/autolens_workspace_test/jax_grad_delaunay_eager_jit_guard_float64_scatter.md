# imaging/jax_grad/delaunay.py: the rtol=1e-10 eager-vs-jit guard sits inside float64 scatter on the rebuilt data

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-09-06

Left over from phase 6 (autolens_workspace_test#293 / #294). The script runs on
the weekly `workspace-smoke.yml` / `release-integrate` channels under the 900 s
`jax_grad/` budget, not on the PR gate. It passes on `origin/main` (0.2"/px,
962 masked pixels, 330 source pixels) and fails on the rebuilt data (0.3"/px,
432 masked pixels) at `util.assert_eager_jit_consistent(..., rtol=1e-10)`.
Every configuration measured, no tolerance touched:

| pixels | mask | image px | ratio | eager vs jitted rel. diff | verdict |
|---:|---:|---:|---:|---|---|
| 300 | 3.5" | 432 | 0.76 | 1.84e-9 | FAIL |
| 200 | 3.5" | 432 | 0.53 | 1.27e-10 | FAIL (closest) |
| 170 | 3.5" | 432 | 0.46 | 6.66e-10 | FAIL |
| 130 | 3.5" | 432 | 0.37 | guard passes | FD then fails: abs_err 57/130 vs tol 5/13 (under-resolved) |
| 300 | 4.5" | 716 | 0.46 | 5.40e-10 | FAIL |

The discrepancy does not track the mesh/mask ratio monotonically, so the guard
is now measuring float64 reproducibility of this problem rather than a
constant-folding failure. The sibling `regularization.py` was fixed in phase 6 by
`pixels` 300 -> 200 (its certification is FD-based); this one has two guards
that pull in opposite directions.

Ask: decide what the 1e-10 guard is protecting against (the `pure_callback`
constant-folding case it names) and test *that* directly — e.g. compare against
a deliberately constant-folded evaluation, or assert on the gradient rather than
the scalar — instead of a scalar agreement at 1e-10; alternatively size the mesh
from the data and re-derive the FD tolerance from the flip-crossing scatter the
script already documents. Widening 1e-10 by itself is not an answer.

<!-- was a member of the ci-timing-fast-tests epic (retired COMPLETE 2026-09-06, ledger complete/archive/epics/ci_timing_fast_tests_epic.md); now ordinary backlog -->
