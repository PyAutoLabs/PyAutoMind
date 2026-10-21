# Survey 01 — autolens_profiling and autolens_inference layout census (2026-10-21, Explore worker, read-only)

Root paths: `lens/autolens_profiling` (P) and `lens/autolens_inference` (I). All file:line references are relative to those roots.

**Three findings matter most for the plan:**
- **P `results/` is the inverse of `scripts/`.** Scripts go dataset → model → measurement. Results go measurement → dataset → (model or flat), with legacy model names (`pixelization`, not `rectangular`).
- **I's current SLaM results are not committed.** All 40 current files under `results/slam/imaging/` are git-untracked, as are `prepared/` and `results/archive/2026-10-19_numba_thread_oversubscription/`. Only the two 2026-09-24 archives, `searches/`, `simulators/` and `logs/` are tracked (108 files).
- **Neither repo has a latest/active/best/current marker file.** "Which result counts" lives in three places: a `Superseded-by` column in P's campaign index, an `archived: true` flag in I's summary, and an explicitly null "selected reference" in both catalogues.

## 1. `scripts/` trees (file counts exclude `__pycache__`)

**P**: 107 non-misc files and 212 misc files (184 `.py`). The scheme is **dataset → model/mesh (or likelihood plane) → `<measurement>.py`**. The routing contract is `catalogue/script_routes.json` (`profiling-script-routes` v1, checked at `_script_routes.py:18`). `catalogue/migration.md:3` records that 80 legacy paths were moved and their wrappers retired.
```
cluster/{image_plane[1], source_plane[1]}
datacube/delaunay[4]
imaging/{delaunay[5], delaunay_nn[2], mge[5], mge_mass[1], pixelized[17], rectangular[9], sersic[5],
         likelihood_breakdown[pycache only - stale]}
interferometer/{delaunay[12], mge[3], pixelized[1], rectangular[3]}
lens[1]/{critical_curves[2], deflections[7], solver[11]}      # dataset-free library components
multi_dataset/delaunay[1]
point_source_image/image_plane[9]
point_source_source/source_plane[7]
misc/  (see below)
```
- The leaf measurement names are `likelihood_breakdown`, `likelihood_runtime`, `*_numba`, `quick_update` and `hazards`.
- There are also ad-hoc experiments: `*_ab.py` A/B scripts, `fixed_light_*` (16 of the 17 files in `imaging/pixelized`), `streaming_*`, `fft_size_levers`, `gradient_mode_*` and `solver_config_sweep`.
- There is no "setup" level. Instrument and config are CLI flags.

**P `scripts/misc/`** is already grouped into subfolders (212 files):

| Folder | Files | Topic |
|---|---|---|
| `test/` | 70 | 21 fixed_light, 20 breakdown helpers, 10 tooling/catalogue/wiki, 8 hazards, 4 jax_compile, 2 vram, 2 lens/point solver, 1 wall, plus `__init__` and `browser_setup_page.cjs` |
| `likelihood_breakdown/` | 36 | see split below |
| `jax_compile/` | 14 | compile/pins/pilot/probe (its `results/` subfolder is empty) |
| `hazards/` + `hazards/checks/` | 14 + 13 | numerical-hazard scanners |
| `tooling/` | 12 | build_catalogue, dashboard, readme, setup_wiki, baseline, check_* |
| `numba_interferometer/` | 9 | numba NUFFT/inversion bake-off |
| `simulators/` | 8 | |
| `delaunay_nn/` | 5 | |
| `likelihood_runtime/` | 4 | sweep and aggregate |
| `vram/` | 4 | |
| `wall/` | 4 | |
| `latent/` | 3 | |
| `nnls_warm_start/` | 3 | |
| `pipeline_resume/` | 2 | |
| `cell_builders/` | 1 | |
| `quick_update/` | 1 | README only |
| `searches/` | 0 | pycache only, orphaned |

