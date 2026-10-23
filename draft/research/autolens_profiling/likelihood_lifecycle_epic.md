# Likelihood lifecycle epic: optimal setups baked into PyAutoLens, Pulse/Insight day zero, and one repeatable profiling → inference → gradient → sampler sequence per likelihood

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoPulse
- autolens_inference
- PyAutoInsight
- PyAutoNerves
- PyAutoArray
- PyAutoLens
- PyAutoBrain
- PyAutoMind
Themes:
- profiling
- samplers
- hpc-gpu
- dashboard
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Witness: phase 0 — `pyauto-pulse check` accepts a `profiling-summary@3` catalogue in which every record carries `class` and `status` and refuses a second `current` record on one key, the Pulse board's first selector is Class with Optimal as the default, and a test in autolens_profiling asserts `results/<dataset_type>/<variant>/` mirrors `scripts/<dataset_type>/<variant>/`; phase 5 — `al.Setup.auto(dataset)` on a CPU-only host and on an A100 host resolves to the setup the Pulse designation decision names optimal for that likelihood and regime, prints the two-line setup banner at fit start, writes `setup.json` beside the search output, and a parity test proves the library rule table equals the Pulse designations
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Filed: 2026-10-21

Repos touched beyond the header list (one issue per repo per phase): autolens_visualization, PyAutoEyes, PyAutoGalaxy, PyAutoFit, autolens_workspace, autolens_assistant, PyAutoCortex.

Research report, architecture and detailed phase bodies: `likelihood_lifecycle_epic_report.md` alongside this file (written 2026-10-21 by the Fable 5.1 xhigh architect session from five Explore surveys in `likelihood_lifecycle_epic_surveys/`; no code edited). This file is the ledger: the phase cards, the human rulings, the orchestration protocol and the running status.

## Summary

Four projects share one job and no vocabulary. `autolens_profiling` measures what one likelihood evaluation costs and publishes to **PyAutoPulse**; `autolens_inference` runs whole fits and publishes to **PyAutoInsight**; both organs validate and render, judge nothing, and the Brain's profiling conductor judges. Today nothing in any of them says which measurement is *current* or which setup is *optimal*, the two project repos use different setup grammars and results trees that do not mirror their scripts, and nothing in the library chooses a compute setup from the hardware and the data (report §1).

This epic gives the four projects one vocabulary (likelihood, instrument, regime, setup, class, status, model variant, measurement), a `profiling-summary@3` contract that carries producer-declared `class` (optimal / secondary / experimental) and `status` (current / superseded / archived), results trees that mirror `scripts/` with a dated `archive/`, a Pulse board whose first selector is Class and whose default view is current-only, inference wall-time validation as a Pulse evidence axis, Insight records that assume `setup_mode: auto`, and, once the evidence is in, `setup="auto"` in the source with a banner, a `setup.json` and a run-time estimate. It ends by turning the sequence into one Brain verb so a new or re-optimised likelihood re-runs the chain from a single command (report §3.9).

Three invariants hold throughout: a designation of "optimal" is always a Pulse decision record backed by cited evidence, never something a dashboard infers; exactly one record is `current` per (likelihood, instrument, setup, host class, model variant, measurement), chosen by the producer under the day-zero rule, never by date; and auto decides only implementation choices (backend, device, operator, precision, route, threads, default cores), never the model, the sampler or the HPC request (report §3.4).

## Phases

Epic slug `likelihood-lifecycle`. Library first in every phase. One issue per repo per phase; each ships on its own behind `start_dev` → `ship_library` / `ship_workspace`. Phase prompts are filed lazily, one per phase, with `Epic: likelihood-lifecycle` and an integer `Phase:`; sub-issues are lettered inside the prompt body. Issue one phase at a time, never the whole map. Detailed bodies: report §4.

