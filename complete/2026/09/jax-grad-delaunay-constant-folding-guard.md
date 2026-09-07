# jax_grad/delaunay tests the pure_callback constant-folding hazard directly (rtol 1e-10 guard retired)

autolens_workspace_test#302 → `ccc0ad35`, closing autolens_workspace_test#298, merged 2026-09-07. One of six corrective PRs shipped 2026-09-07 under the human-authorised Heart RED corrective-PR exception (reasons: `release validation FAILED (stage integrate)` and `workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)`). Fable session planned; Opus subagents implemented per task; merged via /prm the same day. Validation of the RED clearing is the next scheduled Workspace Smoke and Release Integrate runs on fresh wheels.

- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/298
- completed: 2026-09-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/302
- corrective-red: authorization https://github.com/PyAutoLabs/autolens_workspace_test/issues/298#issuecomment-5573411750

## What shipped
- `scripts/misc/util.py`: additive `assert_mesh_callback_not_constant_folded(f_eager, f_jit, x, x_perturbed, *, min_abs_diff, rtol=1e-6)` — pins the trace point at `x`, checks the perturbation re-meshes (`min_abs_diff`), then eager-vs-jit at `x_perturbed`. `assert_eager_jit_consistent` and its ten other call sites unchanged.
- `scripts/imaging/jax_grad/delaunay.py`: the 1e-10 call replaced by the new check (perturbation `einstein_radius x 1.03`, rewires 93% of the simplex table) plus an explicit rtol=1e-6 sanity check; FD certification at 1e-2 untouched.

## Key traps / findings
- The 1e-10 failure was deterministic (CI rel 3.04e-9, local 8.75e-10): XLA reassociation of the in-graph scatter-add, not folding. Even eager-vs-eager (`value_and_grad` forward vs plain call) sits at 4.7e-10.
- The plan's "results must differ under frozen tables" guard was unfalsifiable: frozen host tables still give `|f(x) - f(x_pert)|` of 1e2–1e3 (vertex positions stay traced). Eager-vs-jit at a re-triangulated point discriminates: folded 8e-3–2.7e-1 vs honest 2e-10–3.5e-9.
- Injection point matters: patching the trace-time Python wrapper does nothing under jit; the compiled program calls the host function on every execution.
- CI (jax 0.11.1) is the final arbiter of the perturbed-point residual; local headroom under 1e-6 is ~300x. PR CI was green on both matrix legs.

## Original prompt

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
Issued: 2026-09-07

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
