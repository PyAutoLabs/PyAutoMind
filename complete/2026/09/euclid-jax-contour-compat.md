## euclid-jax-contour-compat
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/622
- completed: 2026-09-18
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/623
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/123

Restored jax-zero-contour 2.0.0 compatibility with JAX 0.11.2 through a lazy cached local ZeroSolver subclass, used by both LensCalc construction sites. It wraps the custom_root callable in jax.tree_util.Partial before the upstream while-loop; no monkey patch or module-level JAX imports. No public API or numerical algorithm changed.

Merged library f3bab3b8 at 90e757d336e62b75790befacc77e2d6dde460879 after all four CI checks passed; integration 8bc2713 at ae45e490f75260533d0f18bb3bc2ce951377a0d5 after all three CI checks passed. Git ancestry verified for both branches. The standalone workspace regression covers circle values, jit, bounded vmap and gradients, both LensCalc paths and cache reuse; curated smoke list unchanged per independent review.

Validation: 1236 library tests; integration and Euclid latent regression PASS on JAX 0.10.2/0.11.2; full Euclid 0.11.2 suite 230 passed; 41/41 local workspace smoke; independent Sol review CLEAN. Pipeline #90 then passed all 9 CI checks and merged at 9cdee7b1. Its science deployment remains tracked separately by pipeline issue #89.

Human-authorized development-only Heart RED override: live user "I authorize" after branch validation and exact RED `release validation FAILED (stage integrate)` and YELLOW `manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml` were shown. Scope included shipping and green-CI merges, not release or SLURM submission. Authorization recorded on issue, PR bodies, active registry and first autonomy log table. Heart remains RED for releases; pending-release obligation retained.

Limitations: upstream does not promise vmap for arbitrary terminated contours. Einstein-radius reverse-gradient shape failure also occurs on unmodified PyAutoGalaxy/JAX 0.10.2 and is not claimed fixed. Evidence: tmp/euclid-flat-fields/repair-validation.md and repair-review.md.

Task validation outputs retained under tmp/euclid-flat-fields before worktree cleanup. No science outputs removed; no SLURM jobs submitted.

## Original prompt

# Restore JAX 0.11 zero-contour compatibility for Euclid deployment

Type: bug
Target: @PyAutoGalaxy @autogalaxy_workspace_test
Autonomy: human-required
Priority: high
Filed: 2026-09-18
Blocks: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/90
Status: implemented and validated; task-specific Heart shipping authorized
Issued: 2026-09-18
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/622

## Original user request

Euclid + euclid_dr1 deployment (PyAutoMind/tmp/handoffs/euclid-flat-fields.md)

The user approved the pipeline plan and subsequently approved its task-specific Heart RED development override and merge only with all required CI green. This new upstream source repair is proposed, not yet approved. The science modelling-script submission hold remains.

## Reproduction and fix locus

Pipeline #90 at 7fbdbe5 has 230 local tests and 9/9 smoke passes, independent review CLEAN. Both CI unit matrix legs fail the existing latent JAX trace test with JAX/jaxlib 0.11.2 and jax-zero-contour 2.0.0; local JAX/jaxlib is 0.10.2.

A standalone circle-contour calculation with no PyAuto code passes on JAX 0.10.2, fails on 0.11.2 with functools.partial not a valid JAX type. ZeroSolver.newton uses jax.lax.custom_root; its step_parallel_tol puts the returned callable into a lax.while_loop state. A diagnostic-only adapter wrapping that callable with jax.tree_util.Partial passes the contour calculation and a gradient under 0.11.2. No installed package or production source was patched.

Evidence: PyAutoMind/tmp/euclid-flat-fields/{ci-failed.log,zero-contour-repro.py,repro-jax010.log,repro-jax011.log,zero-contour-candidate.py,repro-candidate.log}. Third-party source: CKrawczyk/Jax-Zero-Contour.

## Proposed plan

1. Add a narrowly scoped optional-dependency adapter in PyAutoGalaxy, used by both ZeroSolver construction sites in autogalaxy/operate/lens_calc.py. Normalize the callable to a JAX-compatible Partial in a subclass, without globally monkey-patching the third-party class or importing JAX at module import time.
2. Extend JAX integration coverage in autogalaxy_workspace_test/scripts/misc/latent/ (not library NumPy unit tests): contour/Einstein-radius values, jit, vmap and gradients under both JAX 0.10.2 and 0.11.2. Retain all existing pipeline tests; no skips, expected failures, or CI downgrade.
3. Run PyAutoGalaxy's NumPy suite, affected integration/smoke checks, Euclid failing latent trace test on both JAX versions, and independent review. Ship the separate library repair through standard gates, then rerun pipeline #90 CI and resume the originally approved source-checkout deployment. Existing Heart RED reasons still require the proper task-specific shipping authorization for the new library task.

## Branch survey

PyAutoGalaxy and autogalaxy_workspace_test are clean on main; conflict guard reports no claims for either. Proposed branch: feature/euclid-jax-contour-compat. Proposed worktree: ~/Code/PyAutoLabs-wt/euclid-jax-contour-compat. No issue, source branch, or source edit has been created for this proposed repair.

## Live approval — 2026-09-18

The user approved the upstream adapter source plan and merging repair PR(s) and pipeline #90 only when every required CI check is green. No repeat source-plan approval is needed. Preserve release/readiness gates; the pipeline Heart override does not automatically cover this task. No SLURM submissions until modelling-script approval.

## Repair validation — 2026-09-18

Implemented and staged in euclid-jax-contour-compat. PyAutoGalaxy: 1236 passed; both-version integration and Euclid latent regression pass; full Euclid JAX 0.11.2 suite: 230 passed; workspace smoke 41/41 passed. Independent Sol review CLEAN. The curated smoke list remains unchanged after review; the new standalone `_jax.py` regression is retained. No source commit/push/PR yet: task-specific Heart RED development override remains required. Exact reason: `release validation FAILED (stage integrate)`; yellow: `manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`. Full evidence and limitations: issue #622 comment 5729071263 and tmp/euclid-flat-fields/repair-validation.md.

## Human-authorized development-only Heart RED override — 2026-09-18

The live user replied **“I authorize”** to: “Authorize the development-only Heart override for #622’s repair PRs, acknowledging these reasons, and their green-CI merges?”

Exact current RED: `release validation FAILED (stage integrate)`.
Exact current YELLOW: `manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`.

Passed branch gates: 1236 library tests; both-version JAX integration and Euclid regression; 230 full Euclid tests under JAX 0.11.2; 41/41 workspace smoke scripts; independent Sol review CLEAN.

Scope: commit, push and pending-release PRs for euclid-jax-contour-compat / #622, then merge only with every required GitHub CI check green, library first. Heart remains RED for releases. No release, failed-check bypass, protection override or SLURM submission is authorized. Existing modelling-script hold remains.
