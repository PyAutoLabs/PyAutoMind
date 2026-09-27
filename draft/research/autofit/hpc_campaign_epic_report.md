# HPC campaign epic — research report and phased plan

Written 2026-09-27 by the Fable architect session. No code edited. Companion to the prompt in `hpc_campaign_epic.md`. Four Opus research surveys fed this report (prior art, carbon methodology, codebase, euclid_dr1 glue + Slurm mechanics); their full text is not reproduced here, the citations are.

## 0. Summary

- **The campaign failed on information, not compute.** Nothing on the cluster records what a fit is doing, how much it used, or why it stopped. Every "how's it going?" rebuilt that picture from `squeue`, `sacct`, `du` and log greps, at minutes of latency and tens of thousands of tokens.
- **Three latent PyAutoFit bugs caused the downstream failures** and would keep causing them at 15k scale: the result zip is written non-atomically, `restore()` deletes the good directory before extracting and deletes the zip after, and `fit()` has no exception handler so a failed fit leaves no record. Fix these first; they ship on their own.
- **Ask 1 (single point of reference) is kept but reshaped**: two sources of truth joined by one cluster-side collector. The fit writes a tiny atomic `status.json` in its own directory; Slurm accounting is authoritative for how a task ended; a single `campaign status` command joins them into a ~2 KB digest the agent reads in one call. The Cortex ledger stays prose and is *fed* by the digest, not replaced.
- **Ask 2 (plan before submit) is kept** as a `campaign plan` command: capacity probe + calibration pilot + quantile right-sizing + ETA/disk forecast, rendered as a plan the human approves. Drift detection lives in the digest (cluster side) because the session rule forbids agent-side monitoring.
- **Ask 3 (carbon) is kept at reduced scope**: Green Algorithms estimation with site constants in Nerves config, central value plus range, allocation-basis nudges. Carbon-aware *delay* is dropped for full campaigns (oracle saving ≤3%) and offered only as a `--begin` hint for short deferrable arrays.
- **One declarative `campaign.yaml` is the spine** of everything else: stages, manifest, resources, success checks, per-index `aftercorr` chaining, failure classes, resubmission. All fit-level and campaign-level machinery lands in PyAutoFit (`autofit.campaign`) behind a scheduler-adapter protocol; Slurm is the first adapter. Lensing guidance, templates and the `hpc/sync` verbs land in `autolens_assistant`.
- **Six phases, ~14 issues across 6 repos.** Phase 0 (bug fixes) and phase 1 (status record) are independently shippable and are the first pilot on the remaining Euclid DR1 tiles.

## 1. Research findings

### 1.1 What the codebase does today (file refs are canonical `main`, 2026-09-27)

**PyAutoFit writes nothing when a fit fails.** `fit()` (`fit/PyAutoFit/autofit/non_linear/search/abstract_search.py:602`) has no try/except/finally. The only machine-readable "done" signal is `.completed` (`paths/directory.py:570`), touched at `abstract_search.py:890` *before* zipping, so under `hpc_mode` it survives only inside the zip.

**A running HPC fit writes almost nothing.** `hpc_mode` swaps in update cadences of 1e99 (`abstract_search.py:254-260`) and the pipeline config does the same. A running DR1 fit leaves only the Nautilus `checkpoint.hdf5` (in `files/search_internal/`, deleted at completion by default at :1135-1137 and excluded by `hpc/sync pull`), `search.log`, and the block-buffered SLURM `.out`. Timer files (`timer.py`) also live in `search_internal/`. `search.summary` (`text/text_util.py:257-356`) is prose. No ETA is computed; sampler progress (Nautilus `n_like`, `n_live`, `log_z`, `f_live`, `n_eff`) reaches disk only at a full update or in the final `samples_info.json`.

**Two hazards lose completed results:**
- `zip_directory` (`tools/util.py:76-84`) writes straight to `<path>.zip`, unlike `open_atomic` at :94. A walltime kill during the final zip leaves a truncated zip. On the next run `restore()` (`paths/abstract.py:484-506`) deletes the good directory *before* extracting, then raises `BadZipFile`. This is the "16 of 31 files, no samples" zip that failed at SED (`351091_101`).
- `restore()` also deletes the zip *after* extracting. Two jobs reading the same upstream result (vis_pix and SED both restore the vis_lp result; the pipeline calls `search.paths.restore()` explicitly at `scripts/initial_lens_model.py:408-411`) race: one deletes the zip while the other reads it. This matches the ledger note "SED task 192 will find no vis_lp seed zip".

**No resource measurement exists.** No peak RSS, CPU time, GPU memory or per-attempt wall clock is recorded anywhere on the fit path. The only memory probe is the GPU pre-flight guard in MultiStartGradient (`mle/multi_start_gradient/search.py:791-870`).

**The DR1 completion signal is unreliable.** None of the 23 `vis_lp*`/`vis_pix*` submit scripts in `hpc/batch_cpu/` use `set -e`, so `echo "Finished vis_lp"` prints even when Python raised; only a TIMEOUT/OOM kill suppresses it. The next-5000 vis_pix/SED manifests were built by selecting on that marker. The "already done" guard requires *exactly one* vis_lp zip (a count, not a completeness check); the truncated zip passed it. The reliable test is `.completed` inside the zip.

**Stage chaining is whole-array `afterany`**, so the 250-task vis_pix array waited on one straggler (`350804_192`), the human then cleared dependencies and hand-built manifests. Slurm `aftercorr` (task N starts when upstream task N *succeeds*) removes all of this, and the stages already share identical 0-based manifests.

**Resources and paths are hard-coded across 49 near-copy scripts**, generated by two regex generators (`hpc/upload_rest/gen_submit_scripts.py`, `hpc/batch_cpu/gen_sed_rest_full.py`). Every script is 8 CPU / 64 GB. `PROJECT_PATH` and the mail address are embedded in each. A hand capacity model lives in a generator comment.

**`hpc/sync` status verbs are thin and expensive.** `jobs`/`sacct` use default formats (bare `sacct -u` covers only since midnight, no MaxRSS/TotalCPU/array ids/reasons); `du` walks multi-10k-file trees; `tail` tails every `.out`; `wait-and-pull` blocks the local shell polling squeue. The template in `lens/autolens_assistant/hpc/sync` (600 lines) and the pipeline copy (696 lines) have drifted (sbatch-arg passthrough, `restrict_pull_dirs`, `SSH_BULK` only in the pipeline copy). Neither has a status or summary verb.

