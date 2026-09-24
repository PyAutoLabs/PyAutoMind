# Certified positive solver — flip the scalar JAX default to certified + PDIP fallback

Type: feature
Target: autoarray
Repos:
- @PyAutoArray
Themes:
- inversion
- profiling
Difficulty: small
Autonomy: supervised
Priority: high
Status: split out of `certified-solver-phase-b` at close-out — phase B shipped in `complete/2026/09/certified-solver-phase-b.md` (https://github.com/PyAutoLabs/autolens_profiling/pull/302); this is what remains
Epic: certified-positive-solver
Phase: B (remainder)
Consequence: judge
Blocked-by: the PyAutoArray release shipping PyAutoArray#567
Witness: With the installed (released) PyAutoArray, a scalar `jax.jit` mapper-only JAX inversion with
default settings reports `positive_only_solver_used == "certified"` with `certified_fallback == "pdip"`,
while a `jax.jit(jax.vmap(fn))` batch and the NumPy backend still use PDIP / their current solver;
likelihoods match the pre-flip PDIP default to <= 1e-9.
Review-minutes: 15
Unattended: no
Filed: 2026-09-24

## Why

Phase B (autolens_profiling#300, PR #302, A100 array 350588) measured scalar certified + PDIP fallback
at 1.7x (Delaunay) / 1.4x (rectangular) over scalar PDIP with every lane inside the 1e-9 gate, and the
human adopted the policy on 2026-09-24. Under `jit(vmap)` certified+PDIP is slower than PDIP (the
batched `lax.cond` is a select), so the vmap path keeps PDIP until the phase-C guard
(`draft/feature/autofit/certified_solver_cond_free_batched_fallback.md`) exists.

## Do

1. After the release that ships PyAutoArray#567, change the PyAutoArray config default for the scalar
   JAX path: `positive_only_solver: certified`, `certified_fallback: pdip`. The vmap composition keeps
   library PDIP; NumPy unchanged.
2. Decide how the scalar-vs-vmap distinction is expressed (config default vs PyAutoFit Fitness batching
   selecting PDIP explicitly) — the batched path must not silently inherit the certified default.
3. Tests: default dispatch, vmap path unchanged, NumPy unchanged; downstream JAX parity at <= 1e-9.

## Context

- Record: `complete/2026/09/certified-solver-phase-b.md`; policy note
  `autolens_profiling/results/notes/certified_solver_policy_phase_b_2026_09.md`.
- Phase A: `complete/2026/09/certified-positive-solver.md` (PyAutoArray#566 / PyAutoArray#567).
