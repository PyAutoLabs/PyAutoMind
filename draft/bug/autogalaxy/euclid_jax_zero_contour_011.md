# Restore JAX 0.11 zero-contour compatibility for Euclid deployment

Type: bug
Target: @PyAutoGalaxy @autogalaxy_workspace_test
Autonomy: human-required
Priority: high
Filed: 2026-09-18
Blocks: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/90
Status: proposed; source plan approval required

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
