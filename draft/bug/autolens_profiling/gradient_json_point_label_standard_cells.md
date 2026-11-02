# Standard-size gradient cells record `"point": "prior_medians"` while evaluating at iid draw 0

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- jax-gradient
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: every standard-size driver passes the real evaluation point to `harness.run_gradient(point=...)` (as `galaxy_group_standard.py` does), the stored `results/**/gradient.json` `point` fields of standard-size cells read "iid draw 0 of the seeded sequence", and `gradient_witness.py --check` / `build_catalogue.py --check` stay green
Review-minutes: 3
Unattended: ready
Filed: 2026-11-02

Found in autolens_profiling#515 (research note `wiki/research/gradient_campaign_impact_border_tie.md`). The imaging (`standard_jax_cell` path in `scripts/imaging/*/likelihood_runtime.py`), interferometer (`likelihood_breakdown/interferometer_standard.py`), datacube (`datacube_standard.py`) and multi_dataset (`multi_dataset_standard.py`) standard drivers call `run_gradient(...)` without `point=`, so the harness default label `prior_medians` is written although the instance is `iid_instances(...)[0]`. Only `galaxy_group_standard.py` passes `point="iid draw 0 of the seeded sequence"`.

The wrong label made the PyAutoArray#671 defects (which only bite at the exact prior medians) look like a campaign risk. Fix the drivers, then correct the stored labels in place (label-only edit of the committed records; the values are unaffected) or note the correction where the records are catalogued.
