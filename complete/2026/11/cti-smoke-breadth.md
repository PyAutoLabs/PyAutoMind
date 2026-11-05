## cti-smoke-breadth
- issue: https://github.com/PyAutoLabs/autocti_workspace/issues/43
- completed: 2026-11-05
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/44

Merged autocti_workspace#44 (a92e5245) on 2026-11-05 by glance-tier auto-merge (plan approved by the human). Issue #43 closed. cti-upkeep phase 3a.

`smoke_tests.txt` grows from 6 to 36 scripts, grouped by area (overview, dataset_1d, imaging_ci, plot) and dependency-ordered (simulator → fit → database → plot). AGENTS.md "Smoke tests (CI)" now describes the representative set, what is left out and why, and the timings; the smoke_tests.yml header comment matches.

Triage of all 79 scripts (profile_smoke):
- 74 pass once dependency-ordered.
- 5 are genuinely broken, filed as `draft/bug/autocti_workspace/five_failing_scripts_triage_20261105.md`.
- `non_uniform_cosmic_rays` (~200–430 s, called by overview_4) keeps both of those out of smoke.

Evidence:
- Fresh clone, 36/36 under profile_smoke (213 s) and profile_release (317 s, the release gate).
- CI smoke legs 6 min (3.12) / 5 min (3.13), all 7 jobs green.
- Independent review (separate model): CLEAN. It checked every producer→consumer dependency and spot-ran the database and plot chains.

Note: Heart sets no explicit smoke budget; the yardstick used was the autolens smoke leg (6–7 min).

## Original prompt

# autocti_workspace: representative smoke coverage (cti-upkeep 3a)

Type: maintenance
Target: autocti_workspace
Repos:
- @autocti_workspace
Themes:
- cti
- smoke
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `smoke_tests.txt` (~35 dependency-ordered entries across overview/, dataset_1d/, imaging_ci/, plot/) passes in full from a fresh clone under both `config/build/profile_smoke.yaml` and `profile_release.yaml`, and autocti_workspace CI smoke (3.12 + 3.13) is green within ~6 min per leg.
Review-minutes: 5
Unattended: ready
Epic: cti-upkeep
Phase: 3a
Filed: 2026-11-05
Issued: 2026-11-05

Human request (2026-11-05): "yeah do 3a" — phase 3a of the cti-upkeep ledger: grow
autocti_workspace `smoke_tests.txt` from a handful of scripts to a representative set across
`dataset_1d/`, `imaging_ci/`, `plot/`, `advanced/database` within Heart's smoke time budget.

## Triage (2026-11-05, all 79 scripts, profile_smoke, scratch copy)

- 74 pass once ordering dependencies are respected (simulator → fit → database → plot).
- 5 genuine failures, out of scope here (filed separately):
  `plot/fpa/imaging_ci/database.py` (KeyError PIXSCAY), `plot/diagnostics/imaging_ci/well_filling.py`
  (TypeError), `dataset_1d/advanced/temporal/database.py` (instance has no `time`),
  `dataset_1d/advanced/temporal/plot.py` (SQLAlchemy error), `imaging_ci/advanced/chaining/noise_scaling.py`
  (needs a `poisson/simple` dataset no simulator writes).
- `imaging_ci/simulators/overview/non_uniform_cosmic_rays.py` passes but takes 434 s, so it stays out of smoke.
- No explicit Heart smoke budget exists; the yardstick is the autolens smoke leg (6–7 min); autocti is ~2 min today.

## Plan (approved 2026-11-05)

Grouped, dependency-ordered list with a comment per group, ~190 s locally. Verify from a fresh clone under
both profiles, because release.yml runs the same list as a release gate. Update the AGENTS.md smoke section
(replace "keep it tiny" with representative coverage + a timing table) and the `smoke_tests.yml` header comment.
