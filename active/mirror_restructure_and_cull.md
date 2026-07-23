# autolens_workspace_test: mirror-taxonomy restructure + earn-your-slot cull (Phase 2)

Type: refactor
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
- autolens_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Blocked-by: draft/feature/workspaces/env_inline_declarations.md (Phase 1b — declarations make moves config-free)

Phase 2 of the 2026-07-23 maintainability plan. Start only after Phase 1b:
once env requirements are in-file, moving a script carries its config with it
and this becomes a file-move task, not another config-sweep campaign.

**Target taxonomy** (mirror autolens_workspace): `imaging/ interferometer/
point_source/ cluster/ multi/` + one `misc/` for dataset-agnostic material.
Survey evidence (2026-07-23): 130 scripts, 18 folders + 7 loose top-level
files; 19 in smoke, 23 in no_run, 90 (69%) release-sweep-only.

**Moves (from the survey's mapping table):**
- `jax_likelihood_functions/{imaging,interferometer,point_source,multi,
  light_multipole}/*` → fold into the matching dataset folder. `datacube/*` →
  `interferometer/` (user workspace precedent: interferometer/features/
  datacube). `weak/*` → `misc/weak/` (target taxonomy has no weak/).
- `jax_grad/` → DISSOLVE by dataset: imaging_* → imaging/, interferometer →
  interferometer/, point_source → point_source/, weak + util → misc/.
- `potential_correction/` → SPLIT: subhalo_recovery.py → imaging/,
  subhalo_recovery_interferometer.py → interferometer/.
- `jax_substructure/` → imaging/. `model_composition/` → imaging/.
- `aggregator/`, `database/`, `mass/`, `mass_via_integral/`,
  `jax_assertions/`, `latent/` → `misc/<same-name>/` (results-DB and
  dataset-agnostic concerns).
- Loose top-level files (`hessian_jax`, `profiles_jit`, `tracer_jax`,
  `tracer_multiplane`, `critical_curves_zero_contour`, `coolest_*`) → misc/
  (coolest under misc/interop/).
- `profiling/` → `autolens_workspace_developer/` (zero live references
  confirmed; the two files are sibling-coupled — `profile_lens_aggregator.py`
  imports `mock_lens_results` — move together). Developer repo already hosts
  jax_profiling/, visualization_profiling/ siblings.
- `gallery/` STAYS IN PLACE — the Eyes agent (PyAutoBrain) hard-codes
  `scripts/gallery/gallery_run.sh` against the workspace root and
  gallery_build.py hard-codes its own depth (parents[2]). Repointing is its
  own task: draft/refactor/pyautobrain/eyes_gallery_repoint.md.

**Config updates in the same PR:** smoke_tests.txt paths, no_run.yaml
patterns, and any surviving profile patterns must follow the moves (validator
dead-pattern guard will catch misses). run_all_scripts.sh also hard-codes a
stale Windows WORKSPACE path — fix while touching it.

**Cull (earn-your-slot review of the 90 release-only scripts + 13 duplicate
candidates).** Criterion: a script keeps its slot only if it covers something
neither library unit tests nor the validated user workspace already covers
(the user workspace runs its own smoke + release validation). Strongest
duplicates from the survey: cluster/csv_api.py (identically named user
script), cluster/lenstool_parity, cluster/likelihood_sanity, both
potential_correction scripts (user features/potential_correction has release
overrides), coolest_* (guides/coolest_interop.py), weak-lensing surface
(user weak/), imaging/convolution* (unit-test territory), mass/* (profile
self-consistency = unit tests), imaging/simulator/*, jax_likelihood_functions/
imaging/subhalo (user advanced/subhalo). Review individually — delete, demote
to no_run, or keep with a recorded reason.

**Protected — do NOT cull:**
- `mass_via_integral/` — guards integral deflection/potential code DELETED
  from autogalaxy source; no unit test covers it.
- Any `jax_likelihood_functions` script's hardcoded log-likelihood literal —
  the absolute regression assertion is unique value even where the pipeline
  duplicates a user script. Cull only if the literal assertion is preserved
  somewhere equivalent.

**Follow-ons (file separately as this ships, per no-bulk-issue):**
autogalaxy_workspace_test same recipe (cleaner — no gallery/profiling/mass);
autofit_workspace_test gets ONLY the sub-moves (profiling extraction, jax
folds) — its taxonomy legitimately differs; autolens_profiling mirroring is a
later cosmetic pass.
