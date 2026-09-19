# Mass-field workspace sweep completed

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/559
PRs: https://github.com/PyAutoLabs/autolens_workspace/pull/560 (merged 2026-09-18) and https://github.com/PyAutoLabs/autolens_workspace_test/pull/322 (merged 2026-09-19, 279a69d4).

Workspace and regression examples now use a separate fields= model slot. The subsequent flat-form adoption is recorded in mass-field-flat-sweep.md; its workspace_test changes shipped in the same PR #322. The deliberate galaxy-attached legacy regression remains.

Completed: 2026-09-19.
The human removed the release hold and authorized these prerequisite merges to unblock workspace regrouping. All current-head workflow runs passed: seven checks on autolens_workspace#562 and three on autolens_workspace_test#322, including both Python 3.12 and 3.13 smoke jobs. Upstream PyAutoLens #742 and #744 are merged. Git ancestry proves the task branches are merged; canonical checkouts were fast-forwarded. No release was performed.

The shared task worktree is retained because its ignored data includes 17 MB + 3.5 MB of output and 23 MB + 4.8 MB of datasets. No data was deleted; development claims are released. Retained worktrees must have their Git links repaired during the folder migration.

## Original prompt

# autolens_workspace + autolens_workspace_test: every external field moves to `fields=` (`al.MassField`)

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
- autolens_workspace_test
Themes:
- cluster
- notebooks
Difficulty: large
Autonomy: supervised
Priority: normal
Consequence: judge
Witness: an AST walk over `scripts/` of both repos (every `Galaxy(...)` call and every `af.Model(al.Galaxy, ...)` checked for a `shear` / `mass_sheet` / `potential` keyword; every `galaxies=` argument checked for a `MassField`) reports exactly three galaxy-attached sites — `autolens_workspace_test/scripts/misc/mass/galaxy_attached_legacy.py` (×2) and the legacy case in `misc/interop/coolest_round_trip.py` — and no `MassField` inside `galaxies=`; `grep -rn shear_galaxy` returns nothing outside that legacy script's quoted ruling (text greps alone are insufficient: the single-line `af.Model(al.Galaxy, ..., shear=shear)` form escapes `al\.Galaxy\(.*shear=` and `^\s*shear=`, and prose sentences saying the library still accepts `al.Galaxy(shear=...)` are expected hits); the traced grid at fixed instance values of the migrated `imaging/`, `interferometer/`, `multi_galaxy/`, `group/` simulators/models is `np.allclose` (max abs diff 0.0) to the pre-change one; the local smoke subset (listed on the issue) is green against library `main`; both repos' CI smoke green; notebooks, `workspace_index.json` and `llms-full.txt` regenerated; `check_navigator.py --root <checkout> --banners=fail` clean from the parent directory.
Review-minutes: 15
Unattended: needs-human
Epic: mass-field
Phase: 3
Merge-gate: PyAutoGalaxy and PyAutoLens releases carrying phases 1–2 on PyPI (library `main` ≥ PyAutoGalaxy `33714b80` / PyAutoLens `71973806`). Started 2026-09-17 ahead of the release on the human's ruling, to validate the library API with real workspace runs before releasing; PRs open as drafts labelled pending-release and merge only after the release.
Filed: 2026-09-17
Issued: 2026-09-17

Third phase of `draft/feature/autogalaxy/mass_field_epic.md` (read it first),
**re-scoped 2026-09-17 on the human's ruling**: *"other than maybe an
autolens_workspace_test integration test we shouldn't be using a shear_galaxy or
putting shears or any other field in galaxies from now on. The user-facing API
from here on is fields in the model as a separate thing."* That reverses the
epic's "imaging/ keeps the galaxy-attached form" decision and absorbs the former
phase 4 (`group/`, prompt retired 2026-09-17). Every `ExternalShear`,
`MassSheet` or `ExternalPotential` attached to a `Galaxy` in either workspace
moves into an `al.MassField` in its own `fields=` slot; the library keeps the
galaxy-attached form working and unwarned, so users' own scripts are untouched.

Consequence to state in the PR and the `imaging/modeling.py` prose: a migrated
example composes a different model and gets a new PyAutoFit result identifier,
so an `output/` folder produced by the old example is not resumed by the new one.

## Survey (autolens_workspace `e794ffdd`, autolens_workspace_test `9f837ea`)

