# 04 — Inference and profiling infrastructure survey for `autofit_inference` and `autofit_profiling`

Read-only survey, 2026-10-07. Every repo was read on `main`. Citations are workspace-relative paths.
Nothing was edited.

## 0. The two findings that change the brief

1. **The inference-side organ already exists, and it is not Pulse: it is PyAutoInsight.**
   `organs/PyAutoInsight` (born 2026-10-04, `PyAutoMind/complete/2026/10/insight-organ-birth.md`)
   holds the inference instance registry (`registry.yaml`), the **`inference-summary@1`** read
   contract (`REFERENCE.md`), receipts and snapshots, campaigns and tasks, and a Pages board. Its
   only real producer is `autolens_inference` (instance `lens`). A **`galaxy_summary_v1.json`
   second-producer fixture** (`tests/fixtures/`) already shows a second producer can be read with
   no reader changes. So `autofit_inference` would feed **Insight**, the same way
   `autofit_profiling` feeds **Pulse**. The workspace-root `AGENTS.md` routing table lists neither
   Insight nor Ears. That table is stale on disk: the workspace root is not a git repo, and the
   regenerated table "lives on disk only" (`complete/2026/09/autolens-inference-birth.md`,
   deviations). The repos_sync map blocks inside the organ repos do list Insight.
2. **`autofit_profiling` is already a filed, human-gated task in Pulse.**
   `organs/PyAutoPulse/tasks/autofit_profiling_bootstrap.md` is campaign `autofit` in
   `campaigns.yaml`, status `needs-decision`. It is waiting on the human's repo-creation question;
   `gh repo view PyAutoLabs/autofit_profiling` returned nothing on 2026-10-04. Its witness:
   port `autofit_workspace_developer/{ep,graphical}` plus the analytic benchmark, reproducing
   their committed baselines, then open **epic 1**, a ranked bottleneck table for one `search.fit`
   on a fast likelihood. Epic 2 (the EP loop) follows only after epic 1's top findings ship. The
   new epic should **adopt this task**, not write a second spec.

Related fit-side Cortex projects already exist: `analytic_gaussian` and `ep_toy_gaussian`
(`organs/PyAutoCortex/projects.yaml` lines 118–144, both with `assistant: autofit_assistant`, CPU
only, outside the workspace under `/mnt/c/Users/Jammy/Science/…`). Insight already tracks them as
campaigns `analytic-gaussian` and `ep-toy-gaussian` (`PyAutoInsight/campaigns.yaml`). Their
lessons apply directly (section 5).

---

## 1. `lens/autolens_inference` — how it works

**Shape.** Standalone scripts with no `pyproject.toml`. `ruff.toml` is the root sentinel that
leaves walk up to (`AGENTS.md` "Import model"). The layout is
`scripts/<dataset_class>/{slam,searches/<sampler>}/<leaf>.py`, with shared framework under
`scripts/misc/{simulators,tooling,wall,test,searches,slam}`. Other top-level pieces:
`_inference_cli.py` (704 lines, shared flags, device info, output paths, auto-simulate,
`check_pinned*`), `instruments/`, `config/`, `hpc/`, `results/`, `wiki/project/state.md`
(the Cortex ledger) and `dashboard/summary.json`.

**What defines a leg.** Every run carries a `--config-name` from the grammar
`{local,hpc_a100}_{jax_cpu,numba_cpu,jax_gpu}_{dense,sparse}_{fp64,mp}`. `CONFIG_NAME_RE`
(`_inference_cli.py:47`) refuses a name that disagrees with the flags actually passed. The
**target** is `<instrument>/<variant>/seed<n>`, for example `simple/source_plane_solved/seed0`.

- A **parity row** is the set of runs that share a target and differ only in config name. "The
  backend is a column, never a reason to split a table" (AGENTS.md).
- The **run variant** is a path level between the instrument and the config name. The
  **instrument** is a flag, never a directory.
- The **cell** is the script path below `scripts/`, minus `.py`. The cell is also the cost profile
  and the wall-rate key (`scripts/misc/wall/check_submits.py`). A leaf is split when its cost
  profile changes, never just because a flag changed.

The search leg is `scripts/misc/searches/_point_runner.py::run_point_search`. Each leaf is about
25 lines, for example `scripts/point_source/searches/nautilus/simple_source_plane.py`. It runs
**sampler × dataset-class × instrument × variant × config × seed**.

**How the "right answer" is judged.**
- Each result row carries `truths`, the `posterior` (median, σ, ±1σ), `truth_delta_sigma`
  (= (median − truth)/σ per parameter, a plain key intersection, `_point_runner.py:247`),
  `log_likelihood_at_truth`, `max_log_likelihood`, `log_evidence` and the `completed`/`status`
  markers. Example: `results/searches/point_source/nautilus/simple/source_plane_solved/hpc_a100_jax_cpu_dense_fp64/search_seed0.json`.
- **There is no automatic acceptance threshold.** The ledger reads worst-case
  `truth_delta_sigma`, for example "1.33σ (`gamma_2`)" and "5.4σ dense / 4.7σ sparse" in
  `wiki/project/state.md` lines 166 and 321. A human rules in the Cortex.
- The exporter hard-codes `scientific: {convergence: not_assessed, acceptance: not_assessed}`
  (`scripts/misc/tooling/export_inference_summary.py:152`).
- "Witness" means two different things. It is the Cortex `witness_file: results/**/*.json` glob.
  It is also a `PYAUTO_TEST_MODE=1` plumbing witness (`.github/workflows/profile.yml`, manual
  dispatch) whose rows are never committed.

**Result schema** (`schema_version: 1`, per-row JSON):
- Identity: `target`, `sampler`, `variant`, `model`, `priors`, `config_name`, `backend`,
  `inversion`, `precision`, `instrument`, `dataset_class`, `seed`, `version`.
