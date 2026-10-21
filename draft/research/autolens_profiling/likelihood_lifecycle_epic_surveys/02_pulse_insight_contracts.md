# Survey 02 — PyAutoPulse and PyAutoInsight data model, contracts, dashboards, boundaries; the Brain profiling conductor (2026-10-21, Explore worker, read-only)

**Top-line findings for the epic:**
- **Pulse has no recency mechanism.** No field or logic expresses "latest", "superseded" or "best" for a result. The only lever is the producer-supplied setup `role`, which the JS uses as a ranking nudge. The default view is a heuristic curated choice, not "latest". Most records (100 of 112) have no `measured_at`, so a day-zero reset has to be expressed by the producer: a new field such as a setup or record `status` (current/archived), or a role. Pulse cannot infer it.
- **Insight already separates current from history.** It does this through a per-record `archived` flag. The HST work is already partly cleaned up: the folders `archive/2026-09-24_superseded_by_cleanslate` and `..._pre_likelihood_speedup` exist.
- **Insight setup IDs exclude the compute setup; the run folders include it.** Setup IDs are `dataset/model/instrument`. The project's run folders and record IDs embed `hpc_a100_jax_gpu_dense_fp64` and similar.
- **Optimal-vs-secondary must be a producer declaration.** Making it Pulse's first selector is consistent with the boundary only if the producer (autolens_profiling, through a recommendation, role or selection) or a human decision record says which setup is optimal. Otherwise it collides with "Pulse never selects a latest/fastest row". The v2 `recommendations` list (5 entries exist today) and `role` are the two existing hooks.
- **Doc drift:** Pulse REFERENCE.md:9, :36, :42 and :99-101 still describe v1 as live, and Insight REFERENCE.md:68-69 says the live registry is `inference-summary@1`. Both registries actually pin v2 or v3.

---

## 1. PyAutoPulse (`organs/PyAutoPulse`, local `main` @ e3d411e)

### Registry (`registry.yaml`, schema 1): 2 instances

| instance | repo | summary_path | supported_schema | library_refs | cortex |
|---|---|---|---|---|---|
| `lens` | autolens_profiling | dashboard/catalogue.json | profiling-summary@2 | Lens, Galaxy, Array, Fit | null |
| `fit` | autofit_profiling | dashboard/catalogue.json | profiling-summary@2 | Fit | null |

- Registry rows have no lib, dataset, likelihood or setup fields. The allowed fields are listed in REFERENCE.md:18-26, and unknown fields are refused.
- Setup identity lives in the producer's v2 catalogue `setups[]`: `id, label, dataset, model, instrument, configuration_id, configuration{}` (REFERENCE.md:115-130). Producers may also add the optional field `role`.
- Lens snapshot contents:
  - 584 setups, 112 records, 105 selections.
  - `archive_record_count` is 20,999.
  - Roles: `legacy_or_experimental` 552, `planned_baseline` 29 (IDs `baseline/imaging/mge/hst` and so on), `reference_candidate` 3.
  - Every record has validation `unreviewed`.
  - Only 12 of 112 records carry `measured_at`.
- Receipts:

| receipt | outcome | schema | records | commit | fetched |
|---|---|---|---|---|---|
| lens | ok | v2 | 112 | 173ab272 | 2026-10-19 |
| fit | ok | v2 | 31 | 58e56b96 | 2026-10-15 |

### Other state

**`campaigns.yaml`** (v1, `last_checkin: 2026-10-17T15:12:59Z`): 13 campaigns.

| status | campaigns |
|---|---|
| needs-decision | setup-baseline, critical-curves |
| active | point-source-image-cpu, cluster-pointsolver, linear-solver, imaging, measurement-tools, autofit |
| parked | point-source-image-gpu, interferometer, delaunay-nn-cpu, certified-solver |
| complete | point-source-source |

- Tasks: 30 rows (ready 11, parked 6, complete 5, needs-decision 3, active 3, superseded 1, needs-slicing 1). There are 31 files in `tasks/`; `hst_mge_cpu_pilot_choices.md` has no ledger row.
- Statuses are enumerated in `pulse/campaigns.py:18-28`, with `CLOSED = {"complete","superseded"}` at :29. "superseded" exists only for ledger campaigns and tasks, not for results.

