## Outcome

Merged as autolens_inference#62 (e744a4a, 2026-11-11). It fixes PyAutoInsight's
`lint` red on main ("dataset family differs from setup" on 8
point_source_image validation records), which was blocking PyAutoInsight#42.

- Cause: `inference_catalogue.py` named each phase-4 reference setup's
  `dataset_family` by the likelihood `dataset_type`, while records carry
  `dataset.class` = `Family.data_class` (the `dataset/<class>/` directory).
  They differ for point_source_image (→ point_source) and datacube
  (→ interferometer; latent, no rows yet).
- Fix: a `DATASET_CLASS` map used by the setup builder; setup ids unchanged;
  the Insight check is unchanged.
- Evidence: two new tests (fail without the fix, pass with it); 475 project
  tests passed; Insight's validator gives 8 errors on main → 0 on the branch;
  all CI lint steps green; PR CI green.
- Follow-up in the same session: Insight refresh + lint on main, then merge
  PyAutoInsight#42 (the last organism-map regeneration).

## Original prompt

# Insight lint red on main: lens point_source_image validation records "dataset family differs from setup"

Type: bug
Target: PyAutoInsight
Repos: @PyAutoInsight @autolens_inference
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Filed: 2026-11-11
Issued: 2026-11-11

## Evidence

PyAutoInsight `lint` (`bin/pyauto-insight check --offline`) fails on unchanged
`main`. Control dispatch: https://github.com/PyAutoLabs/PyAutoInsight/actions/runs/42992657574
(2026-11-11). It was last green on main 2026-10-23. It surfaced on
PyAutoInsight#42 (an AGENTS.md-only organism-map regeneration), which cannot
merge while the check is red.

    FAIL lens: invalid: results/point_source_image/image_plane/simple/validation/default/{jax_cpu_na_fp64,jax_gpu_na_fp64}/seed_{0,1}/stages.json (+ #stage-4066153148bc7e45): dataset family differs from setup

The check is `insight/catalogue.py` ~line 214: the record's `dataset.class` must
equal its setup's `dataset_family`. The offending files came in with
autolens_inference c2737ab ("Ingest phase-4 wall-time validation rows"), part of
the likelihood-lifecycle phase-4 ingest. Likely a `point_source` vs
`point_source_image` naming mismatch between the record writer and the setup
registry (the epic glossary names the family `point_source_image`). Unverified.

## Repair scope

Find which side is wrong (record writer or setup registry) and fix it at the
source. Do not relax the Insight check. Then re-run Insight lint on main and
merge PyAutoInsight#42 (the last of the 7 organism-map regenerations; the other
six merged 2026-11-11), which clears Heart's remaining manifest-drift mismatch.