The 36 files in `likelihood_breakdown/` split by topic:
- **fixed_light CPU kernels/solvers (12):** `fixed_light_{cpu_common, cpu_kernels, draws_steps, numba_draws_steps, numba_memo_policy_steps, numba_scaling_steps, numpy_kernels, numpy_solvers, probe_cpu, s4b_checks, scaling_table, system}`
- **Step decompositions (4):** `active_set_steps`, `matrix_free_steps`, `reconstruction_steps`, `sparse_steps`
- **Injection A/Bs (3):** `library_solver_injection`, `logdet_reuse_injection`, `psf_cube_injection`
- **Statistics/gates (7):** `ab_verdict`, `overhead_verdict`, `family_gates`, `interval_gates`, `warmup_gate`, `round_bootstrap`, `size_sweep_table`
- **Attribution/accounting (6):** `call_accounting`, `xla_attribution`, `host_callback_probe`, `nautilus_batches`, `timing`, `provenance`
- **Interferometer (2):** `interferometer_pixelized`, `interferometer_pixelized_numpy`
- **README and `__init__` (2)**

**I**: 19 non-misc files and 35 misc files. The scheme is **dataset → model family (rectangular / delaunay / simple) or task (slam / searches) → leaf**.
```
imaging/{delaunay[5], rectangular[5]}           # baseline_slam, emcee, nautilus, nuts, smc
imaging/{searches[1], slam[1]}                  # README only
interferometer/{searches[1], slam[1]}           # README only
point_source/{simple[3], searches[1], slam[1]}  # baseline, multi_start_adam, multi_start_adam_n3000
misc[2]/{experiments[3], searches[2], simulators[4], slam[2], test[15], tooling[3], wall[4]}
```
- The two misc-root files are one-off migrations: `flatten_cleanslate.py` and `rename_light_fixed.py`.
- `misc/experiments` holds `prepared`, `run` and `wave`.
- The shared runners are `misc/slam/_runner.py` and `misc/searches/_point_runner.py`.

## 2. `results/` trees

**P `results/`**: 326 MB in total, 1456 of 1473 files tracked.

| Directory | Files | Size |
|---|---|---|
| `breakdown/` | 971 | 134M |
| ↳ `imaging` (flat) | 625 | 103M |
| ↳ `interferometer` | 247 | 17M |
| ↳ `point_source_image` | 52 | 8.6M |
| ↳ `point_source_source` | 28 | 5.0M |
| ↳ `cluster` | 12 | 652K |
| ↳ `datacube` | 7 | 296K |
| `lens/` | 100 | 176M |
| ↳ `solver` (corpus/ alone is 165M) | 69 | 173M |
| ↳ `deflections` | 28 | 1.2M |
| ↳ `critical_curves` | 3 | 1.9M |
| `runtime/` | 133 | 1.6M |
| ↳ `imaging` | 94 | 784K |
| ↳ `interferometer` | 22 | 424K |
| ↳ `point_source_source` | 9 | 224K |
| ↳ `datacube` | 5 | 40K |
| ↳ `point_source_image` | 2 | 80K |
| ↳ `multi_dataset` | 1 | 8K |
| `notes/` (56 ledgers + 2 frozen packs) | 68 | 2.0M |
| `simulators/` | 35 | 2.1M |
| `nnls_warm_start/` | 34 | 4.8M |
| `hazards/{component, likelihood, matrix}` | 29 | 1.6M |
| `logs/{point_source_image, point_source_source}` | 24 | 484K |
| `streaming_scaling/` | 20 | 768K |
| `likelihood/{datacube, imaging, interferometer, point_source}` | 14 | 600K |
| `baselines/PreOptimizationTimes` | 13 | 148K |
| `delaunay_nn/` | 9 | 588K |
| `misc/fixed_light_probe` | 6 | 824K |
| `quick_update/` | 5 | 24K |
| `parallel_scaling/imaging` | 4 | 292K |
| `sweep/` | 4 | 36K |
| `pipeline_resume/` | 2 | 112K |
| `README.md`, `provenance_grandfathered.txt` (46K) | | |

