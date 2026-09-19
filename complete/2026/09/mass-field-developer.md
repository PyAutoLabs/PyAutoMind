## mass-field-developer
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/142 (closed completed 2026-09-19)
- completed: 2026-09-19
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/143 (merge b2267ce4)
- epic: mass-field (developer workspace sweep)
- summary: Migrated live JAX profiling, minimal-search, plotting-alignment, LOS, and standalone MGL builders from galaxy-attached shear to top-level `MassField` values through `fields=`. Preserved all `source_science/**` measurement archives, `legacy/quantity/**`, Euclid-owned debug scripts, the committed LOS tracer witness, and two examples tied to an unavailable legacy SLaM namespace. The helper is consumed from current PyAutoGalaxy/PyAutoLens source `main`; no packaged release is required. Validation included an AST re-walk, 32 passing LOS tests, re-measured imaging and point-source likelihood pins, representative JAX/search/plotting/SLaM runs, formatting and lint checks. The repository has no configured CI checks, so human-invoked `/prm` authorized the merge from this local evidence.

## Original prompt

# Is `autolens_workspace_developer` in the MassField epic? — 72 galaxy-attached sites, no CI, archived measurements

Type: maintenance
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
Themes:
- cluster
- hygiene
- jax-compile
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft — human approved the live-code migration on 2026-09-19
Consequence: judge
Witness: FIRST, the human's scope ruling recorded on the issue. IF in scope: an AST re-walk reports zero `af.Model(al.Galaxy, ..., shear=...)` / `al.Galaxy(..., shear=...)` outside the named exclusions; the two float regression pins are re-measured (not assumed) and either hold or are re-pinned with the measurement recorded; `source_science/results/{1..4}_*/` are byte-unchanged; `legacy/quantity/**` and the two `euclid_bug/` scripts are untouched; one script from each of `jax_profiling/`, `searches_minimal/`, `slam_pipeline/` runs end to end by hand.
Review-minutes: 30
Unattended: never
Epic: mass-field
Source-gate: PyAutoGalaxy#625 and PyAutoLens#745 merged; current source `main` is sufficient for this developer workspace
Filed: 2026-09-18
Issued: 2026-09-19

## Human scope ruling, 2026-09-19

The human approved the cross-repository flat-fields migration and confirmed the deleted `autolens_jax_joss` checkout is out of the sweep. Migrate the live modelling trees in this developer workspace, preserving the exclusions below for committed measurements, frozen archives and Euclid-owned debug scripts. The initial work plan was presented and approved in this session. The chaining helper is merged on the current PyAutoGalaxy/PyAutoLens source branches; on 2026-09-19 the human confirmed that these source workspaces may consume the current source API without waiting for a packaged release.

Implementation scope correction: preserve all of `source_science/**`, including shared `fit_helpers.py`, `sim_helpers.py`, and `extract_mge_truth.py`. `run_all_tests.py` imports the shared helpers and is explicitly idempotent against cached fit identifiers behind committed measurement rows. Migrating those helpers would change the archived run contract even with `results/**` byte-unchanged. The live-code AST witness excludes this measurement tree.

Implementation compatibility finding: `slam_pipeline/dspl.py` and `slam_pipeline/light_dark_mge.py` import the local `slam_pipeline` namespace, which has no `source_lp`, `source_pix`, or other pipeline modules in this checkout. Their `shear=` arguments target that absent legacy API, so they cannot be validated or converted to a `fields` argument without restoring or replacing the external pipeline. Preserve these two scripts as legacy examples. `slam_pipeline/mgl_slam_batch.py` is the runnable standalone stage builder to migrate.

Original request (verbatim):

> We have been doing work which updates workspaces and lots more to a fields API, can we review where the updating te API for everything got too (E.g. I dont think we have done HowToLens) and continue all of that until its done?
>
> yes do all that, note that autolens_jax_joss is deleted more recently. But lets go

## The question this prompt asks

