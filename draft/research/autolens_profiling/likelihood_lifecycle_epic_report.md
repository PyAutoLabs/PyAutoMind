# Likelihood lifecycle epic — research report and phased plan

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: evidence record for the likelihood-lifecycle epic — never issued; read it from the epic ledger
Consequence: glance
Review-minutes: 0
Unattended: never
Epic: likelihood-lifecycle
Filed: 2026-10-21

Written: 2026-10-21 by the Fable 5.1 (xhigh) architect session from five read-only Explore surveys in `likelihood_lifecycle_epic_surveys/` (01 profiling/inference layout, 02 Pulse/Insight contracts, 03 Eyes/viz coverage, 04 source setup knobs, 05 Brain conductors and epic format). No code was edited. The ledger and phase cards are in `likelihood_lifecycle_epic.md`; this file holds the evidence, the critique, the architecture and the detailed phase bodies. Cite the surveys (`surveys/NN §x`) rather than re-surveying.

## 0. Summary

The four projects already exist and already have boundaries that fit the ask: `autolens_profiling` measures likelihood cost and publishes `profiling-summary` to PyAutoPulse; `autolens_inference` runs full fits and publishes `inference-summary` to PyAutoInsight; Pulse and Insight validate contracts and render declarations, judge nothing, and the Brain's profiling conductor is the only judge of timing. What is missing is **one vocabulary and one lifecycle** shared by all four, and the data to drive a library-side automatic setup choice:

