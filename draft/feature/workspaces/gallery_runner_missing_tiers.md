# Gallery runner: add visualization_upper + decide the modeling_visualization_jit tier

Type: feature
Target: workspaces
Repos:
- autolens_workspace_test
Themes:
- visualization
- ci-smoke
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: glance
Witness: `scripts/gallery/gallery_run.sh` DEFAULT_SCRIPTS contains both `imaging/visualization_upper.py` and `interferometer/visualization_upper.py`, a run of the tier they were slotted into renders their 12 and 17 figures, and `eyes survey autolens_workspace_test` reports no never-rendered `visualization_upper` producer.
Review-minutes: 3
Unattended: ready
Filed: 2026-07-16 (backfilled from git)

First real findings from the Eyes conductor's live survey (PyAutoBrain#117
Phase 2, `eyes survey autolens_workspace_test`):

1. `scripts/imaging/visualization_upper.py` and
   `scripts/interferometer/visualization_upper.py` produce full figure sets
   (12+17 png) but are missing from `scripts/gallery/gallery_run.sh`'s
   DEFAULT_SCRIPTS — add them (time them first; slot into fast or slow tier).
2. The `modeling_visualization_jit*` scripts (imaging ×3, interferometer,
   point_source) are never-rendered in the survey. Decide: include them in a
   runner tier (probably `--all`) or exclude them from the producer-token
   match story — they are JIT smoke tests whose figures may still be worth
   eyeballing once.
3. While there: consider `eyes survey` output as the runner's source of
   truth for gaps going forward (the survey already diffs producers vs
   rendered trees).