**Run state is split three ways and drifting.** `wiki/project/state.md` (the `projects.yaml` ledger) was last touched 2026-09-18 and still names array 343480; current runs live only in dated journals and the Cortex ledger, whose `## Runs` statuses are free text set at submit time and never update (342650 is still "open"). Its "Traps — don't repeat" list is durable knowledge and should stay.

**The Cortex deliberately holds run state as prose.** `cortex.py` has `run`, `running`, `done [--failed] [--wall]`, `log`, `now`; `RUN_STATES = ("open","running")`. A machine-readable `.cortex/pull.json` manifest and scoring legs (decisions 40/51) were retired by decision 60 on 2026-09-12: "Nothing in a ledger is inferred from results". The Brain Cortex conductor (`agents/conductors/cortex/_cortex.py`) runs `<sync_cli> pull` then `jobs` and prints squeue *verbatim*, parsing nothing. Its door "runs once and ends. No timer, no subscription, no cron, no loop".

**There is no permission control for scheduler commands.** `.claude/settings.json:37-60` has the API gate, the Mind guard and the end-at-deliverable matcher; none inspects `ssh`, `hpc/sync`, `sbatch`, `scancel` or `scontrol`. `scontrol hold/release/update` has been used by hand. The rule is prose only ("never submit unless asked").

**PyAutoNerves** is a first-layer-wins `Config` (`conf.py:83`); `push` prepends a layer (no-op if already first, :251-257); `register` adds package defaults with `keep_first`. A site layer would be one extra `push`; none exists. Cluster facts are spread across `sync.conf` (gitignored bash), submit-script headers and memory notes. `general.yaml` `output.log_to_file`/`log_file` are dead keys.

**The end-at-deliverable rule** (`organs/PyAutoMind/policy/end_at_deliverable.md`, hook-enforced) forbids anything that outlives the turn. Any watching must live on the cluster: Slurm itself, the fit's own status file, or a human-owned cron. The agent reads state once per human-initiated check-in.

### 1.2 Prior art (workflow and tracking systems)

| System | Per-task record | Aggregation | Many-writer strategy | Failure classes / retry |
|---|---|---|---|---|
| Snakemake | `benchmark:` TSV per job (max_rss/uss/pss, cpu_time, io, mean_load; psutil sampled) | head process polls `sacct` scoped by a per-run UUID job name, 40 s → 180 s backoff | one file per job | `retries`, resources as callables of `attempt`, failed nodes auto-excluded, `--slurm-efficiency-report` |
| Nextflow / nf-core / Seqera | trace row per task (status, exit, realtime, %cpu, peak_rss, I/O); `.exitcode` + `.command.trace` in a per-task work dir | single head writer | dir per task | `errorStrategy` on `exitStatus` (nf-core: retry on 130–145, 104, 175–177; else finish), `task.previousTrace` (24.10) sizes a retry from *measured* usage, `resourceLimits` caps it; Seqera turns observed usage into recommendations |
| Parsl | task/try states + resource samples in SQLite | **one** DB-manager process is the only writer | maildir-style filesystem radio: write `tmp/`, atomic rename to `new/` | per-app retries |
| FireWorks | launch record + `stored_data`; hourly ping | MongoDB; **offline mode** writes `FW_ping.json`/`FW_action.json` in the launch dir, `lpad recover_offline` collects | file per launch + periodic collector | FIZZLED, `detect_lostruns` on ping timeout, `rerun_fws` |
| Balsam | explicit state machine | central REST | clients → server | `RUN_ERROR` vs `RUN_TIMEOUT` kept apart, each with its own handler hook |
| MLflow / W&B | metrics series + system metrics (10 s / 2 s sampling) | server or local store | per-run dir, `wandb sync` idempotent from cron | none |
| Slurm sacct/sstat/seff/jobstats | State (TIMEOUT, OUT_OF_MEMORY, NODE_FAIL), ExitCode `code:signal`, MaxRSS (on the `.batch` step), TotalCPU, Elapsed, ReqMem | slurmdbd; "Do not run sacct … from loops" | authoritative | jobstats prints actionable notes ("request less memory") |
| HyperQueue | task state per instance + server journal | server | server-mediated | `--filter=failed` resubmission, `--max-fails` |
| XALT | JSON per exec | hourly locked cron loader → DB | file per record | n/a |

Sources: Snakemake benchmark.py and slurm plugin catalog; Nextflow reports/tracing/process docs and nf-core `base.config`; Parsl `monitoring/radios/filesystem.py`; FireWorks offline and failures tutorials; Balsam jobs guide; MLflow system-metrics docs; W&B offline docs; SchedMD `sacct`, `sstat`, `scontrol`, `job_array`, `sched_config`, `cons_tres`, `sbatch`, `rest` pages; HyperQueue failure docs; XALT file-transport docs. Walltime prediction: Tsafrir, Etsion & Feitelson, IEEE TPDS 18(6) 2007; Gaussier et al., SC15 (asymmetric loss penalising under-prediction); Rodrigues et al., arXiv:1611.02905 (memory).

**Patterns to adopt:** one tiny status file per fit in its own directory, written by tmp-then-rename (Parsl/Nextflow/FireWorks); one periodic collector as the sole aggregator with one batched `sacct --parsable2` per cycle (FireWorks `recover_offline`, XALT, Snakemake); two sources of truth joined (fit file for science progress, sacct for fate: a file that says RUNNING while sacct says TIMEOUT is the key triage signal, because a SIGKILLed process cannot write its own obituary); an explicit state machine keeping timeout / OOM / bad input / missing seed apart (Balsam, nf-core); retries sized from measurement not a multiplier (`previousTrace`) and capped; resubmit only the failed subset as `--array=<list>%K` (HyperQueue); calibration pilot + high-quantile walltime (Tsafrir 2007, SC15); fix pending tasks in place with `scontrol update`; jobstats-style efficiency notes in the digest; validate each stage's output before the next.

**Patterns to avoid:** SQLite on NFS in any mode (SQLite docs: WAL "does not work over a network filesystem"; rollback mode "has led to database corruption"); many nodes appending one JSONL (`O_APPEND` is not atomic across NFS clients); per-job `sacct`/`squeue` loops; blind `× attempt` escalation on a bad-input failure; central live services (MongoDB/REST/W&B) as a hard dependency of firewalled compute nodes; trusting `TotalCPU` on signal-killed jobs; arrays beyond the site `MaxArraySize` (default 1001, which is why DR1 runs 1000-task parts).

