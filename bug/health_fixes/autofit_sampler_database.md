# Fix Autofit release sampler and database regressions

Type: bug
Target: health_fixes
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

## Context

Release run `28784914443` failed two @autofit_workspace cookbooks and seven
@autofit_workspace_test scripts. The cookbook failures reproduce on current `main`:
Emcee proposes invalid LogUniform values and raises `ValueError: Probability function
returned NaN`. Database failures include empty aggregators, stale/mismatched scraped
search metadata, and changed likelihood assertions.

Primary library: @PyAutoFit.

## Scripts

- `autofit_workspace/scripts/cookbooks/result.py`
- `autofit_workspace/scripts/cookbooks/samples.py`
- `autofit_workspace_test/scripts/database/directory/general.py`
- `autofit_workspace_test/scripts/database/directory/multi_analysis.py`
- `autofit_workspace_test/scripts/database/scrape/general.py`
- `autofit_workspace_test/scripts/database/scrape/grid_search.py`
- `autofit_workspace_test/scripts/database/scrape/multi_analysis.py`
- `autofit_workspace_test/scripts/database/scrape/sensitivity.py`
- `autofit_workspace_test/scripts/features/minimal_output.py`

## Required work

1. Reproduce each script from a clean output/database state using the exact release
   profiles; directory and scrape scripts must not consume prior local runs.
2. Fix Emcee initialization/proposal handling so bounded priors cannot emit NaN
   probabilities during reduced release-mode sampling.
3. Audit database directory and scrape paths, identifiers, session lifecycle, grid and
   sensitivity metadata, and minimal-output expectations against current PyAutoFit.
4. Fix library defects in PyAutoFit. Change script assertions only when the documented
   output contract intentionally changed, with an explicit explanation.
5. Add unit/integration coverage, run PyAutoFit pytest, and rerun all nine scripts.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