**How P `results/` fails to mirror `scripts/`:**
- **Top level is mixed.** It is split by measurement (`runtime`, `breakdown`, `hazards`, `lens`), by tool (`delaunay_nn`, `nnls_warm_start`, `quick_update`, `pipeline_resume`, `parallel_scaling`, `streaming_scaling`, `sweep`, `misc`), and by kind (`notes`, `logs`, `baselines`).
- **Model names are legacy.** Results use `pixelization`, `pixelization_numba`, `delaunay_numba` and `mge_mass_jax` where scripts use `rectangular/` and `*_numba.py`. `catalogue/registry.json` `model_aliases` bridges them, and `_script_routes.py:57-65` maps `rectangular` back to `pixelization`.
- **`breakdown/imaging/` is completely flat (625 files):** 451 `fixed_light_*`, 98 `delaunay*`, 44 `pixelization*`, 18 `matrix_free*`, 8 `mge*`, plus job-id sidecars. `breakdown/interferometer/` instead has per-instrument subdirs (`alma_high`, `jvla`, `sdp81`, `sma`, `n_sweep`) and 120 loose files.
- **`runtime/` mixes depths.** Some runs sit at model level (`runtime/imaging/delaunay/delaunay_hpc_a100_fp64.json`), others at instrument level (`…/delaunay/hst/comparison.json`). There are also odd folders: `a100_logs`, `a100_probes`, `stdout_captures`.
- **Dates and controls live in suffixes:** `_constant_split_2026_09_05`, `_control_2026_09_07`, `_lever1`, `_chunk1024`, `_n3000`, `_r2.0`, `_t8`, `local_rtx2060_mp`, `_job350651`.

**P naming conventions**, all defined in `results/README.md`:
- **Versioned summary** (`results/README.md:81-82`): `<cell>_<purpose>_<instrument>_v<YYYY.M.D.PATCH>[_sparse].json/png`, where purpose is `summary` or `breakdown`.
- **Sweep** (`results/README.md:89-96`): `runtime/<class>/<model>[/<instrument>]/<config_name>[_sparse].json` plus `comparison.json`. "Each cell dir holds the *latest* sweep" (line 89) — overwrite-in-place is the only "latest" semantics.
- **Config grammar** (`scripts/misc/tooling/build_dashboard.py:138-142`): `local_cpu_fp64|local_cpu_mp|local_gpu_fp64|local_gpu_mp|hpc_ral_cpu_fp64|hpc_a100_fp64|hpc_a100_mp` plus `_sparse`. This is `<tier>_<device>_<precision>`, parsed at `build_dashboard.py:871-879`.
- **Output path** (`_profile_cli.py:736-790`): `<cell>_<config_name>[_n<N>][_sparse][_rtu]`.

**How a P result ties to its script:**
- Only by the filename's leading cell token (the legacy stem; `_script_routes.legacy_stem`, `_script_routes.py:46`), plus the catalogue's `evidence.path` and `method.id`.
- Result JSONs carry a provenance block at `device.provenance` (`results/README.md` artefact policy, rule 5) with revisions and host but **no script path**. The only `"script"` field in the tree is in `lens/solver/corpus/manifest.json`.

**I `results/`**: 5.1 MB in total.

| Directory | Files | Size | Tracked? |
|---|---|---|---|
| `archive/` (3 dated dirs) | 58 | 2.0M | 2 of 3 |
| `searches/point_source/{multi_start_adam, multi_start_adam_n3000, nautilus}` | 53 | 1.3M | yes |
| `slam/imaging/hst` | 41 | 1.5M | **no** (only `.gitkeep`) |
| `logs/point_source` (job 367140) | 8 | 104K | yes |
| `simulators/` | 4 | 220K | yes |