1. **No notion of "current" or "optimal" exists anywhere.** Pulse has 584 setups, 112 selected records and 20,999 archived ones, all `unreviewed`, and no field that says which record is live (`surveys/02 §1`). autolens_profiling has no marker either; "latest" means overwrite-in-place (`surveys/01 §2`). Insight has an `archived` flag but every `reference_record_id` is null.
2. **The two project repos disagree on grammar and structure.** Profiling names a setup `<tier>_<device>_<precision>[_sparse]`, inference names it `<where>_<backend>_<inversion>_<precision>`; profiling's `results/` is the inverse of its `scripts/` tree (measurement first, 625 flat files under `breakdown/imaging`); inference's current clean-slate SLaM rows are untracked (`surveys/01 §1–§2, §5`).
3. **Nothing in the stack chooses the compute setup from hardware or data.** `use_jax`, the sparse operator and its type, `number_of_cores`, precision and the interferometer transformer are each set by hand, with defaults that differ by layer; science projects carry `--use_cpu` argparse blocks; the only hardware-aware choices are the interferometer numba-vs-FFT cost model and the Sibson unroll (`surveys/04 §1`). The one place environment variables can be set before JAX imports is `autonerves.jax_wrapper` (`surveys/04 §3`).
4. **Eyes already covers all ten dataset types** (autolens_visualization PR #5, merged 2026-10-21, 72 figures), so the Eyes phase shrinks to human sign-off, bespoke figures, and a fit-figure step inside profiling campaigns, which currently render fit subplots into a tempdir and discard them (`surveys/03`).
5. **The lifecycle is not encoded.** The pieces exist (profile_likelihood skill, profiling conductor, Pulse gradient_cost_probe task, sampler_pipeline skill, samplers faculty, Insight), but no conductor or skill chains likelihood → profile → Pulse → validate → gradient → sampler (`surveys/05 §4`). Insight forbids an inference conductor, so the chain is a profiling-conductor verb that files Mind prompts.

The plan is nine phases. Phase 0 builds the spine (vocabulary, `profiling-summary@3` with `class`/`status`, mirrored results trees, day-zero history cut, Insight `setup_mode: auto`); phases 1–4 collect the evidence (figures, profiling campaigns, the day-zero freeze, inference wall-time validation); phase 5 bakes the result into the source as `setup="auto"` with a banner, `setup.json` and a run-time estimate; phases 6–7 add gradient breakdowns and the sampler campaign; phase 8 turns the sequence into `pyauto-brain profiling lifecycle` so a new or re-optimised likelihood re-runs the chain from one command.

## 1. Research findings

### 1.1 The four projects today (`surveys/01`, `surveys/02`)

| | autolens_profiling | PyAutoPulse | autolens_inference | PyAutoInsight |
|---|---|---|---|---|
| Role | measures per-evaluation likelihood cost (runtime, breakdown, compile, memory, hazards) | validates `profiling-summary`, renders, records human decisions; never judges | runs full fits (SLaM, searches); parity base runs and sampler comparisons | validates `inference-summary`, renders; no conductor, no acceptance |
| Contract | `profiling-summary` v1 (dashboard) + v2 catalogue (584 setups / 112 records / 21k archive) | supports @1, @2; registry pins `lens`/`fit` at @2 | `inference-summary` v1 export, v2 catalogue; `fit` instance at @3 | supports @1–@3 |
| "Current" | none; overwrite-in-place; wiki campaign index has `Superseded-by` | none; `role` is a JS ranking nudge; all records `unreviewed` | `archived` flag by path prefix; `reference_record_id` null | renders `archived` separately |
| Setup grammar | `<tier>_<device>_<precision>[_sparse]` | validates the producer's `configuration{}` | `<where>_<backend>_<inversion>_<precision>` | setup IDs `dataset/model/instrument` exclude compute setup |
| Tree | `scripts/<dataset>/<variant>/<measurement>.py` but `results/<measurement>/<dataset>/flat`; `wiki/campaigns` flat; no archive | — | `results/<task>/<dataset>/<instrument>/<variant>/<config>/`; `results/archive/<date>_<slug>/` | — |
| Open ledgers | #436 cluster robust PointSolver, #166 log_det default, #128 MGE NaN lanes, #103 warm-compile, #50 lint | #62 interferometer large-mask anchor (open issue), PR #68 post-/prm links (unmerged, rebase after) | #4 project ledger, PR #30 docs | none |
| Stalled | `baseline/campaign.json` draft: 29 cells × 3 devices × 2 precisions × 6 measurements = 1,044 slots | `setup-baseline` campaign `needs-decision` since 2026-10-06 with six recorded unknowns | clean-slate rows (10-17) uncommitted; `README.md:66` says "No pipeline runs yet" | `hst-imaging-mass-samplers` needs-decision; wave 1 attempt 2 unsubmitted |

What the inference runs so far measured (`surveys/01 §5`): the SLaM rows are backend-parity base runs (same target and seed across five configs, compared on posterior, `log_evidence` and wall); the search rows compare Nautilus vs MultiStartAdam on the point-source problem. Nothing compares wall time against the Pulse per-evaluation estimates, and `misc/wall` only gates SLURM `--time`. The human's reading is right: these are validation data for Pulse, not sampler comparisons for Insight.

The boundary sentences that constrain the design (`surveys/02 §3`): Pulse "never selects a latest/fastest row", "recomputes no ratio", "ranks nothing", "judges nothing"; Insight "do not create an inference conductor, select defaults or turn process completion into scientific acceptance". Everything the epic puts on a dashboard must therefore be a **producer declaration** or a **human decision record**, with the Brain's profiling conductor as the judge in between.

### 1.2 Eyes and figures (`surveys/03`)

Every one of the ten dataset types has a `fit.png` in `lens/autolens_visualization/gallery/viz_manifest.yaml` (imaging and interferometer have the full figure set plus parametric and Delaunay variants; the other eight have dataset + fit only). Only `imaging/hst` is shared byte-for-byte with autolens_profiling; the other viz datasets are separate seeded simulations. The two Eyes drafts (`multi_galaxy_gallery.md`, `group_cluster_gallery.md`) are largely superseded by PR #5 and should be re-scoped to what is left: group point-source, cluster extended and image-plane chi², bespoke point/cluster/weak figures. Profiling has no written fit-figure inspection step at all; `quick_update.py` renders `subplot_fit_quick` into `tempfile.mkdtemp` and throws it away.

### 1.3 The source knobs (`surveys/04`)

Twenty-odd knobs set the compute setup by hand. The ones the auto factory must own: `use_jax` (defaults True on lens/galaxy/interferometer/point analyses, False on base `af.Analysis` and weak), `Imaging.apply_sparse_operator()` (JAX) vs `apply_sparse_operator_cpu()` (numba), `Interferometer.apply_sparse_operator(method=, use_jax=)`, `transformer_class` (DFT vs NUFFT, guard only above 10,000 visibilities), `Settings.use_mixed_precision`, `Settings.interferometer_route` and the numba-vs-FFT cost model, `SettingsSearch.number_of_cores` (forced to 1 under JAX by the fork rule; nothing reads `cpu_count` or `SLURM_CPUS_PER_TASK`), and the thread variables (`OMP/MKL/OPENBLAS_NUM_THREADS`, warned about, never set; `NUMBA_NUM_THREADS` never read). Environment is set at import by `autonerves.jax_wrapper` (`XLA_FLAGS`, `JAX_ENABLE_X64`, compile cache) but `JAX_PLATFORMS` is left to batch scripts. Two facts fix the layering: env vars must be set before JAX initialises (Nerves), and dataset-dependent choices cannot live in Nerves (PyAutoArray/PyAutoLens). The CLI announces only "Starting non-linear search with JAX (GPU: …)" or "with N cores"; nothing reports operator, route, transformer or precision. Two stale claims to retire: `apply_over_sampling` no longer drops the sparse operator (PyAutoArray db94e80a, 2026-09-27), and the "JAX: Applying vmap and jit" log line no longer exists.

### 1.4 Brain, Mind and the existing tasks to adopt (`surveys/05`)

Epics are filed as `<name>_epic.md` (ledger) + `_report.md` (this file) + `_surveys/`, with an `epics.md` entry, and phase prompts filed lazily with `Epic:` plus an **integer** `Phase:` (non-integers sort last). The intake conductor does not split epics; "too-large means decompose, never dispatch", and decomposition stays with the strongest model. Existing tasks this epic adopts rather than duplicates:

- Pulse `setup-baseline` campaign and `tasks/setup_baseline_campaign.md` (→ phase 3 replaces its 1,044-slot draft manifest with the Optimal/Secondary matrix).
- Pulse `tasks/gradient_cost_probe.md` (→ phase 6), `tasks/search_settings_estimation_infrastructure.md` (→ phase 5 estimator), `tasks/hst_mge_cpu_pilot.md` (→ phase 2 imaging/mge CPU cell).
- Insight `hst-imaging-mass-samplers` campaign (clean-slate base rows → phase 4; wave plan → phase 7), `tasks/gradient_sampler_validated_likelihoods.md` (→ phase 7).
- Mind `draft/research/autolens_profiling/matrix_free_interferometer_phase5.md` (→ phase 8 dogfood instance; it already says it is part of the human's profiling programme), `draft/bug/autonerves/jax_enable_x64_env_ignored_and_fp32_leg_runs_fp64.md` (→ phase 5A), `draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md` (→ phase 5H), `draft/feature/pyautoeyes/{multi_galaxy,group_cluster}_gallery.md` (→ phase 1 re-scope).
- Adjacent, not touched: `hpc-campaign` phase 4 consumes this epic's estimates (its report §8 already asks for them); `results-library` owns post-run indexing; `search-extensibility` B5c scored waves continue on `autofit_inference`.

## 2. Critique of the asks

Taken as written, with these refinements:

1. **"Only the most recent results" → "exactly one current record per key".** Recency by date is the wrong rule: a laptop run last week must not displace an A100 run from the pinned release. Current is defined per (likelihood, instrument, setup, host class, model variant, measurement) as the record the producer declares current, normally the most recent one measured on the pinned release and a reference host. Superseded records stay in the tree (collapsed under History); archived ones move to `archive/`.
2. **Eyes phase is already shipped** (§1.2). Phase 1 is sign-off plus the profiling-side figure step. Keeping the figure next to the timing record is what makes a profiled likelihood inspectable later, so `profiling-summary@3` gets a `figures[]` field and Pulse links it; Eyes stays the judge of figure quality.
3. **The "true sampler campaign" is an Insight campaign, not a Pulse one.** Pulse is per-evaluation cost; Insight is which sampler finds the right answer fastest. The ask says "PyAutoPulse campaign to try different samplers"; the plan reads that as Insight (phase 7), with the per-evaluation gradient cost staying on Pulse (phase 6).
4. **"Insight assumes the optimal setup on GPU" → `setup_mode: auto`.** For most likelihoods auto resolves to the A100 setup. For point-source source-plane and weak lensing the evaluation is so cheap that CPU is optimal (GPU warm-up dominates), so the honest statement is "Insight runs under auto, which is GPU wherever GPU is the designated optimum", and every record carries `setup_resolved` as provenance. Folder names stop encoding the setup (`…/<sampler>/auto/seed_<n>`); an explicit override is allowed only for a parity leg and is named `explicit/<setup_id>/`.
5. **`_fixed_light` becomes `model_variant: light_fixed`**, run only under the Optimal class. The same field carries future model-side variations (MGE vs Sérsic lens light, mass model family) without new grammar.
6. **The stalled `setup-baseline` protocol is replaced, not resumed.** Its six unknowns (frozen revisions, environment lock, hardware identity, per-cell settings and witnesses, compile builder, precision coverage) are answered pragmatically by the day-zero rule in §3.6: pin = a released tag; environment = the RAL shared venv recorded by PyAutoDNA receipts; hosts = `hpc_ral_cpu` and `hpc_a100` only; settings = the script plus dataset hash; witness = parity against a reference log-likelihood plus the fit figure; compile is **not** an axis of the Optimal class (the per-cell compile builder is unavailable); mixed precision is `experimental` until the x64 bug is fixed.
7. **"Does auto do everything?" No.** Auto owns implementation choices with no scientific content (backend, device, operator, precision, transformer/route, threads, default cores). It never touches the model, the pixelization mesh or resolution, over-sampling, regularisation, the sampler or its settings, or the HPC resource request. §3.4 gives the per-likelihood table; the SLaM problem is solved by resolving one setup at pipeline start and threading it, not by re-applying per stage.
8. **A Brain "feature agent" for the sequence → a `lifecycle` verb on the profiling conductor.** Insight forbids an inference conductor and the feature conductor phases features generically. The profiling conductor already diffs grids against results and emits dispatch plans; a `lifecycle` verb that emits the Mind epic and phase prompts for a named likelihood is the smallest honest extension. Intake files the prompts; the sampler stage is routed through the existing sampler_pipeline skill and samplers faculty.
9. **Archive scheme.** `archive/YYYY/MM/<slug>/` at the repo root in both project repos, as the ask suggests; autolens_inference's three `results/archive/<date>_<slug>/` directories are re-homed into it so there is one scheme. Nothing is deleted; `git mv` keeps history.
10. **multi_galaxy, group and cluster at standard size only**, as asked. The `regime` field exists from day zero with a single `standard` bin for those types, so the size dimension is added later as new bins, not new grammar.

## 3. Architecture

### 3.1 Vocabulary (the taxonomy every project and the library share)

| Term | Definition | Values / grammar |
|---|---|---|
| **dataset_type** | the PyAutoLens dataset family | `imaging`, `interferometer`, `datacube`, `point_source_image`, `point_source_source`, `multi_galaxy`, `group`, `cluster`, `multi_dataset`, `weak` (the 10 types; mirrors `scripts/<dataset_type>/`) |
| **likelihood variant** | the likelihood evaluated for that type | `sersic`, `mge`, `mge_mass`, `rectangular`, `delaunay`, `delaunay_nn`, `image_plane`, `source_plane`, … (mirrors `scripts/<dataset_type>/<variant>/`; legacy `pixelized`/`pixelization` retired) |
| **likelihood** | `<dataset_type>/<variant>` | e.g. `imaging/delaunay`, `interferometer/mge`, `cluster/source_plane` |
| **instrument** | a concrete dataset instance with size descriptors | `hst`, `euclid`, `jwst`, `sma`, `alma`, `jvla`, `simple`, … with `n_pixels_masked`, `n_vis`, `n_channels`, `n_galaxies`, `n_sources` |
| **regime** | the named size bin a rule branches on | per dataset type, declared in the contract (e.g. interferometer `n_vis_lt_1e5`, `n_vis_1e5_1e7`, `n_vis_ge_1e7`); `standard` where a type has one bin |
| **setup** | the compute configuration tuple | `backend` ∈ {numba, jax}; `device` ∈ {cpu, gpu}; `operator` ∈ {dense, sparse, na}; `precision` ∈ {fp64, mixed}; `transformer` ∈ {dft, nufft, wtilde, streaming, na}; `threads` (int) |
| **setup_id** | canonical string | `<backend>_<device>_<operator>_<precision>[_<transformer>]`, e.g. `numba_cpu_sparse_fp64`, `jax_gpu_dense_fp64`, `jax_gpu_sparse_fp64_wtilde` (replaces both current grammars; the site/tier moves to `host_class`) |
| **host_class** | where it ran (provenance, never identity) | `hpc_ral_cpu`, `hpc_a100`, `local_laptop`, `local_gpu` (laptop rows never qualify as current, per the existing reference-host rule) |
| **model_variant** | model-side variation of the same likelihood | `default`, `light_fixed`, … ; non-default variants run only under the Optimal class |
| **measurement** | the evidence axis | `runtime` (jit likelihood), `breakdown`, `gradient` (value_and_grad), `compile`, `memory_host`, `memory_device`, `parity`, `walltime_validation` |
| **class** | the designation of a setup for a likelihood + regime + hardware class | `optimal`, `secondary`, `experimental`; declared by the producer from a Pulse designation decision; Optimal requires a `decision_id` |
| **status** | lifecycle state of a record | `current` (exactly one per key), `superseded` (kept, hidden by default, `superseded_by` set), `archived` (moved to `archive/`, counted not rendered) |
| **day_zero** | the frozen baseline tag | the released library tag + profiling commit every Optimal/Secondary current record was measured on |

Where the vocabulary lives: canonically in the Pulse contract document (`REFERENCE.md`, `profiling-summary@3` enumerations) and its validator; mirrored by the producers' catalogue builders and, from phase 5, by the library's `Setup` type, with a parity test in autolens_profiling that reads both.

### 3.2 Contracts

**`profiling-summary@3`** (Pulse; additive on v2, version bumped because `status`/`class` change what the catalogue means). Record fields added: `likelihood {dataset_type, variant}`, `instrument`, `regime`, `setup {…}` + `setup_id`, `host_class`, `model_variant`, `measurement`, `class`, `status`, `superseded_by`, `day_zero`, `figures[] {kind, path, sha256}`, `decision_id`, `release_pin`, `measured_at`. Validator rules: exactly one `current` per (likelihood, instrument, setup_id, host_class, model_variant, measurement); `class: optimal` ⇒ `decision_id` present and resolvable in `decisions.yaml`; `archived` records are excluded from `records[]` and counted in `archive_record_count`; `planned_cells` carry `class` so coverage is reported per class. Pulse renders class and status; it still computes no ratio and selects nothing.

**`walltime-validation@1`** (new Pulse evidence axis, produced by autolens_inference). Record keyed by (likelihood, instrument, setup_id, host_class, model_variant, sampler, seed): `wall_s`, `likelihood_evals`, `implied_ms_per_eval`, `reference_runtime_record_id` (the day-zero `runtime` record it is compared with), `predicted_ms_per_eval`, `ratio_measured_over_predicted`, `cores`, `parallel_efficiency` (relative to the 1-core row of the same key), `release_pin`, `slurm_job_id`, `max_log_likelihood`, `parity_status` ∈ {match, diverged, not_assessed}. All derived numbers are producer-computed and declared; Pulse renders them. The contract text says explicitly that these are full-fit measurements, so Pulse's "never interpret a per-likelihood measurement as a total-fit prediction" rule is respected in the other direction too.

**`inference-summary`** (Insight; additive, no version bump unless the validator refuses unknown keys): `setup_mode` ∈ {auto, explicit}, `setup_resolved {…}`, `setup_id`, `model_variant`. Setup IDs stay `dataset/model/instrument`. Folders: `…/<sampler>/auto/seed_<n>` or `…/<sampler>/explicit/<setup_id>/seed_<n>`.

**Pulse decision kind `designation`**: `decisions/<id>.md` + `decisions.yaml` row with `likelihood`, `regime`, `hardware_class` (cpu_many_core | gpu_a100 | laptop), `optimal: <setup_id>`, `secondary: [<setup_id>…]`, `evidence: [record ids]`, `rule` (one sentence in terms of dataset properties, per the 2026-10-16 human rule that rules are written so an agent can apply them from data alone), `supersedes`. The library rule table (§3.5) is generated from, and tested against, these records.

### 3.3 Provisional designations (to be confirmed by phases 2–3; written here so phase 0 can label existing records)

| Likelihood | GPU present (A100) | CPU many-core (RAL `ral`) | Laptop (few cores, no GPU) | Secondary | Rule branches on |
|---|---|---|---|---|---|
| imaging/sersic, imaging/mge (parametric) | `jax_gpu_dense_fp64` | `jax_cpu_dense_fp64` | `jax_cpu_dense_fp64` | — | none (`standard`) |
| imaging/rectangular, imaging/delaunay (pixelized) | `jax_gpu_dense_fp64` (`jax_gpu_sparse_fp64` secondary until the light_fixed divergence is explained) | `numba_cpu_sparse_fp64` + cores | `jax_cpu_dense_fp64` | `jax_cpu_sparse_fp64`; numba dense dropped by human decision 2026-10-18 | cores ≥ threshold (from phase 4 efficiency curve); source pixels |
| interferometer/mge | `jax_gpu_dense_fp64_<dft|nufft>` | `jax_cpu_dense_fp64_<dft|nufft>` | same | — | `n_vis × n_pix` crossover ≈ 1e7 (workspace text); DFT refused above 10,000 vis today |
| interferometer/rectangular, /delaunay | `jax_gpu_sparse_fp64_wtilde`; `streaming` at `n_vis ≥ 1e7` | per the interferometer decision matrix: numba direct_conv vs FFT cost model (symmetric gate 0.7); `streaming` at large n_vis | `jax_cpu_sparse_fp64_wtilde` | dense routes | `n_vis`, mask extent, source pixels (regimes `n_vis_lt_1e5`, `1e5_1e7`, `ge_1e7`) |
| datacube/delaunay | as interferometer per channel; GPU dense per channel within VRAM | as interferometer | as interferometer | — | `n_channels × n_vis`, VRAM |
| point_source_image/image_plane | `jax_gpu_dense_fp64` (A100 0.934 ms reference) | `jax_cpu_dense_fp64` | same | — | PointSolver settings stay explicit (cluster robust-settings campaign) |
| point_source_source/source_plane | `jax_cpu_dense_fp64` (cheap; GPU warm-up dominates) | `jax_cpu_dense_fp64` | same | `jax_gpu_dense_fp64` | none |
| multi_galaxy/*, group/* | as imaging rules | as imaging | as imaging | — | `n_galaxies` deferred (single `standard` bin) |
| cluster/source_plane (and image_plane) | as point_source_source (× n_sources) / as point_source_image | same | same | — | `n_sources` deferred |
| multi_dataset/* | as imaging; one setup for the whole analysis sum (highest regime wins) | as imaging | as imaging | — | per-dataset sizes |
| weak/* | `jax_cpu_dense_fp64` (cheap) | same | same | `jax_gpu_dense_fp64` | none |

Mixed precision is `experimental` everywhere at day zero (the fp32 leg currently runs fp64: Mind bug draft). Compile cost is recorded where available but is not a class axis.

### 3.4 The auto / explicit boundary

Auto decides, and the user never has to: **backend, device, operator, precision, transformer/route, thread environment, and the default `number_of_cores`** (from `SLURM_CPUS_PER_TASK` or CPU affinity, capped per likelihood by the phase-4 parallel-efficiency curve). The user decides, and auto never touches: **the model** (including pixelization mesh type and shape, over-sampling, regularisation), **the sampler and its settings**, **the HPC resource request** (partition, cores, GPUs: auto reads it, never writes it), and **any explicit override** (`al.Setup(...)` / `PYAUTO_SETUP=<setup_id>`), which is how a profiling leg, an A/B test or a science project forces a Secondary setup.

Per likelihood, what auto has to get right:

| Likelihood | Auto owns | Stays explicit | Notes |
|---|---|---|---|
| imaging parametric | backend/device/precision/threads | model, over-sampling, sampler | no operator; mixed precision only after validation |
| imaging pixelized | + operator (sparse numba on many-core CPU; dense JAX on GPU) + default cores | mesh type/shape, regularisation, sampler | the backend/operator consistency check lands in the inversion factory; the SLaM pipeline resolves one setup and threads it through every stage (`apply_over_sampling`/`apply_mask` keep it) |
| interferometer parametric | + transformer by `n_vis × n_pix` | model, sampler | replaces the DFT > 10,000 guard with a choice |
| interferometer pixelized | + route (direct_conv/FFT/w-tilde/streaming) by regime | mesh, sampler | the existing cost model becomes one rule among the designations |
| datacube | as interferometer, per channel, VRAM-aware | channel selection | |
| point source image-plane | backend/device | PointSolver grid/settings | solver settings are scientific until the robust-settings campaign says otherwise |
| point source source-plane, weak | backend=jax, device=cpu | model | auto may decline the GPU |
| multi_galaxy, group, cluster | as the underlying likelihood | model | one `standard` regime for now |
| multi_dataset | one setup for the summed analysis | per-dataset models | |

### 3.5 The auto factory, layered

```
PyAutoNerves   autonerves.environment.Environment.detect()
               → gpu (bool), gpu_name, gpu_memory_gb, cores (SLURM_CPUS_PER_TASK → sched_getaffinity → cpu_count),
                 ram_gb, numba, nufftax, site hint (SLURM_CLUSTER_NAME, hostname class)
               jax_wrapper honours PYAUTO_SETUP=auto|cpu|gpu|<setup_id> at import: only explicit cpu/numba intents
               set JAX_PLATFORMS=cpu and the *_NUM_THREADS variables before JAX initialises; auto sets nothing
               at import (JAX picks the GPU when present, which is the optimum wherever GPU is designated).
PyAutoArray    aa.Setup (dataclass = the §3.1 setup tuple + rule_id + regime)
               aa.Setup.auto(dataset, model, environment) — rule table config/setup_rules.yaml generated from the
               Pulse designation decisions; regimes computed from the dataset (n_pixels_masked, n_vis, …) and
               from whether the model carries a pixelization / linear light profiles
               dataset.apply_setup(setup) — attaches the right sparse operator / transformer; idempotent;
               carried by apply_over_sampling / apply_mask / apply_noise_scaling
               inversion factory: raises when operator and backend disagree (today's silent "neither" leg)
               threads at runtime: numba.set_num_threads + threadpoolctl (no env var needed post-import)
PyAutoGalaxy/  Analysis*(dataset, setup="auto") default; use_jax=... kept as an explicit override that maps to a
PyAutoLens     Setup; weak and point analyses aligned; multi-dataset sums resolve one setup; SLaM helpers accept
               a setup once; setup.json written beside the search output; two-line banner at fit start:
                 "Setup: jax/gpu/dense/fp64 (A100-SXM4-80GB) · rule imaging-pixelized-gpu · optimal (Pulse day zero 2026.11.x)"
                 "Estimate: ~1.9 ms/eval · Nautilus n_live=150 ≈ 2.1e5 evals · ~7 min on this hardware · override: PYAUTO_SETUP"
PyAutoFit      SettingsSearch(number_of_cores="auto") → setup.threads; fork rule unchanged; log_fit_start prints
               the banner; the resolved setup is stored in the search's metadata.
Estimator      al.Setup.estimate(dataset, model, search) → RuntimeEstimate(ms_per_eval, source record id,
               expected_evals (Insight table; Nautilus heuristic labelled as such until phase 7), parallel
               efficiency (phase 4), wall) — data file autolens/config/runtime_estimates.yaml regenerated by an
               autolens_profiling exporter from the Pulse day-zero snapshot and PR'd into PyAutoLens on refresh.
Assistant      al_explain_setup skill: reads setup.json + the designation rule + autolens_profiling/inference notes
               and explains the choice and the estimate; al_configure_search updated to "auto unless…".
```

Rollout: ship `setup="auto"` opt-in with the banner reporting what auto *would* choose when the user passed explicit knobs (one release), then flip the default (next release). The human may shortcut this (ruling R6).

### 3.6 Day zero

Day zero is a rule, not a date: a record is `current` and may carry `day_zero: <tag>` only if it was measured on the pinned **released** tag, on a reference host class (`hpc_ral_cpu`, `hpc_a100`), with provenance, a parity witness and (from phase 1) a fit figure. At phase 0 the history cut labels existing records without re-running anything: the 29 `planned_baseline` setups and 3 `reference_candidate` records become `current` provisional Optimal/Secondary rows where they meet the host rule; other records on the mirrored keys become `superseded`; dead experiments (dated suffixes, `_lever`, `_probe`, pre-2026-09 series) move to `archive/`. Phase 3 then re-measures whatever is not on the day-zero tag and stamps the baseline; Pulse snapshots it as `day_zero`.

### 3.7 Repository layouts after phase 0

autolens_profiling (`results/` mirrors `scripts/`; archive at the root):
```
scripts/<dataset_type>/<variant>/{likelihood_runtime,likelihood_breakdown,gradient_breakdown,quick_update,hazards}.py
scripts/lens/{solver,deflections,critical_curves}/…        scripts/misc/<group>/…  (groups as today, test/ split by group)
results/<dataset_type>/<variant>/<instrument>/<setup_id>/<host_class>/
        runtime.json runtime.png breakdown.json breakdown.png gradient.json fit.png parity.json provenance.json
        history/<release_pin>_<YYYY-MM-DD>/…                 # superseded records of the same key
results/lens/<component>/…   results/misc/<group>/…   results/notes/ → wiki/campaigns/<dataset_type>/<variant>/ (ledgers) 
wiki/campaigns/<dataset_type>/<variant>/<campaign>.md   wiki/campaigns/{lens,misc}/…   wiki/setups/ (generated, unchanged)
archive/YYYY/MM/<slug>/      # moved with git mv; README pointer at the old path's parent
catalogue/migration_day_zero.json   # old path → new path (+ sha256), consumed by the catalogue builder and Pulse
```
autolens_inference:
```
scripts/<dataset_type>/<variant>/{validation,samplers}/…   scripts/misc/<group>/…
results/<dataset_type>/<variant>/<instrument>/validation/<model_variant>/<setup_id>/seed_<n>/stages.json
results/<dataset_type>/<variant>/<instrument>/samplers/<model_variant>/<sampler>/{auto|explicit/<setup_id>}/seed_<n>/
results/misc/…      archive/YYYY/MM/<slug>/   (the three dated dirs re-homed)
```

### 3.8 Dashboards

Pulse: selector order becomes **Class (Optimal default | Secondary | Experimental | All) → Likelihood (dataset type → variant) → Instrument → Hardware class → Measurement**, with a History toggle revealing superseded rows and a Coverage panel listing Optimal cells that are `not_measured`. The check-in and research lookups (Brain memory faculty, assistant skills) read `class: optimal` + `status: current` unless asked otherwise. Insight: unchanged structure; the setup page shows `setup_resolved` as provenance and the record table drops the setup from its names.

### 3.9 The lifecycle sequence (phase 0E documents it; phase 8 automates it)

```
L0 register    likelihood + variant + instrument in script_routes/taxonomy; regime declared; Pulse planned cells (class per setup)
L1 figures     fit.png rendered through the viz plotter and signed off (Eyes loop when new)
L2 profile     runtime + breakdown under Optimal and Secondary candidates on reference hosts with parity; → current, prior → superseded
L3 designate   Pulse designation decision + wiki decision-rule note + library rule-table PR + runtime_estimates refresh + workspace/assistant text
L4 validate    full-fit wall-time validation (autolens_inference → Pulse walltime_validation)
L5 gradient    value_and_grad breakdown + FD check (→ Pulse gradient)
L6 samplers    Insight campaign under auto (only when the change could alter sampler choice)
L7 close       Pulse task complete; Mind record; Cortex note where the science changed
```
A re-optimisation of an existing likelihood re-enters at L2 and supersedes; a new likelihood starts at L0.

## 4. Phased plan (bodies; the cards are in the ledger)

Epic slug `likelihood-lifecycle`. Library first in every phase; one issue per repo per phase; each phase ships behind `start_dev` → `ship_library` / `ship_workspace`; phase prompts are filed lazily with `Epic: likelihood-lifecycle` and an integer `Phase:`; sub-issues are lettered inside the prompt body, never in the `Phase:` field.

### Phase 0 — Spine (PyAutoPulse, autolens_profiling, autolens_inference, PyAutoInsight, PyAutoBrain) — no dependencies
- **0A PyAutoPulse** `likelihood-lifecycle/0-contract`: `profiling-summary@3` per §3.2 (validator, REFERENCE.md, README doc-drift fix), `walltime-validation@1` evidence axis, `designation` decision kind, first selector Class, current-only default with History, Coverage panel per class, archived counted not rendered. Rebase after PR #68. Witness: `pyauto-pulse check` accepts a fixture @3 catalogue with one `current` per key and refuses a second; the rendered board's first `<select>` is Class.
- **0B autolens_profiling** `likelihood-lifecycle/0-restructure`: (i) move-only PR from `catalogue/migration_day_zero.json` (git mv; README pointers; `results/notes` ledgers to `wiki/campaigns/<dataset_type>/<variant>/`; `archive/YYYY/MM/<slug>/`); (ii) catalogue builder reads the mirrored tree, emits @3 with class/status by the §3.6 rule, legacy model names retired, grammar converted; (iii) `scripts/misc/` grouping polish (test/ split by group, `misc/searches` orphan removed, one-off scripts to archive, README per group); (iv) coverage matrix tool (extend the profiling conductor's `campaign` grid diff) over likelihood × class × measurement → current / superseded / missing / stale; (v) parity witness convention (`parity.json`: reference log-likelihood, tolerance, status). Data guard: moves and content never in one PR. Witness: `tests/test_results_mirror_scripts.py` passes; `build_catalogue --check` current; Pulse receipt refetches @3.
- **0C autolens_inference** `likelihood-lifecycle/0-restructure`: commit the untracked clean-slate rows first (their own PR); move-only PR to the §3.7 layout with the three archives re-homed; exporter emits `walltime-validation@1` from the base rows (implied ms/eval against the matching Pulse runtime record, parallel efficiency where 1-core rows exist) and adds `setup_mode`/`setup_resolved`; README "No pipeline runs yet" retired; Cortex ledger paths updated. Witness: `export_inference_summary --check` current for both artefacts; Pulse ingests the validation receipt.
- **0D PyAutoInsight** `likelihood-lifecycle/0-contract`: accept the additive fields, render `setup_resolved` as provenance, doc-drift fix (REFERENCE says @1 live). Witness: `pyauto-insight check` green on the re-exported lens catalogue.
- **0E PyAutoBrain** `likelihood-lifecycle/0-template`: `skills/profiling/lifecycle.md` (§3.9 as a prompt template), profiling conductor `campaign` grid on the new tree and config grammar, samplers faculty paths, Pulse/Insight check-in prose. Witness: `pyauto-brain profiling campaign` dry run reads the mirrored tree.

### Phase 1 — Figures (autolens_visualization, PyAutoEyes, autolens_profiling) — no dependency on 0; before 2
- **1A** Eyes review loop over the 10 `fit.png` (human sign-off; critiques → intake); re-scope `draft/feature/pyautoeyes/{multi_galaxy,group_cluster}_gallery.md` to group point-source, cluster extended + image-plane, bespoke point/cluster/weak figures.
- **1B** autolens_profiling: `_profile_cli.py` renders and keeps `fit.png` per cell through the same plotter the viz harness uses (`subplot_fit_quick` out of the tempdir); `figures[]` in the catalogue; fit-figure inspection written into `skills/profile_likelihood` and the campaign template; a note per dataset type on how the profiling instrument differs from the viz dataset.

### Phase 2 — Profiling campaigns (autolens_profiling → Pulse) — depends on 0 and 1
One issue per dataset type (imaging and interferometer may each be one; the rest pair naturally: point_source image+source, multi_galaxy+group, cluster, multi_dataset+datacube, weak). Per issue: coverage matrix → missing/stale cells → scripts added where absent (group, multi_galaxy, weak are new) → RAL submission (CPU on `ral` only; A100 with `--gres`; human authorisation per batch) → parity + fit.png → results as `current` → Pulse receipt → wiki campaign page under the mirrored path with the pre-registered rule and verdict. Imaging reuses the 2026-10-17 results that are on the pinned tag; everything else is re-measured. Adopts `hst_mge_cpu_pilot`. Ends with the human's "campaigns complete" confirmation, the explicit gate for phase 3.

### Phase 3 — Day zero (autolens_profiling, PyAutoPulse) — depends on 2 confirmed
Pin the tag; re-measure the Optimal/Secondary cells not on it; stamp `day_zero`; Pulse snapshot `day_zero`; one `designation` decision per likelihood × hardware class (human records; conductor drafts); `wiki/campaigns/<dataset_type>/<variant>/day_zero.md` decision-rule notes; `setup-baseline` campaign adopted and closed with its manifest replaced; Coverage panel shows no `not_measured` Optimal cell; runtime_estimates export exists (consumed in 5E).

### Phase 4 — Wall-time validation (autolens_inference → Pulse) — depends on 3
Per dataset type: the full model (SLaM where it exists) under the Optimal GPU and Optimal CPU setups plus the Secondary CPU setup, seeds ≥ 2; cores sweep 1/2/4/8/16/32 on `ral` for the CPU likelihoods; `model_variant: light_fixed` only under Optimal; records per §3.2 with `ratio_measured_over_predicted` and `parallel_efficiency`; parity against the reference posterior (the jax_gpu_sparse light_fixed divergence from 2026-10-18 is the first `diverged` row and blocks that setup's Optimal designation until explained). Adopts the clean-slate base rows; never re-runs what exists on the pinned tag. Output: the Pulse validation panel and the efficiency curve that sets the per-likelihood cores cap for 5D.

### Phase 5 — Auto setup in the source — depends on 3 (rules) and 4 (cores cap, efficiency for the estimator)
Sub-issues in library-first order: **5A** PyAutoNerves (environment probe; `PYAUTO_SETUP` at import; x64 bug), **5B** PyAutoArray (`Setup`, `Setup.auto`, rule table, `apply_setup`, consistency check, transformer choice), **5C** PyAutoGalaxy + PyAutoLens (`setup="auto"`, `setup.json`, banner, SLaM threading, defaults aligned), **5D** PyAutoFit (`number_of_cores="auto"`, banner hook, metadata), **5E** estimator + `runtime_estimates.yaml` exporter (autolens_profiling) + PyAutoLens data file, **5F** autolens_workspace + HowToLens (stale prose retired; `cpu_fast_modeling.py` becomes the override example; `example_cpu_and_gpu.py` contradiction fixed; concise CLI explanation), **5G** autolens_assistant (`al_explain_setup`; `al_configure_search` rewritten), **5H** science projects (`--use_cpu` → `--setup`; env blocks removed) and the euclid single-process-route draft closed by it. Witness: ledger header phase 5 witness + the rule-table ⇔ designations parity test.

### Phase 6 — Gradient (autolens_profiling → Pulse) — depends on 2; may run alongside 4–5
Adopt `gradient_cost_probe`: forward vs `value_and_grad` ms/eval + strict FD check on every Optimal cell (and CPU cells where a gradient sampler would run on CPU); `measurement: gradient` records; a hazard where grad/forward exceeds ~4× or FD fails, each filed as its own optimisation prompt through intake; `gradient_breakdown.py` per likelihood in the mirrored scripts tree.

### Phase 7 — Sampler campaign (autolens_inference → PyAutoInsight) — depends on 5 and 6
Per dataset type under `setup_mode: auto`: Nautilus control, gradient samplers (NUTS, MultiStartGradient) and non-gradient samplers (emcee, zeus, dynesty, SMC) as capability allows; ≥ 3 seeds; pre-registered protocol (success rate with intervals, wall per right answer, evaluations-to-converge); `model_variant: light_fixed` only under Optimal; research wiki per dataset type at the mirrored path; Insight dashboard + decision records; the evaluations table refreshes the estimator (5E). Adopts the `hst-imaging-mass-samplers` wave plan and `gradient_sampler_validated_likelihoods`. Runs through the sampler_pipeline skill and samplers faculty; Insight stays conductor-free.

### Phase 8 — The lifecycle verb (PyAutoBrain, PyAutoMind) — depends on 0E; finalised after 7
`pyauto-brain profiling lifecycle --likelihood <dataset_type>/<variant> [--instrument …] [--trigger new|reoptimised]` reads the taxonomy and coverage matrix and emits the epic ledger plus phase prompts for §3.9 (intake files them; integer phases; witnesses pre-filled from the templates). Dogfood on `matrix_free_interferometer_phase5.md`. Documented in the profiling conductor AGENTS.md and the Brain board; a Brain test renders the prompts from a fixture.

## 5. Risks and open questions for the human (recommendations inline)

- **R1 Vocabulary and grammar** (§3.1): approve as written? Recommended: yes; the only naming choice with history cost is `setup_id` dropping the tier prefix, handled by the migration map.
- **R2 Day-zero history cut** (§3.6): label-only at phase 0, re-measure at phase 3, delete nothing. Recommended: yes.
- **R3 Provisional designations** (§3.3) as the phase-0 labels. Recommended: accept provisionally; phases 2–3 confirm.
- **R4 Mixed precision** is `experimental` until the x64 bug is fixed and a validated cell exists. Recommended: yes.
- **R5 Compile cost** is not an axis of the Optimal class. Recommended: yes; the per-cell compile builder stays a separate task.
- **R6 Default flip to `setup="auto"`**: one opt-in release with a "would choose" banner, then the flip. Alternative: flip immediately. Recommended: opt-in first.
- **R7 `host_class` as provenance, not identity**: laptop measurements never become `current`. Recommended: yes (matches the existing reference-host rule).
- **R8 Insight naming** `…/<sampler>/auto/seed_<n>` with `setup_resolved` provenance. Recommended: yes.
- **R9 Compute authorisation** is per phase and per batch; CPU arrays on `ral` only; A100 with `--gres`; phases 2 and 4 are the expensive ones (phase 4 full SLaM fits are hours per seed on A100 and about a day per chain on jax_cpu by the 2026-10-18 rows). Recommended: phase 2 first on the cells the coverage matrix calls missing, nothing else.
- **R10 `setup-baseline`** campaign adopted and closed by phase 3 with its 1,044-slot manifest replaced. Recommended: yes.
- **R11 Ordering of phase 6**: the ask lists gradients after the source factory; nothing in 6 depends on 5, so it may run alongside 4–5 if RAL time allows. Recommended: allow.
- Risks: the move-only PRs are large (1,473 files, 326 MB, `results/lens/solver/corpus` 165 MB) and must be reviewed as renames; Pulse PR #68 is open and unmerged; the jax_gpu_sparse light_fixed divergence is unexplained; library phases ship pending-release and the day-zero pin must be a released tag, so a release sits between phases 2 and 3 and another between 5 and 7; sessions must end at their deliverable (no self-armed timers) and the Mind shared checkout rules apply to every ledger update.

## 6. Candidate tasks for `ideas.md` (propose, do not append)

- Pulse hygiene: `tasks/hst_mge_cpu_pilot_choices.md` has no ledger row (surveys/02 §1).
- PyAutoFit: document the JAX fork rule next to `number_of_cores="auto"` and the XLA intra-op thread behaviour on CPU.
- PyAutoNerves: decide `XLA_PYTHON_CLIENT_PREALLOCATE` when auto resolves to a CPU setup on a GPU host.
- autolens_workspace: the `guides/using_jax.py` reference to the retired "Applying vmap and jit" log line.
- autolens_profiling: `scripts/misc/searches/` orphan and `results/README.md` redirect table after the move.

## 7. Resume note

Start with the ledger's "How to orchestrate" section, then phase 0A. Do not re-run the surveys; they are current as of 2026-10-21 and cited by section above. Every phase prompt names its witness from §4 and its human gate from the ledger.

## Amendment 2026-10-25: node throughput (human-approved)

**Ruling:** numba CPU setups run one serial process per core under Nautilus multiprocessing, so CPU and GPU are compared as **throughput per node, or per hardware budget**, never by per-call latency alone. Phase 2 projects this; it does not run multi-worker jobs. The phase structure is unchanged. These are the changes:

- **Phase 2 (new sub-task 2x, before 2b):** rows record `cpus_per_eval` and `peak_rss_gb`. The catalogue projects `projected_node_throughput` per declared reference host (RAL ral node 236 cores / 921 GB; RAL gpu node 124 cores / 885 GB / 4×A100; laptop), with a declared parallel efficiency η (1.0 upper bound until measured). Prompts: `draft/feature/autolens_profiling/likelihood_lifecycle_p2x_node_throughput.md` (producer, plus a 2a backfill from sacct) and `draft/feature/pyautopulse/likelihood_lifecycle_p2x_throughput_view.md` (Pulse view and research page).
- **Phase 3 (designation):** keep separate Optimal GPU and Optimal CPU designations, but pre-register the comparison rule before reading the data: rank by projected throughput on the named hardware budget, and show per-call latency only as secondary evidence. Designations made before phase 4 carry `basis: projected` and are revisited when η is measured.
- **Phase 4 (wall-time validation):** extend the planned 1/2/4/8/16/32 cores sweep on `ral` to 64 and 128 workers, and add a memory-limited ao case. Measure whether the W~ operator is shared between workers after fork, and the Nautilus `n_batch` ceiling. Feed the measured η per (setup, host) back to the producer, replacing the declared η.
- **Phase 5 (`setup="auto"`):** the rule table and `number_of_cores="auto"` choose by throughput. The worker count is capped at min(cores / cpus_per_eval, available memory / peak_rss), so auto never forks more ao workers than memory allows. When a GPU and many cores are both present, the choice follows projected (later measured) throughput, not device type.
- **Communication:** no summary, wiki page or dashboard headlines a "GPU is N× faster" figure from latency alone (2a example: hst Delaunay A100 is 27× faster per call, but a ral node projects to about 9× the A100's throughput at η = 1).