### Phase 0 — Spine: vocabulary, contracts, mirrored trees, day-zero history cut (PyAutoPulse, autolens_profiling, autolens_inference, PyAutoInsight, PyAutoBrain) — no dependencies
- Goal: one vocabulary (report §3.1); `profiling-summary@3` with `class`/`status`/`figures`/`decision_id` and the `walltime-validation@1` evidence axis (§3.2); `results/` and `wiki/campaigns/` mirror `scripts/` in both project repos with `archive/YYYY/MM/<slug>/` (§3.7); the history labelled current / superseded / archived without re-running anything (§3.6); Insight accepts `setup_mode: auto` + `setup_resolved`; the lifecycle sequence written as a template (§3.9).
- Sub-issues in order: 0A Pulse contract + board (rebase after Pulse PR #68) → 0B autolens_profiling (commit nothing new first; move-only PR from a migration map, then the catalogue builder, misc grouping polish, coverage matrix tool, parity convention) → 0C autolens_inference (commit the untracked clean-slate rows in their own PR, then move-only, then the exporter) → 0D Insight additive fields + doc drift → 0E Brain lifecycle template + conductor grid on the new tree.
- Human gates: rulings R1–R3, R7, R8 (below); approval of each move-only PR (data guard; moves and content never in one PR).
- Witness: the phase-0 witness in the header. Size: large (0B is the bulk). Compute: none.

### Phase 1 — Figures: every dataset type's fit.png to the human's satisfaction, and a figure step inside profiling campaigns (autolens_visualization, PyAutoEyes, autolens_profiling) — no dependency on 0; before 2
- Already shipped 2026-10-21: autolens_visualization PR #5 covers all ten dataset types with `dataset.png` + `fit.png` (72 figures). Remaining: 1A the `/eyes` review loop over the ten `fit.png` with the human (critiques → intake), and re-scoping the two stale Eyes drafts (`draft/feature/pyautoeyes/multi_galaxy_gallery.md`, `group_cluster_gallery.md`) to group point-source, cluster extended + image-plane, bespoke point/cluster/weak figures; 1B `_profile_cli.py` renders and keeps `fit.png` per cell through the viz plotter, `figures[]` in the catalogue, the inspection step written into `skills/profile_likelihood` and the campaign template.
- Witness: ten `fit.png` signed off by the human; the profiling CLI writes `fit.png` for a named cell on CPU. Size: medium. Compute: laptop.

### Phase 2 — Profiling campaigns for every dataset type under Optimal and Secondary setups (autolens_profiling → Pulse) — depends on 0 and 1
- One issue per dataset type or natural pair (imaging; interferometer; point_source image + source; multi_galaxy + group; cluster; multi_dataset + datacube; weak). The coverage matrix names the missing and stale cells; scripts are added where absent (group, multi_galaxy, weak are new); RAL runs with CPU on `ral` only and A100 with `--gres`, authorised per batch; every cell carries parity, provenance, `fit.png` and the pinned tag; results land as `current`, prior cells become `superseded`; the campaign page lives at the mirrored wiki path with its pre-registered rule and verdict. Imaging reuses the 2026-10-17 rectangular/Delaunay × numba/JAX × CPU/GPU results that are on the pinned tag. multi_galaxy, group and cluster at standard size only (`regime: standard`). Adopts Pulse `hst_mge_cpu_pilot`.
- Witness: the coverage matrix shows zero missing cells for class ∈ {optimal, secondary} × measurement ∈ {runtime, breakdown} across the ten dataset types.
- Human gate: the explicit "campaigns complete" confirmation that opens phase 3. Size: large; compute heavy.

### Phase 3 — Day zero: freeze the baseline and fully populate the Pulse board (autolens_profiling, PyAutoPulse) — depends on 2 confirmed
- Pin one released tag; re-measure the Optimal/Secondary cells not on it; stamp `day_zero`; Pulse snapshot `day_zero`; one `designation` decision per likelihood × hardware class (the conductor drafts, the human records); `wiki/campaigns/<dataset_type>/<variant>/day_zero.md` decision rules written in terms of dataset properties; the stalled `setup-baseline` campaign adopted and closed with its 1,044-slot manifest replaced; Coverage shows no `not_measured` Optimal cell; the `runtime_estimates` export exists for phase 5E.
- Witness: Pulse snapshot `day_zero` exists; every Optimal cell is current, measured on the tag, and designated by a decision record. Human gate: confirm the freeze (R10). Size: medium.

### Phase 4 — Inference wall-time validation on RAL (autolens_inference → Pulse) — depends on 3
- Per dataset type the full model (SLaM where it exists) under the Optimal GPU and Optimal CPU setups plus the Secondary CPU setup, seeds ≥ 2; a cores sweep on `ral` for the CPU likelihoods; `model_variant: light_fixed` only under Optimal; records with `implied_ms_per_eval`, `ratio_measured_over_predicted`, `parallel_efficiency` and `parity_status` published as `walltime-validation@1`. Adopts the clean-slate base rows of `hst-imaging-mass-samplers`; never re-runs what exists on the tag. The 2026-10-18 jax_gpu_sparse light_fixed divergence is the first `diverged` row and blocks that setup's Optimal designation until explained.
- Witness: every Optimal setup has a validation record with its ratio; one parallel-efficiency curve per CPU likelihood sets the cores cap for 5D. Human gate: compute authorisation (R9). Size: large; compute heavy.

### Phase 5 — Optimal setup baked into the source: `setup="auto"`, environment, banner, `setup.json`, run-time estimate, docs, assistant, science projects — depends on 3 (rules) and 4 (cores cap, efficiency)
- Library-first sub-issues: 5A PyAutoNerves (environment probe; `PYAUTO_SETUP` honoured at import; the x64 bug) → 5B PyAutoArray (`aa.Setup`, `Setup.auto`, rule table generated from the Pulse designations, `dataset.apply_setup`, operator/backend consistency check, transformer choice by regime) → 5C PyAutoGalaxy + PyAutoLens (`setup="auto"`, `setup.json`, two-line banner, one setup threaded through SLaM, defaults aligned) → 5D PyAutoFit (`number_of_cores="auto"`, banner hook, metadata) → 5E estimator (`al.Setup.estimate`, `runtime_estimates.yaml` exporter in autolens_profiling, PyAutoLens data file) → 5F autolens_workspace + HowToLens (stale prose retired, `cpu_fast_modeling.py` becomes the override example, `example_cpu_and_gpu.py` fixed, concise CLI explanation) → 5G autolens_assistant (`al_explain_setup`; `al_configure_search` rewritten) → 5H science projects (`--use_cpu` → `--setup`; env blocks removed). Boundary per report §3.4; layering per §3.5.
- Human gates: approve the auto/explicit boundary table (report §3.4) and the rollout (R6). Witness: the phase-5 witness in the header. Size: too-large → each sub-issue medium or large.

### Phase 6 — Gradient: `value_and_grad` breakdowns for every likelihood under its Optimal setup (autolens_profiling → Pulse) — depends on 2; may run alongside 4–5 (R11)
- Adopts Pulse `gradient_cost_probe`: forward vs `value_and_grad` ms/eval plus a strict finite-difference check on every Optimal cell; `measurement: gradient` records; a hazard and its own optimisation prompt wherever grad/forward exceeds ~4× or the FD check fails; `gradient_breakdown.py` per likelihood in the mirrored scripts tree.
- Witness: a current gradient record with a passing FD check for every Optimal setup. Size: medium; compute moderate.

### Phase 7 — Sampler campaign on Optimal setups under `setup_mode: auto` (autolens_inference → PyAutoInsight; research wikis) — depends on 5 and 6
- Per dataset type: Nautilus control, gradient samplers and non-gradient samplers as capability allows, ≥ 3 seeds, a pre-registered protocol (success rate with intervals, wall per right answer, evaluations-to-converge), `model_variant: light_fixed` only under Optimal, a research wiki per dataset type at the mirrored path, Insight board and decision records, and the evaluations table that refreshes the estimator. Adopts the `hst-imaging-mass-samplers` wave plan and Insight `gradient_sampler_validated_likelihoods`. Runs through the sampler_pipeline skill and samplers faculty; Insight stays conductor-free.
- Witness: Insight shows ≥ 3-seed scored rows per sampler per dataset type with `setup_mode: auto`. Human gates: protocol freeze; compute. Size: large; compute heavy.

### Phase 8 — The lifecycle as a Brain verb (PyAutoBrain, PyAutoMind) — depends on 0E; finalised after 7
- `pyauto-brain profiling lifecycle --likelihood <dataset_type>/<variant> [--instrument …] [--trigger new|reoptimised]` reads the taxonomy and coverage matrix and emits the epic ledger plus integer-phased prompts for the §3.9 chain, which intake files. Dogfood on `draft/research/autolens_profiling/matrix_free_interferometer_phase5.md`. No inference conductor is created.
- Witness: the verb's prompts pass `intake census` hygiene and the dogfood instance runs its chain through L4. Size: medium.

## Human rulings needed before phase 0 (recommendations in report §5)

R1 vocabulary and `setup_id` grammar (recommend: as §3.1). R2 day-zero history cut: label only, delete nothing (recommend: yes). R3 provisional designations as the phase-0 labels (recommend: accept, phases 2–3 confirm). R4 mixed precision `experimental` until the x64 bug is fixed (recommend: yes). R5 compile cost not an Optimal-class axis (recommend: yes). R6 `setup="auto"` opt-in release then default flip (recommend: opt-in first). R7 `host_class` is provenance; laptop rows never `current` (recommend: yes). R8 Insight folders `…/<sampler>/auto/seed_<n>` (recommend: yes). R9 compute authorisation per phase and batch; CPU on `ral` only (recommend: phase 2 on missing cells only). R10 `setup-baseline` adopted and closed by phase 3 (recommend: yes). R11 phase 6 may run alongside 4–5 (recommend: allow).

## How to orchestrate (for the session that runs this)

1. Read this file and report §3–§4. Open a survey only when a phase body cites it. Do not re-survey.
2. Per phase: file `draft/<type>/<target>/likelihood_lifecycle_p<N>_<slug>.md` with `Epic: likelihood-lifecycle`, `Phase: <N>` (integer), the phase's witness, `Blocked-by:` for its dependency, then `/start_dev` it. Library first; one issue per repo per phase; sub-issues lettered in the body.
3. Delegation: the orchestrating session keeps planning, worktree setup, PR wording, registry updates and every human conversation; edits, tests, prose and ship phases go to Opus workers with a progress file per worker (Brain `skills/MODEL_DELEGATION.md`). Narrative science prose stays Opus.
4. Data guards: move-only PRs are separate from content PRs and never inside a feature PR; the untracked autolens_inference rows are committed before anything moves; RAL checkouts are never moved under a live job.
5. Compute: CPU arrays on `--partition=ral` only, never `gpu` or `ral,gpu`; A100 jobs request `--gres`; every batch has an explicit human go; never reorder or cancel another campaign's jobs.
6. Sessions end at their deliverable: no self-armed timers, loops or subscriptions to wait for CI, a review or a merge; the human runs `/prm`. Pulse PR #68 is open and unmerged: rebase phase 0A after it.
7. Releases: library phases ship pending-release; the day-zero pin (phase 3) must be a released tag, so a human `/review_release` sits between phases 2 and 3 and another between 5 and 7.
8. After each phase: append a dated entry to the Ledger below (issues, PRs, records, what changed in the rulings), update the `epics.md` status line, regenerate the Mind dashboard and push through the shared-checkout procedure (temp worktree + cherry-pick when the canonical Mind checkout is dirty).

## Adopted and adjacent work

- Adopted: Pulse `setup-baseline` campaign + `tasks/setup_baseline_campaign.md` (→ 3), `tasks/gradient_cost_probe.md` (→ 6), `tasks/search_settings_estimation_infrastructure.md` (→ 5E), `tasks/hst_mge_cpu_pilot.md` (→ 2); Insight `hst-imaging-mass-samplers` (base rows → 4, wave plan → 7), `tasks/gradient_sampler_validated_likelihoods.md` (→ 7); Mind `draft/research/autolens_profiling/matrix_free_interferometer_phase5.md` (→ 8 dogfood), `draft/bug/autonerves/jax_enable_x64_env_ignored_and_fp32_leg_runs_fp64.md` (→ 5A), `draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md` (→ 5H), `draft/feature/pyautoeyes/{multi_galaxy,group_cluster}_gallery.md` (→ 1A re-scope).
- Adjacent, untouched: `hpc-campaign` phase 4 consumes this epic's estimates; `results-library` owns post-run indexing; `search-extensibility` B5c waves continue on autofit_inference; the cluster PointSolver robust-settings and cowls/ansofi science work continue under their own ledgers and are not re-run here.

## Original request (verbatim, 2026-10-21)

- We need to revist Pulse, Insight, _profilng and _inference and really hone exaclty what the setup is between these
four projects. This will include having the "optimal" setups as prominent (e.g. numba sparse cpu, JAX gpu dense)
and the other set ups as secondary. I think on the dashboard this selection of "optimal" or "secondary" will be on the very first set of panel selecctions.
On Insight we will assume runs are always using the optimal setup on GPU, 
I think that _fixed_light runs can anotehr term called "variant", which only run using the optimal sevtup.

- In fact, I think we need to bake the notion of "optimal" into the source code, whereby the setup is chosen 
automatically based on the available hardware, the dataset and the nature of the computation, and it should make sure and set 
environment variable required for that setup. For interferometry the optimal
setup depends on the number of visibilities, and this itself changes depending on CPU or GPU. I suspect the same
situation will play out for image and source chi, and group and cluster datasets. It require ssome thought given how
optimal can change depending on the data how we ensure that is cleanly readable in the PyAutoPulse dashboard. This is a whole
epic intake in and of itself, and also requires documentation updates throughout the workspace and concise clear text
explaining this on the command line when autolens runs.
- 
- For Pulse, I think we first need a day zero clean up of the history, and we need to have a mechanism that ensures that typically
only the most recent resutls are on the dashboard and looked up when AI does research. These would be the results that directly
correspond to the automatic choice of dataset setup.

- I now appreciate that the autolens_infernece runs we've done so far are not really about PyAutoInsight (e.g. they are not yet comparing samplers)
but instead they are validating the likelihood evaluation time estimated in Pulse and checking that the inference times scale accordingly,
helping put some numbers against things like how efficent is CPU parallelization. I thikn that this is extra information that
needs to make its way to the suitable information slots on the PyAutoPulse dashboard.
- 
- When explicitly PyAutoInsight runs which are about comparing samplers, the folder names should not be the specific setup
  (e.g. [hpc_ral_numba_cpu_sparse_fp64]) but instead they should be assumed to use the optimal setup and always run on
A100 GPU if the sampler is using JAX gradient, if the sampler does not use gradient still just use optimal GPU setup. 


Lets produce an epic which address this in the most logical order feasible:

Dataset types which need autolens_profiling and autolens_inference entries:

imaging
interferometer
point source image chi squared
point source source chi squared
multi_galaxy
group
cluster
multi dataset
datacube (inside interferometry)
weak

1) Setup PyAutoEyes on all the above dataset types and ensure the fit.png file we need for each, which is definitely something
we need to inspect during _profiling campaigns, is to my satisfaction.

