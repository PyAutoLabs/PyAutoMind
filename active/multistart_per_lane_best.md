# Claude Development Prompt: MultiStartGradient Per-Lane Best Preservation

Type: feature
Target: PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Epic: jax-inference-profiling
Phase: 3

## Original request (verbatim)

> continue the JAX profiling epic task, which is working out JAX gradients for
> samplers in autolens use cases, its in automind in one of the epics

(Continuation session 2026-08-23: PR#150 / CP-2 merged; the next critical-path
item is CP-3, whose recorded pre-req is this change.)

## Goal

`MultiStartGradient` (Adam / ADABelief / Lion / Prodigy) currently preserves
each lane's **final** position and a single **global** best
(`best_params`/`best_fom`), but not each lane's own **best** (position,
figure-of-merit, step index). The inference programme's Phase 3
(`autolens_profiling/results/notes/inference/PROGRAMME.md` §4, §7) needs
per-lane basin classification to measure Prodigy's per-start hit probability
p_hit — final positions are unreliable for this (a lane can wander off its
best basin late, die, or get clipped after its best step).

Add per-lane best tracking to the `_fit` loop and persist it in
`search_internal`:

- `lane_best_params` — physical units on capture (mirroring `best_params`).
- `lane_best_foms` — per-lane best figure-of-merit.
- `lane_best_steps` — the step index at which each lane's best was recorded.

Constraints:

- No behaviour change to the search itself (pure diagnostics — no gating, no
  redraws keyed on it; the same rule as the NaN-lane counters).
- Resume path loads the new keys defensively (legacy `search_internal` files
  without them must still resume).
- Physical-units-on-capture under a `Scaler`, same reasoning as
  `best_params`.
- Decide + document resurrection semantics (reset per-lane best on redraw vs
  keep lane-slot history).
- Tests in `test_autofit/non_linear/search/mle/test_multi_start_gradient.py`.

## Evidence

- PROGRAMME.md Phase 3: "PyAutoFit currently preserves each lane's *final*
  position but not its *best* — a small source change Phase 3 needs first";
  §7 table row "Per-lane *best* position/FOM preservation in MultiStartGradient
  | Phase 3 pre-req | Diagnostics".
- CP-3 (§9) is the next strictly-ordered critical-path item after CP-2
  (completed 2026-08-23, PR#150 merged).
- Loop site: `autofit/non_linear/search/mle/multi_start_gradient/search.py`
  (`_fit`, global-best capture around the `foms_np`/`best_index` block;
  `search_internal` dict assembly; resume block; `samples_via_internal_from`).