The I layout is `results/<task>/<dataset>/<instrument or sampler>/<variant>/<config_name>/{stages|search}_seed<N>.json`. It does not mirror `scripts/<dataset>/<model>/`:
- It leads with the task (`slam`/`searches`).
- It uses an instrument level, which scripts do not have.
- It uses variant names (`slam_base` means rectangular).

The result → setup binding is a heuristic, `setup_id()` at `scripts/misc/tooling/inference_catalogue.py:22-42`, based on variant/mesh. There is no script path in the rows.

## 3. `wiki/` trees

**P `wiki/`** (647 files, 13M):
```
README.md, index.md
campaigns/ [28 = 27 campaigns + _template]
research/  [1]   jacobi_a100_batched_divergence.md
setups/    [616] index.md, findings.md + 8 datasets:
  cluster[10]{image_plane, source_plane}   datacube[7]{delaunay}   experiments[7]{mge}
  imaging[356]{delaunay 101, delaunay_matern 13, delaunay_nn 42, knn 12, mge 57, other 27, rectangular 103}
  interferometer[204]{delaunay 53, delaunay_hilbert_1500 10, mge 25, rectangular 49,
                      rectangular_adapt_image_32x32 7, streaming 59}
  multi_dataset[10]{delaunay, mge}   point_source_image[8]{image_plane}
  point_source_source[12]{other, source_plane}
```
- **What partly mirrors `scripts/`:** `setups/` follows dataset → model. It is generated by `build_setup_wiki.py` ("do not edit"), with an instrument level inside each `index.md`. Leaf pages are 20-hex hash IDs, one per exact configuration.
- **Where its model names diverge from `scripts/`:** `delaunay_matern`, `knn`, `other`, `streaming`, `rectangular_adapt_image_32x32`, `delaunay_hilbert_1500`, `experiments`. It also has no `lens/` family.
- **What does not mirror:** `campaigns/` (flat, by topic), `research/`, and `index.md`. The campaign index is one row per campaign, with a **`Superseded-by`** column at `wiki/index.md:16,30`. Five rows are filled: Fixed lens light → HST GPU residue; Numba interferometer revisit → Interferometer likelihood; DelaunayNN A100 → A100 pixelized baseline; Numpy deflections → Gaussian deflections precompute; PreOptimization baseline → DelaunayNN A100.
- **Campaign statuses:** 13 complete, 8 open, 3 draft, 2 parked, 1 no-go (status vocabulary at `wiki/README.md:21-40`).

**I `wiki/`** (5 files, 72K):
- `project/` holds `state.md` (the Cortex ledger) and `_template.md`.
- `setups/` holds `delaunay.md`, `rectangular.md` and `point_source.md`. These are keyed by setup family, not by script path.

**Existing `archive/` directories:** only `I/results/archive/`, with three dated folders: `2026-09-24_pre_likelihood_speedup/`, `2026-09-24_superseded_by_cleanslate/` and `2026-10-19_numba_thread_oversubscription/`. Each mirrors the `slam/imaging/hst/<variant>/<config>/` layout; the last also contains `prepared/`. P has no archive directory. "Archive" there is a catalogue concept: unreviewed legacy evidence (`wiki/setups/index.md:8`, `catalogue/README.md:45,102`). P also has frozen `results/baselines/` and two frozen evidence packs in `notes/`.

## 4. The summary contracts

