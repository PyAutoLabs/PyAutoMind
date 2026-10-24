# Likelihood lifecycle phase 1B: profiling CLI renders and keeps `fit.png` per cell, `figures[]` in the v3 catalogue, fit-figure inspection step in the profiling skill and campaign template

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- figures
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: the profiling CLI writes `fit.png` for a named cell on CPU (laptop), beside the cell's result files in the §3.7 mirrored tree, using the same plotter the autolens_visualization harness uses (`subplot_fit_quick`); `build_catalogue` emits that figure in the record's `figures[]` and `build_catalogue --check --validate-with ../PyAutoPulse` stays valid at `profiling-summary@3`
Review-minutes: 25
Unattended: never
Epic: likelihood-lifecycle
Phase: 1
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-24
Issued: 2026-10-24
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/452

Phase 1 sub-issue 1B of the `likelihood-lifecycle` epic (ledger `draft/research/autolens_profiling/likelihood_lifecycle_epic.md`; report §4 "Phase 1"). Phase 0 is complete (2026-10-24). Phase 2 requires every campaign cell to carry `fit.png`, so 1B lands before phase 2. 1A (the `/eyes` review loop over the ten autolens_visualization `fit.png`, human sign-off) runs separately when the human has time and does not block 1B.

## What

1. `_profile_cli.py` renders `fit.png` for each profiled cell through the same plotter the viz harness uses (`subplot_fit_quick`, out of a tempdir), and keeps it in the cell directory of the mirrored tree (`results/<dataset_type>/<variant>/<instrument>/<setup_id>/<host_class>/[<model_variant>/]fit.png`). It must never time the plotting, and must stay off when `AUTOLENS_PROFILING_SMOKE` is set.
2. `build_catalogue.py` already adds `figures[]` where `fit.png` exists. Confirm the path and shape against the Pulse v3 contract, and add a test with a fixture cell.
3. Write the fit-figure inspection step into `skills/profile_likelihood` (the workspace profiling skill) and the campaign template, and add a short note per dataset type on how the profiling instrument differs from the viz dataset.
4. Prove it on the laptop for one named CPU cell (e.g. imaging/mge/hst on `local_cpu`). That figure is evidence, not a measurement: it lands under `experiments/` or is kept out of the commit, so it never becomes a `current` row.

## Out of scope

Re-measuring anything (phase 2); 1A human sign-off; new Eyes galleries (the re-scope of `draft/feature/pyautoeyes/{multi_galaxy,group_cluster}_gallery.md` belongs to 1A); RAL jobs.
