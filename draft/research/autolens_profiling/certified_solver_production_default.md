# Certified positive solver — production default and batched (vmap) policy (phase B)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoFit
Themes:
- profiling
- inversion
- hpc-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft — phase A (PyAutoArray certified solver, opt-in) MERGED 2026-09-23 as PyAutoArray#567, unreleased; blocked on the release that ships it
Epic: certified-positive-solver
Phase: B
Consequence: judge
Blocked-by: PyAutoMind/complete/2026/09/certified-positive-solver.md (phase A) — PyAutoArray#567 merged 2026-09-23, unreleased — blocked on the release that ships it
Witness: On the A100 (HST Delaunay N=1500 and rectangular, fp64, production budget) one matched
table of the exact production composition `jax.jit(jax.vmap(fn))` at B = 4/8/16 for: library PDIP
(today's default — the never-measured baseline), certified with `pdip` fallback, certified with
`none` fallback, and scalar `jax.jit(fn)` x B — per completed likelihood, with every lane pinned to
<= 1e-9 against scalar library PDIP; followed by a written production policy (default solver,
fallback mode, and whether PyAutoFit's Fitness batching should change) and, if the default flips,
the PyAutoArray config PR that flips it.
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-09-23

## Why

Phase A ships the certified active-set solver into PyAutoArray behind `positive_only_solver: certified`
(opt-in) for mapper-only JAX inversions. Production Nautilus evaluates `jax.jit(jax.vmap(fn))`
(`autofit/non_linear/fitness.py`), where the `lax.cond` PDIP fallback becomes a `select` and both
branches run: residue phase 2 (autolens_profiling#273) measured certified+fallback at 44.6 ms/lane
vs 31.1 ms scalar at B=16, and fallback-off at 24.9 ms/lane. Nobody has measured PDIP itself under
vmap per lane, so the production default cannot be set from existing evidence.

## Do

1. Extend `fixed_light_trace.py --vmap-batch` (phase-2 machinery) with a `--solver {pdip,certified}`
   x `--fallback {pdip,none}` arm driven through the LIBRARY setting (config override), no monkeypatch.
2. A100 array over B = 4/8/16 x the four rows above, Delaunay and rectangular, distinct seeded lanes;
   pins vs scalar library PDIP at 1e-9 (note phase 3's finding: the phase-2 2.6e-9 residual sits between
   jit(vmap) and scalar jit, not in the solver — declare how the gate treats that before submitting).
3. Decide: default solver per backend; fallback mode; whether a cond-free batched fallback (pad-and-mask,
   or run the fallback outside the batch in PyAutoFit) is worth a PyAutoFit prompt. Record the policy in
   `results/notes/` and, if the default flips, open the PyAutoArray config PR.

## Out of scope

NumPy solvers; MGE-inclusive certified solves; mixed precision; Euclid rectangular budget sweep (own prompt).
