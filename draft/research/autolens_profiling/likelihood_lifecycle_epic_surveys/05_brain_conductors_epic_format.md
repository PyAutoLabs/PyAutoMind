# Survey 05 — Mind epic format, Brain intake/conductors, overlapping epics and tasks (2026-10-21, Explore worker, read-only)

## 1. Epic format (PyAutoMind)

Two filing shapes exist.

**(a) Research epic, split across sibling files.** Used by search-extensibility and hpc-campaign, both in `organs/PyAutoMind/draft/research/autofit/`:
- `<name>_epic.md` is the ledger. It holds the header, a Summary, `## Original request (verbatim)`, and then Status, Resume and dated Ledger sections that are appended as the work advances. Search-extensibility headings: Summary :37, Original request :67, Status :71, Resume :176, Ledger :219.
- `<name>_epic_report.md` holds the research report and the phase plan.
  - Search-extensibility report: `## 4. Phased plan` :442 → `### Track A — PyAutoFit framework` :446 → `#### A0 — Safety net and repair (no dependencies; order …)` :448, `#### A1 — Declare, gate, registry (depends on A0a; …)` :495, and so on to `#### B5` :675. Then come §5 risks/questions, §6 "Candidate tasks for `ideas.md` (scholar mode; propose, do not append)", §7 resume note and §8 collated review decisions.
  - HPC report: `## 5. Phased epic plan` :221 opens with "Epic slug: `hpc-campaign`. Library first in every phase; each phase ships behind the ordinary `start_dev` → `ship_library`/`ship_workspace` gates. One issue per repo per phase." Phases look like `### Phase 0 — Result integrity and failure records (PyAutoFit, pipeline) — no dependencies` :225, and issues inside a phase like `- **PyAutoFit #A** \`hpc-campaign/0-integrity\`: … Done: …`.
- `<name>_epic_surveys/` holds numbered survey outputs (`01_search_architecture.md` … `04_inference_profiling_infra.md`; HPC uses `carbon.md`, `codebase.md`, `euclid_hpc.md`, `prior_art.md`).
- `<name>_epic_reviews/` holds independent reviews named `NN_<model>_<scope>.md`, e.g. `01_codex_gpt6_astra.md`, `07_codex_astra_a4_stack_premerge.md`.

**(b) Campaign map in one file.** Used by `draft/feature/autofit/results_library_epic.md`, which also has a sibling `_report.md`. Its sections are Scope :28, Original request :47, Boundary :51, `## Phases` :77, then `### Phase 0 — Integrity and honesty primitives (PyAutoFit) — no dependencies` :84 through Phase 5 :245, then Open questions :279 and `## How to start` :299. The Phases intro (:79-82) reads: "Library first in every phase. One issue per repo per phase, and each phase ships on its own behind the ordinary `start_dev` → `ship_library` / `ship_workspace` gates." How to start (:302-305): "Issue one phase at a time, never the whole map."

**Phase prompts are separate files, filed only when that phase starts.** Each goes under the ordinary `draft/<type>/<target>/` path with `Epic:` plus `Phase:`. Example: `draft/research/autofit_inference/search_ext_b5c2b_scored_wave_submit.md` carries `Epic: search-extensibility` and `Phase: B5c-2b`, plus `Blocked-by:`, `Consequence: judge`, `Witness:`, `Review-minutes: 45` and `Unattended: needs-slicing`.

**Exact headers**
- `search_extensibility_epic.md:3-33`: `Type: research` / `Target: autofit` / `Repos:` (15 bullets) / `Themes:` (searches, jax, documentation, inference, profiling) / `Difficulty: large` / `Autonomy: human-required` / `Priority: high` / `Epic: search-extensibility` / `Status: draft` / `Filed: 2026-10-07` / `Witness: <one long checkable sentence>`. No `Phase:` and no `Depends:`.
- `hpc_campaign_epic.md:3-20`: `Type: research` / `Target: autofit` / `Repos:` (6) / `Themes:` (hpc, euclid, carbon) / `Difficulty: large` / `Autonomy: human-required` / `Priority: high` / `Status: draft` / `Filed: 2026-09-27`. There is **no `Epic:` line**, and hpc-campaign has **no `## hpc-campaign` entry in `epics.md`**; it is only named inside the results-library entry.
- `results_library_epic.md:3-26`: `Type: feature` / … / `Difficulty: too-large` / `Autonomy: human-required` / `Priority: high` / `Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued` / `Consequence: judge` / `Witness: phase 0 — …; phase 1 — …` / `Review-minutes: 30` / `Unattended: needs-slicing` / `Epic: results-library` / `Filed: 2026-10-07`.
- There is no `Depends:` key anywhere. Dependencies go in the phase headings ("— depends on 1") or in `Blocked-by:`.