| Repo | Files mentioning `ExternalShear` | By folder |
|---|---|---|
| autolens_workspace | 217 (+4 with `MassSheet`/`ExternalPotential`) | multi_galaxy 57, imaging 54, interferometer 36, group 27, multi_dataset 17, guides 17, point_source 8, weak 1 |
| autolens_workspace_test | 87 (+6 sheets) | imaging 32, interferometer 21, misc 16, multi_dataset 14, multi_galaxy 3 |

Idiom counts in autolens_workspace `scripts/`: `shear_galaxy` 202 sites (all
under `multi_galaxy/`), `.galaxies.lens.shear` 97 (89 attribute accesses, 4
aggregator string paths), SLaM chaining `shear=<result>.model|instance.galaxies.lens.shear`
71, `shear=shear` 69, `tracer.galaxies[` 4 sites under `multi_galaxy/`.
`point_source/` and `weak/` mention shear in prose only. `cluster/` has none.

## The idiom table (apply mechanically, then read the surrounding prose)

1. **Model composition.** `shear = af.Model(al.mp.ExternalShear)` /
   `lens = af.Model(al.Galaxy, redshift=0.5, bulge=bulge, mass=mass, shear=shear)` /
   `model = af.Collection(galaxies=af.Collection(lens=lens, source=source))` →
   drop the `shear=` kwarg from the galaxy and add
   `field = af.Model(al.MassField, redshift=0.5, shear=af.Model(al.mp.ExternalShear))` /
   `model = af.Collection(galaxies=af.Collection(lens=lens, source=source), fields=af.Collection(field=field))`.
   Redshift = the lens redshift. `multi_galaxy/`: the `shear_galaxy` entry
   leaves `galaxies=` and becomes this `fields=` slot. Where an
   `ExternalPotential` or `MassSheet` is composed, use
   `al.model_util.mass_field_from(lens=lens, potential=True, ...)` so the centre
   tie to `lens.mass.centre` is the one-line default.
2. **Instances / simulators.** `al.Galaxy(redshift=0.5, ..., shear=al.mp.ExternalShear(gamma_1=0.05, gamma_2=0.05))`
   + `al.Tracer(galaxies=[lens, source])` → `field = al.MassField(redshift=0.5, shear=al.mp.ExternalShear(...))`
   + `al.Tracer(galaxies=[lens, source], fields=[field])`. Deflections sum over
   planes, so committed datasets are bit-identical — **never regenerate a
   committed dataset**; prove it once per repo with `np.allclose` on a
   simulator's tracer before/after.
3. **SLaM / chaining.** Inside a stage's `af.Model(al.Galaxy, ..., shear=<result>.model.galaxies.lens.shear)`
   drop the kwarg and give the stage's `af.Collection(...)` a
   `fields=<result>.model.fields` (free) or `fields=<result>.instance.fields`
   (fixed) — the same choice the removed kwarg made. `slam_start_here.py`,
   `imaging/features/advanced/**/slam.py`, `multi_galaxy/**/slam.py`,
   `group/**/slam.py`, `interferometer/**`, `multi_dataset/**`.
4. **Result / aggregator access.** `result.instance.galaxies.lens.shear.gamma_1` →
   `result.instance.fields.field.shear.gamma_1`; string paths
   `"galaxies.lens.shear.magnitude"` → `"fields.field.shear.magnitude"`
   (`guides/results/**`, `csv_make.py`, `samples.py`); likelihood walkthroughs
   summing `lens.shear.deflections_yx_2d_from(...)` → `field.shear...` /
   `tracer.fields[0]`; sensitivity mapping `base_model.galaxies.lens.shear.gamma_1 = ...`
   → `base_model.fields.field.shear.gamma_1`.
5. **Sheets.** `mass_sheet=ag.mp.MassSheet(...)` on a galaxy
   (`autolens_workspace_test/scripts/imaging/substructure/test_{simulate_e2e,scan_multiplane,batched_simulate}.py`)
   → a `MassField` per plane in `fields=`. `imaging/features/advanced/los_halos/simulator.py`:
   `halos = sampler.galaxies_from(sheets_as_fields=True)` / `sheets = sampler.fields_from()`
   (or `galaxies_and_fields_from()`), `al.Tracer(galaxies=[lens, source] + halos, fields=sheets)`,
   the `hasattr(g, "mass_sheet")` loops → `tracer.fields`; prose "each plane
   carries a `MassField` with a negative-κ sheet". `simulator_jax.py` prose only.