**`profiling-summary` v1**, defined in `P/dashboard/README.md:21-92` and in code at `scripts/misc/tooling/build_dashboard.py:117-125`:
```
SUMMARY_SCHEMA = "profiling-summary"; SUMMARY_VERSION = 1; SUMMARY_PROJECT = "autolens_profiling"; SUMMARY_SCOPE = "release-runtime"; DRIFT_POLICY = "runtime-drift-2x-1ms"
```
- **Envelope** (`README:32-46`): `schema`, `version`, `project`, `scope`, `generated_at`, `evidence_updated_at`, `valid_until` (always null), `producer_revision`, `comparison_policy`, `coverage.{expected, observed, excluded}`, `records`, `comparisons`, `limitations`.
- **Record id** (`README:50`): `<series key>@<library version>`, e.g. `runtime:imaging/delaunay/hst:hpc_a100_fp64@2026.9.27.1`.
- **Record identity axes** (`README:58-60`): `section`, `cell`, `config`, `sparse`, and `tier`/`device`/`precision` parsed from the config label (null plus a reason if outside the grammar). Also `backend`, `library_version`, `release_date`.
- **Provenance** (`README:61-63`): `host`, `job`, `loadavg`, `has_provenance`, `qualified`, `reason`. Only `hpc_*` rows can be qualified (`build_dashboard.py:73`, `REFERENCE_HOST_CLASS_PREFIXES = ("hpc_",)`).
- **Comparisons** (`README:69-80`): `status` ∈ `drifted | improved | flat | insufficient`.
- **Change rule** (`README:91-92`): adding a field is allowed in v1; changing a field's meaning bumps the version.

**`profiling-summary` v2 catalogue** (`P/dashboard/catalogue.json` plus shards, documented in `catalogue/README.md:51-61`):
- Keys include `setups` (584), `records` (112), `selections` (105), `planned_cells` (435, all `status: not_measured`), `recommendations` (5), `evidence_shards`, `archive_record_count`, `script_routes`.
- The setup ID is dataset → model → instrument → exact configuration (`README:3-4`).
- **"Selected/current" semantics:** `references` "select supported metrics … as **unreviewed candidates**… no latest/fastest fallback exists" (`catalogue/README.md:33-35`). The registry has exactly 3 references (two `delaunay_hpc_a100_fp64` artifacts and one streaming row). "No acceptance, temporal comparisons, drift score or current-performance assertion is produced" (`catalogue/README.md:85`).
- **Registry** (`catalogue/registry.json`, schema `profiling-catalogue-registry` v1):
  - `families` (9), `model_aliases`, `model_patterns`, `sources`, `overrides`
  - `cells` (29), `devices` (`cpu`, `gpu`, `a100`), `slots` (5 axes: runtime, breakdown, compile, host RSS, device peak)
  - `references`, `hazard_bindings`, `hazard_discovery`, `recommendations`
- **Draft baseline campaign** (`P/baseline/campaign.json`, `profiling-baseline-campaign` v1, `status: "draft"`): 29 cells × {cpu, gpu, a100} × {fp64, mixed} × 6 measurements = 1,044 slots (`baseline/README.md:28-30`).

**`inference-summary` v1 and v2:**
- Documented at `I/INFERENCE_SUMMARY.md:3-4` ("schema `inference-summary`, version 1"); code at `scripts/misc/tooling/export_inference_summary.py:300-301`. The catalogue is v2 (`inference_catalogue.py:47`, `README.md:140`).
- **Envelope** (`export_inference_summary.py:299-337`): `source_commit`, `producer_revision`, `generated_at`, `evidence_updated_at` (null), `coverage.observed.archived_records`.
- **Comparison policy:** `comparison_policy.id = "declared-target-seed-stage-v1"`, `ranking: "none"`, "no automatic parity certification or best-seed selection".
- **Record fields** (`export_inference_summary.py:119-222`):
  - `id` (path, or `path#stage-<hash>`), `parent_run_id`, `stage`, `target`, `dataset.{class, instrument, id}`, `model`, `pipeline`, `sampler`
  - `configuration` (the `CONFIG` tuple at lines 50-84: `config_name`, `variant`, `inversion`, `mesh`, `regularization`, `lens_light_mode`, `release_pin`, `stages_from`, `shared_from_config`, `fitted_backend`, …)
  - `backend`, `hardware`, `precision`, `seed`, `library_version`
  - `execution.status`, `scientific.{convergence, acceptance} = "not_assessed"`
  - `timings.{setup_s, sampling_s, total_s, compile_s}`
  - **`archived`** (line 221: true when the path starts with `archive/`, lines 266 and 284)
