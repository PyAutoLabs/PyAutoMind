# MGE lens-light stage writes no latent output: one non-finite latent drops all twelve

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: the `vis_lp` search of `euclid_dr1_prelim` tile 102005065 (342398 dataset and config) writes `files/latent/latent_summary.json` with every finite latent populated, and a unit test shows a latent that is NaN on every sample no longer suppresses the other latents.
Review-minutes: 20
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-10

## Symptom

In PyAutoLens latent output, the MGE lens-light stage (`initial_lens_model` `vis_lp` in the euclid
pipeline) writes no latent output at all. All ten dr1_prelim `initial_lens_model/vis_lp` results
of RAL job 342398 have no `files/latent/latent_summary.json` and no `latent.results`; `search.log`
says

    compute_latent_samples: no finite latent samples remained after masking; skipping latent output.

`latent_samples_from` masks globally, so one latent that is non-finite on every sample drops all
twelve latents for the search; the `vis_pix` stage of the same tiles is fine (12 keys, all
populated).

## Do

1. Diagnose which latent is non-finite for the two-basis MGE model and why (aperture-flux latents
   on a `Basis` of linear Gaussians? `effective_einstein_radius` on the `vis_lp` mass?).
2. Decide whether the global NaN mask should sacrifice the offending latent and keep the rest
   instead of dropping the whole block.

## Why it matters

Any producer pointed at `vis_lp` (`lens_mass.py --search_name=vis_lp` is a supported flag) gets
silently blank latent columns for this reason, unrelated to the retired `latent.` prefix bug, and
the SED chain seeds `sersic_lens_model` from `vis_lp`, so this needs a verdict before the
`euclid_dr1_prelim` SED fits are trusted.

Related: `complete/2026/09/catalogue-latent-prefix-blank.md` (the retired `latent.` prefix
this is distinct from) and `complete/2026/09/aggregate-csv-latent-sigma3.md` (shipped 2026-09-10, PyAutoFit#1598) (the
silent-None path that hides both).