**`decisions.yaml`:** 4 decision records.
- linear-solver-mapper-default-jacobi (2026-10-08)
- adaptsplit-zero-weight-delaunay-only (2026-10-15)
- interferometer-route-gate-cost-model (2026-10-15)
- direct-conv-symmetric-gate (2026-10-16)

Supersession is done only by a new dated record with Supersedes / Superseded-by links (decisions/README.md:29-31).

**Other files:**
- `migration.yaml`: 26 Mind prompts migrated 2026-10-03 from Mind @f21898e, each with a sha256.
- `snapshots/` and `receipts/`: lens.json and fit.json. A snapshot is the last good summary verbatim; a receipt is the resolved commit plus outcome (REFERENCE.md:215-238).
- `checkins/`: 2026-10-13.md, 2026-10-13-evening.md, 2026-10-17.md.

### Contract and validator

- Supported versions: `pulse/summary.py:23`, `SUPPORTED = {("profiling-summary", 1), ("profiling-summary", 2)}`.
- Entry points: `supported()` at summary.py:102, `validate()` at :119 (sends v2 to `pulse/catalogue.py:345 validate()`), and `classify()` at :314.
- Live pins are @2 (registry.yaml:11, :18).

### Does anything express "active/latest/superseded/best"?

Only weak, producer-owned hooks:
- **Setup `role`:** read only in JS ranking at `pulse/setup_browser.js:171` (`reference_candidate` gives -100). catalogue.py does not validate it.
- **Selections:** `status` ∈ accepted / unreviewed / not_measured / failed / unusable / inapplicable (REFERENCE.md:164-182).
- **Record `validation.status`:** accepted / unreviewed / rejected (REFERENCE.md:153-155).
- **Recommendations and hazards:** hazard `status` open / resolved / unknown (REFERENCE.md:184-200).
- **v1 only:** comparisons with drifted / improved / flat. v2 requires `comparisons == []` (catalogue.py:356-360).

### How the dashboard picks results

- It is not all history and not latest. The v2 catalogue is a producer-selected set: 112 records out of a 21k archive.
- The browser then applies a fixed default heuristic:
  - **Eligibility filter** (`setup_browser.js:150-157`): float64 only, and pixel models at 1500 source pixels only.
  - **`curated()` / `defaultRank()`** (`setup_browser.js:158-198`): keeps one setup per axis and device. It prefers purpose-built `results/<axis>/` paths, `reference_candidate`, non-experiment filenames and short filenames.
  - **Default instrument and device:** default instrument is `hst`, else the first; default device is `cpu`, else the first (`setup_browser.js:876-887`).
  - **Archived deep links:** shown as "Archived configuration (linked)" but "never injected into the default selector" (`setup_browser.js:893-895`, :943-947).

### Dashboard structure

**HTML hero nav** (`pulse/board.py:574-578`): Active campaigns → Profiling Results → Decision History. The HTML main area is built in this order (board.py:581-590):
1. Check-in prompt and campaigns table
2. One setup browser per instance
3. Decision History

**`dashboard.md` sections:**
- `# PyAutoPulse — profiling dashboard`
- `## Profiling Check In` (:4)
- `## Active campaigns` (:30), with per-campaign `### Active tasks`
- `## Profiling Results` (:188), with a per-instance "<project> — choose a setup" disclosure (dataset → model: instruments)
- A collapsed "Capture, qualification and legacy diagnostics" section containing `## lens` (:265) and `## fit` (:310)
- `## Decision History` (:333)

**Selector order (current):**
1. A navigation disclosure: Project → dataset family → model (with JAX or Numba label) links. These open `?view=model` (`setup_browser.js:329-399`).
   - Family order: imaging, interferometer, datacube, point_source_image, point_source_source, multi_dataset, cluster, lens, experiments (`setup_browser.js:73-83`).
   - Model priority: delaunay, rectangular, mge, knn, mge_mass, sersic (:369).
2. On the model page, `<select>`s in this order:
   1. **Instrument** (:909-925)
   2. **Device** (:926-941)
   3. **Configuration** (:948-955)
3. Then headline metrics and the axis panels (Runtime / Breakdown / Compilation / Memory, :42-47).