- **Docs on archive and acceptance:** "archived results are included with `archived: true`; they are not current baselines" (`INFERENCE_SUMMARY.md:15-16`), and "no … winner or best seed is invented" (`:25-26`).
- **v2 setups** (`inference_catalogue.py:8-12, 49-57`): `imaging/rectangular/hst`, `imaging/delaunay/hst`, `point_source/simple/simple`, each with `reference_record_id = None`, `reason = "No explicitly accepted current baseline…"`.
- **Config grammar** (`I/AGENTS.md:98`): `{local,hpc_a100,hpc_ral}_{jax_cpu,numba_cpu,jax_gpu}_{dense,sparse}_{fp64,mp}`, i.e. where × backend × inversion(operator) × precision. Caveat at `AGENTS.md:102-104`: older CPU rows carry `hpc_a100` even though they ran on CPU.
- **Grammar mismatch between repos:** P is `<tier>_<device>_<precision>[_sparse]`; I is `<where>_<backend>_<inversion>_<precision>`.

## 5. I run directories

`slam/imaging/hst/<variant>/<config>/stages_seed{0,1}.{json,png}`, all untracked:

| Variant | Config dirs (file count) |
|---|---|
| `slam_base` | `hpc_a100_jax_cpu_dense_fp64` (4), `hpc_a100_jax_cpu_sparse_fp64` (2, seed0 only), `hpc_a100_jax_gpu_dense_fp64` (4), `hpc_a100_jax_gpu_sparse_fp64` (4), `hpc_ral_numba_cpu_sparse_fp64` (4) |
| `slam_base_light_fixed` | same 5 configs; `hpc_a100_jax_cpu_sparse_fp64` is **empty** |
| `slam_delaunay` | `hpc_ral_numba_cpu_sparse_fp64` (3) |
| `slam_delaunay_light_fixed` | `hpc_ral_numba_cpu_sparse_fp64` (3) |

- **Searches:** `searches/point_source/{multi_start_adam, multi_start_adam_n3000, nautilus}/simple/source_plane_solved/{hpc_a100_jax_cpu_dense_fp64, hpc_a100_jax_gpu_dense_fp64, local_jax_cpu_dense_fp64}/search_seed0-4`.
- **Archive:** the archive dirs use older names: `delaunay_1250/` instead of `slam_delaunay`, `hpc_a100_numba_cpu_*`, and `hpc_a100_jax_gpu_dense_fp64__rate_probe_342695`.
- **Names do encode the setup.** The config folder name equals the row's `config_name`. A row also stores `backend`, `inversion`, `precision`, `variant`, `release_pin`, `slurm_job_id`, `chain_wall_s` and per-stage `wall_s`, `likelihood_evals` and `log_evidence` (checked in `slam_base/hpc_ral_numba_cpu_sparse_fp64/stages_seed0.json`).

**What the runs measured:**
- **SLaM rows** are the backend-parity "base run": the same target and seed across configs, compared on posterior, `log_evidence` and wall (`wiki/project/state.md:7-22`; README parity view at `README.md:107-113`).
- **Search rows** compare samplers on the point-source problem: Nautilus vs MultiStartAdam with a 300-step and a 3000-step ceiling. Columns include an "estimated likelihood share" of wall (`state.md:364-376`, `README.md:72-99`).
- **None of it validates wall time against autolens_profiling estimates.** `misc/wall` only gates SLURM `--time` from rates measured in this repo (`scripts/misc/wall/README.md:3-6`).
- `README.md:66` still says "No pipeline runs yet". That matches the SLaM rows being uncommitted.