### 1.3 Slurm mechanics that matter (SchedMD docs, cited in the survey)

- `scontrol update JobId=<array>` changes only still-pending tasks; started tasks are split into their own records. Running jobs can only have memory *reduced*; users cannot raise a running job's `TimeLimit` (pending only). Memory is an integer in MB (`12G` rejected, `12288` accepted). A task that was running at update time and later requeues comes back with its *old* request (composed from the split-record and requeue rules; the DR1 experience).
- `MaxRSS`/`TotalCPU` are on the `.batch` step line; `-X` reports them as zero. `-j <id>` sets the default window to epoch. seff = `TotalCPU / (Elapsed × AllocCPUS)` and `max step mem / allocated mem`, trivially reproducible.
- With `CR_Core_Memory`, a memory request blocks the node even with idle cores: 8 CPU × 64 GB on a ~920 GB/252-core node → 14 tasks, 112/252 cores, exactly the stranding observed. `--mem-per-cpu` ties memory to the CPU count (one knob instead of two). "Reasonably accurate time limits are important for backfill"; `bf_max_job_array_resv` defaults to 20 pending tasks per array with reservations.
- `--dependency=aftercorr:<upstream>` chains per index; `--kill-on-invalid-dep=yes` cancels tasks whose dependency can never be met. `--signal=B:USR1@600` (may arrive up to 60 s early) plus a bash `trap` writes a pre-timeout status record and forwards a checkpoint signal. `--time-min` lets backfill shrink a job's time only if the fit can resume.
- Structured live state: `squeue --me -r -O ArrayJobID,ArrayTaskID,StateCompact,Reason,PriorityLong,Nice,StartTime,TimeLeft,MinMemory,NumCPUs`; `sinfo -N -O Partition,NodeHost,StateCompact,CPUsState,Memory,AllocMem,FreeMem` (a `*` suffix means unreachable, not free); `sprio -j` for the priority breakdown (nice is *subtracted*; `%Q` is the integer priority, `%y` the nice).
- `slurmrestd` is off by default and admin-run: the portable route is CLI `--parsable2`/`--json` over the existing ssh alias. Energy accounting (`AcctGatherEnergyType`) is off by default and meaningful only for node-exclusive jobs.
- Peak memory from inside a pooled job: cgroup v2 `memory.peak` via `/proc/self/cgroup`; `VmHWM` is per process and `getrusage(RUSAGE_CHILDREN).ru_maxrss` is the largest single child, not the sum.

### 1.4 Carbon and energy methodology

