# Flat MassField workspace adoption completed

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/561
PRs: https://github.com/PyAutoLabs/autolens_workspace/pull/562 (89b910dd) and https://github.com/PyAutoLabs/autolens_workspace_test/pull/322 (279a69d4), both merged 2026-09-19.

Examples now pass fields=field directly; results readers and sensitivity guards follow the flat prior paths. The second-dataset offset example retains its external field. Notebooks and navigation artifacts shipped with the implementation.

Prior recorded validation (not rerun in this merge-only close-out): 8/8 numerical equivalence cases, bit-identical log_likelihood -37796.54513586828, workspace smoke 38/38 plus 2 notebooks, regression smoke 32/32, and zero notebook AST mismatches.

Identifiers change by design: old output is not renamed or resumed; composition_mge now uses 29f82bd3de24984b94657c328b64c3be. The legacy galaxy-attached identifier remains unchanged. Sibling tutorial/developer/profiling/assistant adoption remains separate work.

Completed: 2026-09-19.
The human removed the release hold and authorized these prerequisite merges to unblock workspace regrouping. All current-head workflow runs passed: seven checks on autolens_workspace#562 and three on autolens_workspace_test#322, including both Python 3.12 and 3.13 smoke jobs. Upstream PyAutoLens #742 and #744 are merged. Git ancestry proves the task branches are merged; canonical checkouts were fast-forwarded. No release was performed.

The shared task worktree is retained because its ignored data includes 17 MB + 3.5 MB of output and 23 MB + 4.8 MB of datasets. No data was deleted; development claims are released. Retained worktrees must have their Git links repaired during the folder migration.

## Original prompt

# autolens_workspace + autolens_workspace_test: adopt the flat (bare) `fields=` form

Type: feature
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
Witness: an AST walk over `scripts/` of both repos (every `fields=` keyword value node classified, never a text grep — chaining is shape-transparent, so a `grep` for `fields.field` cannot reveal a stale chained stage and mixing forms inside one file is silently legal) reports **zero** single-entry `fields=af.Collection(field=...)` sites outside the one sanctioned regression site in `autolens_workspace_test/scripts/misc/mass/galaxy_attached_legacy.py`, **no file mixing forms**, and the genuine multi-field site `autolens_workspace/scripts/imaging/.../los_halos/simulator.py` plus all `al.Tracer(fields=[field])` list call sites untouched; per representative model per folder `model.prior_count` is unchanged and the sorted `model.unique_prior_paths` sets are equal after normalising `fields.field.` -> `fields.`, with the log-likelihood bit-identical; `autolens_workspace_test/scripts/multi_galaxy/composition_mge.py`'s identifier pin is **recomputed** from the `autolens_workspace_test/` cwd and green on the smoke gate, while `galaxy_attached_legacy.py`'s pin `35ebe935...` does **not** move; the sensitivity prior re-centring in `slam_source_{parametric,pixelized}.py` is shown to actually fire under the flat form (the `hasattr(base_model.fields.field, "shear")` guard returns False under it and would silently skip); 356 notebooks, `workspace_index.json` and `llms*.txt` regenerated through `PyAutoHands/autohands/generate.py`; smoke green in both repos.
Review-minutes: 25
Unattended: needs-human
Epic: mass-field
Phase: 6
Filed: 2026-09-18
Issued: 2026-09-18

## Context

PyAutoLens **#744** (issue #743, merged 2026-09-18 at `478213e78`) made the model slot
`fields=` accept a **bare `MassField`** alongside a collection. That library task
deliberately shipped the capability only — its record
(`complete/2026/09/mass-field-bare-fields.md`) names
`tmp/handoffs/autolens-flat-fields-sweep.md` as the follow-up adoption sweep. This is
that follow-up, and phase 6 of `draft/feature/autogalaxy/mass_field_epic.md`.

