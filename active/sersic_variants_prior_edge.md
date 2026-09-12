# Four Sersic-stage variants on the 100 euclid_sersics core lenses (`--variant`)

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- hpc
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: `--variant` omitted reproduces today's path/unique_tag/model exactly; four `sersic_lens_model_<variant>/vis` dirs per lens
Review-minutes: 25
Filed: 2026-09-12
Issued: 2026-09-12

User request (verbatim, 2026-09-12, after the euclid_sersics core run 342696 —
100 lenses, both stages — finished):

"""
Do the next lot of sersics i think we can do each batch of 100 at the same time and
then we'll have the info we need to decide what to do in production
"""

Two decisions taken in the same conversation:

- **A single central-noise setting**, not a ladder: `A = 9`, `sigma = 0.17"`.
- **Plan-page defaults** for the rest: the source Sersic index is left untouched,
  and the point component is an MGE of **5 Gaussians with a free centre**.

## Context

The euclid_sersics project exists to explain why the lens-light Sersic index piles
up at the prior edge `n = 5` in the June catalogue (67 % of these 100 lenses sit
above 4.5). The plan page ("Euclid Sersics Plan", rev 3) fixed four variants to be
run on the *same* 100 lenses, so their `n` distributions can be compared pairwise
and production can decide on a prior or model change:

- `baseline` — today's model, unchanged, on the new data (reproduces June).
- `wide_n` — lens `sersic_index` prior widened to `Uniform(0.5, 10.0)`; the source
  Sersic is untouched. Distinguishes "the prior edge is the cause" from "the data
  really want a high `n`".
- `central_noise` — the data are untouched and the model is identical to
  `baseline`; only the **noise map** is inflated in a Gaussian bowl at the lens
  light centre (`1 + 9 exp(-r^2 / 2 * 0.17"^2)`). If the pile-up is driven by the
  few central pixels, down-weighting them moves `n`.
- `sersic_point` — the lens galaxy gains a compact MGE `point` component (5 linear
  Gaussians, sigma log-spaced 0.01"-0.2", shared free centre), so an unresolved
  nucleus has somewhere to go other than the Sersic's cusp. Sersic prior unchanged.

Nothing in the pipeline can run a variant today:

- `@euclid_strong_lens_modeling_pipeline/scripts/sersic_lens_model.py` hard-codes
  `unique_tag="sersic_lens_model"` and composes the model inline inside
  `fit_sersic`, so there is nothing unit-testable and nowhere to vary.
- `@euclid_strong_lens_modeling_pipeline/util.py` `load_vis_dataset` has no
  noise-inflation hook, and `parse_fit_args` has no `--variant`.
- There is no CPU submitter for the Sersic stage in the pipeline at all (June's
  lives only in the `euclid` science clone).

## Deliverable (PR 1 — the pipeline)

1. `scripts/sersic_lens_model.py`: extract the inline model block into a pure
   `sersic_model_from(...)` helper (the precedent is
   `scripts/initial_lens_model.py:vis_lp_model_from`, split out for exactly this
   reason), and give `fit_sersic` a `variant: str | None = None` argument.
   `variant=None` must be **byte-for-byte today's behaviour** — same path, same
   `unique_tag`, same model — so every other project is untouched; any other
   variant writes to `unique_tag=f"sersic_lens_model_{variant}"`, which sits
   beside the others under one dataset and is scraped by
   `catalogue/scripts/lens_sersic.py --unique_tag` with no change.
2. `util.py`: a pure `inflate_noise_map_gaussian(dataset, centre, amplitude,
   sigma_arcsec)` helper (`Imaging.apply_noise_scaling` is a top-hat
   *replacement* and cannot be reused for a multiplicative map, but its rebuild
   pattern can be copied), a keyword-only `noise_inflation=None` on
   `load_vis_dataset` applied after the artefact noise-scaling loop and before
   the mask, and `parse_fit_args(with_variant=False)` mirroring the existing
   `with_seed` pattern.
3. `hpc/batch_cpu/submit_sersic_variants`: array of one task per lens, the four
   variants run **sequentially inside the task**. Not 0-399: all four variants
   restore the same `initial_lens_model/vis_lp/<hash>.zip`, and PyAutoFit's
   `restore()` unzips and deletes that zip, so four concurrent processes on one
   directory race. Sequential per lens removes the race and still runs all 400
   fits in parallel across the array. A failed variant must not kill the other
   three.
4. Documentation: one route-table row in `hpc/README.md`, one line each in
   `scripts/README.md` and `catalogue/README.md`.
5. Tests in the style of `tests/test_util.py` and `tests/test_vis_lp_model.py`:
   the noise-inflation profile (ratio `1 + A` at the centre, the Gaussian decay,
   `-> 1` far out, data and PSF untouched), and the four models via
   `sersic_model_from` (prior counts 12 / 12 / 12 / 16, the widened `n` prior
   really reporting `(0.5, 10.0)` while the source keeps `(0.8, 5.0)`, the point
   Basis's five Gaussians and sigma range, and the `--variant` round-trip
   including rejection of an unknown name).

Verification: `pytest -q -m "not slow" tests` green, and the `variant=None` test
is what pins "nothing else changed".

## Follow-ups (not this PR)

- The science clone `euclid_sersics` gets a site copy of the submitter, a local
  one-lens pre-flight over all four variants, and the 100-task array submission.
- PR 2: `scripts/analysis/sersic_variants.py` — per-variant `n` histograms,
  fractions above 4.5 / 4.9 / 9.5, paired deltas against `baseline` and against
  June, and the nucleus flux fraction for `sersic_point`.