- Provenance: `library_revisions{…}`, `device{}`, `host`, `slurm_*`, `cores`, `use_jax`,
  `test_mode`, `status`, `completed`, `resumed`, `output_path`.
- Search: `free_parameters`, `n_live`, `n_batch`.
- Clocks: `wall_s` (from `samples_info`), `total_wall_s` (elapsed `search.fit`), `compile_s`.
- Results: `likelihood_evals`, `log_evidence` (+ `_err`, + a note when it is unavailable),
  `max_log_likelihood`, `posterior`, `truths`, `truth_delta_sigma`.
- The **admission bar**: `per_call_s` (batched `jax.jit(jax.vmap(Fitness.call))` after
  `WARMUP_CALLS`, median of `TIMED_CALLS`), `per_call_single_s`, `likelihood_s`, `overhead_s`,
  `likelihood_share`, and a `timing{batched,single}` block.

The admission bar asks whether the likelihood is a big enough share of a fit for speeding it up
to matter. It is directly reusable and is the natural bridge to `autofit_profiling`. The
point-source row shows a 0.04 % likelihood share: Nautilus overhead dominates.

**Local versus RAL.**
- Locally, run the leaf with `--config-name local_…`.
- On RAL, `hpc/batch_{gpu,cpu}/submit_<name>` are copied from `template`. The template exports
  `JAX_PLATFORMS=cuda,cpu`, `JAX_ENABLE_X64=True` and `NPROC=$SLURM_CPUS_PER_TASK`, and runs
  `nvidia-smi`.
- Every submit carries a `# WALL-BASIS:` block (`cell / device / precision / lanes / steps /
  source: rates|unmeasured / probe-first`). `check_submits.py --check` gates it in CI against
  `scripts/misc/wall/rates.py`, which shipped **empty** on purpose.
- `hpc/sync` (562 lines) has **no `push`**. The RAL copy is a git clone updated by `git pull` on
  the login node. The verbs are `pull/logs/status/submit/jobs/sacct/cancel/tail/du/check`. A pull
  writes `.cortex/pull.json` (Nautilus checkpoint size and mtime), so the Cortex can tell an
  advancing run from a stalled one.
- Results are committed locally by a human, never by a RAL job. Outputs are **kept**
  (`config/general.yaml`: `hpc_mode: false`, `remove_files: false`, `samples_to_csv: true`).

**Dashboard and publication.**
- `scripts/misc/tooling/build_readme.py` renders auto-tables into `README.md` between sentinels,
  with a `--check` idempotence gate in `lint.yml`.
- `export_inference_summary.py` (stdlib only, 333 lines) writes `dashboard/summary.json` as
  `inference-summary@1`.
- `.github/workflows/inference-summary.yml` commits it on pushes to `results/**`, then sends
  `repository_dispatch: insight-refresh` to PyAutoInsight using the org secret `PAT_PYAUTOLABS`.
- This repo has **no Pages page of its own**. Its Insight `dashboard_url` is the GitHub README
  (`PyAutoInsight/registry.yaml`).

**Cortex hook-up.**
- The `projects.yaml` row is `autolens_inference` (lines 264–276): `remote`, `local_path`,
  `ral_root`, `mirror: none` (pulls land in the checkout), `sync_cli: hpc/sync`, `sync_verbs`,
  `ledger: wiki/project/state.md`, `assistant: autolens_assistant`,
  `witness_file: results/**/*.json`, `partition: both`, `status`, `note`.
- The ledger of record is `PyAutoCortex/projects/autolens_inference.md` (Now / Runs / Log),
  written only with `scripts/cortex.py` verbs.
- `CORTEX.md` in the project points at both records.

**Lens-specific versus generic.**

| Generic, reusable as-is or with renames | Lens-specific |
|---|---|
| ruff-sentinel import model; `default_cores`; `device_info_dict`; `resolve_output_paths`; `auto_simulate_if_missing`; `check_pinned*` | `BACKENDS` numba/jax; `INVERSIONS` dense/sparse; `MESHES`, `STAGES` (SLaM), `delaunay_regularization`, `rect_mesh_classes`, `variant_name` |
| Result-row skeleton plus the `truth_delta_sigma_from` / admission-bar timing code in `_point_runner.py` | The point-source model, `FitPositionsSourceSolved`, `instruments/` |
| `hpc/sync` (rename `PROJECT_NAME`), SLURM templates, the WALL-BASIS gate | The 13–21 GB RSS HST notes; `config/latent.yaml` |
| `build_readme.py` auto-table machinery; `export_inference_summary.py`, which is close to generic (`"project": "autolens_inference"` at line 261; reads `instrument`) | `slam/_runner.py`, the parity view on `mass_total[1]` |
| `inference-summary.yml` sender; `lint.yml` (ruff, `--check`, pytest, lychee, smoke env var) | |

## 2. `lens/autolens_profiling` — the producer → summary → Pulse chain

- **Producers.** About 50 cells under `scripts/<dataset>/<model>/<measurement>.py`. Each writes a
  versioned `summary_v<lib version>.json` + PNG under `results/`. The version string is the
  PyAutoLens release, so a trend is one point per release (AGENTS.md "Running Profiles").
  `_profile_cli.py` (925 lines) adds `provenance_dict`, `machine_info_dict`, `_loadavg` and
  autotune-cache counting to the inference CLI.
- **Routing.** `catalogue/script_routes.json` with `_script_routes.py`, stdlib only, schema
  `profiling-script-routes@1`: legacy alias to canonical path. `catalogue/registry.json` declares
  the families, cells, devices and slots of the intended matrix.
- **Render.** `scripts/misc/tooling/build_dashboard.py` (1,272 lines) produces
  `dashboard/{index.html, series.json, state.json, summary.json, catalogue.json + catalogue/shards}`.
  It uses Brain `board/_theme.py`. `lint.yml` runs `--check`. `pages_dashboard.yml` publishes to
  `https://pyautolabs.github.io/autolens_profiling/` and then sends `pulse-refresh` to PyAutoPulse.
