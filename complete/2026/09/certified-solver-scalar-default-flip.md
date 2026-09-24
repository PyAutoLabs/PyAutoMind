## certified-solver-scalar-default-flip

- issue: none — never started (retired at `/start_dev` planning, 2026-09-24)
- completed: 2026-09-24 (retired, not implemented)
- superseded-by: `draft/feature/autofit/certified_solver_cond_free_batched_fallback.md` (certified-positive-solver phase C)
- retired-at: `/start_dev` planning session, 2026-09-24, on the human's call ("retire this prompt as superseded by phase C")

### Why this is a record and not a backlog prompt

The prompt asked to make the certified positive-only solver (+ PDIP fallback) the default for
**scalar** JAX likelihoods (`jax.jit(fn)`, `use_jax_vmap=False`) while the batched
`jax.jit(jax.vmap(fn))` path kept PDIP. Phase B measured that scalar gain at 1.7x (Delaunay) /
1.4x (rectangular) per likelihood on an A100.

Planning found it is not worth building:

1. **No production run takes the scalar path.** The human: "I dont think anyone is running
   AutoLens without JAX vmap mode on". A scalar-only default reaches almost no real fits.
2. **Scalar is not a lever in its own right.** Batching already speeds up the rest of the
   likelihood: library PDIP `jit(vmap)` goes 79.2 → 51.8 → 38.9 ms/lane (Delaunay B4/8/16)
   against a flat ~51 ms scalar PDIP. The row that beats everything is certified + fallback
   `none` **under** `jit(vmap)` (25.9 ms/lane Delaunay B16, 24.5 rectangular), which is
   phase C once the uncertified-lane guard exists.
3. **Keeping the batched path off certified needs real complexity.** Scalar and batched
   calls can't be told apart inside the library with a gradient-safe public API:
   - `jax.custom_batching.custom_vmap` breaks `jax.grad` in JAX 0.10.2 ("Linearization failed
     to produce known values for all output primals").
   - `BatchTracer` detection needs `jax._src` (removed from the public namespace in 0.10) and
     misses `vmap(jit(f))`, because the inner `jit` is traced unbatched.
   - PyAutoFit vmaps in at least four places (`Fitness._vmap`, NUTS, SMC, NSS).
   The only safe design found was explicit scalar opt-in marks across PyAutoNerves, PyAutoFit
   and PyAutoArray: too much machinery for a path production does not use.

Anyone who does run scalar JAX can already opt in with `positive_only_solver: certified` in
config (shipped in PyAutoArray#567); the packaged default stays `pdip`.

## Original prompt

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
