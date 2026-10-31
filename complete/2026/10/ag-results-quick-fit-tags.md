## Outcome

Corrective fix for Heart RED `release validation FAILED (stage integrate)`: Release Integrate `autogalaxy / guides`
had failed since 2026-10-30 on `scripts/guides/results/workflow/csv_make.py` (KeyError on latent
`galaxies.galaxy.bulge.sersic_index_x2`).

Cause: `_quick_fit.py` wrote its latent fits as `simple_0`/`simple_1`, while `start_here.py`,
`aggregator/galaxies_fit.py` and `aggregator/samples.py` resume `unique_tag=dataset_name` (`simple`) with a
plain `AnalysisImaging`, so they wrote a third, latent-free fit. PyAutoFit#1737 made `AggregateCSV` strict by
default, so that row's missing latent now raises instead of leaving an empty cell.

Fix (autogalaxy_workspace#267, merged 67f6ed9): canonical fit under the bare `dataset_name` plus
`dataset_name_1`, mirroring autolens_workspace; tag prose in png_make/fits_make updated; 3 notebooks regenerated.
Strict mode kept.

## Validation
- Local guides/results 12/12 PASS under profile_release incl. csv_make.py (latent present on both rows).
- PR CI 8/8 jobs green; independent review CLEAN.
- Corrective-PR exception: authorization autogalaxy_workspace#266 comment 6542894772; autonomy_log row `corrective`.

## Follow-ups (not filed)
- Optional hardening: `_quick_fit` idempotence check counts ≥2 fits, not the tags, so a stale pre-change
  local `output/results_folder` must be deleted once.
- `guides/galaxies.py` hung >20 min on the dev box (2.6s in CI) — local-only, unrelated.
- Heart stays RED until a fresh Release Integrate run passes `autogalaxy / guides`.

## Original prompt

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