The 2026-09-17 human ruling that fixed the `fields=` API — *"the user-facing API from
here on is fields in the model as a separate thing"* — named only **`autolens_workspace`
and `autolens_workspace_test`**. It did not name `autolens_workspace_developer`.

So **whether this repo is in the epic at all is a human scope decision**, and this
prompt asks it rather than presuming it. It is deliberately a separate prompt from the
other code consumers
(`draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md`)
because its risk profile is different in kind, not in degree.

Reasonable answers include: (a) in scope, migrate it; (b) explicitly out of scope,
recorded in the epic's Decisions so nobody re-derives the question; (c) partially — the
live modelling trees migrate, the measurement trees never do.

## Size

**72 galaxy-attached sites in 57 files**: 51 `af.Model(al.Galaxy, ..., shear=)` model
builders plus 21 `al.Galaxy(..., shear=)` instance/simulator sites, across
`jax_profiling/**`, `searches_minimal/**`, `slam_pipeline/**` (three live SLaM
pipelines), `plotting_alignment/**`, `source_science/*`.

## Why it is higher-risk — the five facts that decide it

1. **There is no CI at all.** `.github/` is absent. No `smoke_tests.txt`, no
   `no_run.yaml`, no `config/build/`, no `# ENV:` declarations, and exactly **one**
   pytest file (`los/test_los.py`). **Nothing would catch a regression except running
   scripts by hand.** Any migration plan must say which scripts get run and by whom.

2. **`source_science/results/{1..4}_*/` ship committed artefacts** — `RESULTS.md`,
   `fit_comparison.{json,md}`, `fits/` and `.png` — whose reproducibility depends on
   **cached fits keyed by the current identifiers**. Migrating changes every identifier
   and orphans those caches; `run_all_tests.py` depends on that idempotence.
   **EXCLUDE these result snapshots**: they are archived measurements, and a migration
   that rewrites them destroys the record it claims to maintain.

3. **`legacy/quantity/**` is an explicit FROZEN archive** — its README says "a frozen
   copy of the `quantity` fitting module", archived 2026-05-22. **Exclude by rule**, no
   case-by-case judgement.

4. **`euclid_bug/{likelihood_comparison,run_initial_lens_model_pix_cpu}.py` are
   Euclid-owned** debug scripts. **Coordinate, do not unilaterally edit.**

5. **Two float regression pins must be re-measured, never assumed:**
   - `jax_profiling/jit/imaging/mge.py:859` —
     `EXPECTED_LOG_LIKELIHOOD_HST = 27373.152646517716`
   - `jax_profiling/jit/point_source/source_plane.py:496` — `= -294.1401881258811`

   Both build their instance via `physical_values_from_prior_medians` →
   `instance_from_vector`, and **that vector's ordering changes when a second top-level
   collection is composed**. The pins are therefore expected to move, and the only
   acceptable evidence is a measurement: run each, record the new value, and re-pin
   with the before/after in the PR. A pin that "still passes" without being re-measured
   is a red flag, not a green one.

## If the ruling is "in scope"

- Three live SLaM pipelines (`slam_pipeline/{dspl,light_dark_mge,mgl_slam_batch}.py`)
  chain stages, so the **silent-drop** failure mode applies: a stage carrying galaxies
  forward without `fields=` loses the external field with no error. They use the helper
  recorded in `complete/2026/09/mass-field-chaining-helper.md`, merged on current source `main`.
- Target idiom is the flat form:
  `field = af.Model(al.MassField, redshift=..., shear=af.Model(al.mp.ExternalShear))`
  then `fields=field`; prior paths read `fields.shear.gamma_1`.
- Witness is an **AST re-walk, never a grep** (memory `ASTwitness`): a text grep misses
  single-line `af.Model(al.Galaxy, ..., shear=shear)` and over-reports multi-line
  kwargs.
- A committed `los/dataset/imaging/los_halos/tracer.json` holds serialized-tracer hits
  — a historical artefact, excluded.

Filed 2026-09-18 from the flat-`fields=` adoption sweep's follow-up audit
(issue autolens_workspace#561), which surveyed this repo and found no Mind prompt
covering it for the epic.
