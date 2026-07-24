## Outcome — RESTRUCTURE SHIPPED + MERGED 2026-07-24 (PR #212); cull routed onward

Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/211 (OPEN —
remains the cull ledger). Move-only mirror restructure merged: scripts/ now
mirrors autolens_workspace (imaging/ interferometer/ point_source/ cluster/
multi/ + misc/), 130 scripts in → 130 out, 117 git-mv renames, only 0-byte
__init__ deletions. Two collision renames (datacube → *_datacube). gallery/ +
profiling/ deliberately untouched (Eyes coupling; blackjax developer-repo claim).

## Why it was cheap
The __Env__ declaration system (Phases 1a/1b/#189) made env config travel with
the files: the whole 130-script move needed only 16 no_run pattern updates +
one override pattern edit. KEY GATE SUBTLETY: release-mode derive_jax_markers
loses the path-marker when jax scripts leave jax_* folders — exactly
compensated by their in-file `jax` declarations (verified empirically per
script, both profiles, empty base: 0 diffs).

## Cull outcome (decision list on #211)
0 deletes recommended; human decisions 2026-07-24: mass_via_integral
KEEP-AND-RUN (live cross-validation of analytic deflections vs independent
scipy-quad integrals — nothing else covers it); the 17 simulator demotes
SUPERSEDED by Phase 2b (auto-bootstrap via should_simulate + uncommit
regenerable datasets, tip-removal only — never-rewrite rule). 5 low-confidence
flags still await human markup. Blind spot found: user imaging
potential_correction runs under SMALL_DATASETS=1 (mesh-starving) while its
interferometer sibling is exempted — fold the fix into Phase 2b or a config
follow-up.

## Gotchas
- jax_grad's `import util` resolves via sys.path[0]=script dir — movers needed
  the mass/-style sys.path shim; misc/weak.py stays co-located, no shim.
- file/dir name coexistences kept deliberately: imaging/simulator.py +
  imaging/simulator/, misc/weak.py + misc/weak/.
- Sibling-simulator subprocess spawns are workspace-root-relative path strings
  — 11 targets rewritten and existence-verified.

## Follow-ups
Phase 2b simulator_auto_bootstrap (issued next); 5 cull flags; profiling/ move
on blackjax ship; eyes_gallery_repoint; test_results_relayout (drafted).

## Original prompt

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