- **Contracts.** `summary.json` is `profiling-summary@1` (`dashboard/README.md` documents
  envelope, records, comparisons and refusals). `catalogue.json` is the **v2 setup catalogue**.
  The live Pulse registry row now reads `summary_path: dashboard/catalogue.json`,
  `supported_schema: profiling-summary@2` (`PyAutoPulse/registry.yaml`). v2 is the current
  contract.
- **Drift policy** (owned by the project, displayed by Pulse). `comparison_policy.id`
  `runtime-drift-2x-1ms` (ratio 2.0, floor 1 ms) compares the two newest releases per series.
  Statuses: `drifted|improved|flat|insufficient`. Rows are qualified only when produced on the
  pinned host `RELEASE_SWEEP_NODE=euclid-ral-gpu-2` with load average at or below
  `RELEASE_SWEEP_LOADAVG_CAP=8.0` (`hpc/release_sweep.conf`). Refused rows go into
  `coverage.excluded` and are never dropped silently. `profile.yml` is manual or on-release only,
  never a PR gate.
- **Wiki and skills.** `wiki/index.md` keeps one row per campaign (question, status, headline
  with host and job, verdict, library PRs and release, next). Pages live under
  `wiki/campaigns/*.md` and `wiki/setups/`, checked by `check_wiki.py`. `skills/profile_likelihood/`
  is copied out by Brain `bin/install.sh`. `baseline/campaign.json` is a draft 1,044-slot matrix
  driven by `baseline_readiness.py` (enumerate/validate/report, stdlib, no execution).
- **Generic pieces.** The v2 catalogue exporter pattern, the `--check` idempotence discipline,
  `provenance_dict` and `machine_info_dict`, the release-sweep host pin with load-average
  refusal, the campaign-wiki row format, and the `pulse-refresh` sender. The lens-specific parts
  are `build_dashboard.py`'s constants (`SUMMARY_PROJECT`, `PAGES_URL`, the
  `"library": "PyAutoLens"` default, the `autolens_version` key it scans for) and every cell.

## 3. `organs/PyAutoPulse` — registering a second instance

Pulse anticipates multiple instances. `AGENTS.md` "Adding an instance" gives four steps, and
`tests/fixtures/second_producer.json` proves "no project-specific branching".

1. The project publishes a summary behind a contract version the reader supports
   (`profiling-summary@1` or `@2`), documented in the project repo.
