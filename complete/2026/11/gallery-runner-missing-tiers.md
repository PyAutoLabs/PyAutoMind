- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/354
- completed: 2026-11-06
- summary: RETIRED as obsolete, no change made. The gallery runner it targeted (`gallery/gallery_run.sh`, `gallery_build.py`) was deleted on 2026-09-30 (0dc177b, PyAutoEyes phase 5), and no `*visualization_upper.py` producer exists; lens figures now render in `autolens_visualization` and are collected by PyAutoEyes. The Witness asks for a DEFAULT_SCRIPTS line in a file that no longer exists.
- found by: pilot live shift 2026-11-06-pm worker (parked with the question on autolens_workspace_test#354); human ruling 2026-11-06: "retire the gallery prompt".
- leftover (not filed here): `pyauto-brain eyes survey`'s "Next action" still says to run the deleted `gallery/gallery_run.sh` (`PyAutoBrain/agents/conductors/eyes/_eyes.py:29,144`).

## Original prompt

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