Phase 3 (`active/mass_field_workspace_sweep.md`, autolens_workspace#559) moved every
galaxy-attached field into `fields=af.Collection(field=field)`; `autolens_workspace#560`
merged at `c79c8d3`, and `autolens_workspace_test#322` is still an open draft. This task
removes the remaining stutter:

```python
# today (phase 3, collection form)               # target (flat form)
field = af.Model(al.MassField, redshift=0.5,     field = af.Model(al.MassField, redshift=0.5,
                 shear=af.Model(al.mp.ExternalShear))             shear=af.Model(al.mp.ExternalShear))
model = af.Collection(galaxies=...,              model = af.Collection(galaxies=...,
    fields=af.Collection(field=field))               fields=field)
# paths: fields.field.shear.gamma_1             # paths: fields.shear.gamma_1
```

`field` and `shear` keep their names. The withdrawn `fields=af.Collection(shear=shear)`
proposal is not used. `euclid_strong_lens_modeling_pipeline` already shipped this idiom
(PR #90, merged `9cdee7b`, task `euclid-fields-api` / issue #89) and is the **reference
implementation** — mirror it. Euclid ownership stays with that session; nothing here
edits it.

### Approved decisions (human, 2026-09-18)

| Decision | Ruling |
|---|---|
| `autolens_workspace_test` sequencing | **Fold into the existing draft PR #322 before merge** (the repo ships the collection form nowhere, so it goes straight to flat and `composition_mge.py`'s pin moves once, not twice) |
| 112 `al.Tracer(fields=[field])` call sites | **Leave as lists** (mirrors merged euclid; `tracer.fields` is always a normalized list) |
| Scope | **`autolens_workspace` + `autolens_workspace_test` only** |
| Reader back-compat | **Migrate cleanly, no prose note in the example scripts** |
| `galaxy_attached_legacy.py` collection half | **Keep as collection-form** — the workspaces' last regression witness for that form |
| Sensitivity scripts | **Hand-verify, leave parked** in `no_run.yaml` |
| `markdown/` mirrors | **Out of scope, file a follow-up** (already two generations stale) |
| `autolens_workspace_developer`, HowToLens, profiling, inference, joss, assistant | **Out of scope, follow-ups filed** |

### Identifier contract

Choosing the flat form intentionally changes prior paths and result identifiers.
Flat scripts write to **new** `output/` directories; existing trees keyed on the old
identifiers are orphaned and are **not** resumed; no pin is aliased to an old value and
no directory is renamed. The migration note goes in both PR bodies and the Mind record,
not in the example scripts.

## Method rule (non-negotiable)

**AST, never grep.** Chaining is *shape-transparent*: a stage taking
`result.model.fields` works unchanged in both forms, so a `grep` for `fields.field`
cannot reveal a stale chained stage — the constructing `af.Collection(field=...)` is the
only witness. Mixing forms inside one file is silently legal. Therefore the witness is an
AST walk classifying every `fields=` value node, **per-file atomicity** is required (no
file left mixing forms; watch the 3 pixelization/delaunay scripts carrying 2-3
construction sites each), and completion is proven by a re-walk, **never** by zero grep
hits.

## Original prompt (verbatim, 2026-09-18)

Task: perform a complete adoption sweep of the new bare MassField fields= API across the autolens project workspaces, examples and tutorials.

Read /home/jammy/Code/PyAutoLabs/AGENTS.md; follow start-dev and the library-first/workspace shipping workflow. Audit first, present the repository/file inventory, existing claims and a concrete phased plan, then wait for my approval before editing. Continue through implementation, validation and PRs after approval. Reuse existing tasks/branches where this work is already underway; do not create duplicate issues or overwrite another session's changes.

Prerequisite: verify https://github.com/PyAutoLabs/PyAutoLens/pull/744 is merged and verify the installed stack contains its bare MassField support. It is an additive library capability: direct/sliced Tracer, analysis, aggregation and Result accept bare fields, while tracer.fields is ALWAYS a normalized list. The library task deliberately retained collection examples; this is the explicitly requested follow-up adoption sweep.

For a model with one MassField, prefer:
    field = af.Model(al.MassField, redshift=0.5, shear=af.Model(al.mp.ExternalShear))
    model = af.Collection(galaxies=..., fields=field)

Use fields.shear.gamma_1/gamma_2, not fields.field.shear.gamma_1/gamma_2. Keep the variable field and inner profile name shear. An earlier fields=af.Collection(shear=shear) naming proposal was withdrawn. Keep genuine multi-field collections and intentional collection-form compatibility examples/tests.

Inventory all relevant repos from PyAutoMind/repos.yaml, active/planned tasks and live branches. Initial targets include autolens_workspace, autolens_workspace_test, autolens_workspace_developer, HowToLens and autolens_assistant; inspect autolens_profiling and autolens_inference for live runnable model builders. Locate the actual SLaM implementation and callers instead of assuming PyAutoLens/slam exists. Identify any further maintained autolens project/workspace consumers from the body map. Read each repo's instructions only when routed to it.

Euclid ownership is separate: issue https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/89 and task euclid-fields-api cover the pipeline plus euclid_dr1 deployment in another chat. Include its status in the inventory, coordinate shared dependencies, and do not edit or deploy that session's files here. Do not mutate science datasets, historical run artifacts, HPC installs or submit jobs as part of this workspace sweep. For other science projects, report remaining callers as explicit follow-ups instead of silently changing live runs.

Audit and implement all affected surfaces, not just a text replacement:
- Script model builders for imaging, interferometer, point sources, group/multi-galaxy/cluster and multi-dataset fits.
- SLaM and other staged pipelines: correctly carry free model fields vs fixed instance fields, retain shared priors/redshifts, and preserve deliberate stage-specific prior resets.
- Result readers, aggregators, CSV/catalogue consumers, diagnostics, plotting/export examples, tests, docs, assistant skills and generated notebooks/catalogues/indexes. Preserve compatibility with historical collection-form and galaxy-attached results where those readers support stored results.
- Model-side result.model.fields / result.instance.fields may be a bare MassField; instantiated tracer.fields remains a list. Do not flatten tracer storage or change multi-field physics.
- Exclude generated outputs, archived experiment snapshots and old result JSON/identifiers from automatic rewriting. Classify remaining grep hits: intentional collection, multi-field, historical compatibility, generated-from-source, other owner or missed migration.
- Change maintained notebook sources and regenerate through the repo's tooling; do not independently hand-edit generated notebooks. Update catalogue/index artifacts through their generators.

Identifier contract: choosing the flat form intentionally changes prior paths and result identifiers. Capture representative baseline paths/counts/identifiers before edits; prove counts, physical model, shared priors and likelihoods remain equivalent. Do not pin the new identifier to the old one, rename old result directories to fake continuity, or silently resume legacy searches under the new form. Clearly document the new-run/resume implications. Keep regression coverage for the supported collection form.

Testing: use repository conventions, representative model construction and chained end-to-end witnesses covering all five library consumers, collection backward compatibility, historical result readers, multi-field systems and changed downstream paths. Library unit tests stay NumPy-only; any needed JAX checks belong in the workspace-test layer. Run required affected-repo tests/smoke/notebook validation against the actual changed stack, with independent review. Do not expand unrelated smoke lists just to make a gate larger. Preserve source-checkout/PyPI release gates and label any downstream PRs that cannot yet run against a published library.

Deliver a repo-by-repo completed/remaining inventory, validated PRs and dependencies, identifier migration notes, generated-artifact status, and justified remaining collection-form references. Do not claim the sweep is complete based solely on zero grep hits.

Library prerequisite update: PR #744 merged 2026-09-18 at 478213e787781517113e96f80013270df482f665 after all four CI checks passed. Still verify the actual installed local/RAL source before adoption.

## Plan (approved 2026-09-18)

### Phase 0 — register, gate, baseline (no source edits)

1. File this prompt, add the `active.md` row, open the issue on `autolens_workspace`
   cross-referencing #559, PyAutoLens#743/#744 and euclid #90; record the phase here.
2. **Claim**: reuse task `mass-field-workspace-sweep`'s worktree
   `~/Code/PyAutoLabs-wt/mass-field-workspace-sweep` (holds both repos, clean) rather
   than cutting a conflicting branch; record the parallel-claim note on `active.md`.
3. **GATE** — diagnose draft PR #322's red leg
   (`latent_integration_smoke_jax.py:313` asserting one `files/latent/latent_summary.json`;
   green on `main`, red on the draft, and #322's only change to it is adding `fields=`)
   before any rewrite. Report the finding and confirm the path with the human. Do not
   layer the flat form onto an unexplained red.
4. Capture pre-edit baselines: per-folder representative `prior_count`, prior-path sets
   and `model.identifier` (**not** `unique_identifier`), each recorded with the cwd it
   was computed from; the AST census per file.

### Phase 1 — `autolens_workspace` (branch `feature/mass-field-flat-sweep` off `main`)

- **143 single-entry sites -> flat**, in 130 files: `imaging` 37, `multi_galaxy` 29,
  `group` 26, `interferometer` 24, `guides` 14, `multi_dataset` 12, `point_source` 1.
  (`cluster/`, `weak/` model no external shear — untouched.)
- **Leave untouched**: 166 chained `result.{model,instance}.fields` sites, 9 aliases,
  112 `al.Tracer(fields=[field])`, 3 `al.Tracer(fields=instance.fields)`, and the genuine
  multi-field `los_halos/simulator.py:292`.
- **Reader family — one commit, they are coupled**: `scripts/guides/results/_quick_fit.py`
  (builder, latent **key strings** `"fields.field.shear.magnitude"/".angle"`,
  `instance.fields.field.shear.*`) and `scripts/guides/results/workflow/csv_make.py`
  (`add_variable(argument=...)` reads the key that script writes). Split across commits =>
  a silently empty CSV column. Also `scripts/guides/results/aggregator/samples.py` (tuple
  path and string path).
- **Highest-risk site**:
  `scripts/imaging/features/advanced/subhalo/sensitivity/slam_source_{parametric,pixelized}.py`
  — `hasattr(base_model.fields.field, "shear")` returns **False** under the flat form,
  silently skipping a deliberate shear prior re-centring. Rewrite the guard **and** both
  assignments to `base_model.fields.shear.*`.
- **Do not** add `fields=` to the 13 intentionally field-free light-only stages.
- **Prose**: 54 "`fields` collection" lines in 38 scripts; 9
  `result.instance.fields.field.shear` docstring/`__Model__` lines; `__Model__` bullets
  "in its own `fields` collection".
- **Generated, never hand-edited**: regenerate the 356 notebooks with
  `PYTHONPATH=../PyAutoHands/autohands python3 ../PyAutoHands/autohands/generate.py autolens`
  from the repo root. `workspace_index.json` and `llms*.txt` come from the same flow.
- `markdown/` — out of scope (follow-up filed).

### Phase 2 — `autolens_workspace_test`, folded into draft PR #322

On the existing `feature/mass-field-workspace-sweep` branch/worktree.

- **66 single-entry sites -> flat** across 65 files (`interferometer/jax_grad/gradient.py`
  has 2). Every one is the identical literal, preceded by one of two identical comment
  lines that must move with it.
- `scripts/multi_galaxy/model_fit.py` — `model.fields.field.shear.prior_count` ->
  `model.fields.shear.prior_count`.
- `scripts/multi_galaxy/composition_mge.py` — three coupled edits: **recompute the pin**
  (currently `b99831e66dd27eee314113e8e58235b6`, collection form) **from the
  `autolens_workspace_test/` cwd**, fix the path grouping
  (`path[1] in ("lens","source","field")` -> `"shear"`), and update the docstring note.
  On the smoke gate — a wrong pin goes red on the first run; a human eyeballs the value.
- `scripts/misc/mass/galaxy_attached_legacy.py` — pin `35ebe935...` must **not** move; the
  collection-form model stays collection-form.
- `scripts/misc/interop/coolest_round_trip.py` — untouched (tracer-side list indexing).
- 19 chained sites in the 4 scrape SLaM scripts — no edit. 18 tracer-side/multi-field
  sites — untouched.
- No notebooks in this repo; the only generator is `gallery/gallery_run.sh`.

### Verification

- `prior_count` unchanged; prior-path sets equal after normalising `fields.field.` ->
  `fields.`; log-likelihood bit-identical on a representative model, per folder.
- **Completion witness**: AST re-walk (zero single-entry collection sites outside the
  sanctioned one; no file mixing forms).
- `autolens_workspace`: `python .github/scripts/run_smoke.py` over the migrated builder
  entries (38 active entries). Note the gap — `smoke_tests.txt` contains no `*/slam.py`,
  no `guides/results/*`, no sensitivity script — so additionally hand-run one full SLaM
  chain end-to-end and hand-verify the sensitivity prior reset actually fires, recording
  the evidence on the PR. A coverage follow-up is filed.
- `autolens_workspace_test`: smoke subset incl. `composition_mge.py`; hand-run one of the
  four SLOW-skipped chained scrape scripts; re-test `latent_integration_smoke_jax.py`
  under the flat form specifically (a third distinct structure — Phase 0's diagnosis does
  not automatically transfer).
- Independent review (`codex exec -m gpt-6-astra -s read-only -C <wt> --ephemeral -o <file>`).
- No library edits: PyAutoLens has 0 migrate sites, PyAutoGalaxy has no `fields=` slot.

### Ship

- `ship_workspace` for `autolens_workspace` -> PR; update draft PR #322 with the Phase 2
  commits. Identifier migration notes in both PR bodies and the Mind record.
- Heart is RED (`release validation FAILED (stage integrate)`) + YELLOW (manifest drift) —
  this task inherits it; **PR-open needs the human's explicit ack**, recorded verbatim.
- `/prm` is the human's call; merge stays human.

## Follow-ups to file (not done here)

- **HowToLens phase 5** — 28 galaxy-attached sites / 22 scripts. Amend
  `draft/docs/workspaces/mass_field_sibling_sweep.md` (written in the collection era) so it
  teaches the flat form directly and migrates once rather than twice.
- **`autolens_workspace_developer`** — 72 galaxy-attached sites (51 builders, 3 live SLaM
  pipelines), no CI at all, and committed `source_science/results/` numbers whose
  reproducibility depends on cached fits keyed by current identifiers. Needs its own prompt.
- `autolens_profiling` (52), `autolens_assistant` (11, wiki edits need re-provenance),
  `autolens_inference` (3, incl. a live SLaM runner), `autolens_jax_joss` (7),
  `PyAutoReduce/prototypes` (2).
- **`autolens_jax_joss` is missing from `repos.yaml`** though it exists on disk and GitHub;
  `repos_sync.py --check` only drift-checks manifest->disk, so it is invisible to every
  manifest-driven sweep. Add it, and consider a disk->manifest check.
- **`chaining_util.mass_from` takes no `fields` argument**, and there is no `fields`
  handling in `PyAutoLens/autolens/util/` — every future chained migration is a
  hand-written per-stage decision with a silent-drop failure mode.
- `mass_field_from` is advertised for the flat slot in its docstring but no test exercises
  it there.
- `autolens_workspace/markdown/` (31 pages) two generations stale — dedicated regeneration run.
- Sensitivity-script CI coverage once the visualization refactor lands.