**Rules**
- **The epic registry (`epics.md`).**
  - Entry schema (:11): "`## <slug>` then `- title:` / `- ledger:` / `- notes:` (and optionally `- status:` …never per-phase detail, which belongs in the ledger)".
  - Retirement (:15): an entry whose status "**begins** SHIPPED or COMPLETE is retired by `lifecycle.py epics --retire`".
  - Membership (:21-25): "A member prompt declares its membership in its own header: `Epic: <slug>` … plus an optional `Phase: <n>`. The dashboard then keeps members out of the pick lists … shows them only grouped, phase-ordered, under their epic".
  - `AGENTS.md` adds that registry files, `epics.md` included, "are changed through skills".
- **The header spec (`REFERENCE.md`).**
  - Header block :316-339: `Difficulty: medium # small | medium | large | too-large`, `Autonomy: supervised # safe | supervised | human-required`, `Priority: normal # low | normal | high`, `Consequence: glance # notify | glance | judge`, `Unattended: ready # ready | needs-slicing | never`, plus `Witness:`, `Review-minutes:`, `Filed:`, `Issued:`, `Blocked-by:`, `Epic:`.
  - :397-401: "`Epic: <slug>` (`epics.md`, plus an optional `Phase: <n>`) makes this prompt one phase of an ordered programme".
  - :308 "One prompt = one task = one PR". No YAML.
  - :746-752: the old `z_features/` umbrella trackers were retired into `complete/archive/epics/`.
- **Profiling and inference ownership.**
  - `docs/pulse-task-migration.md:36`: "Mixed library/science tasks and shared epics remain here [Mind] with Pulse pointers."
  - `docs/insight-task-migration.md:5-7`: Mind retains "bounded implementation PR lifecycle, repository claims and mixed library/production epics".
  - So a cross-cutting pipeline epic belongs in Mind. Its profiling tasks go in Pulse `tasks/` and its inference tasks in Insight `tasks/`.
- **Gotcha: `Phase:` ordering.** `_intake.py:1281-1284` reads `phase = int(header.get("phase", ""))`, and a non-integer value becomes `None`. Phase ids such as `A0a`, `B5c-2b` or `6b2` therefore sort after the numbered members as if they had no phase (`_intake.py:1797`). Use integers if dashboard ordering matters.

## 2. Intake conductor

Files: `organs/PyAutoBrain/agents/conductors/intake/{AGENTS.md, INTAKE_TAXONOMY.md, _intake.py, intake.sh}`.

**It does not split an epic automatically.** It files one prompt per input.
- AGENTS.md:77-85: "**`too-large` means decompose, never dispatch.** … The route is a decomposition pass first: rewrite it as a sequenced series of `small`/`medium` prompts, each with concrete acceptance criteria and stated dependencies … The original prompt becomes the series' tracker or is retired. Decomposition is planning judgment — it stays with the strongest available model".
- For `large` it only adds a risk note: "Large: expect to split into phased PRs at start_dev time." (`_intake.py:691-692`).
- The dashboard's one-tap epic resume (`_epic_prompt`, `_intake.py:1056-1078`) tells the session to read the ledger, work out the last completed phase, then continue "through the normal workflow (… filing the phase's prompt first if none exists)". So it is one prompt per phase, filed lazily.

**What a "declared" header means** (AGENTS.md:61-74; `_intake.py:227-270`). A pasted header block, or the ideas.md inline style `Difficulty large, supervised.`, wins over the derived estimate. Declared `Type:`, `Autonomy:` and `Priority:` also win, and the IntakeDecision reports `difficulty_source`.
- A block counts as a header only if it is contiguous, made only of known keys, and declares at least one anchor key.
- Anchor keys (:255): `type, target, repos, difficulty, autonomy, priority`.
- Known keys (:246-251): `type, target, difficulty, autonomy, priority, status, issued, filed, epic, phase, blocked-by, closes-when, consequence, witness, review-minutes, unattended, lane, memory, repos, themes`.
- Fields such as `Parent:` or `Community:`, which the matrix-free phase-5 prompt uses, are not in this list. Values in backticks or code fences are not declarations.

