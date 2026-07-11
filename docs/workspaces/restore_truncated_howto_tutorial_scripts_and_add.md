# Restore truncated HowTo tutorial scripts and add a completeness check

Type: docs
Target: workspaces
Repos:
- autogalaxy_workspace
- autolens_workspace
- howtofit
- howtogalaxy
- howtolens
- workspaces
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Restore truncated HowTo tutorial scripts and add a completeness check to prevent recurrence.

ROOT CAUSE: HowToLens/HowToGalaxy tutorials were bootstrapped from autolens_workspace/autogalaxy_workspace at the initial 'bootstrap HowTo* from workspace tutorials' commit. Several scripts were cut off mid-generation (classic LLM output-token cutoff while re-emitting a long file) and have been frozen at the truncated line count ever since. The original workspace source no longer exists, so restoration must draw on the sibling HowTo repo and git history, then author the remaining lens/galaxy-specific prose+code. Confirmed break: HowToLens/scripts/chapter_1_introduction/tutorial_1_grids_and_galaxies.py ends mid-tutorial on a docstring promising a log10 plot with no code following and no Wrap Up (429 lines vs the complete 654-line HowToGalaxy sibling).

SCOPE:
1. Audit every tutorial script across HowToLens, HowToGalaxy, HowToFit (and the source workspace repos) for the same truncation signature: ends mid-docstring, no Wrap Up section, abrupt cutoff, or line count far below its sibling. Confirmed/suspect so far: HowToLens tutorial_1_grids_and_galaxies (confirmed), tutorial_2_ray_tracing, tutorial_4_dealing_with_failure, tutorial_4_bayesian_regularization; HowToGalaxy tutorial_4_dealing_with_failure, tutorial_4_bayesian_regularization. Note tutorial_4_point_sources and tutorial_5_lensing_formalism in HowToLens are DELIBERATE 'not written yet' stubs - do NOT treat as truncated.
2. Fully restore each confirmed-truncated script: author the missing prose + code (Opus tutorial-prose work), mirroring the HowToGalaxy/HowToFit sibling where one exists, lens/galaxy-flavoured, ending in a proper Wrap Up.
3. PREVENTION: add a lightweight tutorial-completeness linter (scripts/check_tutorials_complete.py) wired into each HowTo repo's CI (and workspaces) that flags scripts ending mid-docstring or cut off without a Wrap Up, so this regression is caught on every push.

Restore scope: full prose+code. Prevention: CI lint check in the HowTo repos plus workspaces.

PHASE ORDER (per user): do HowToLens first (audit + restore + CI linter), then repeat the same audit + restore + CI wiring in HowToGalaxy and HowToFit. Each phase is docs-only (no library changes) and ships as its own PR.

<!-- formalised by the Intake (Conception) Agent on 2026-07-11 from user-intake -->