There is no setup-quality or optimal selector today. A new first selector would go before :909.

---

## 2. PyAutoInsight (`organs/PyAutoInsight`, local `main` @ 1039374)

### Registry (`registry.yaml`, schema 1)

| instance | repo | summary_path | supported_schema | cortex |
|---|---|---|---|---|
| `lens` | autolens_inference | dashboard/catalogue.json | inference-summary@2 | autolens_inference |
| `fit` | autofit_inference | dashboard/summary.json | inference-summary@3 | autofit_inference |

Receipts: lens is v2, 148 records @71bfd57b (2026-10-21). fit is v3, 12,973 records @6d26b557.

### Contract and validator

- Supported versions: `insight/summary.py:22`, `VERSIONS = (1, 2, 3)`.
- Entry points: `supported()` at :64, `validate()` at :75, `validate_shard_index()` at :336, `classify()` at :447. The v2 setups and prepared-problems contract is in `insight/catalogue.py:139 validate()`.
- REFERENCE.md:16 states support for v1, v2 and v3.

### Campaigns, decisions and other files

**`campaigns.yaml`** (`last_checkin: 2026-10-18T17:00:00Z`): 10 campaigns.

| status | campaigns |
|---|---|
| superseded | slam-hst-base, slam-hst-delaunay |
| needs-decision | hst-imaging-mass-samplers, point-source-admission, ep-toy-gaussian |
| needs-slicing | graphical-ep |
| blocked | analytic-gaussian, slope-hierarchy-scale, ic50-scale |
| running | gaussian-x3-search-benchmark |

- Tasks: 11 (needs-decision 4, blocked 2, complete 2, needs-slicing 2, running 1).
- Campaigns also carry `recent_progress`, `blockers`, `job_status` and `checkin_report`.
- **`decisions.yaml`:** 1 record, `hst-cleanslate-drop-numba-dense` (2026-10-18). Quote: "lets just drop dense numba we would never use it" (decisions/hst-cleanslate-drop-numba-dense.md:5).
- **`sampler_candidates.json`:** 5 candidates. dynesty, nautilus and blackjax-nuts are integrated; ultranest and pocomc are prospective. Every one is `benchmark_status: not_assessed`.
- **`docs/`:** only `migration-landed-2026-10-04.md`, a migration record that is not a check-in.
- **`checkins/`:** 2026-10-17T111853Z, 2026-10-18T170000Z and 2026-10-19T171637Z.

### How instances and records are keyed

- **Instance keys** are just `lens` and `fit`.
- **Setup IDs** are `<dataset_family>/<model_family>/<instrument>`. There are 11 of them: `imaging/{rectangular,delaunay}/{hst,euclid,jwst,jwst_lw,ao}` and `point_source/simple/simple`. They do **not** include the compute setup.
- **Record IDs** do include the compute setup, because they are evidence paths. For example: `results/archive/2026-09-24_superseded_by_cleanslate/slam/imaging/hst/slam_base/hpc_a100_numba_cpu_sparse_fp64/stages_seed0.json#stage-…`.
- **Record fields:** `configuration.config_name` (e.g. `hpc_a100_jax_gpu_dense_fp64`), `configuration.inversion` (dense/sparse), `backend` (jax_gpu / jax_cpu / numba_cpu) and `precision` (fp64).
- **Project folders** (campaigns.yaml:44): `output/autolens/imaging/hst/slam/<variant>/<config>/seed_<n>/<stage>/` and `results/slam/imaging/hst/<variant>/<config>/`. Local copies exist, e.g. `lens/autolens_inference/results/slam/imaging/hst/slam_base/{hpc_a100_jax_cpu_dense_fp64, hpc_a100_jax_cpu_sparse_fp64, hpc_a100_jax_gpu_dense_fp64, hpc_a100_jax_gpu_sparse_fp64, hpc_ral_numba_cpu_sparse_fp64}`.
- **Implementation filter:** derived from `backend` (`insight/setup_browser.py:34-42`). Imaging delaunay and rectangular always get JAX and Numba filters (:280-281).

### Current vs history