2) Perform all autolens_profiling and PyAutoPulse optimization campaigns for all datasets above. For imaging, the 
current most recent results show all the variants we want to optimize (rectangular, Delaunay) / (numba, JAX for GPU and CPU). 
Many of these campaigns are already on the PyAutoPulse dashboard, but some are not, and thus should be added. For multi galaxy,
group and cluster we could in priciple need to do profiling depending on how large they are (and thus number of galaxies)
but for now just use their standard setup and we'll make this a dimension we come bck to in the future.

3) in autolens_profiling and PyAutoPulse complete all "day zero" optimization and fully populate all information throughout
the dashboard. This can only happen once all the profiling loops in 2 are done to a point I confirm they are complete.

4) Perform autolens_inference runs like those which are in the inference folder currently, which validate the run times on
RAL for a full lens model which can be compared to the day zero results as an indepedent check and put more context and
information on them.

5) Use all this information to determine the optimal setup for all the different datasets and setups, which then becomes factories
in the source code with an "auto" mode the default and maybe even a in built mechanism to give the suer a number of samples 
and run time prediction metric. This then has all the workspace updates, AI assistant updates (e.g. being able to explain
the auto choice and look at the autolens_profiling and autolens_inference repos to explain further where the run time
estimate and slow down comes from.)