**Valid enumerations**
- Work types: `_sizing.py:51-62`: feature, bug, refactor, docs, test, release, maintenance, research, human_review, triage. `human_review` is declaration-only (`MANUAL_ONLY_WORK_TYPES`, :74). Aliases (`_intake.py:237-242`): hygiene/upkeep→maintenance, tests→test, documentation→docs.
- `_sizing.py:423` `DIFFICULTY_LEVELS = ("small", "medium", "large", "too-large")`.
- `_sizing.py:424` `AUTONOMY_LEVELS = ("safe", "supervised", "human-required")`.
- `_sizing.py:433-434` `CONSEQUENCE_TIERS = ("notify", "glance", "judge")`, `UNATTENDED_LEVELS = ("ready", "needs-slicing", "never")`.
- Priority: `low|normal|high` (INTAKE_TAXONOMY.md:78). `_sizing.py:471` also tolerates `medium`, mapped to the same rank as normal.
- Autonomy caps by type (`_sizing.py:961-966`): refactor/test/maintenance→safe; bug/research→supervised; release/human_review/triage→human-required.

**`bin/pyauto-brain intake --help`** lists the modes `"<raw text>"`, `classify --file P`, `ideas`, `census`, `dashboard`, `formalise [prefix]`, `reconcile [prefix] [--repo <target>]`. `--apply` goes before the subcommand and is off by default (dry-run). It has no epic or split mode.

## 3. Overlap check