- Records carry `archived` (REFERENCE.md:28-29). The lens instance has 122 archived and 26 current records.
- "Historical project records are labelled archived and separated from current results" (REFERENCE.md:36-37).
- The setup page shows current "Sampler results" separately from a "Historical project results" disclosure (`setup_browser.py:210-229`).
- `reference_record_id` is a producer selection of an accepted baseline (REFERENCE.md:121-130). All 11 are null today.

### Dashboard structure

**Hero nav** (`insight/board.py:373-376`): Active campaigns, Inference Results, Decision History, Sampler candidates.

**`dashboard.md` sections:**
- `# PyAutoInsight — inference control room` (:1)
- `## Check in on all inference work` (:14)
- `## Active campaigns` (:38)
- `## Active tasks` (:51)
- `## Inference Results` (:67), containing `## autolens_inference` (:71; setup links plus a "Full captured evidence and provenance" record table of about 31.9k lines) and `## autofit_inference` (:31979)
- `## Decision History` (:32099)
- `## Sampler candidates` (:32103)

**Setup-page selectors:** only **Instrument** (`setup_browser.py:136-142`). The implementation choice is made at the navigation link (:282-287).

---

## 3. Boundary statements (verbatim)

### Pulse

- AGENTS.md:20-22: "It validates the exchange contract only and never judges a timing — the Brain's profiling conductor (`triage`) does."
- AGENTS.md:44 (organ map): "Validates the contract only; never judges, scores or issues verdicts (the Brain's profiling conductor judges)."
- AGENTS.md:137-140: "It does not move pins, combine unmatched timings, apply the compile threshold to runtime, compute an ecosystem-wide speed score or issue a Heart verdict."
- AGENTS.md:144-145: "**Recomputes no ratio.** … it never divides two measurements."
- AGENTS.md:150: "**Ranks nothing across projects** — no league table, no speed score."
- AGENTS.md:153-157: "**Judges nothing.** The Brain's profiling conductor is the only judge … Fetching or rendering never submits a job, re-pins a baseline, logs a lesson, edits source or grants approval."
- REFERENCE.md:173: "The producer chooses references; Pulse never selects a latest/fastest row."
- REFERENCE.md:109-110: "this catalogue presents selected results, not release trends."
- REFERENCE.md:154-155: "these are producer declarations, never an acceptance decision inferred by Pulse."
- README.md:73-74: "No rendering action accepts a baseline, changes campaign state, runs profiling, or selects the fastest run."
- CHECKIN.md:25-26: "The check-in itself authorizes no job submission, default/baseline change, release or merge."
- CHECKIN.md:66-67: "Do not infer an accepted choice from timings, a passing run, or an agent recommendation."

### Insight

- AGENTS.md:8-10: "Do not create an inference conductor, select defaults or turn process completion into scientific acceptance. Refreshing the board neither checks in nor changes task status."
- AGENTS.md:14: "No scientific libraries are imported by this reader. No automatic compute submission."
- AGENTS.md:35: "never infers scientific acceptance or submits compute."
- REFERENCE.md:6: "There is no inference conductor and no new scientific execution engine."
- REFERENCE.md:35-36: "No universal threshold, default-sampler promotion or best-seed selection is performed."
- REFERENCE.md:122-123: "This **does not select it as trusted**."
- REFERENCE.md:185-186: "No acceptance, ranking, best seed or universal convergence threshold is calculated even when controls match."
- CHECKIN.md:32-33: "never rank incompatible targets or cherry-pick the best seed."

**Implication for inference wall-time validation on Pulse:** it must arrive as producer records, presumably a new axis or metric that needs a contract extension. REFERENCE.md:159-162 shows extra meanings "require an explicit contract extension", and component timings are never runtime. Inference wall time must not be presented as a per-likelihood cost (REFERENCE.md:199-200: "must not … interpret a per-likelihood measurement as a total-fit prediction").

---

## 4. Open issues and PRs