6) Go over all autolens_profiling run breakdowns but with jax.grad instead of just jax.jit, so we can make sure all
gradient calculation run times are optimal.

7) We are now at the point for all likelihood functions where PyautoLens automatically chooses an optimal setup
and we can begin a true PyAutoPulse campaign to try different samplers (optimal only on GPU) and write up their
results both as research wikis but also as inspectable things to dashboard.

At this point, its clear we have a logical sequence of how we go from a likelihood function (which could be a variant
that depends on the model type, dataset type, JAX or numba) to optimizing it, putting run time estimates in
autolens_profiling, PyAutoPulse dashboard, inference runs to check against, and then gradient and sampler runs.
If I add a new type of model or dataset or even just optimize an existing one by changing the approch (and thus updating
what is its cuirrently "active" or "best") profiling times this structure should be reproduceable or easy for me to
instruct AI. I think this is a specific brain feature agent which lays out a Mind issue with this sequence of tasks?

I think its also clear that autolens_profiling has grown extremely large and unordered and has become very hard
to manage, when the prompt above is me trying to basically condense it down to a more structured format. The scripts
folder is good, it has a structure which makes it easy to find a given script and setup. The results folder is
a mess without structure and makes it hard for a human to navigate (which should be the goal even if this is mostly)
AI facing. I think the results folder should mirror the scripts folder so we have one centralized method of
navigating things that is categorized sensible (note how this also mirrors the PyAutoPulse dashboard). I think the
same should also be true of the wiki folder, which has aspects which are but I think "campaigns" can adopt the same
folder structure. I think the misc folder has loads of scripts and is impossible for a human to make sense of,
I think putting all non dataset specific stuff in misc is good as there is a lot of misc stuff but this folder
also needs some sort of grouping to help a human. I think a census of whether this also has a lot of old stuff
we can remove or archive with date (e.g. autolens_profiling/achive/2026/motnh) would help as we need to avoid this
repo becoming a monster like it is now. 

