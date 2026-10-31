# Bug: autogalaxy results guides write latent-less fits beside _quick_fit's, csv_make KeyError

Consequence: judge
Autonomy: human-required

## Original request (2026-10-31, human, verbatim)
"yes do it" — approving: make autogalaxy_workspace scripts/guides/results/start_here.py resume the
_quick_fit.py fit (same unique_tag + latent analysis); check the autolens_workspace twin.
Corrective-PR exception authorized for Heart RED reason "release validation FAILED (stage integrate)".

## Defect
@autogalaxy_workspace `scripts/guides/results/_quick_fit.py` writes its two latent fits with
unique_tag `simple_0` / `simple_1`, while `start_here.py`, `aggregator/galaxies_fit.py` and
`aggregator/samples.py` build the same model + search with `unique_tag=dataset_name` ("simple")
and a plain `ag.AnalysisImaging`. They claim to resume the helper's fit but instead run a third,
latent-less fit into `output/results_folder`. `workflow/csv_make.py` aggregates all fits and
`add_variable("galaxies.galaxy.bulge.sersic_index_x2")` raises KeyError under
`AggregateCSV(strict=True)` (PyAutoFit#1737, merged 2026-10-29 21:35). Release Integrate
autogalaxy/guides red since 2026-10-30 (runs 41026647430, 41184365143).

## Fix
Mirror @autolens_workspace's `_quick_fit.py`: write the canonical fit under the bare
`dataset_name` plus `f"{dataset_name}_1"`, so the single-result tutorials resume it.
Update the png_make/fits_make prose naming the tags. autolens_workspace already correct — no change.