2. Add a validated fixture to `tests/fixtures/`.
3. Add one `registry.yaml` row, schema 1:
   - `instance`: a key, e.g. `fit`, matching `^[a-z][a-z0-9_-]*$`.
   - `repo: autofit_profiling`. This must be a **PyAutoMind `repos.yaml` key**; `path` and
     `github` are resolved from the body map and may not be written in the row.
   - `summary_path`, `supported_schema` (exact pin, e.g. `profiling-summary@2`),
     `dashboard_url` (https, the project's own page).
   - Optional `library_refs` (body-map identities, e.g. `[PyAutoFit, PyAutoNerves]`) and
     `cortex_project` (an existing Cortex key or `null`; lens uses `null`).
   - The same `(repo, summary_path)` may be registered only once.
4. `bin/pyauto-pulse board`, then commit `dashboard.{md,html}`, `badge.json`, `state.json`,
   `receipts/fit.json` and `snapshots/fit.json`. `check --offline` must pass in CI.

The receipt and snapshot formats are fixed (`REFERENCE.md` "Ingest"). The badge is shields JSON
with label `pulse`. `state.json` is Brain cockpit v1. On the project side, add a
`pages_dashboard.yml` that sends `pulse-refresh`. The org-level `PAT_PYAUTOLABS` now covers every
public repo, so no per-repo secret step is needed (`complete/2026/09/eyes-fit-cti-instances.md`).

**Lens-flavoured assumptions in Pulse** (minor):
- `pulse/setup_browser.py:43` builds the instance label with
  `repo.removesuffix("_profiling").replace("autolens","AutoLens")`, so the fit instance would be
  labelled `autofit`. This is cosmetic.
- v2 setups require `dataset/model/instrument`. `instrument` may be null with an
  `unknowns.instrument` reason, which is already sanctioned for dataset-independent component
  profiling.
- v1 identity has a single `library`/`library_version` and a `release_date` derived from the
  version string. PyAutoFit versions use the same date encoding, so this works.
- The axis table `runtime|compile|breakdown|memory` (`pulse/summary.py:42`) fits search-overhead
  profiling. The `breakdown` axis is exactly the "ranked bottleneck table".
- The campaign/task ledger is shared across instances (campaign `autofit` already exists).
- The Brain **profiling conductor is lens-coupled**: `agents/conductors/profiling/_profiling.py`
  resolves `autolens_profiling` at line 107, and the repos_sync `FIREWALL_ALLOWLIST` names it.
  Teaching it about a second project is a separate Brain change. It is not needed for Pulse
  ingest.

**Insight** mirrors this one-to-one for `autofit_inference`:
- `registry.yaml` row fields: `instance, repo, summary_path, supported_schema: inference-summary@1,
  dashboard_url, library_refs, cortex_project`.
- `bin/pyauto-insight fetch|board|check --offline|census`. The reader is stdlib only.
- The reader **accepts producer-asserted** `scientific.convergence ∈ {converged, not_converged}`
  and `acceptance ∈ {accepted, rejected}` (`insight/summary.py:239`), and counts accepted records
  as "qualified".
- A pre-registered protocol in `autofit_inference` may therefore emit real verdicts. That is
  where it can go beyond autolens_inference, which emits `not_assessed` everywhere. The
  `REFERENCE.md` guardrails still hold: no ranking of incompatible runs, no best-seed selection.

## 4. Body map, Cortex and other registries

**`organs/PyAutoMind/repos.yaml`.** One row per repo:
- Required: `path` (e.g. `fit/autofit_inference`), `github: PyAutoLabs/<name>`,
  `category: project`, `role: "<one line>"`.
- Optional: `board_owner`, hook adapters. The precedent rows are `autolens_inference` (line 351)
  and `autofit_visualization` (line 366).
- Then run `python3 scripts/repos_sync.py --write`. It regenerates the root `AGENTS.md` table
  (on disk only), the `WORKFLOW.md` owner map, the organ `map` blocks, `.pyauto-root`, and the
  two generated hooks (`.claude/hooks/session-start.sh`, `end-at-deliverable.sh`, plus Codex
  hooks) in every checked-out repo.
- `--check` legs a new repo must satisfy:
  - PyAutoHeart `config/repos.yaml`: add the repo to the `excluded:` list, as for
    `autolens_inference` and `autofit_visualization` (lines 194–203).
  - PyAutoHands `pre_build.sh` and `autohands/config/workspaces.yaml`: do not add it.
  - Brain `bin/ensure_workspace_labels.sh` owner pairs.
  - Hygiene coverage, which is derived from the body map.
  - The `origin` remote must match.
  - Checkout both ways: the repo **must be checked out** at the declared path.
  - **Tenant firewall**: naming the repo in any Brain/Heart/Build `.py`/`.sh` needs a
    `FIREWALL_ALLOWLIST` entry (`repos_sync.py:1557`). The `samplers` faculty and profiling
    conductor entries are at lines 1576–1588.
  - The `repos_sync:{history,deliverable,filing,standards}` blocks must be present in the new
    repo's `AGENTS.md` (not silent: a missing block is reported).
  - The target repo's own layout lint must allowlist `.claude/` and `CLAUDE.md`.
- Also update `ROUTING.md` (target vocabulary) and `epics.md`, as autolens_inference did.

**`organs/PyAutoCortex/projects.yaml`.**
- Restricted YAML subset parsed by `scripts/cortex.py`. Every field except `note` is required,
  and unknown fields are errors.
- Fields: `remote, local_path, ral_root, mirror, sync_cli, sync_verbs (flow list), ledger,
  assistant, witness_file, partition (gpu|ral|both), status (active|dormant|planned|retired),
  note`.
- The header says "Science repos are NOT added to PyAutoMind/repos.yaml". Yet `autolens_inference`
  sits in both. Precedent: a workspace-root **project repo** goes in both maps, while an
  out-of-workspace science folder (`analytic_gaussian`) goes in Cortex only.
- Proposed row:
  `autofit_inference: remote PyAutoLabs/autofit_inference; local_path /home/jammy/Code/PyAutoLabs/fit/autofit_inference; ral_root /mnt/ral/jnightin/autofit_inference; mirror none; sync_cli hpc/sync; sync_verbs [pull, logs, status, submit, jobs, sacct, cancel, tail, du, check]; ledger wiki/project/state.md; assistant autofit_assistant; witness_file results/**/*.json; partition ral; status active`.
- The ledger file is `projects/autofit_inference.md` (Now / Runs / Log), created and written
  only through `cortex.py` verbs, and `cortex.py check` must pass.
- The log must be newest-first (memory `cortexLogOrder`: backdated entries fail).
- `autofit_profiling` needs **no** Cortex row. `autolens_profiling` has none; Pulse uses
  `cortex_project: null`.

**Brain samplers faculty** (`agents/faculties/samplers/`, `skills/samplers`,
`skills/sampler_pipeline`):
- **Tiers**: `minimal` (`autofit_workspace_developer/searches_minimal`, external sampler wired
  straight into `af.Model`/Analysis), `archive` (`…/searches`), `integration`
  (`autofit_workspace_test/scripts/searches`), `promoted` (PyAutoFit
  `autofit/non_linear/search/<group>/<module>`).
- **Findings maturation lane**: experiment (`autolens_workspace_developer/searches_minimal`,
  `*_findings.md`), then mature (`autolens_inference/scripts/<dataset>/searches/<sampler>/`,
  one cell per sampler × dataset_class × model_type), then user-facing guides.
- **Standard problem**: 1D Gaussian (centre 50, normalization 25, sigma 10), 100 points, noise
  σ = 0.01, `np.random.seed(1)`.
- **Benchmark records**: the table in `searches_minimal/output/comparison.txt` plus
  `PyAutoMemory/wiki/methods/concepts/sampler-benchmarks.md`.
- **MLTracker diagnostics** (`searches_minimal/_metrics.py`): wrap the likelihood or rebuild the
  per-eval log L history. Report **evals-to-ML and time-to-ML** (the first eval at which the
  running max is within 1 nat of the final max), plus ESS, log Z, max log L and time per eval.
- **Promotion criteria** (all four): comparable row, converged (log Z within ~1 nat of the
  reference, parameters recovered), a concrete win, implementation cost justified.
- **How `autofit_inference` should feed it.** It becomes the **fit-side mature tier**: the
  standard-problem catalogue that criterion 3 cites alongside autolens_inference. Leaves must
  declare `run_search(sampler=, dataset_class=, model_type=)` literally. `_samplers.py:_declared_cell`
  parses that AST call. The autolens leaves call `run_point_search(sampler=…)` and fall back to
  path parsing, which is a latent mismatch worth fixing in passing. The faculty needs a
  `PYAUTO_FIT_INFERENCE` surface plus a firewall allowlist edit (Brain change). Results should
  also append to `sampler-benchmarks.md` as the durable memory.

**The consumer.** `fit/autofit_assistant/skills/af_configure_search.md` currently recommends
Nautilus "as the default" from prose, and line 112 tells users to "benchmark on their real
likelihood rather than folklore". The target is a `wiki/core/concepts/` page, for example
`search_selection.md`, generated or cited from the `autofit_inference` catalogue at a pinned
commit. **Naming collision:** `autofit_assistant/benchmarks/` is an **AI-agent prompt benchmark**
(frozen prompts, rubric, `runs/`), not a search benchmark. Name the new material "search
catalogue", not "benchmarks".

## 5. Existing fit-side seeds

| Asset | Path | Use for |
|---|---|---|
| 3-Gaussian dataset + simulator | `HowToFit/dataset/example_1d/gaussian_x3` (`model_{0,1,2}.json`, `max_log_likelihood.json` = 172.39); `HowToFit/scripts/simulators/simulators.py:132` | **Shape only.** All three components are co-centred at 50 (σ 1/5/10, norm 20/40/60): 9 params, exchangeable, so label-switching is multimodal. Also `gaussian_x2`, `gaussian_x5`, `gaussian_x2__offset_centres`, `gaussian_x2_split` |
| Simulator utility | `PyAutoFit/autofit/example/util.py:317` `simulate_dataset_1d_via_profile_1d_list_from` | `PIXELS=100`, `SIGNAL_TO_NOISE_RATIO=25` (noise 0.04), **unseeded `np.random.normal`**, so the project must seed it itself |
| Seeded simulator pattern | `fit/autofit_visualization/scripts/misc/simulators/gaussian.py` (`DATASETS` name → (kwargs, seed)) | Copy this pattern |
| Integration scripts per search | `autofit_workspace_test/scripts/searches/{Nautilus,Nautilus_jax,DynestyStatic,DynestyDynamic,Emcee,Zeus,BlackJAXNUTS,NSS,LBFGS,MultiStartAdam,MultiStartProdigy,…}.py` | Working settings and pytree registration (`enable_pytrees()`, `register_model(model)`) for each search; the first-wave search menu |
| MLTracker + comparison table | `autofit_workspace_developer/searches_minimal/{_metrics.py, *_simple.py, nuts_jax.py, output/comparison.txt}` | Port `_metrics.MLTracker` into the project as the diagnostics contract; the comparison table becomes rows |
| Nautilus overhead anatomy | `searches_minimal/nautilus_bottleneck_findings.md` (NN training 40–52 %, bounds 25–38 %, likelihood 0.6 % on a 10-d 5 µs likelihood; JAX path passes `pool=None`) | First finding for **autofit_profiling** epic 1; the motivating admission-bar result |
| EP / graphical profiling packages | `autofit_workspace_developer/{ep,graphical}/{fit,simulator,sanity,util}.py`, `profiles/N*_summary.json`, `baseline.json`, `aggregate_profiles.py` | What the Pulse task says to port into autofit_profiling |
| Analytic posterior benchmarks | `autofit_workspace_test/scripts/graphical/analytic_*.py` | Closed-form posterior control (a lineage already used by Cortex `analytic_gaussian`) |
| Aggregator profiling | `autofit_workspace_test/scripts/profiling/aggregator/` | Possible autofit_profiling cell (output/I/O overhead) |
| Sibling-repo template | `fit/autofit_visualization` (10 commits): `_viz_cli.py`, `activate.sh` (PyAutoNerves + PyAutoFit only, no HPC), `ruff.toml`, `.github/workflows/{lint,render}.yml` (render on `pyautofit-release` → `eyes-refresh`), `AGENTS.md` "project repo vs organ" section | The fit-side skeleton: library resolution, release-triggered workflow, organ dispatch |

No `gaussian_x3` exists outside HowToFit. There is no separated, ordered, or background-carrying
multi-Gaussian dataset anywhere in `fit/`.

---

## 6. Reuse versus rewrite

### `autofit_inference`

| Component | Source | Action |
|---|---|---|
| ruff sentinel, `.gitignore`, `AI_POLICY.md`, `CLAUDE.md`, `LICENSE`, `CORTEX.md`, `wiki/project/{state,_template}.md` | autolens_inference | **Copy**, rename |
| `AGENTS.md` | autolens_inference | **Copy the structure**, rewrite domain sections. Keep the `repos_sync:*` blocks verbatim |
| `activate.sh` | autofit_visualization (laptop) + autolens_inference (RAL `PYAUTO_HPC_BASE` branch) | **Merge**: fit-only `PYTHONPATH` (Nerves, Fit), RAL venv branch |
| `_inference_cli.py` → `_autofit_inference_cli.py` | autolens_inference | **Generalise**. Keep `default_cores`, `device_info_dict`, `resolve_output_paths`, `auto_simulate_if_missing`, the config-name regex idea. Drop inversion, mesh, stages, instrument. New grammar, e.g. `{local,ral,a100}_{numpy,jax_cpu,jax_gpu}_{fp64,fp32}` |
| Search runner | `scripts/misc/searches/_point_runner.py` | **Generalise** into `scripts/misc/searches/_runner.py::run_search(sampler=, dataset_class=, model_type=, …)` with a sampler registry (settings per sampler from `autofit_workspace_test/scripts/searches/*`). Keep row schema v1 field names, `truth_delta_sigma_from`, and the admission-bar timing |
| MLTracker | `autofit_workspace_developer/searches_minimal/_metrics.py` | **Copy** into `scripts/misc/searches/`; record evals-to-ML / time-to-ML per row |
| Simulators | autofit_visualization `scripts/misc/simulators/gaussian.py` | **Copy the seeded pattern**; new `gaussian_x3` truth (section 7) |
| `build_readme.py` (+ `--check`) | autolens_inference | **Copy**, replace table specs |
| `export_inference_summary.py` + `inference-summary.yml` | autolens_inference | **Copy and parametrise** `project`. Add a protocol-driven `scientific` block (section 7) |
| `hpc/sync`, `sync.conf.example`, `batch_cpu/template`, WALL-BASIS gate `scripts/misc/wall/*` | autolens_inference | **Copy**, `PROJECT_NAME=autofit_inference`. Ship a `batch_cpu` (`--partition=ral`) template only; leave out `batch_gpu` until a GPU question exists |
| `config/general.yaml` (outputs KEPT) | autolens_inference | **Copy**; drop `latent.yaml` and the positions keys |
| `.github/workflows/lint.yml` (+ smoke `AUTOFIT_INFERENCE_SMOKE=1`), `profile.yml` test-mode witness | autolens_inference | **Copy**. The toy model is cheap enough that CI can run a real 1-seed witness |
| Catalogue + research wiki | autolens_profiling `wiki/index.md` row format + `wiki/campaigns/` + `catalogue/` | **Adapt**: one wiki row per (model × search family) verdict; machine catalogue JSON for the assistant |

### `autofit_profiling`

| Component | Source | Action |
|---|---|---|
| Skeleton (`ruff.toml`, AGENTS, activate, hpc, lint) | autolens_profiling / autofit_inference | **Copy** |
| `_profile_cli.py` | autolens_profiling | **Generalise**: keep `provenance_dict`, `machine_info_dict`, `_loadavg`, `device_info_dict`, `check_pinned*`; drop mesh helpers |
| Ported baselines | `autofit_workspace_developer/{ep,graphical}`, `aggregate_profiles.py`, analytic benchmark | **Port with history** (the Pulse task witness: reproduce committed numbers) |
| Epic-1 cells | Nautilus anatomy (`nautilus_profile.py`, findings md); `searches_minimal/*`; aggregator profiling | **Re-home** as `scripts/<model>/<search>/<measurement>.py` cells, e.g. `gaussian_x1/nautilus/search_fit_breakdown.py` (`axis: breakdown`) |
| Dashboard exporter | autolens_profiling `build_dashboard.py` + `build_catalogue.py` | **Rewrite thin**: emit `profiling-summary@2` `catalogue.json` directly (setups / records / selections / hazards / recommendations), not the 1,272-line v1 trend renderer. Validate with `--validate-with ../PyAutoPulse` |
| Release-sweep pin | `hpc/release_sweep.conf` | **Copy the idea**: pin one quiet `ral` CPU node, load-average cap |
| `pages_dashboard.yml` → `pulse-refresh` | autolens_profiling | **Copy** |

### Shared package?

Not at birth. Precedent: autolens_inference copied profiling's skeleton, and the birth record
explicitly deferred hoisting `instruments/` and `simulators/` ("a separate prompt once the third
copy exists"). The stdlib-only pieces now have three or four copies: `hpc/sync`
(profiling, inference, euclid pipeline, science projects), the WALL-BASIS gate, the
`--check`-idempotent renderers, and the `inference-summary` / `profiling-summary` exporters. They
are the strongest candidates for a later shared "project kit". Natural owners would be Hands
(tooling) or Nerves (config/handshake). File that as a post-birth refactor prompt, not part of
the birth epic. The organ readers (Pulse, Insight) are already the shared, generic layer.

---

## 7. Recommended first benchmark: `gaussian_x3` (10 parameters)

**Model.** Three `af.ex.Gaussian` (centre, normalization, sigma) plus one constant background
term, for **10 free parameters**. A thin custom `Background(level)` profile summed in the
Analysis keeps it PyAutoFit-native. If you would rather add no new class, use 3 Gaussians (9)
plus a shared noise-scaling parameter, but background is the more natural tenth.
- **Break label-switching** with ordered centres:
  `model.add_assertion(g0.centre < g1.centre)`, `…g1.centre < g2.centre`. Alternatively give each
  component disjoint centre priors.
- Pre-register **one** choice. Assertions are what the user-facing workspace teaches. Disjoint
  priors make "truth" trivially identifiable but remove a real failure mode.
- Recommendation: assertions plus broad shared priors, for example centre U(0,100),
  normalization LogUniform(1e-2, 1e2), sigma U(0.5, 30), background U(−1, 1). These mirror
  autolens_inference's choice of library-default priors, "the ones a user runs"
  (`_point_runner.py` docstring).

**Dataset (one in wave 1).** `gaussian_x3_blend`: 100 pixels (x = 0..99, the `af.ex` convention),
for example centres 25 / 45 / 60, σ 3 / 6 / 10, normalizations 30 / 50 / 40, background 0.02.
Components 2 and 3 overlap, which creates real correlation and a secondary-mode risk without
being pathological. Noise is **σ = 0.04** (`SIGNAL_TO_NOISE_RATIO=25`, the `af.ex` default), so
the dataset stays readable by every `af.ex` tool. Simulate with an explicit `np.random.default_rng(data_seed)`;
never use the unseeded util as-is. Commit the JSON (`data, noise_map, model_*.json, truth.json`)
as autofit_visualization does. A `gaussian_x3_separated` easy control can come in wave 2.

**Truth and the "right answer".** Pre-register this before any run (the analytic_gaussian lesson
in section 9).
1. **Reference posterior**: 3 long runs each of Nautilus (`n_live=2000`) and DynestyStatic
   (`nlive=1000`), seeds 0–2. They must agree on log Z to within 0.2 nat and on per-parameter
   medians to within 0.1σ. This is the reference, not the generating truth.
2. Per run, **success** means all of:
   - (a) `max_log_likelihood ≥ ref_max_logL − 1` nat. This is the MLTracker tolerance and the
     only criterion for MLE searches.
   - (b) For posterior searches, every parameter satisfies `|median − ref_median| / ref_σ ≤ 1`
     **and** `σ_run / σ_ref ∈ [0.5, 2]`.
   - (c) For evidence-bearing searches, `|logZ − ref_logZ| ≤ 1` nat (faculty promotion
     criterion 2).
3. Also record `truth_delta_sigma` against the generating truth (the autolens_inference field).
   It is a check on data and model, not on the search: across *data* seeds it should look
   roughly N(0,1).
4. Emit `scientific.convergence`/`acceptance` from this protocol, with `protocol_id` and
   `reason`. Insight accepts these values.

**Run-time metrics.**
- Per row: `total_wall_s`, `wall_s`, `compile_s`, `likelihood_evals`, **evals-to-ML** and
  **time-to-ML** (MLTracker), ESS and ESS/s where meaningful, `per_call_s` / `likelihood_share`
  (the admission bar, which links to autofit_profiling).
- Headline per (search × config): **success rate over seeds**, and **expected wall per right
  answer** = mean `total_wall_s` / success rate. Report the median and p84 too; never pick a
  best seed.

**First-wave searches** (all promoted and integration-tested; settings from
`autofit_workspace_test/scripts/searches/*`), grouped so incompatible outputs are never ranked
together:
- **Nested** (posterior + log Z): `Nautilus` (workspace default and `n_live` 100/200/400),
  `DynestyStatic`, `DynestyDynamic`, `NSS` (JAX).
- **MCMC** (posterior, no log Z): `Emcee`, `Zeus`, `BlackJAXNUTS`. NUTS is a warm-start
  *consumer* (faculty table). Run it twice: cold from the prior, and chained from a short
  Nautilus. Never compare its cold leg as though it were a provider.
- **MLE** (point only): `LBFGS`, `MultiStartAdam`, `MultiStartProdigy`. Judged on (a) only.
  `Drawer` is a sanity floor and is not benchmarked.

**Seeds and configs.**
- Wave 1: 1 dataset × **10 search seeds** × the searches above × `local_numpy_fp64` (callback
  path) and `local_jax_cpu_fp64` where the search is JAX-native. That is about 250 runs, mostly
  seconds to minutes each.
- Wave 2 moves to RAL `--partition=ral` arrays (never `gpu`). It adds 5 data realisations ×
  10 seeds, plus the `separated` control.
- A100 legs are deferred: a 100-pixel likelihood is dispatch-bound, so a GPU says nothing about
  the search unless batched vmap (NSS, MultiStart) is the question.
- One explicit, well-reasoned note: ten seeds do not resolve success rates below about 80 %, so
  report Wilson intervals.

---

## 8. Minimum viable registration path

**`autofit_inference`.** Steps 3–6 are organ PRs; the core bundle can land together.
1. Human gate: `gh repo create PyAutoLabs/autofit_inference --public`, after a dedicated
   confirmation question (the precedent of the first agent-run org-repo creation).
2. Clone to `fit/autofit_inference` and land the skeleton PR. It must include the
   `repos_sync:*` blocks and a layout allowlist for `.claude/` + `CLAUDE.md`.
3. Mind: add a `repos.yaml` row (`category: project`, `path: fit/autofit_inference`), run
   `repos_sync.py --write`, update `ROUTING.md` targets and `epics.md`, run `repos_sync --check`.
4. Heart: add the repo to `config/repos.yaml` `excluded:`.
5. Cortex: add a `projects.yaml` row (section 4) and run `cortex.py check`. When the first task
   starts, create `projects/autofit_inference.md` via `cortex.py`.
6. Insight, once the exporter exists: add a fixture, add a `registry.yaml` row
   (`instance: fit`, `repo: autofit_inference`, `summary_path: dashboard/summary.json`,
   `supported_schema: inference-summary@1`, `dashboard_url: https://github.com/PyAutoLabs/autofit_inference#readme`,
   `library_refs: [PyAutoFit]`, `cortex_project: autofit_inference`), then run
   `pyauto-insight board`, commit, and `check --offline`.
7. Brain (optional at birth): `bin/clean_slate.sh` exclusion. The samplers-faculty
   `PYAUTO_FIT_INFERENCE` surface goes in a later PR, with a `FIREWALL_ALLOWLIST` entry for every
   Brain file that names the repo.
8. Org profile: add a `.github` `profile/README.md` row.
9. RAL: `git clone` into `/mnt/ral/jnightin/autofit_inference` on the login node, check that
   `source activate.sh` resolves autofit, and run `hpc/sync check`.

**`autofit_profiling`.**
1. The human answers the open question in the Pulse task `autofit_profiling_bootstrap`, then
   `gh repo create`.
2. Steps 2–4 as above, with no Cortex row.
3. Port the baselines (the task witness).
4. Pulse: add a v2 fixture and a `registry.yaml` row (`instance: fit`,
   `summary_path: dashboard/catalogue.json`, `supported_schema: profiling-summary@2`,
   `dashboard_url: https://pyautolabs.github.io/autofit_profiling/`,
   `library_refs: [PyAutoFit, PyAutoNerves]`, `cortex_project: null`), run `board`, commit
   receipts and snapshots.
5. Update `campaigns.yaml` campaign `autofit`: status and next step.
6. Project side: enable Pages, add `pages_dashboard.yml` → `pulse-refresh`.

The registry rows (Pulse and Insight) **must come after** the Mind `repos.yaml` row merges. Both
readers resolve `repo` from the body map and refuse unknown identities.

---

## 9. Risks and gotchas

- **Thresholds calibrated on unrepresentative seeds.** Cortex `analytic_gaussian`: the criterion-2
  μ threshold was calibrated on 5 seeds with |a_μ| 0.002–0.020 against a 95th percentile of 0.077
  over 200 seeds, and both reviewers called the threshold under-calibrated
  (`PyAutoCortex/projects/analytic_gaussian.md`). Calibrate tolerance bands on the reference runs'
  seed scatter, and pre-register them. Related memory: "witness bands tighter than seed scatter"
  (autolens_inference GPU legs).
- **Unseeded simulators and samplers.** `af.ex.util` draws noise without a seed. Unseeded
  dynesty/emcee/zeus made autofit_visualization re-renders non-reproducible
  (`eyes-fit-cti-instances.md`). Separate `data_seed` from `search_seed` and record both.
- **Label switching.** The existing `gaussian_x3` is co-centred and exchangeable. Without
  ordering, "truth" is ill-posed and `truth_delta_sigma` is meaningless.
- **Do not judge on completion.** `status: complete` / `completed` is execution, not convergence
  (Insight `REFERENCE.md`; the exporter's `not_assessed`).
- **Config names that lie.** autolens_inference CPU legs run on `ral` nodes but are named
  `hpc_a100_numba_cpu_…` (Cortex run 350682). Choose a grammar whose `where` field means the
  hardware, and validate the flags against the name (`CONFIG_NAME_RE`).
- **JAX env.** Every sbatch must export `JAX_ENABLE_X64=True` (or an fp64 config silently runs in
  fp32) and `NPROC=$SLURM_CPUS_PER_TASK` (or a job takes the whole node). GPU jobs also need
  `JAX_PLATFORMS=cuda,cpu` (AGENTS "Backend facts").
- **Benchmark honesty** (samplers faculty): a `pure_callback` under single-JIT constant-folds and
  can look 20–30× faster than it is. Time with `vmap` on traced inputs and warm up first: a timing
  taken straight after compile read 2.4× steady state (`_point_runner.py` docstring). The Nautilus
  JAX path uses `pool=None`, so MLP training is serial (`nautilus_bottleneck_findings.md`).
- **RAL partitions.** `ral` is the CPU partition; there is no `cpu` partition. **Never** put CPU
  arrays on `gpu` or `ral,gpu` (hard rule, 2026-09-30, memory RALgpuCPU). Never run
  `HPCPullPyAuto` while jobs are running (memory RALpullMains).
- **Outputs.** Keep them (`hpc_mode: false`, `remove_files: false`); `output/` stays gitignored.
  With `hpc_mode: true`, PyAutoFit deletes the unzipped tree.
- **Firewall and CI ordering.** A Mind PR naming the repo in Brain is red until Brain merges, and
  re-running a `pull_request` job reuses the old merge commit, so the branch must be moved
  (`eyes-fit-cti-instances.md`). Generated dashboards on Mind and Cortex `main` make birth PRs go
  `dirty` within the hour (autolens-inference birth).
- **Shared Mind checkout.** Push via a temporary worktree plus cherry-pick, never
  `reset --hard`; another session's `git add -A` swept a draft into the wrong commit at the
  autolens_inference birth. Give subagents a private env and assert `PYAUTO_ROOT` before
  `repos_sync --write`, because a parallel `worktree_create` once spilled `--write` into canonical
  checkouts.
- **Cortex discipline.** Ledgers are written only through `cortex.py` verbs, newest first. Run
  lines never flip to `done` (memory RunDone).
- **Nothing inherited.** autolens_inference forbids citing retired-programme numbers. Decide up
  front whether `searches_minimal/output/comparison.txt` and the EP `profiles/` baselines are
  *ported evidence* (Pulse task: yes, reproduce them) or *motivation only* (recommended for
  autofit_inference: re-measure).
- **The "benchmarks" name** in autofit_assistant means agent prompts, and the
  `run_search`/`run_point_search` mismatch can hide cells from the samplers faculty (section 4).

---

## 10. Phased birth plan

**Phase 1 — Births and registration (supervised; human gates on both `gh repo create` calls).**
- Two skeleton PRs (autofit_inference, autofit_profiling), copied per section 6.
- Mind `repos.yaml` + `repos_sync --write`, ROUTING, `epics.md`; Heart `excluded:`; Cortex
  `autofit_inference` row; org profile rows; Brain `clean_slate.sh`; RAL clone + `hpc/sync check`.
- Witness: `repos_sync --check` and `cortex.py check` pass, both `lint.yml` runs are green, and
  `hpc/sync check` reaches RAL.

**Phase 2 — autofit_inference harness and dataset.**
- Generalised `_runner.run_search(sampler=, dataset_class=, model_type=)`, MLTracker, a seeded
  `gaussian_x3_blend` simulator with committed data, row schema v1.
- The reference posterior (Nautilus + Dynesty long runs) and a written, pre-registered protocol
  (`wiki/project/protocol_gaussian_x3.md`).
- README auto-tables and `export_inference_summary` with protocol verdicts.
- CI witness: 1 seed × Nautilus.

**Phase 3 — Wave-1 runs and Insight registration.**
- Cortex task `gaussian_x3_search_wave1`: 10 seeds × first-wave searches, local CPU (numpy and
  JAX). Optionally RAL `ral` arrays with WALL-BASIS rows measured in phase 2.
- Commit the rows. Register the Insight instance `fit` and add an Insight campaign.
- Write the research-wiki campaign page plus a `catalogue/search_catalogue.json` that the
  assistant can read.

**Phase 4 — autofit_profiling port and epic 1 (the existing Pulse task).**
- Port `ep/`, `graphical/` and the analytic benchmark, reproducing the committed numbers.
- Re-home the Nautilus anatomy as a `breakdown` cell.
- `profiling-summary@2` catalogue exporter, Pages, `pulse-refresh`, Pulse `registry.yaml` row
  `fit`.
- Open epic 1 with a ranked bottleneck table for a single `search.fit`. Feed the
  `likelihood_share` admission bar from autofit_inference rows.

**Phase 5 — Consumers.**
- autofit_assistant `wiki/core/concepts/search_selection.md` plus an `af_configure_search.md`
  update citing the catalogue at a pinned commit.
- Samplers faculty `PYAUTO_FIT_INFERENCE` mature-tier surface, with the firewall allowlist edit.
- `PyAutoMemory/wiki/methods/concepts/sampler-benchmarks.md` entry.
- Then wave 2 (data realisations, the separated control, a second model family) and the deferred
  "project kit" refactor prompt.