I think that autolens_inference is doing ok, it seems more structured but even its results folder would benefit
from being dataset folder names with a misc and prob having an achive put in.


At the end of all this we also need to ensure optimal mode streamlines the different CPU settings which
require a number_of_cores input to start Python multiprocessing, which is true across all scripts
but a particular challenge for SLaM pipelines:

❯ For the autolens_workspace slam.py examples, does this all mean a user has to manually adapt them to support CPU and GPU?

  Searched for 1 pattern, ran 2 shell commands

No. The same script runs on a GPU or a CPU without changes. The use_jax=True comment in scripts/imaging/start_here.py:344 says it directly: JAX uses the GPU if there is one, otherwise multithreaded CPU. Every autolens_workspace SLaM example passes use_jax=True, so a user with no GPU just gets JAX on the CPU.

What --use_cpu in euclid_dr1 and now cowls_ansofi switches on is a different, optional route: Numba plus a multiprocessing pool, with the CPU sparse operator. It's an optimisation for one case only: pixelized sources on a many-core CPU. There it can beat JAX on a GPU, because the pixelized inversion relies on sparse linear algebra that JAX doesn't handle well. For light-profile or MGE fits, JAX is faster even on a CPU.

The workspace already shows that route in separate examples rather than as a switch:
- scripts/imaging/features/pixelization/cpu_fast_modeling.py, which includes a CPU-fast SLaM section
- scripts/multi_galaxy/features/pixelization/cpu_fast_modeling.py

So the main SLaM examples work anywhere as they are. A user who wants the fast Numba path for pixelized sources follows cpu_fast_modeling.py. That means editing by hand: use_jax=False on each analysis, apply_sparse_operator_cpu() again after every apply_over_sampling (that call drops it), and number_of_cores.

The one real gap is that last step. Moving a pixelized SLaM script to the fast CPU route means touching every stage, which is why the science projects added a --use_cpu switch. If you want the workspace to offer the same switch, for example in slam_start_here.py or cpu_fast_modeling.py, I can file it as a workspace prompt. I don't think it's needed for users to run the examples.

I guess we need to balance if optimal mode is gonna try and do _everything_ or if we still need it to be on the user
explicit side, think hard about where this separation is for different likelihood functions.

## Status