| Repo | Open issues | Open PRs |
|---|---|---|
| PyAutoLabs/PyAutoPulse | **#62** campaign: interferometer large-mask likelihood — memory and routing (Aris 512×512) | **#68** docs: link /prm close-outs and refresh receipts after 2026-10-17 merges |
| PyAutoLabs/PyAutoInsight | none | none |
| PyAutoLabs/autolens_profiling | #436 research: cluster-scale robust PointSolver settings; #166 Decide default log_det_method (slogdet vs cholesky); #128 research: what kills MGE multi-start lanes (62% NaN); #103 feat(jax_compile): warm-compile baselines; #50 lint.yml not ruff-clean | none |
| Jammy2211/autolens_profiling | repo does not exist | — |
| PyAutoLabs/autolens_inference | #4 Project ledger: autolens_inference | #30 docs(hpc): pin table lists tag commits |

**#62 (OPEN issue, 18 comments):**
- It anchors the Pulse campaign `interferometer` / task `interferometer_large_mask_aris`.
- It tracks three PyAutoArray members, #626, #627 and #628 (sparse data vector; AdaptSplit log-det parity; numba route-gate cost model).
- It holds laptop baseline tables.
- Its last comment adds the matrix-free interferometer inversion (PyAutoArray#638, phases 1-4 merged 2026-10-21) as a future dense-vs-matrix-free campaign. The Mind prompt is `draft/research/autolens_profiling/matrix_free_interferometer_phase5.md`.

**#68 is a PR, not an issue (OPEN, unmerged, branch `feature/pulse-post-prm-2026-10-17`):**
- It is a ledger link pass after the 2026-10-17 `/prm`. It updates `next:` for 9 tasks and 5 campaigns, adds "Post-/prm" sections to tasks and to checkins/2026-10-17.md, and refreshes receipts (lens @c40e33c8).
- It says "Not a check-in". It is not on local main, so an epic branching from main should rebase over or after it.

---

## 5. Brain profiling conductor

**Files:**
- `organs/PyAutoBrain/agents/conductors/profiling/{AGENTS.md, _profiling.py, _catalogue.py, profiling.sh}`
- `organs/PyAutoBrain/skills/profiling/{SKILL.md, profiling.md}`

**How it works:**
- **What it emits:** a dry-run `ProfilingDecision`. "It does NOT run sweeps itself and never edits source" (_profiling.py:9-10; profiling.md:10-12).
- **`campaign`** (`_profiling.py:256-321`):
  - Diffs the grid against `results/runtime/<cls>/<model>/<inst>/<model>_<cfg>.json`. The grid comes from the project's `catalogue/script_routes.json` or the v2 `script_routes`.
  - Counts each run as done, `.unusable.json`, or missing.
  - Config names come from `TIER_CONFIGS` at :61-64: `local_cpu_fp64`, `local_cpu_mp`, `hpc_a100_fp64`, `hpc_a100_mp`.
  - Emits local `sweep.py` commands or RAL `sbatch` lines, under the CPU-usability policy `results/notes/design_lock_in.md`.
- **`ingest`** (:562) and **`ingest_compile`** (:452): find unpinned and drifted rows and emit table, pin and baseline steps. Pins are sticky in `jax_compile/pins.json` (AGENTS.md:58-62).
- **`triage`** (:805-850):
  - Reads `~/.pyauto-heart/profiling_drift.json`.
  - Applies the rule at :829-833: "stale pin → re-pin … else library regression → file bug/ via intake".
  - The compile-drift classification table is at AGENTS.md:150-163, and the drift gate (2.0× and +1.0 s, newer than pin) at AGENTS.md:49-56.
- **Where decision rules and knowledge are written:** the conductor writes none.
  - Human decisions go to Pulse `decisions/<id>.md` plus `decisions.yaml` (CHECKIN.md:60-80; decisions/README.md:13-31).
  - Pre-registered decision rules and verdicts live in the project wiki's campaign-page header contract (`lens/autolens_profiling/wiki/README.md:27-28`, `**Pre-registered rule:**` / `**Verdict:**`), with full ledgers in `results/notes/`.
  - Science facts go to Cortex.

**Is there an inference conductor?**
- No. `grep -ril insight organs/PyAutoBrain/agents` matches only `agents/_pyauto_root.py:69` (a repo-name list).
- Inference is touched only by the read-only `faculties/samplers` (AGENTS.md:36-38, :175 reference autolens_inference and autofit_inference).
- Insight forbids creating an inference conductor (Insight AGENTS.md:8-9; REFERENCE.md:6).