6. **Positional indices.** Removing a `shear=` kwarg removes a *profile*, not a
   galaxy, so `tracer.galaxies[k]` sites outside `multi_galaxy/` do not move.
   Under `multi_galaxy/` the `shear_galaxy` *galaxy* leaves the list, so the 4
   `tracer.galaxies[` sites (`features/advanced/shapelets/fit.py`,
   `features/linear_light_profiles/modeling.py`, `features/scaling_relation/slam.py` ×2)
   are re-checked and made named access.
7. **Prose.** "The lens galaxy's total mass distribution is an `Isothermal` and
   `ExternalShear`" → "an `Isothermal`; the external shear is an `ExternalShear`
   held in a `MassField`" (parameter counts unchanged); every "only `lens_0`
   carries the shear" line (~25 files under `group/`, `multi_galaxy/`) goes; the
   `__External Shear__` section is rewritten once in `imaging/modeling.py`
   (single-galaxy reader: a field is a container like a galaxy, shear + sheet +
   potential in one; several fields means several planes; `tracer.galaxies`
   never holds one; `model.info` shows it under `fields`) and reused with the
   regime's wording in `multi_galaxy/modeling.py` ("lens pair") and
   `group/modeling.py` ("group"). `point_source/modeling.py:53` and
   `weak/modeling.py:110` say the shear is *absent* — reword to name the field.
8. **Guides.** `guides/profiles/mass.py` `__Mass Sheets__`: introduce
   `al.MassField` as the container for `ExternalShear`, `MassSheet`,
   `ExternalPotential`, the tracer `fields=` argument, the model `fields=` slot and
   `al.model_util.mass_field_from(lens=..., potential=True)` with the centre tie;
   say the galaxy-attached form remains supported by the library for existing
   user scripts. `guides/coolest_interop.py`: after `from_coolest` the shear
   returns as an `al.MassField` in `tracer_via_coolest.fields` — print and explain
   it; export a `Tracer(fields=[...])` to show the 1:1 `MassField` entity mapping.
9. **The one legacy regression** (the human's "maybe an integration test"):
   new `autolens_workspace_test/scripts/misc/mass/galaxy_attached_legacy.py` —
   builds the galaxy-attached tracer (`al.Galaxy(shear=..., mass_sheet=...)`) and
   its `MassField` twin, asserts deflections / convergence / potential
   `np.allclose`; composes the galaxy-attached *model* and asserts its
   `unique_identifier` equals the constant frozen in the script (computed on
   library `main` when the script is written — this is the workspace-side
   identifier pin); fits both models through `AnalysisImaging` under
   `PYAUTO_TEST_MODE=2`. `misc/interop/coolest_round_trip.py` keeps its legacy
   galaxy-attached case (phase 2's legacy-peel regression), gains a `MassField`
   case beside it, and its post-import checks follow the shear into
   `tracer_back.fields`. `misc/mass/sheets.py` gains a `__MassField__` section.
   `multi_galaxy/model_fit.py` and `multi_galaxy/jax_likelihood/lp.py` move the
   `lens_0` shear to `fields=` and their "exactly one shear" prior-count
   assertions check the slot (equal lens prior counts). Everything else in the
   test repo migrates by the table.
10. **Untouched.** `Galaxy`, prior configs, `n_main_from` logic (`lens_` prefix
    over `galaxies`; only its docstring's "not counted" list changes), the
    `extra_galaxies` / `scaling_galaxies` collections, committed datasets,
    `notebooks/` (regenerated, never edited).

## Acceptance

Witness above. Regenerate notebooks with PyAutoHands `generate.py autolens`
from the worktree's workspace root (it `rmtree`s `notebooks/` and stages into
the cwd repo); run `scripts/check_sizes.sh`; navigator check from the parent
directory, never `--root .`. The local smoke subset is run before the PRs open
and its table is posted on the issue; a library defect it exposes is a new
library task on the same branch name (never a workspace stand-in).

## Ledger

- 2026-09-17: filed as the `multi_galaxy` + LOS + guides sweep (57 files),
  `imaging/` kept galaxy-attached per the epic.
- 2026-09-17: re-scoped to both repos, every folder, on the human's ruling
  (quoted above); phase 4 prompt
  `propagate_shear_galaxy_idiom_to_group_cluster.md` absorbed and retired;
  `autolens_workspace_test` folded in from phase 5 with one legacy regression
  kept; started ahead of the release with the merge gated on it.