- 2026-10-21: filed by the Fable 5.1 xhigh architect session with the report and five surveys. NOT STARTED: no phase issued; rulings R1–R11 open.
- 2026-10-21 (later): phase 0 IN PLANNING — 0A prompt filed and planned via `/start_dev`; 0A MERGED (PyAutoPulse#70, record complete/2026/10/likelihood-lifecycle-p0-pulse.md); next 0B autolens_profiling (see Ledger). Next: approve → create_issue → start_library on PyAutoPulse → Opus worker implements → ship_library; then file 0B.

## Ledger

(append one dated entry per phase: issues, PRs, Mind records, ruling changes)

- 2026-10-21 (phase 0 opened, Fable 5.1 medium orchestrator): sub-issue 0A prompt filed at `draft/feature/pyautopulse/likelihood_lifecycle_p0_pulse_contract.md` (`Epic: likelihood-lifecycle`, `Phase: 0`) assuming rulings R1, R2, R3, R7 as recommended and R4/R5 as validator enumerations only; `/start_dev` run to the plan; plan approved in chat; issue https://github.com/PyAutoLabs/PyAutoPulse/issues/69, branch `feature/likelihood-lifecycle-p0-pulse`, prompt moved to `active/`. Pulse PR #68 still open — 0A branches from main and rebases after it. 0B–0E prompts are filed one at a time once 0A ships.
- 2026-10-21 (0A shipped to PR): Opus worker implemented all ten steps on `feature/likelihood-lifecycle-p0-pulse` (5 commits daa131d…d08db2f; ruff clean, pytest 296 passed vs 207 on main, node browser checks pass, `pyauto-pulse check --offline` OK; witness run by hand with a scratch registry). PR https://github.com/PyAutoLabs/PyAutoPulse/pull/70 open, tier judge → human `/prm`. Heart YELLOW at ship (workspace manifest drift; PyAutoArray release validation stale), unrelated to Pulse. **Contract deviations from report §3.2 recorded on the PR:** v3 records carry `metric`/`unit`/`values` (not v2's `measurement: {metric: value}`); v3 has no `setups[]`/`selections[]` — each record declares its setup and `planned_cells` replaces selections; `decision_id` resolves against any `decisions.yaml` entry until phase 3 writes designations. 0B's catalogue builder must emit this shape (REFERENCE.md "`profiling-summary` v3"). Pulse PR #68 still open; no drift on main so no rebase was needed. MERGED 2026-10-21 by human `/prm` (91870ade); issue #69 closed; record `complete/2026/10/likelihood-lifecycle-p0-pulse.md`. **0A DONE.**
- 2026-10-21 (0B queued, 0C planned): 0B prompt `draft/feature/autolens_profiling/likelihood_lifecycle_p0_profiling.md` filed and registered in `planned.md` — autolens_profiling is claimed by `cluster-pointsolver-robust-settings` (#436, 5 unmerged commits, live RAL sweeps), so the move-only PR waits. 0C prompt filed, plan approved, issue https://github.com/PyAutoLabs/autolens_inference/issues/41, task `likelihood-lifecycle-p0-inference` on `feature/likelihood-lifecycle-p0-inference`; it depends on 0A only, so it runs ahead of 0B (`reference_runtime_record_id` re-pointed when the `lens` pin moves to @3).
- 2026-10-21 (0C shipped to PRs): Opus worker built three stacked branches; verified ruff clean, pytest 216, exporter `--check` current, `pulse.walltime.validate` clean. PRs https://github.com/PyAutoLabs/autolens_inference/pull/42 (63 clean-slate files committed, README regenerated) → #43 (move-only, 177 renames, map `catalogue/migration_2026_10.json`, mirror test) → #44 (lifecycle fields + `dashboard/walltime_validation.json` as `walltime-validation@1`, 56 records). Tier judge → human `/prm` in order. **Findings for the epic:** 0 of 56 walltime records match a Pulse lens@2 runtime record (lens@2 HST records never state dense/sparse; only Delaunay-1500 A100 exists) — the `predicted_ms_per_eval` column fills only after 0B re-pins `lens` to @3 with per-record `setup_id`; `parity_status` is a declared `PARITY_RULINGS` table (only the 2026-10-18 jax_gpu_sparse light_fixed divergence → 2 `diverged` rows, nothing `match`); stage folded into `sampler` as `nautilus:<stage>` plus a `stage` field; SLaM jax_cpu rows keep `hpc_a100` (host null). MERGED 2026-10-21 by human `/prm`: #42 acafb68 → #43 07880c2 → #44 bdc8b2d; PyAutoPulse#71 a7ef9ba (registry row `lens-walltime`, 56 records on the board); PyAutoCortex#74 (ledger note + re-rendered dashboard). Issue #41 closed; record `complete/2026/10/likelihood-lifecycle-p0-inference.md`. **0C DONE.** Phase 0 remaining: 0B (queued behind cluster-pointsolver), 0D PyAutoInsight, 0E PyAutoBrain.

- 2026-10-23 (0D opened, Fable 5.1 orchestrator): found Insight's `lens` receipt `invalid` since the 0C merge (bdc8b2d) — the committed `prepared/<id>/manifest.json` reference pre-move record ids and ~43 records name an unemitted prepared problem (producer-side 0C regression; the additive fields themselves pass Insight's validator, so no `inference-summary` bump). 0D prompt filed at `draft/feature/pyautoinsight/likelihood_lifecycle_p0_insight.md` → `active/`; plan approved in chat (human: infrastructure only, all Insight results are rerun later under Optimal setups); issue https://github.com/PyAutoLabs/PyAutoInsight/issues/39, task `likelihood-lifecycle-p0-insight`, branch `feature/likelihood-lifecycle-p0-insight` in PyAutoInsight + autolens_inference (PR 1 exporter reference fix, PR 2 Insight fields/`setup_resolved` provenance/doc drift; witness = `receipts/lens.json` back to ok). Note: `planned.md` marks 0B unblocked (cluster-pointsolver-robust-settings merged 2026-10-22) but the human has the cluster-pointsolver starting-grid work live on autolens_profiling in another session — 0B stays queued until that claim clears.
- 2026-10-23 (0D shipped to PRs): Opus worker built https://github.com/PyAutoLabs/autolens_inference/pull/45 (exporter publishes migration-mapped prepared-problem ids; 15 dangling `problem_id` withheld with reasons; new reference-resolution test; artefacts re-exported; pytest 218) and https://github.com/PyAutoLabs/PyAutoInsight/pull/40 (`lifecycle_errors` in `summary.validate` for v1/v2/v3; `Setup:` provenance line; REFERENCE/README/CHECKIN drift fixed, walltime-validation routed to Pulse; pytest 219). Insight validator 0 errors on the fixed catalogue (was 57: 36 artifact + 6 baseline + 15 problem). Tier judge → human `/prm`, #45 FIRST; #40 `lint` red only on the committed invalid lens receipt (pre-existing on main) until the Insight refresh rewrites it to ok (= 0D witness). Heart YELLOW at ship, unrelated. Phase 0 remaining after 0D merges: 0E (Brain lifecycle template), 0B (queued behind the autolens_profiling starting-grid claim).
- 2026-10-23 (0D DONE): human `/prm` — autolens_inference#45 MERGED 5bdae73 (its `Publish inference summary` run dispatched the Insight refresh b3e8e1d1 → `receipts/lens.json` ok at 5bdae73a, 284 records: **0D witness met**); PyAutoInsight#40 lint was red only on the stale committed receipt → origin/main merged into the branch (f0543ae), fresh CI green, MERGED f2b38228; issue #39 closed; record `complete/2026/10/likelihood-lifecycle-p0-insight.md`. **0D DONE.** Phase 0 remaining: 0E (PyAutoBrain lifecycle template + conductor grid) next; 0B queued behind the autolens_profiling starting-grid claim.
- 2026-10-23 (0E queued): prompt `draft/feature/pyautobrain/likelihood_lifecycle_p0_brain.md` filed (template `skills/profiling/lifecycle.md` with §3.9 L0–L7 as a renderable phase-prompt template; profiling conductor `campaign` reads a `profiling-summary@3` catalogue + §3.7 mirrored `results/` tree by feature-detection with per-class coverage, legacy byte-identical; samplers faculty mature tier → `scripts/<dataset_type>/<variant>/samplers/`; Pulse/Insight read prose: current+optimal default, walltime-validation is Pulse's, Insight `setup_mode: auto`). Heart STALE at the door. Brain Feature Agent: library workflow, direct. **Hard conflict**: PyAutoBrain claimed by `github-token-p2b-writers-app` (PyAutoBrain#534, another live session) → registered in `planned.md` as `likelihood-lifecycle-p0-brain`; `/start_dev` resumes when that task ships. 0E does not wait on 0B (fixture-proven reader; live witness with 0B).
- 2026-10-23 (0E opened under human claim override): human authorized proceeding on PyAutoBrain alongside `github-token-p2b-writers-app` (#534). Issue https://github.com/PyAutoLabs/PyAutoBrain/issues/535, task `likelihood-lifecycle-p0-brain` promoted planned.md → active.md (library-dev), branch `feature/likelihood-lifecycle-p0-brain`, worktree `~/Code/PyAutoLabs-wt/likelihood-lifecycle-p0-brain`. Opus worker implements (a) `skills/profiling/lifecycle.md` template, (b) conductor @3/mirrored-tree coverage by feature-detection (fixture-proven, legacy byte-identical), (c) samplers faculty paths, (d) Pulse/Insight read prose.
- 2026-10-23 (0E shipped to PR): https://github.com/PyAutoLabs/PyAutoBrain/pull/536 (185a370): `skills/profiling/lifecycle.md` L0–L7 template (8 prompt blocks, `Epic: lifecycle-<dataset_type>-<variant>`, integer phases, 5 placeholders; test renders imaging/delaunay through intake `census()`); conductor `campaign` → per likelihood × class × measurement grid (current/stale/superseded/missing) on a @3 catalogue, `SetupIdError` on bad grammar, `local_*` never current, class reported as declared, CPU→`ral` / A100→`gpu --gres`; legacy byte-identical (live dry-run sha be73b898… before=after); samplers faculty reads `scripts/<dataset_type>/<variant>/samplers/` (3 point_source + 8 imaging cells live, `validation/` own tier); prose updated. pytest 1268→1282. Deviations: stale judged vs envelope `release_pin` else newest record pin (@3 has no catalogue-level pin — possible Pulse follow-up); v3 `--tier` echoed, routing by `host_class`. Tier judge → human `/prm`. Heart YELLOW at ship, unrelated.
- 2026-10-23 (0E DONE): human `/prm` — PyAutoBrain#536 MERGED a64b7990 (Brain Tests 3.12/3.13 green, CLEAN, no freeze); issue #535 closed; record `complete/2026/10/likelihood-lifecycle-p0-brain.md`. **0E DONE.** Phase 0 remaining: 0B only (queued behind the autolens_profiling starting-grid claim). Phase 1 (figures) has no dependency on 0 and may be filed next; phase 8 renders `lifecycle.md`.

- 2026-10-23 (0B opened, Opus 5.5): claim guard clear on autolens_profiling + PyAutoPulse (cluster-pointsolver starting-grid #439/#440 merged). Plan approved in chat; issue https://github.com/PyAutoLabs/autolens_profiling/issues/442, task `likelihood-lifecycle-p0-profiling`, branch `feature/likelihood-lifecycle-p0-profiling`; prompt → `active/`, planned.md row removed. Plan decisions: R3 provisional Optimal rows emitted `class: secondary` + `provisional_optimal: true` in `limitations` (Pulse requires `decision_id` for `optimal`); mirror test lives in `scripts/misc/test/`; the move-only PR carries map-derived path-index rewrites (grandfather manifest, script_routes/wiki_bindings destinations, `ALLOWED_NOTES_DIRS`) so main stays green. Sequencing: open autolens_profiling#441 (cluster decision docs) touches two move targets → map sha256 recomputed and move PR opened only after #441 merges; never under live RAL jobs on a RAL checkout. Six autolens_profiling PRs + one Pulse re-pin, tier judge → human `/prm` each.
- 2026-10-23 (0B PR 1 map drafted + §3.7 rulings): Opus worker built `scripts/misc/tooling/build_migration_map.py` + `catalogue/migration_day_zero.json` (7b9e9e34, unpushed): 1,509 files (1,481 `results/` + 28 wiki pages), no collisions, `--check` mode, tests/ruff green — but **952 unresolved (63%)**: §3.7 as designed fits about a third of the tree. Human rulings (chat): (a) optional `<model_variant>` path segment after `<host_class>` for non-default variants (light_fixed 428 files mirrored, not archived; `_rtu`, `numba_mge_mass`); (b) size scans → `<cell>/scans/`, experiment arms + experiment-script outputs → `<cell>/experiments/`, else `results/misc/<group>/`, never `current`; (c) CPU jobs on RAL GPU nodes → `hpc_ral_cpu`, host-less `_v…` summaries → archive; (d) sparse interferometer W~ → `_wtilde` per §3.3 (setup_id names the likelihood route, not the transformer class). Map regeneration in progress.
- 2026-10-23 (0B PR 1 open): rulings applied (c9ffd9ee) — unresolved 952 → 23 (19 dense interferometer/datacube rows with no transformer recorded, 4 cluster image_plane with no instrument); kinds mirrored 212 / scan 204 / experiment 418 / misc 198 / archive 272 / lens_component 97 / wiki_campaign 82 / unchanged 3; 20 setup_ids; history 0 (every multi-release series was host-less → archived). PR https://github.com/PyAutoLabs/autolens_profiling/pull/444, tier judge → human `/prm` after reviewing the map. Open for the human: only 2 light_fixed rows are `current` (all sized `_nN` rows are scans) — name a production nN per mesh before the builder PR if one exists. #441 still open: rebase + rerun the generator after it merges.
- 2026-10-23 (0B PR 1 MERGED): human `/prm` — autolens_profiling#444 MERGED aeef2756 (lint green; main had moved only by the CI-only #443, so the map was current). #441 still open — PR 2 regenerates the map first if it has merged (lint does not gate on the map's `--check`, so main stays green either way). Issue #442 and the task stay open. Next: PR 2 move-only.
- 2026-10-23 (0B standard source-pixel rule, human): the standard size per mesh is **Delaunay 1250** vertices (`_production_config.py` `hilbert_pixels`) and **rectangular 35×35 = 1225** (the square closest to 1250, chosen so the two meshes compare at equal resolution; this deliberately differs from `rect_pixels_yx = 28`, the HST/subhalo production preset, which is left unchanged). For PR 3: a row is `current` only at the standard size, and other sizes stay `scans/`. Where no row exists at the standard size, the nearest size-less row stays `current` with a `limitations` note ("measured at N source pixels; standard 1250/1225") and the coverage matrix reports the standard size as **missing**. Known gaps: light_fixed Delaunay (rows at 1500, none at 1250), light_fixed rectangular (1521/1024, none at 1225), and the main default cells at 1500 → these feed the phase 3 re-measurement list.
- 2026-10-23 (0B PR 2 open as DRAFT): https://github.com/PyAutoLabs/autolens_profiling/pull/446 on `feature/likelihood-lifecycle-p0-profiling-move`: 6d4ce975 (1,384 renames, all R100), c07b5c7e (applier `apply_migration_map.py`, redirect table, pointer READMEs), 45b1cfcc (path adaptation — `results_layout.py` reader shim, `_profile_cli` writes to mirrored cells via the generator's `destination()`, indexes, docs, mirror test). Verified in-session: no results/archive data bytes changed; catalogue/layout checks green; pytest 1503 passed. Still `profiling-summary@2`. Non-adapted writers (explicit `--output-dir` sweeps/HPC submits, point_source runtime, fixed_light witness scripts, flat aggregators) → PR 3. No live RAL profiling jobs. Held as draft until #441 merges (its lint hit the 15-min timeout in the smoke step on a docs-only diff; awaiting human rerun call); then rebuild on fresh main and un-draft. Human to confirm the `baseline/campaign.json` registry hash re-pin.