**`INFERENCE_SUMMARY.md` in five lines:**
1. PyAutoInsight reads `dashboard/summary.json` (`inference-summary@1`), produced by a standard-library-only exporter with `--check`.
2. The generation time is a commit timestamp, not measurement freshness, so `evidence_updated_at` is null.
3. It scans all `results/searches` and `results/slam` rows, including failed ones; archived rows are flagged `archived: true` and are not baselines.
4. Pipelines have parent and stage records; convergence and acceptance stay `not_assessed`, and there is no winner or best seed.
5. It defines the clocks `setup_s` (null), `sampling_s` (`wall_s`), `total_s` (`total_wall_s`) and `compile_s` (separate). Publishing sends `insight-refresh`.

**`CORTEX.md` in five lines:**
1. Rulings of record live in PyAutoCortex `projects.yaml`, row `autolens_inference`.
2. Campaign intent and pending tasks live in PyAutoInsight (`CHECKIN.md`); PyAutoMind keeps implementation issues.
3. The authoritative run ledger is `PyAutoCortex/projects/autolens_inference.md`; `wiki/project/state.md` is commentary.
4. `PyAutoCortex/archive/` holds frozen tasks and rulings; the old `tasks/` and `rulings/` workflow is retired.
5. "Nothing is inherited": the repo was born 2026-09-10 as a restart of `inference_programme`, and only numbers measured in this repo count.

## 6. Large and ignored directories

| Repo | Directory | Size | Status |
|---|---|---|---|
| P | `output/` | 8K (only `trace/`) | ignored |
| P | `dataset/` | 396M | partly ignored; 45 files tracked |
| P | `baseline/` | 40K | tracked, small: README plus `campaign.json` |
| P | `dashboard/` | 48M | tracked (`catalogue/` shards are 45M) |
| P | `results/lens/solver/corpus` | 165M | tracked |
| P | `dataset/abell_1201/` | | untracked |
| I | `output/` | 3.9G | ignored; a symlink to `/mnt/c/Users/Jammy/Science/inference` |
| I | `logs/` | 35M (cpu 11M, gpu 25M) | ignored |
| I | `prepared/` | 84K, 7 hash dirs | untracked |
| I | `dataset/` | 180K | |
| I | `dashboard/` | 2.2M | |

P's largest ignored `dataset/` items are `cluster/` (31M) and `interferometer/alma/preload_inputs_*.npz` (33M).

## 7. "Optimal" / "recommended" / "decision rule" in the wikis

The grep finds 5 files in P and none in I:

| File | Title | Match |
|---|---|---|
| `wiki/README.md:27` | Profiling research wiki | the `Pre-registered rule` header contract |
| `wiki/campaigns/linear_solver_accuracy.md:94` | Linear-solver accuracy | the decision rule committed at `327f571` |
| `wiki/campaigns/delaunay_nn_a100_series.md:59,72` | DelaunayNN A100 series | "probe-recommended batch" |
| `wiki/campaigns/reference_notes.md:22` | Reference notes | "PDIP … near-optimal" |
| `wiki/campaigns/_template.md` | template | |

Related decision content outside that grep:
- Every campaign page carries `**Pre-registered rule:**` and `**Verdict:**` lines.
- All 584 generated setup pages have a `## Recommendations` section. 574 say no evidence is bound; 10 link to the catalogue's 5 historical interferometer recommendations (4 delaunay, 2 mge, 4 rectangular pages).
- Those 5 recommendations come from the interferometer decision matrix (`results/notes/interferometer_likelihood_decision_matrix_2026_09.md`), which says which path and device to use by N_vis × mask × source. It is cited from `results/README.md`, and `catalogue/README.md:155-162` frames it as **unreviewed** historical rules.
- I's wiki has no recommendations. Its setup pages say "No selected reference is declared" (`wiki/setups/rectangular.md`).