- **Green Algorithms** (Lannelongue, Grealey & Inouye 2021, Adv. Sci.; arXiv 2007.07610): `E [kWh] = t × (n_c × P_c × u_c + n_m × 0.3725 W/GB) × PUE / 1000`, `C = E × CI`. Memory is *allocated* memory, so over-reservation costs energy in the model. Defaults PUE 1.67 and 475 g/kWh must not be used for RAL. **GA4HPC** applies the formula to `sacct` output with a site `cluster_info.yaml` (per-partition TDP per core, PUE, CI); it reports failed-job footprint and a "memory needed only" counterfactual. Its own caveats: assumes 100% usage when CPU time is missing, GPUs at 100%, memory-overallocation waste "largely underestimated".
- **Measurement options:** RAPL (`/sys/class/powercap`) is root-only since CVE-2020-8694 and package-level, so not attributable on a shared 256-core node. NVML `power.draw` works unprivileged for an allocated GPU. Slurm `ConsumedEnergy` needs a site plugin and exclusive nodes. **ARCHER2** (docs.archer2.ac.uk/user-guide/energy) is the verified UK precedent: `sacct ConsumedEnergy` × 1.15 (switches/Lustre/CDUs) × 1.10 (plant), real-time South Scotland regional CI, embodied 0.014 kgCO2e per CU.
- **RAL PUE:** R89 measured 1.28–1.45 over 2020–22, mean 1.31 (Ding et al. 2026, arXiv 2608.06622). The new RAL research computer centre is designed for ~1.14. Which building hosts the `ral`/`gpu` partitions is unverified. Same paper: idle servers draw 54% (Intel) to 66% (AMD) of max power, so the GA usage term understates a partially packed node.
- **Per-core TDP:** the node model is unverified (candidates: EPYC 9754 Bergamo 2.8 W/core, 9654 Genoa 3.75, 7763 Milan 4.4 per physical core; if Slurm CPUs are threads, halve it). Central 3.5 W per Slurm CPU, range 2.8–4.4. A generic GA default of 10–12 W/core overstates the CPU term 3–4×. A100: SXM 400 W, PCIe 250/300 W; real JAX draw is usually well under TDP, so measure with NVML.
- **UK grid CI** (NESO Carbon Intensity API, CC BY 4.0, no key, half-hourly, regional endpoint; Harwell OX11 → region 12 "South England"): pulled 2025-01-01 to 2026-09-20 in the survey. National 2025 mean 129 g/kWh (p5 51, p95 231); South England regional mean 188 (p5 81, p95 308); diurnal ~110 at 11–13 h / 01–03 h UTC vs ~160 at 17–19 h; median forecast error 6%. DESNZ company-reporting factor 0.177 kg/kWh (2025), lagging ~2 years. **Choosing national vs regional vs DESNZ moves CI by ±40%**, as large as any other uncertainty.
- **Is carbon-aware delay worth it?** Oracle simulation on the 2025 national series: a 9 h job saves 25% with a ≤24 h delay window, 35% with ≤48 h; a 2 h job 43%; a **two-week campaign 3%**. Real forecasts and queueing shrink these. On a shared always-busy cluster, delaying lets another user's job run (no system saving unless nodes power down; Sukprasert et al., EuroSys 2024). Verdict: low priority for full campaigns, useful only for short deferrable arrays (SED reruns, test arrays).
- **Worked estimate for DR1 (central / range):** vis_pix 4,600 × 9.1 h at 8 CPU, u 0.83, 11 GB → 1,499 kWh (1,140–3,584); vis_lp 5,000 × 1.5 h, u 0.53, 12 GB → 190 kWh (80–856); SED 5,000 × 11 min, u 0.72 → 28 kWh (19–55). **Total ≈ 1.7 MWh, ≈ 0.22 tCO2e (range 0.12–0.85 t), ≈ 0.05 kg per lens.** On GA defaults the same campaign reads 2.3 t, 12× higher: site inputs matter more than the formula. Deltas: 4 vs 8 cores for vis_lp is +4% on the usage basis (GA cannot reward right-sizing) but −33% on the allocation basis; cutting the vis_lp reservation 64 → 12 GB saves ~190 kWh, the whole central vis_lp footprint again; 18% SED timeouts waste 14–55 kWh (+50–200% of SED's own footprint, 1–3% of the campaign); the A100 route at 46 min/lens is about break-even at 300 W and ~40% better at a realistic 150 W draw, but depends on the unverified per-tile GPU time.
- **Reporting guidance:** Lannelongue et al. 2021 "Ten simple rules" (PLoS Comput Biol 17:e1009324; include the pragmatic scaling factor for reruns/tests); Scientific CO2nduct (Mariani et al., Commun. Phys. 2022, LaTeX tables); Stevens et al. 2020 and Portegies Zwart 2020 (Nat. Astron.); Astronomers for Planet Earth (arXiv:2303.05259); Patterson et al. 2021 (measured energy, PUE and location change estimates up to 100×). No formal RAS/A&A footprint mandate was found. Present central + [low, high] with the input that sets each bound, split successful vs failed/rerun energy, give per-object values, name the CI basis. Equivalences (car km, flights, tree-months) are GA defaults; flights vary 1.5–2× and tree-months imply offsetting, so prefer "same analysis on alternative settings" as the comparator.

## 2. Critique of the three asks

### Ask 1 — a single point of reference for run state. KEEP, reshaped.

What is right: the runs must write their own state; scraping directories and the scheduler is the wrong primitive; the agent needs one call.

What to change:
- **Not one store, two joined.** A fit cannot record its own SIGKILL. The per-fit record is authoritative for science progress (stage, iterations, best logL, ETA, attempt) and Slurm accounting is authoritative for fate (TIMEOUT, OOM, NODE_FAIL, exit code, MaxRSS, TotalCPU). The single point of reference is the *digest* produced by joining them, not a database.
- **Not a database on NFS.** SQLite in any mode and shared JSONL appends are both unsafe on NFS. One tiny JSON per fit, tmp-then-rename, rewritten no more than once a minute, is ~80 metadata ops/s at 5,000 writers and is the pattern every surveyed system converged on. The collector runs on the cluster login node and is the only aggregator.
- **It must not replace the Cortex ledger, and must not violate decision 60.** The ledger is prose by ruling; only humans write `result`/`lesson`. But run *status* (open/running/done/failed) is a "cluster fact" the Cortex skill already lets the agent record. The digest feeds a `cortex sync-runs` verb that flips run lines and appends a one-line log entry; nothing scientific is inferred.
- **Token/latency target** for a status check: one ssh call returning a ≤2 KB digest (markdown table + JSON), ~500–1,000 tokens, 10–30 s (one batched sacct + a scan of ≤15k small files). Today's check is 5–10 round trips (rsync pull, squeue verbatim for thousands of array rows, ad-hoc sacct, log greps, `du` that times out) at roughly 20–60k tokens and several minutes. Expected saving ≈ 20× tokens and ≈ 5–10× latency; these are estimates to be measured in the pilot.

### Ask 2 — resource-aware planning before submission. KEEP.

What is right: every failure in the campaign (memory stranding, array caps, short walltimes) was a planning failure that a 1–2% pilot would have caught. Nextflow's `previousTrace`, Seqera's recommendations, jobstats and the walltime-prediction literature all say: measure, then request a high quantile plus margin.

What to change:
- **The "planned conversation" is a document, not a chat feature.** `campaign plan` produces a plan (capacity, per-stage p50/p95/max RSS and wall, proposed CPUs/mem-per-cpu/walltime/throttle/nice, ETA, disk, energy) that the agent presents and the human approves in the ordinary way. No new interaction machinery.
- **Monitoring for drift cannot be agent-side.** The end-at-deliverable rule and the Cortex door both forbid timers. Drift flags (p95 RSS vs request, timeout rate, idle CPUs while tasks pend, stage failure rate) are computed by the collector and surface in the digest at the next human check-in, with the exact `scontrol update` proposal attached. Slurm's own `--mail-type` remains the push channel.
- **Multi-stage chains** are solved by Slurm, not bash: `aftercorr` per index plus a success check per stage recorded in the status file. Failed subsets are resubmitted per failure class (`campaign resubmit --class timeout`) as a new `--array=<list>%K` with resources sized from the failed tasks' own measurements; completed tasks are never rerun because PyAutoFit's identifier short-circuit already skips them.
- **Fairness** is a plan parameter: cap concurrent tasks at a fraction of currently idle CPUs, use `--nice`, and never raise priority. `bf_max_job_user` and fair-share make the scheduler the final arbiter.

### Ask 3 — energy and carbon. KEEP at reduced scope.

What is right: the GA model is cheap, standard, and its inputs (CPU-seconds, allocated memory, wall) are exactly what the status record and sacct already provide, so the estimate is nearly free once ask 1 exists. Reporting central plus range is the honest form.

What to change:
- **Estimation, not measurement, on CPU.** RAPL is unreadable and unattributable on shared nodes; Slurm energy accounting is off. Measure only where it is cheap and correct: NVML on an allocated GPU, and the node CPU model for TDP lookup.
- **Two bases, both reported.** Usage-weighted (what GA computes) cannot reward right-sizing, because the core term reduces to CPU-seconds. The allocation basis (u = 1, reserved memory) is what the *nudges* must use, since stranding cores and memory is the real waste. Report the usage basis as central and the allocation basis as the upper bound.
- **Drop carbon-aware delay for campaigns.** ≤3% oracle saving for a two-week array, and on a shared cluster it mostly shifts who runs. Keep a `--begin` hint from the 48 h forecast only for short deferrable arrays, off by default.
- **Site constants are config, not code.** PUE, TDP per CPU, region, CI basis and whether energy accounting exists go in a Nerves `site` layer using the GA4HPC `cluster_info.yaml` vocabulary so other sites can reuse it. RAL values need human confirmation (CPU model via `lscpu`, hosting building, GPU form factor).
- **The biggest lever is not carbon-specific.** Memory reservation and timeout reruns dominate the avoidable footprint; asks 1 and 2 deliver most of ask 3's benefit.

## 3. Recommended architecture

### 3.1 Components and where they live

| # | Component | Lives in | Depends on |
|---|---|---|---|
| C0 | **Correctness fixes**: atomic zip (tmp + rename), non-destructive concurrency-safe `restore()`, `.completed` verified inside zip, `try/finally` in `fit()` writing a failure record, timer moved out of `search_internal/` | PyAutoFit | nothing |
| C1 | **Per-fit status record** `status.json` beside the output dir (survives `hpc_mode`), atomic, ≤2 KB, ≥60 s cadence, plus `status.jsonl` attempt history; sampler `progress()` hook; resource probe (cgroup `memory.peak`, `getrusage`, NVML); `SIGUSR1`/`SIGTERM` handler → checkpoint flush + status write | PyAutoFit (`autofit.non_linear.status`) | C0 |
| C2 | **Campaign core** `autofit.campaign`: `campaign.yaml` schema; collector → `digest.json` + `digest.md`; failure triage; resubmit lists; disk forecast; `Scheduler` protocol; **Slurm adapter** (batched sacct/squeue/sinfo, sbatch generation with `aftercorr`, pending-task updates); fake adapter for tests | PyAutoFit (stdlib + PyYAML only; Slurm adapter shells out, no import-time dependency) | C1 |
| C3 | **Site/campaign config**: `site.yaml` schema (partitions, cores/mem per node, MaxArraySize, walltime max, TDP per CPU, PUE, region, CI basis, energy accounting flag) as a Nerves config layer | PyAutoNerves | nothing |
| C4 | **Planning**: `campaign plan` (capacity probe + pilot stats + quantile right-sizing + ETA + disk + energy), `campaign pilot` (stratified subset submit), drift flags in the digest | PyAutoFit | C2, C3 |
| C5 | **Carbon**: `autofit.campaign.carbon` (GA model, two bases, ranges, optional NESO fetch for the run window, paper paragraph), `campaign report` end-of-campaign markdown | PyAutoFit | C2, C3 |
| C6 | **hpc template v2** in the assistant: parameterised per-stage batch template (`--export=MANIFEST,STAGE`, EXIT/USR1 traps writing the task record, `set -euo pipefail`), `hpc/sync` verbs `status`, `plan`, `act`, `resubmit`, `report`; `campaign.yaml` example; skill `hpc_campaign.md`; wiki pages updated | autolens_assistant (mirrored to autogalaxy/autocti workspaces later) | C2 |
| C7 | **Cortex feed**: `cortex sync-runs --digest <file>` flips run status lines and appends one log line; `projects.yaml` gains `campaign_file` and `digest` fields; ledger run lines carry the campaign key | PyAutoCortex | C2 |
| C8 | **Brain**: Cortex conductor `pull` reads the digest instead of printing squeue; **scheduler action allowlist** (`hpc/sync act {hold,release,throttle,update-pending,resubmit,cancel}` with an audit log on the cluster and a Cortex log line) plus a PreToolUse hook that blocks raw `scontrol`/`sbatch`/`scancel` over ssh outside `act`; AUTONOMY.md paragraph | PyAutoBrain | C6, C7 |
| C9 | **Euclid pipeline adoption**: replace the 49 scripts with the stage template + `campaign.yaml`; `set -e`; zip-completeness guard; drop hand manifests | euclid_strong_lens_modeling_pipeline (then the euclid_dr1 clone) | C6 |

Everything fit- and campaign-level is generic PyAutoFit; nothing imports Slurm at import time; a `LocalScheduler` (subprocess pool) ships with the fake for tests and for laptops.

### 3.2 Data formats

**`status.json`** (one per fit, at `<output_path>.status.json` beside the zip so it survives `remove_files`):

```json
{"schema": 1, "identifier": "be16dd…", "name": "vis_lp", "path_prefix": "dr1_sep1_rest/Tile1020…",
 "state": "running", "attempt": 2, "failure_class": null,
 "job": {"scheduler": "slurm", "job_id": "351085", "task_id": 17, "node": "ral-n12", "cpus": 4, "mem_mb": 12288, "time_limit_s": 64800, "restart_count": 1},
 "progress": {"n_like": 41200, "n_like_max": 200000, "n_live": 750, "log_z": -1234.5, "max_log_likelihood": -1180.2, "f_live": 0.12, "n_eff": 3100, "fraction": 0.41, "eta_s": 4100},
 "resources": {"wall_s": 5120, "cpu_s": 21900, "cpu_efficiency": 0.53, "peak_rss_mb": 4100, "peak_rss_source": "cgroup", "gpu": null, "cpu_model": "AMD EPYC 9754"},
 "outputs": {"zip": null, "zip_complete": null, "bytes": 18300000},
 "updated": "2026-09-27T14:02:11Z", "started": "2026-09-27T12:36:51Z"}
```

States: `pending` (written by the batch trap before Python starts), `running`, `completed`, `failed` (Python exception; `failure_class` ∈ `exception`, `bad_input`, `missing_seed`, `upstream_incomplete`), `timeout_pending` (USR1 received, checkpoint flushed), `skipped` (already complete). `timeout` and `oom` are never written by the fit; the collector assigns them from sacct.

**`campaign.yaml`** (the single source of truth for a campaign):

```yaml
campaign: euclid_dr1_next10k
project_root: /mnt/ral/jnightin/euclid_dr1
manifest: hpc/run_manifests/next10k.txt        # 0-based line = array index, same for every stage
chunk: 1000                                     # ≤ site MaxArraySize
stages:
  vis_lp:
    script: scripts/initial_lens_model.py --stage=vis_lp
    env: {JAX_PLATFORMS: cpu, OMP_NUM_THREADS: "$SLURM_CPUS_PER_TASK"}
    resources: {cpus: 4, mem_per_cpu_mb: 3072, time: "04:00:00", throttle: 400, nice: 1000}
    success: {zip_complete: output/{sample}/{tile}/initial_lens_model/vis_lp, members: [files/samples_summary.json]}
    retry: {timeout: {time: "p99+25%", max: 1}, oom: {mem: "peak*1.5", max: 1}, exception: none}
  vis_pix:
    after: {vis_lp: aftercorr}
    ...
  sed:
    after: {vis_lp: aftercorr}
    seed: output/{sample}/{tile}/initial_lens_model/vis_lp
    ...
site: ral            # selects the Nerves site layer
```

**`digest.json` / `digest.md`** (one per campaign, written by the collector under `<project_root>/campaign/<name>/`): per-stage counts by state and failure class, p50/p95/max wall and RSS vs request, CPU efficiency, idle-capacity snapshot, ETA (remaining CPU-h ÷ effective throughput), disk used and forecast, energy/CO2e so far (central + range), drift flags with proposed actions, and the `failed_<class>.txt` index lists. The markdown is ≤2 KB; the JSON carries per-task rows for tools.

**`site.yaml`** (Nerves layer, GA4HPC vocabulary): partitions with `cores_per_node`, `mem_per_node_mb`, `max_time`, `max_array_size`, `tdp_w_per_cpu`, `cpu_is_thread`, `gpu_model`, `gpu_tdp_w`; `pue` with `pue_low`/`pue_high`; `grid_region`; `ci_basis`; `energy_accounting: false`.

### 3.3 How the agent consumes it

1. Human asks "how's it going?". Agent runs `hpc/sync status` (one ssh: `python -m autofit.campaign status campaign.yaml` on the login node, which does one `sacct`, one `squeue`, one `sinfo`, scans status files, writes the digest and prints `digest.md`). The agent reads ~700 tokens.
2. If the digest carries drift flags, the agent presents the proposed `act` commands; the human approves; the agent runs `hpc/sync act throttle vis_pix 600` (allowlisted, audited).
3. `cortex sync-runs --digest` updates the ledger's run lines; the human still writes `result`/`lesson`.
4. At the end, `hpc/sync report` renders the campaign report (compute, carbon, failures, results pointers) for the ledger and the paper.

No timers, no subscriptions, no cluster-side daemon; the collector runs when invoked (or from a human-owned cron on RAL if wanted).

## 4. Further features evaluated

| Feature | Verdict | Notes |
|---|---|---|
| Declarative campaign file | **Core** | C2; replaces 49 generated scripts and hand manifests |
| Automatic failure triage with a proposed fix | **Core** | Classes: timeout (raise time to p99+margin or resume), oom (raise mem from peak × 1.5), exception (report, no retry), bad_input (skip and list), missing_seed / upstream_incomplete (rerun upstream index first), node_fail (requeue as-is) |
| Integrity checks on stage outputs | **Core, phase 0** | `.completed` inside zip + expected members + `zipfile.testzip()`; atomic writes make truncation impossible rather than merely detected |
| Guaranteed resume of interrupted fits | **Core, phase 1** | USR1 handler flushes the Nautilus checkpoint and writes `timeout_pending`; attempt counter; checkpoint kept until `.completed`; `--time-min` becomes safe |
| Disk lifecycle and forecasting | **Yes, cheap** | per-fit `bytes` in the status record → campaign total and forecast; `du` retired; `hpc_mode` retention policy (`keep_loose: never/until_pulled`) documented; no automatic deletion |
| Fairness to other users | **Yes, as plan parameters** | throttle ≤ fraction of idle CPUs at plan time, `--nice`, never `--qos` escalation; digest shows the share of the partition in use |
| Allowlisted, logged scheduler-action tool | **Core** | C8; six verbs, audit log on the cluster, hook blocks raw scheduler commands over ssh |
| Notifications | **Drop agent-side** | Slurm `--mail-type=END,FAIL` already exists; anything else needs a timer the session rule forbids |
| End-of-campaign report | **Yes** | C5 `campaign report`: compute, carbon (two bases + range + CI basis), failure census, per-stage tables, pointers to results; paste-ready paper paragraph |
| Beyond Slurm / beyond lensing | **Yes by construction** | `Scheduler` protocol with Slurm, Local and a Fake; PBS later if a user appears; templates mirrored to autogalaxy/autocti workspaces in the last phase |
| Live progress probing of block-buffered logs | **Yes, folded into C1** | the status record replaces reading `checkpoint.hdf5`; `PYTHONUNBUFFERED=1` in the template |
| Carbon-aware start times | **Optional hint only** | `--begin` suggestion from the NESO 48 h forecast for arrays < ~6 h and small; off by default |
| HyperQueue-style packing into fewer Slurm jobs | **Deferred** | only if `MaxArraySize` or scheduler load becomes the bottleneck at 15k |

## 5. Phased epic plan

Epic slug: `hpc-campaign`. Library first in every phase; each phase ships behind the ordinary `start_dev` → `ship_library`/`ship_workspace` gates. One issue per repo per phase. Dependencies are listed as phase → phase.

### Phase 0 — Result integrity and failure records (PyAutoFit, pipeline) — no dependencies

- **PyAutoFit #A** `hpc-campaign/0-integrity`:
  - `zip_directory` writes `<path>.zip.tmp` then `os.replace`; a zip is complete or absent, never truncated.
  - `restore()` gains a non-destructive mode: extract to a temp dir and swap, never delete the zip unless the caller owns the result (`remove_files` *and* this search's own identifier); a read-only `open_result()` for downstream stages that never touches the zip. Concurrency test: two processes restore the same zip.
  - `is_complete` for a zipped result checks `.completed` inside the zip and `zipfile.testzip()`.
  - `fit()` wrapped in `try/except/finally`: on exception write `<output_path>.status.json` with `state: failed`, `failure_class`, traceback file, then re-raise.
  - `Timer` files move to `<output_path>/files/` (survive completion and pull).
  - Done: unit tests for each; a killed-mid-zip fixture resumes cleanly; `autolens_workspace_test` smoke green.
- **euclid_strong_lens_modeling_pipeline #B** `hpc-campaign/0-guards`:
  - `set -euo pipefail` in every submit script; the "Finished" echo replaced by an EXIT trap writing a task record (`campaign/tasks/<A>_<a>.json`) with exit code and a `.completed`-in-zip probe.
  - Zip-count guard replaced by the completeness probe.
  - Done: a forced Python exception produces a `failed` record and no "Finished" marker; a truncated-zip fixture is rejected by the guard.

### Phase 1 — Per-fit status record and resource measurement (PyAutoFit, Nerves, autofit_workspace) — depends on 0

- **PyAutoFit #C** `hpc-campaign/1-status-record`:
  - `autofit.non_linear.status.StatusWriter`: atomic `status.json` (schema in §3.2) at start, every `hpc.status_interval_s` (default 60) from the sampler chunk loop, at USR1/TERM, on completion and on failure; `status.jsonl` attempt history.
  - `NonLinearSearch.progress()` protocol implemented for Nautilus, Dynesty, Emcee, MLE searches (fraction, ETA from likelihood time × remaining calls).
  - Resource probe: cgroup v2 `memory.peak` → `getrusage` fallback; `cpu_s` self + children; NVML on GPU when available; CPU model from `/proc/cpuinfo`; scheduler ids from `SLURM_*` env (generic `Env` mapping so PBS can map later).
  - Signal handling: `SIGUSR1` → flush sampler checkpoint, write `timeout_pending`; `SIGTERM` same then exit 143.
  - Done: a killed-and-resumed Nautilus fit shows `attempt: 2` and resumes from the flushed checkpoint; status file never exceeds 2 KB; write cadence test.
- **PyAutoNerves #D** `hpc-campaign/1-site-config`: `site.yaml` schema (§3.2), `Config.push_site(name)`, validation, example `site/ral.yaml` (values marked unverified until the human confirms). Done: schema tests; autofit reads `site.partitions`.
- **autofit_workspace #E** `hpc-campaign/1-docs`: `hpc/` guide section on the status record and resume contract. Done: smoke green.

### Phase 2 — Campaign core and Slurm adapter (PyAutoFit) — depends on 1

- **PyAutoFit #F** `hpc-campaign/2-campaign-core`:
  - `autofit.campaign`: `campaign.yaml` loader + validation; `Scheduler` protocol (`capacity()`, `query(job_ids)`, `submit(stage, indices, resources, after)`, `update_pending(job_id, **fields)`, `cancel`); `SlurmScheduler` (batched `sacct --parsable2 --units=M`, `squeue -r -O`, `sinfo -N -O`, sbatch script generation with `aftercorr` and `--kill-on-invalid-dep=yes`, `--mem-per-cpu`, `--signal=B:USR1@600`); `LocalScheduler`; `FakeScheduler` for tests.
  - Collector: scan status/task records, join with `query()`, assign `timeout`/`oom`/`node_fail` from sacct, compute per-stage stats and drift flags, write `digest.json` + `digest.md` (≤2 KB), `failed_<class>.txt`.
  - `campaign resubmit --stage --class` sized from the failed tasks' own measurements, capped by site limits.
  - Disk: per-fit bytes → totals and forecast.
  - CLI: `python -m autofit.campaign {validate,submit,status,resubmit}`.
  - Done: end-to-end test on `FakeScheduler` with injected timeout/oom/exception/missing-seed tasks produces the right classes, lists and proposals; digest size test; no Slurm import at module import.

### Phase 3 — Organism integration (assistant, Cortex, Brain, pipeline) — depends on 2

- **autolens_assistant #G** `hpc-campaign/3-hpc-template-v2`: parameterised stage batch template; `hpc/sync` verbs `status`, `act`, `resubmit`, `report` (one ssh each, printing the digest); `campaign.yaml` example; skill `skills/hpc_campaign.md` (plan → pilot → submit → check-in → triage → report); wiki `operations/hpc.md` + `hpc_infrastructure.md` rewritten; the drifted pipeline `sync` features (sbatch passthrough, `restrict_pull_dirs`) folded back into the template. Done: smoke green; the template runs a 3-tile local campaign with `LocalScheduler`.
- **PyAutoCortex #H** `hpc-campaign/3-cortex-feed`: `cortex sync-runs <project> --digest <file>` flips run lines (open/running/done/failed with counts) and appends one `run` log line; `projects.yaml` gains `campaign_file`, `digest`; REFERENCE.md documents the boundary (status is a cluster fact; result/lesson stay human). Requires a schema decision (see risks). Done: fixture digest updates the euclid_dr1 ledger deterministically.
- **PyAutoBrain #I** `hpc-campaign/3-scheduler-governance`: Cortex conductor `pull` reads the digest; scheduler action allowlist policy in `AUTONOMY.md` and `skills/cortex/cortex.md`; PreToolUse hook blocking raw `sbatch|scancel|scontrol` over `ssh`/`hpc/sync submit` outside `hpc/sync act`/`submit` with the human-approval phrase; audit log contract. Done: hook tests; conductor test with a fixture digest.
- **euclid_strong_lens_modeling_pipeline #J** `hpc-campaign/3-adopt-campaign`: `campaign.yaml` for the three DR1 stages, template replaces the 49 scripts, hand manifests retired, `numba.cache: false` on NFS, `PYTHONUNBUFFERED=1`. Done: pipeline CI smoke; a 10-tile RAL dry run through `campaign submit` (human-triggered, science clone).

### Phase 4 — Planning and pilot (PyAutoFit, assistant) — depends on 3

- **PyAutoFit #K** `hpc-campaign/4-plan`: `campaign pilot` (stratified 1–2% subset by input size); `campaign plan` (capacity snapshot, pilot p50/p95/max wall and RSS, proposed CPUs / `mem_per_cpu` / walltime = p95+25% per size bin / throttle ≤ fraction of idle CPUs / nice, ETA = remaining CPU-h ÷ effective throughput, disk forecast, energy placeholder) rendered as `plan.md`; drift flags with exact `update_pending` proposals. Done: plan reproduces the DR1 repack numbers (12 GB / 4 CPU for vis_lp, 16 GB vis_pix, 8 GB SED) from a fixture sacct dump.
- **autolens_assistant #L** `hpc-campaign/4-plan-skill`: skill and wiki updates: the planned conversation, fairness rules, `act` proposals. Done: smoke green.

### Phase 5 — Carbon and campaign report (PyAutoFit, Nerves, assistant) — depends on 4

- **PyAutoFit #M** `hpc-campaign/5-carbon-report`: `autofit.campaign.carbon` (GA model, usage and allocation bases, ranges from site bounds, optional NESO fetch for the run window with cache, `--begin` hint for short arrays); energy in the digest; `campaign report` (compute, carbon, failure census, per-stage tables, paper paragraph with the CI basis named). Done: worked DR1 fixture reproduces §1.4 within rounding; offline by default.
- **PyAutoNerves #N** `hpc-campaign/5-site-carbon`: carbon keys in `site.yaml`; RAL values confirmed by the human or marked as ranges. Done: schema tests.
- **autolens_assistant #O** `hpc-campaign/5-carbon-guidance`: wiki page on footprint reporting and the nudges; skill step "report". Done: smoke green.

### Phase 6 — Generalisation (workspaces) — depends on 3, parallel with 4–5

- **autogalaxy_workspace / autocti_workspace #P**: mirror the hpc template v2 and campaign example. **PyAutoFit #Q**: PBS adapter only if a user asks; `LocalScheduler` documented for laptops/workstations. Done: smoke green in each.

### First pilot on Euclid DR1

Target: the next DR1 batch after the current next-5000 (the remaining ~10k tiles, or a 1,000-tile part if the campaign has moved on). Sequence: phases 0–1 released to PyPI and pulled onto RAL via `HPCPullPyAuto` (the shared venv, only when `squeue` is empty for this user); phase 0 pipeline guards adopted; a 50-tile stratified pilot per stage submitted by the human; the collector (phase 2, run from the science clone even before the assistant template lands) produces the first digest. Success criteria: a status check is one ssh call and ≤2 KB; zero truncated zips and zero "no seed" failures across the batch; every non-completed task carries a failure class; measured p95 RSS and wall per stage recorded in the ledger before the full submit; the full submit uses `aftercorr` and plan-derived resources; cluster occupancy ≥ 80% of the planned share while the arrays run.

## 6. Risks and open questions for the human

1. **Cortex decision 60.** A digest-fed `sync-runs` verb re-introduces machine-written run state that decision 60 retired. Proposed ruling: run *status* and counts are cluster facts (already allowed by the Cortex skill), `result`/`lesson` stay human. Needs a schema decision entry before phase 3.
2. **Status write load on `/mnt/ral`.** 15k writers × one 2 KB rename per minute is ~250 ops/s at peak. Almost certainly fine, but the filesystem is at 90% and shared; the pilot should measure it and the interval is configurable.
3. **`hpc_mode` contract change.** `status.json` and the timer will live *beside* the zip, so `remove_files` no longer leaves a single artefact per fit. Any tool that assumes "one zip per result" (pull scripts, `build_inspect.py`) needs a look.
4. **Site policy unknowns on RAL:** `MaxArraySize`; whether users may *raise* NumCPUs/memory on pending tasks; cgroup v2 on compute nodes; whether `AcctGatherEnergyType` is set; `bf_max_job_array_resv`. One `scontrol show config` and one `lscpu` answer most of these.
5. **Carbon inputs to confirm:** node CPU model (TDP per Slurm CPU, thread vs core), which building hosts `ral`/`gpu` and its PUE, A100 form factor. Until confirmed the report prints ranges.
6. **Resource escalation policy.** Retrying timeouts at p99+25% and OOMs at peak × 1.5 is a default; the human may prefer no automatic escalation on a shared cluster.
7. **Where the pipeline changes land first.** The `euclid_strong_lens_modeling_pipeline` repo is public and tested; the `euclid_dr1` science clone is where the campaign runs and has already diverged (49 scripts, manifests). Phase 3 assumes template → pipeline → clone; the human may prefer to trial in the clone first.
8. **Shared-venv upgrades mid-campaign.** Phases 0–1 change PyAutoFit behaviour on RAL; `HPCPullPyAuto` must only run with no jobs in flight (existing trap).
9. **Scope of the governance hook.** Blocking raw `scontrol` over ssh in the Claude harness protects one surface; Codex/other agents read only the prose policy. Acceptable for now, but say so.
10. **Carbon-aware delay.** Dropped for campaigns on the evidence above; if a funder or journal expects it, it is a small addition later.
11. **GPU route evidence.** The CPU-vs-A100 comparison rests on one 46-minute example lens. A 20-tile A100 pilot with NVML logging (phase 1 provides it) is needed before recommending the GPU route on carbon or time grounds.

## 7. Candidate tasks for `ideas.md` (scholar mode; propose, do not append)

- [from: research hpc-campaign · codebase survey] PyAutoFit: atomic result zip and non-destructive `restore()` (phase 0 issue A) — ships on its own, fixes two DR1 failures.
- [from: research hpc-campaign · codebase survey] PyAutoFit: `fit()` writes a failure record on exception (phase 0).
- [from: research hpc-campaign · euclid_hpc survey] Pipeline: `set -euo pipefail` and completeness-probe guards in every submit script (phase 0 issue B).
- [from: research hpc-campaign · Slurm survey] Pipeline: `aftercorr` per-index stage chaining replaces `afterany` + hand manifests.
- [from: research hpc-campaign · carbon survey] Nerves: `site.yaml` layer with GA4HPC vocabulary; RAL values to confirm.
- [from: research hpc-campaign · Cortex survey] Cortex schema decision: digest-fed run status as a cluster fact (pre-requisite for phase 3).
- [from: research hpc-campaign · Brain survey] Brain: scheduler action allowlist + hook (phase 3 issue I).
- [from: research hpc-campaign · assistant survey] Assistant: fold the pipeline's `hpc/sync` drift (sbatch passthrough, `restrict_pull_dirs`) back into the template now, independent of the epic.

## 8. Note for when work starts (added 2026-09-27, human instruction)

Work on this epic is deferred. When it starts, the assistant that drives it (`autolens_assistant`, or any assistant using this machinery) may or should have two extra sources of information that were not part of the surveys above, and the campaign machinery should consume both:

- **Run-time estimates from `autolens_profiling`.** By then there should be extensive likelihood-profiling results (per likelihood function, resolution, CPU/GPU, fp32/fp64). The `campaign plan` step should draw its per-evaluation time estimates from those results, not only from a calibration pilot, and should use them to advise how to set up the analysis (route, cores, GPU vs CPU) *before* anything is submitted. The pilot then confirms rather than discovers.
- **Inference cost and search choice from `autolens_inference`.** That repo should hold benchmarks of how long lens modelling takes to converge per search (with and without gradients, CPU and A100) and which search finds the right answer fastest. `campaign plan` should combine those with the profiling numbers to estimate wall time per object and to recommend the search and its settings.

In practice most campaigns will run the standard SLaM pipelines, which are designed around these resources, and `autolens_assistant` will already know them. Even so, the planning phase (phase 4, issues K and L) should treat "how long will each fit take and which search should it use" as part of the HPC management task: the plan document lists the profiling and inference records it used, and the assistant skill points at both repos as inputs. Add a cross-repo dependency on `autolens_profiling` and `autolens_inference` results to phase 4 when the epic is scheduled.