- **hpc-campaign** (`hpc_campaign_epic.md` plus `_report.md`). Deferred (report §8 :311). The report summary says "Six phases" (:13), but the phase list runs 0–6, so seven numbered phases.
  - Phase 0: integrity. Phase 1: per-fit status record and RSS/CPU measurement. Phase 2: campaign core and Slurm adapter. Phase 3: organism integration (assistant, Cortex, Brain scheduler governance).
  - **Phase 4 (#K `campaign pilot`/`campaign plan`, #L plan skill) touches estimates.** It right-sizes CPUs, memory and walltime from a calibration pilot.
  - Phase 5: carbon report, including CPU vs A100 and 4 vs 8 cores. Phase 6: generalisation.
  - **Report §8 :315-318 already asks** that `campaign plan` draw per-evaluation time estimates from `autolens_profiling`, and search choice and convergence cost from `autolens_inference`, "to advise how to set up the analysis (route, cores, GPU vs CPU) *before* anything is submitted", and that this dependency be added to phase 4. A new epic that produces those estimates is upstream of hpc-campaign phase 4 and should cross-reference it, not duplicate it.
- **results-library** (`draft/feature/autofit/results_library_epic.md`; `epics.md` entry `## results-library`, "NOT STARTED"). Six phases covering post-run indexing, completeness, exports and packaging. Boundary: hpc-campaign owns run time, results-library owns post-run. Its phase 0 is identical to hpc-campaign #A. No overlap with a likelihood→sampler pipeline.
- **`draft/research/autolens_profiling/matrix_free_interferometer_phase5.md`** (parent `active/matrix_free_interferometer_inversion.md`). Wires `InversionInterferometerMatrixFree` and runs a dense vs matrix-free profiling campaign (laptop CPU plus RAL `ral` CPU legs, A100 only if a JAX leg exists) at 50²–192². It produces a results note with decision rules for the assistant, a Pulse `profiling-summary`, and a workspace example. Its `Blocked-by:` says it is "Part of the human's PyAutoPulse profiling programme (anchor Pulse#62); not to be started before that programme." So it is a likely member or instance of the new pipeline. It uses the non-standard header values `Priority: medium` and `Parent:`.
- **`draft/research/pyautoinsight/slim_inference_repo_outputs_optional_zip_content.md`** (medium/safe). Inventories which zip, image and fits outputs the Insight contract actually uses in autolens_inference and autofit_inference, then slims the visualize/output configs and the samples-weight threshold. It is output hygiene for inference runs and only adjacent to the pipeline.
- **`draft/research/autolens_inference/prepared_problems_without_pickles_export_as_fits.md`** (too-large/supervised). Replaces the `analysis.dill`/`dataset.dill` prepared problems (69% of the output tree) with .fits plus json rebuilt at load, with the witness `|dlogL|<1e-8`. Adjacent: it affects how the "inference check" stage stores prepared problems.
- **`draft/feature/pyautoeyes/*.md`**: `multi_galaxy_gallery.md` (`Epic: pyautoeyes-birth`, `Phase: 6`) and `group_cluster_gallery.md` (`Phase: 7`) are visualization galleries. No overlap.
- **Other Mind hits for pulse/insight/number_of_cores/cpu_fast** (there are no hits for "optimal setup" or "auto mode"):
  - `active/cluster_pointsolver_robust_settings_p1.md`: cluster-pointsolver-speed p1, robust PointSolver settings, CPU on `ral`.
  - `draft/feature/autoarray/interferometer_curvature_preload_phase1.md`: interferometer-likelihood-campaign epic, fixed-mapper curvature reuse. That epic has 6 members but no `epics.md` entry.
  - `draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md` (euclid-dr1-prep): single-process CPU route with `number_of_cores`, a route/cores setup decision.
  - `draft/bug/autolens/runtime_single_jit_median_reach_and_a100_witness.md` (point-source-cpu-speed): runtime-cell single-JIT median and an A100 witness.
  - `draft/bug/autonerves/jax_enable_x64_env_ignored_and_fp32_leg_runs_fp64.md`: the fp32 inference leg actually runs fp64.
  - `draft/refactor/autoarray/sparse_operator_int32_indexes.md`: cuts the 172 MB sparse operator; `cpu_fast_modeling` parity.
  - `draft/bug/autofit/nautilus_ep_default_optimiser_reads_use_jax_unguarded.md`: EP Nautilus `number_of_cores=1` crash.
  - `draft/research/autofit_inference/search_ext_b5c2a_rerun.md` and `search_ext_b5c2b_scored_wave_submit.md`: search-extensibility B5c scored waves.
  - `draft/maintenance/autolens/point_source_cpu_campaign_owed_leftovers.md`: point-source leftovers.
- **Outside Mind, where profiling and inference intent now lives; these overlap most:**
  - Pulse `campaigns.yaml` `setup-baseline` (status `needs-decision`) and `tasks/setup_baseline_campaign.md`: freeze a setup baseline spec, then collect evidence (autolens_profiling#384/#416).
  - Pulse `tasks/gradient_cost_probe.md`: forward vs `value_and_grad` ms/eval with a strict FD check. This is the "gradient" stage.
  - Pulse `tasks/search_settings_estimation_infrastructure.md`: n_starts/batch_size/n_batch estimation.
  - Pulse `tasks/hst_mge_cpu_pilot.md` and `post_certified_solver_likelihood_breakdown.md`.
  - Pulse `autofit` campaign and `tasks/autofit_profiling_bootstrap.md`.
  - Insight `tasks/gradient_sampler_validated_likelihoods.md`: NUTS/HMC trial on FD-validated likelihoods "via the sampler pipeline". This is the "gradient → sampler" stage, and it needs a human decision.
  - The `epics.md` entries `search-extensibility` (autofit_inference, autofit_profiling, Insight/Pulse `fit` instances), `autolens-inference` (ledger is Insight `campaigns.yaml`), `profiling-organ-birth` and `linear-solver-programme` are adjacent precedents.

## 4. Brain conductors and faculties for a repeatable pipeline

Conductors (`agents/conductors/`): batch, bug, build, clone, community, cortex, eyes, feature, health, hygiene, intake, profiling, refactor, release, workspace. Faculties (`agents/faculties/`): memory, review, samplers, sizing, vitals.

- **profiling** (`agents/conductors/profiling/AGENTS.md`)
  - Owns the performance-data lifecycle, with `autolens_profiling` as its workspace. Modes: `campaign` (dispatch plan by tier: local or a100), `ingest` (vram tables, pins; `--axis compile`), `triage` (drift classification) (:18-34).
  - It is the only judge of what Pulse data means; Pulse only validates the contract (:121-128).
  - Refuses: editing source, dispatching Heart, judging library correctness ("Profiling records and flags; it never adjudicates library correctness", :88), developer-loop cost (that is hygiene), release-script cost (:143-148).
  - Writes nothing itself. It emits a `ProfilingDecision` for the session to execute.
  - No inference anywhere: `grep -i inference` over the conductor returns nothing.
- **sampler_pipeline skill** (`skills/sampler_pipeline/SKILL.md`, `reference.md`)
  - A development skill, not a conductor. Stages: Stage 0 ingest repo, Stage 1 prototype in `autofit_workspace_developer/searches_minimal/`, Stage 1b run on the user's own likelihood, Stage 2 profile into `comparison.txt`, Stage 3–5 promote into a PyAutoFit `NonLinearSearch`, integration scripts and docs.
  - Real-likelihood evidence goes through `autolens_inference`. "Per-evaluation likelihood cost stays with the `/profile_likelihood` skill" (reference.md:116). Inference intent is recorded in Insight and timing in Pulse (SKILL.md:75-78).
  - Under `--auto` it is two Mind tasks, trial then promotion, with one judgment gate (reference.md:276-292).
  - Refuses: edits outside `start_dev`, and growing smoke lists.
  - Validating an already-promoted search on a new likelihood is the separate "findings lane" in the samplers faculty (`agents/faculties/samplers/AGENTS.md:124-156`): experiment (wsdev `searches_minimal`) → mature (`autolens_inference/scripts/<dataset>/searches/<sampler>/`) → user-facing guides.
- **feature** (`agents/conductors/feature/AGENTS.md`)
  - The "Growth Agent": selects, sizes and phases features, then emits a `FeatureDecision` into `start_dev` (:8-13).
  - Never edits source; consults vitals and Memory. The declared `Difficulty:`/`Priority:`/`Status: blocked`/`Blocked-by:` drive its ranking (:44-58).
  - Writes no files. This is the natural planner for phasing the new epic.
- **eyes** (`agents/conductors/eyes/AGENTS.md`)
  - Owns the render → present → critique → delegate loop over the four `<lib>_visualization` instances.
  - Never renders (the project harness `gallery/gallery_run.sh` does), never edits plot source, and delegates accepted critiques via intake → start_dev (:3-10).
  - Not relevant to the pipeline beyond an optional "figures" step.
- **cortex** (not read in depth): science run ledgers, pull and checkin. Per MODEL_DELEGATION, Cortex work enters through the declared assistant.
- **profile_likelihood** lives in the science repo, not in Brain: `lens/autolens_profiling/skills/profile_likelihood/SKILL.md`. It runs the CPU/GPU × fp64/mp (+A100) sweep for one `<dataset_type> <likelihood_type>`.

**Verdict: no conductor or skill encodes the full sequence** "likelihood → profiling → Pulse → inference check → gradient → sampler".
- The pieces exist separately: `profile_likelihood` plus the profiling conductor and Pulse for timing; the Pulse `gradient_cost_probe` task for gradients; `sampler_pipeline` plus the samplers findings lane and Insight for inference and samplers.
- `sampler_pipeline` Stage 2 comes closest: it chains profile → `autolens_inference` → Insight/Pulse recording, but from the sampler side, not the likelihood side.
- A new epic would compose these. Profiling belongs to the profiling conductor and Pulse; inference and sampler belong to sampler_pipeline, the samplers faculty and Insight; phasing belongs to the feature conductor; filing belongs to intake.

## 5. `skills/MODEL_DELEGATION.md` (`organs/PyAutoBrain/skills/MODEL_DELEGATION.md`)

```
80 ## Bounded worker contract
82 - Pass only the worktree, affected files, accepted plan, required commands,
83   and the smallest relevant evidence.
84 - Give one coherent phase to a worker and reuse it for related fixes.
...
93 Long Anthropic delegations retain the existing milestone heartbeat: one short
94 line per phase/test/commit milestone in a progress file, roughly every 10–20
95 minutes of healthy work, monitored by the main session and stopped on return.
...
104 Cortex work still enters through the declared assistant and returns scientific
105 results plus assistant drift. The provider policy decides whether that work
106 uses a subagent; the assistant boundary does not force a spawn.
108 Narrative science scripts use Opus in the Anthropic family. ...
110 content heuristic is unchanged: science instruction gets teaching prose; code
111 exercise scripts get concise usage notes.
```

Related rule at :26-28: planning, worktree setup, commit/PR wording, merge decisions, registry updates and all user-facing judgment stay in the main session. Intake AGENTS.md:83-85 adds that decomposition "stays with the strongest available model; the resulting phases are what the cheaper execution models run."

## 6. `policy/`

Files: `community_surface.md`, `dashboard_copy.md`, `end_at_deliverable.md`, `end_at_deliverable_hook.sh`, `hpc_ral.md`, `never_rewrite_history.md`, `remote_sessions.md`, `session_start_hook.sh`, `shared_standards.md`, `smoke_bootstrap.md`, `smoke_bootstrap.py`, `where_to_file.md`.

`policy/hpc_ral.md` (11 lines):
- :9 GPU runs: "`hpc/sync push-submit gpu <script>` submits a SLURM `gpu`-partition array (one dataset per array task; JAX auto-uses the GPU)".
- :10 "**CPU arrays never go on `gpu` (human rule, 2026-09-30).** Bulk/production CPU-only arrays use `--partition=ral` only — never `gpu`, `ral,gpu` or `gpu,ral`, even when ral is drained or busy (wait for ral). … Only exemption: small CPU timing legs on `gpu` without `--gres` with ≤8 CPUs/task, throttle ≤`%2`, and no pending GPU jobs (`squeue -p gpu -t PD` shows no gres/gpu). Partition ≠ device: check TRES for gres/gpu with `scontrol show job` before calling it a GPU run".

The same rule is stated at length in `hpc_campaign_epic.md:24-49`.
