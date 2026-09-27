# euclid_dr1 HPC glue + Slurm mechanics — research report

Scope: read-only survey of `/mnt/c/Users/Jammy/Science/euclid_dr1` (the science clone) plus SchedMD docs. No cluster commands were run. File refs are relative to the clone root unless absolute.

---

## Part 1 — the euclid_dr1 HPC glue

### 1.1 `hpc/sync` (696-line bash CLI) — every verb

Config: `hpc/sync.conf` (gitignored; example in `hpc/sync.conf.example`) sets `HPC_HOST` (ssh alias, `euclid_jump`), `HPC_BASE`, `PROJECT_NAME`; env vars override. `REMOTE_PATH=$HPC_BASE/$PROJECT_NAME` must equal the `PROJECT_PATH` hard-coded in each submit script (`/mnt/ral/jnightin/euclid_dr1`). `PYAUTO_PULL_DIRS` appends extra `output*` roots (the Cortex check-in sets it).

| Verb | What it runs remotely | Cost notes |
|---|---|---|
| `push [--no-data]` | `ssh mkdir -p`, then `rsync -az --partial` per CODE_DIR (`catalogue config hpc preprocess scripts tests tools workflow`) + root files (`activate.sh start_here.py util.py ...`); `dataset/` with `--ignore-existing` | one rsync per dir; data walk is a stat of the whole remote dataset tree |
| `push-data-init` | `tar cf - dataset | ssh -c aes128-gcm tar xf -` | one stream |
| `pull [root ...]` | `logs` first, then `rsync --update --exclude=search_internal` of `output output_sed inspect` (+extras) | rsync stats tens of thousands of files per root; naming roots restricts it |
| `logs` | rsync of `hpc/batch_{cpu,gpu}/{output,error}/` | small but flat dirs: local `hpc/batch_cpu/output` already holds 12,391 files |
| `pull-full` | `ssh tar cf - --exclude=search_internal <root>` piped to local tar (pv if present) | single stream, whole tree |
| `status [root ...]` | `push --dry-run` + `pull --dry-run` | full rsync walk both ways |
| `submit cpu|gpu <script> [sbatch args]` | `ssh "cd $REMOTE_PATH/hpc/batch_<type> && sbatch <args> <script>"` | args are `printf %q` quoted; cwd matters because `-o output/…` / `-e error/…` are relative |
| `push-submit` | push then submit | |
| `jobs` | `squeue --me` (fallback `-u $(id -un)`) | default format only — no reason/priority/array expansion |
| `sacct` | `sacct -u $(id -un)` | default format, default window = since midnight; no `-j`, no `--parsable2`, no MaxRSS/TotalCPU |
| `cancel <id>` | `scancel <id>` | |
| `wait-and-pull [secs]` | polls `squeue --me --noheader | wc -l` every N s over ssh, then `pull` | one ssh per poll; blocks the local shell |
| `tail cpu|gpu` | `ssh -t … tail -f output/*.out` | tails EVERY .out in the dir (thousands) |
| `du` | `du -sh` of `dataset output output_sed inspect` + total + `df -h` | full tree walk of multi-10k-file trees — expensive on RAL NFS/Lustre |
| `check` | ssh echo, remote dir exists, `command -v sbatch`, `df -h $HPC_BASE` | cheap |
| `clear-logs [cpu|gpu]` | interactive confirm, `rm -f` local + remote `*.out *.err` | destroys the only per-task evidence (no status records exist) |

Observations: there is no structured job state anywhere — every "what happened" question is answered by grepping `.out/.err` or by ad-hoc `sacct` commands typed by hand (the ledger shows `sacct -j 3510{85..89} --format=JobID,AllocCPUS,Elapsed`, and a hand-measured "4.1 GB RSS peak, median 53 % of 8 cores"). `jobs`/`sacct` carry no array ids, reasons, MaxRSS, TotalCPU or exit codes in parsable form.

### 1.2 Submit scripts (`hpc/batch_cpu/`, 49 scripts)

Scripts are cloned per batch: `hpc/upload_rest/gen_submit_scripts.py` (15 × `vis_lp_rest_NN` from `submit_initial_lens_model_vis_lp_top1000`, inlines a `datasets=()` literal) and `hpc/batch_cpu/gen_sed_rest_full.py` (5 × `sersic_waveband_rest_full_pNN`, regex-substitutes `-J`, `--array=0-N%60`, `manifest=`, the `-ne 100` length guard and walltime). Later scripts read `hpc/run_manifests/*.txt` (24 files) instead of inlining lists; next5000 vis_pix/SED take `--export=ALL,PART=NN`.

Representative `#SBATCH` blocks (all `-n 1`, `-o output/output.%A_%a.out`, `-e error/error.%A_%a.err`, `--partition=ral`, `--mail-type=END,FAIL`, `--mail-user=james.w.nightingale@durham.ac.uk`):

| Stage / script | cpus | mem | time | array |
|---|---|---|---|---|
| vis_lp `submit_initial_lens_model_vis_lp_priority250` | 8 | 64gb | 18:00:00 | `0-249` (no throttle) |
| vis_lp `…_vis_lp_next5000_p01..05` | 8 | 64gb | 18:00:00 | `0-999%100` (later scontrol'd to 4 CPU / 12288 MB / throttle 400 while pending) |
| vis_pix `…_vis_pix_priority250` | 8 | 64gb | 18:00:00 | `0-249` |
| vis_pix `…_vis_pix_next5000` | 8 | 64gb | 18:00:00 | `0-999%100`, override `--array=0-<n-1>%100` |
| SED `submit_sersic_waveband_priority250` | 8 | 64gb | 06:00:00 | `0-249%60` |
| SED `…_rest_full_pNN` | 8 | 64gb | 02:00:00 | `0-999%60` |
| two-stage `submit_initial_lens_model_two_stage` | 8 | 64gb | 36:00:00 | `0-9` (inline list) |

Hard-coded in every script: `PROJECT_PATH`, `PYAUTO_HPC_BASE=/mnt/ral/jnightin/PyAuto`, `source $PROJECT_PATH/activate.sh`. vis_lp exports `JAX_PLATFORMS=cpu JAX_PLATFORM_NAME=cpu` and all BLAS thread vars = `$SLURM_CPUS_PER_TASK`; vis_pix pins all BLAS vars to 1 and uses `--use_cpu --number_of_cores=$THREADS --iterations_per_quick_update=1000`; SED runs a pre-flight `python -c 'jax.default_backend()=="cpu"'` guard then `scripts/sersic_lens_model_waveband.py` with `PYAUTO_OUTPUT_DIR=output_sed`.

Manifest indexing: **0-based**, `mapfile -t datasets < manifest; dataset=${datasets[$SLURM_ARRAY_TASK_ID]}` — array task N = line N (0-based) of the manifest. Guards on manifest length (`-ne 250` / `-ne 1000`) exist in fixed-size scripts; the PART scripts only check the index is non-empty.

Guards ("already done / skip"):
- **vis_lp**: shell checks only that `dataset/<sample>/<tile>/<tile>.fits` exists. "Already done" is PyAutoFit's own identifier + `.completed` short-circuit ("Fit Already Completed: skipping non-linear search"), so a resubmit of a finished tile costs an interpreter start + dataset load + restore.
- **vis_pix**: shell requires *exactly one* `output/<sample>/<tile>/initial_lens_model/vis_lp/*.zip` (a file count, not a completeness check); then `scripts/initial_lens_model.py` L396-419 does `search.paths.restore()` and raises `RuntimeError` unless `paths.is_complete` (the `.completed` marker inside the restored zip).
- **SED**: shell requires exactly one vis_lp zip, `cp -a` it into `output_sed/<sample>/<tile>/initial_lens_model/vis_lp/`, so the chain's vis_lp call cache-skips; Sersic VIS and each band then cache-skip individually via their own identifiers. No-EXT tiles now run VIS + NIR Y/J/H (grep of `DECAM_G_BGSUB` in the FITS only prints a NOTE).
- Known hole: ledger 2026-09-26 — `351091_101` found a vis_lp zip "with 16 of the usual 31 files, no samples"; the one-zip count guard passed it. The robust test is ".completed member present in the zip" (PyAutoFit zips the whole output dir including `.completed`: `autofit/non_linear/paths/abstract.py::_zip`, `directory.py::completed`).

Stage-chain enforcement: **whole-array `afterany`** (`351090 --dependency=afterany:350804`, `351091 afterany:351090`), set on the sbatch command line (not in the script). Consequences seen in the ledger: the whole 250-task vis_pix array waited on one straggler (`350804_192`); the human cleared SED's dependency with scontrol ("SED does not need vis_pix") and a full array was put on `scontrol hold` for a 10-task by-eye test (`356227`). For the next-5000, the chain was re-done by hand: manifests `vis_pix_sed_next5000_20260926_partNN.txt` list the tiles "whose vis_lp log ended with `Finished vis_lp`", submitted with no dependency. `afterany` + per-task guards means failed upstream tasks produce fast-failing downstream tasks rather than being skipped.

"Finished" markers: each script `echo "Finished vis_lp: $dataset"` / `"Finished vis_pix: …"` / `"Finished: …"` + `date` after the python call. **Bug-grade finding:** none of the 23 `vis_lp*`/`vis_pix*` scripts use `set -e` (grep confirmed; SED, two_stage, reload, gate and bundle scripts do), so `Finished vis_lp` is printed even when Python raised. Only a TIMEOUT/OOM kill (which kills the batch shell) suppresses it. The next-5000 vis_pix/SED manifests were built from that marker, so they would include tiles whose vis_lp raised; the downstream zip guards catch most of these.

GPU scripts (`hpc/batch_gpu/submit_{initial_lens_model,full_model,sersic_waveband}`) additionally hard-fail if `jax.default_backend()` is not gpu (MIG-with-no-instances lesson, `hpc/README.md` "Acceptance on RAL").

### 1.3 Diagnostics

`hpc/diagnostics/jax_fork_control.py` is the only diagnostic: legs `control`, `control_real`, `subprocess` for the JAX-then-fork deadlock question, writes `<output>/results.json` (start method, XLA initialised at fork, wall, PASS/HANG/ERROR); job wrapper `submit_jax_fork_control`. **Nothing measures RSS or CPU efficiency.** The 64 GB → 12 GB repack decision (journal `wiki/project/2026-09-25-scaleup-5000-and-250-followups.md`) came from an ad-hoc sacct read ("peaked at 4.1 GB RSS (median 3.4) and used a median 53 % of their 8 cores, yet each reserved 64 GB, so nodes held 14 tasks (112 of 252 CPUs)"). `gen_sed_rest_full.py` embeds a hand capacity model in a comment ("24 idle nodes (~252 cores / ~920 GB each) … at 64 GB per task memory caps a node at ~14 tasks, i.e. ~336 tasks partition-wide. Keep CAP * parts under that"). `hpc/upload_rest/batch_ready.py` / `batch_expect.py` count per-tile files vs `expected_counts.json` (data-readiness, 11 files/tile, 9 for three tiles).

### 1.4 Modelling scripts and PyAutoFit settings

- `scripts/initial_lens_model.py` (`--stage {all,vis_lp,vis_pix}`): `conf.instance.push(config/, output_path=$PYAUTO_OUTPUT_DIR or output)`; `af.SettingsSearch(path_prefix=<sample>/<tile>, unique_tag="initial_lens_model", info={"magzero": …})`. vis_lp: `af.Nautilus(name="vis_lp", n_live=750, batch_size=50, n_like_max=200000, seed=…)`, no pool (JAX → serial path). vis_pix: `af.Nautilus(name="vis_pix", n_live=300, n_batch=15, n_like_max=100000, number_of_cores=N)` (forked pool).
- `scripts/sersic_lens_model_waveband.py` → `fit(stage="vis_lp")` (cache) → `scripts/sersic_lens_model.py::fit_sersic` (`Nautilus name="vis", n_live=100, batch_size=50, n_like_max=100000`, unique_tag `sersic_lens_model`) → `scripts/lens_model_waveband.py::fit_waveband` (one `Nautilus(name=<band>, n_live=75, batch_size=50, n_like_max=50000)` per non-VIS band, sequential in one process — so one pathological band blocks the rest; state.md "343381_8").
- `config/general.yaml`: `hpc.hpc_mode: true` (forces `remove_files`: loose dir deleted after zipping; PyAutoFit `abstract.py` L181-185), `hpc.iterations_per_quick_update: 1e99`, `output.samples_to_csv: true`, `numba.cache: true` (README recommends `false` on NFS — mismatch), `test.check_likelihood_function: true`.
- **No script writes a status record or timing JSON.** Completion evidence is only PyAutoFit's `.completed` (inside the zip) and the shell's echo markers. No wall/RSS/CPU is recorded by the job itself.

### 1.5 Output footprint per tile (from code)

- `output/<sample>/<tile>/initial_lens_model/vis_lp/<hash>.zip` and `…/vis_pix/<hash>.zip` — with hpc_mode the zip is the only artefact after completion. While running, an unzipped `<hash>/` exists with `files/` (model.json, search.json, samples*, …), `image/`, `files/search_internal/` (Nautilus `checkpoint.hdf5`, the only progress signal for a block-buffered log — state.md trap). Pull excludes `search_internal`.
- `output_sed/<sample>/<tile>/initial_lens_model/vis_lp/<hash>.zip` (copied seed), `…/sersic_lens_model/vis/<hash>.zip`, `…/sersic_lens_model/<band>/<hash>.zip` for each of nir_y/j/h (+ decam_g/r/i/z when EXT present) — up to 9 zips/tile (sep1: 70 zips for 9 tiles).
- Logs: `hpc/batch_cpu/output/output.<A>_<a>.out` + `error/error.<A>_<a>.err` — 2 files per task, all arrays in one flat dir.
- `inspect/<sample>[_<run_tag>]/` per catalogue build. Caveat (state.md trap): RAL `output/` is nested `<sample>/<tile>` but older local mirror was flat.

### 1.6 Run state: `wiki/project/state.md` + journals vs the Cortex ledger

- `projects.yaml` (`/home/jammy/Code/PyAutoLabs/organs/PyAutoCortex/projects.yaml` L104-116) declares `ledger: wiki/project/state.md`, `sync_cli: hpc/sync`, `sync_verbs: [...17 verbs...]`, `partition: ral`, `witness_file: results/**/*.json`. The Cortex ledger proper is `organs/PyAutoCortex/projects/euclid_dr1.md` (Now / Runs / Log).
- `state.md` (309 lines, `last_touched: 2026-09-18`) is **stale**: its "Current run" is array 343480 (top-1000) and "Where we are now" is the ten-lens SED chain. Current runs (350804 … 356556) exist only in the dated journals (`2026-09-25-priority250-submitted.md`, `2026-09-25-scaleup-5000-and-250-followups.md`) and the Cortex ledger.
- Duplicated between them: array IDs, script names, manifests, resources, dependency choices, submission times, human decisions (hold/clear dependency), counts ("240 COMPLETED / 10 RUNNING"). Cortex's `## Runs` statuses (`open`/`running`) are free text set at submit time; e.g. 342650 still "open", "Now" line refers to 344645 — the ledger has no feed from sacct, so status drifts.
- Unique to state.md: the durable "Traps — don't repeat" list (layout mismatch, never touch `/mnt/ral/jnightin/PyAuto` mid-run, block-buffered logs → read `checkpoint.hdf5`, never `pkill -f`, reload deletes the zip first, etc.) — this is knowledge, not state, and should stay.

---

## Part 2 — Slurm mechanics (cited)

### 2.1 `scontrol update` on arrays ([scontrol](https://slurm.schedmd.com/scontrol.html), [job_array](https://slurm.schedmd.com/job_array.html))
- Updating `JobId=<ArrayJobID>` "will affect all of the individual jobs of the array"; `<ArrayJobID>_<task>` targets one. Array task records are only split off "as needed, typically when a task of a job array is started" — so an update on the meta-record changes the **still-pending** tasks; already-started tasks are separate records with their own values.
- `MinMemoryNode` / `MinMemoryCPU`: mutually exclusive for pending jobs; for running jobs MinMemoryNode allows "only reduction". Units: plain integer MB (the ledger records `12G` rejected, `12288` accepted).
- `NumCPUs`, `CPUsPerTask`: settable on pending jobs (the 09-25 repack changed both; changing only one leaves an inconsistent request).
- `TimeLimit`: `+`/`-` increments allowed; "Only a privileged user can increase a running or suspended job's TimeLimit" — users can raise it only while pending.
- `ArrayTaskThrottle=<N>` (0 = unlimited): acts on the scheduler's next pass; lowering it does not kill running tasks (it stops new starts) — inference from the semantics, not stated verbatim.
- Requeue: `scontrol requeue` returns a job to pending (held, priority 0 for `requeuehold`) and keeps its original spec. Combined with the split-record rule, a task that was running at the time of a memory update and later requeues (node failure, preemption) **comes back with its old 64 GB/8 CPU request** — it is no longer covered by the meta-record update. (Documented behaviour composed; not a single quoted sentence.)

### 2.2 `sacct` fields and efficient queries ([sacct](https://slurm.schedmd.com/sacct.html), [seff source](https://github.com/SchedMD/slurm/blob/master/contribs/seff/seff))
Record per task: `JobID,JobIDRaw,JobName,State,ExitCode,DerivedExitCode,Elapsed,ElapsedRaw,TimelimitRaw,Start,End,Submit,AllocCPUS,ReqMem,AllocTRES,MaxRSS,MaxVMSize,TotalCPU,CPUTimeRAW,NodeList,ConsumedEnergyRaw`.
- `MaxRSS`/`TotalCPU` live on the **step** lines (`<id>.batch`, `.extern`), not the allocation line; `-X/--allocations` reports utilisation as zero. So: `sacct -j <arrayid> --parsable2 --noheader -o <fields>` (no `-X`) and join `.batch` to the allocation line by JobID. `ReqMem` is allocation-only.
- `-j` with an explicit id sets the default `--starttime` to epoch (the bare `sacct -u` that `hpc/sync sacct` runs only covers since midnight). `--units=M` for consistent memory units; `--array` expands grouped pending tasks.
- `TotalCPU` may be inaccurate for signal-killed processes (sacct note).
- seff: `cpu_eff = sum(step TotalCPU) / (Elapsed × AllocCPUS)`; `mem_eff = max over steps of TRESUsageInMax mem (× ntasks) / allocated mem`; per job/per array task. seff is a contrib and may not be installed; the formula is trivial to reproduce from the sacct row above.
- `ConsumedEnergy` is meaningful only for exclusive allocations and only if an energy plugin is configured (below).

### 2.3 Live state: `sstat`, `squeue`, `sprio`, `sshare`, `sinfo`
- [sstat](https://slurm.schedmd.com/sstat.html): running steps only; target `<jobid>.batch` (use the per-task JobIDRaw for array tasks), `-a` all steps, fields `MaxRSS,AveRSS,AveCPU,TresUsageInMax,MaxRSSNode`, `--parsable2`.
- [squeue](https://slurm.schedmd.com/squeue.html): `-r/--array` one line per task; `%F` array job id, `%K` task id, `%r`/`%R` reason, `%Q` integer priority vs `%p` normalised, `%y` nice, `%S` expected start, `%L` time left, `%m` min mem (MiB), `%C` cpus; long forms via `-O ArrayJobID,ArrayTaskID,Reason,PriorityLong,Nice,StartTime,TimeLeft,MinMemory,NumCPUs`; `--start` for projected starts; `--json`/`--yaml` dumps (filters still apply).
- [sprio](https://slurm.schedmd.com/sprio.html): per-factor priority breakdown (age, fairshare, jobsize, partition, qos, assoc, tres, nice); `-w` weights. [Multifactor](https://slurm.schedmd.com/priority_multifactor.html): `Job_priority = site_factor + Σ weights·factors … − nice_factor` — i.e. the `Nice=1000` used on 351085-89 subtracts 1000 from the integer priority; only privileged users may go negative ([sbatch](https://slurm.schedmd.com/sbatch.html)). `sshare` gives the account/user fair-share inputs.
- [sinfo](https://slurm.schedmd.com/sinfo.html): `-N -o "%P %n %t %C %m %e"` or `-O Partition,NodeHost,StateCompact,CPUsState,Memory,AllocMem,FreeMem` for per-node alloc/idle/other/total CPUs and memory; `*` suffix = "not responding and will not be allocated any new work" (matches the memory note "idle* nodes are unreachable, not free"); `--json`.

### 2.4 Packing, backfill, submission knobs
- [cons_tres](https://slurm.schedmd.com/cons_tres.html): with `CR_Core_Memory`/`CR_CPU_Memory` memory is a consumable resource; a job's memory request blocks the node even with idle cores. 8 CPU × 64 GB on a ~920 GB/252-core node → 14 tasks, 112/252 cores used — exactly the stranding observed. `--mem` (per node) and `--mem-per-cpu` are mutually exclusive ([sbatch](https://slurm.schedmd.com/sbatch.html)); `--mem-per-cpu` makes memory scale automatically when CPUs are changed (one knob instead of two in the scontrol repack). `DefMemPerCPU`/`DefMemPerNode` default 0 = unlimited ([slurm.conf](https://slurm.schedmd.com/slurm.conf.html)) — always request memory explicitly.
- Backfill ([sched_config](https://slurm.schedmd.com/sched_config.html)): "reasonably accurate time limits are important for backfill scheduling to work well"; `bf_window` default 1 day, `bf_interval` 30 s. 18 h limits on a stage that runs ~0.5-3 h hurt backfill. `bf_max_job_array_resv` (default 20, per [high_throughput](https://slurm.schedmd.com/high_throughput.html)/backfill.c) caps how many pending tasks of one array get future reservations. `--time-min` lets the scheduler shrink `--time` to fit a backfill hole — useful only with checkpoint/resume (Nautilus `checkpoint.hdf5` resume exists).
- Array throttle `%N` ([job_array](https://slurm.schedmd.com/job_array.html)) is a concurrency cap, adjustable later via `ArrayTaskThrottle`. `MaxArraySize` default 1001 (max index 1000) — explains the 1000-task parts; ask admins for RAL's value.
- Dependencies ([sbatch](https://slurm.schedmd.com/sbatch.html), [job_array](https://slurm.schedmd.com/job_array.html)): `afterok` (all tasks exit 0), `afterany`, `afternotok`, `singleton`, and **`aftercorr`: "satisfied after the corresponding task ID in the specified job has completed successfully"** — per-index chaining (vis_pix task N starts when vis_lp task N succeeds), which removes both the straggler wait and the hand-built "Finished vis_lp" manifests. Requires identical manifests/indices across stages (already true). `?` = OR; `--kill-on-invalid-dep=yes` cancels tasks whose dependency can never be satisfied instead of leaving them pending forever.
- `--requeue`/`--no-requeue` (default from `JobRequeue`, default 1); `--nice`, `--qos`, `--begin=now+1hour`.
- `--signal=B:USR1@600`: signal only the batch shell 600 s before the limit ("may be sent up to 60 seconds earlier"); the shell can `trap` it, write a TIMEOUT-pending status record, and forward to Python for a clean checkpoint.

### 2.5 Accounting alternatives
- [slurmrestd](https://slurm.schedmd.com/rest.html): **not on by default**, admin must run it (JWT / local socket / proxy auth). Not assumable on RAL; the CLIs' `--json` output (squeue/sinfo/sacct in recent Slurm) is the practical structured alternative to scraping.
- [sreport](https://slurm.schedmd.com/sreport.html): `cluster AccountUtilizationByUser`, `cluster UserUtilizationByAccount`, `job SizesByAccount`, `-t hours`, start/end windows, TRES incl. energy — campaign-level CPU-hours. `sacctmgr show assoc/qos` for limits.
- Energy: `AcctGatherEnergyType` default is no collection (plugins rapl/ipmi/gpu/pm_counters/xcc) ([slurm.conf](https://slurm.schedmd.com/slurm.conf.html)); `JobAcctGatherType` recommended `jobacct_gather/cgroup`, `JobAcctGatherFrequency` task default 30 s (so MaxRSS is a 30 s-sampled peak). Check `scontrol show config | grep -i energy` before recording ConsumedEnergy.

### 2.6 Per-task status record from inside the job
- Pattern: in the batch script, `trap 'write_status $?' EXIT` (plus `trap … USR1` with `--signal=B:USR1@600`) writing `status/<SLURM_ARRAY_JOB_ID>_<SLURM_ARRAY_TASK_ID>.json` with `SLURM_JOB_ID`, `SLURM_ARRAY_JOB_ID`, `SLURM_ARRAY_TASK_ID`, `SLURM_JOB_NODELIST`, `SLURM_CPUS_PER_TASK`, `SLURM_MEM_PER_NODE`, `SLURM_RESTART_COUNT`, tile, stage, start/end epoch, python exit code, and a completeness probe (`.completed` in the zip). The trap does not fire on SIGKILL (OOM/TIMEOUT after grace) — so a missing/"started" record + sacct `State` is the TIMEOUT/OOM signal; the sacct join remains authoritative. `Epilog`/`EpilogSlurmctld` run as root/SlurmUser and are admin-only.
- Peak memory in-job: `/proc/self/status` `VmHWM` is per-process (misses vis_pix's forked pool workers); `resource.getrusage(RUSAGE_CHILDREN).ru_maxrss` is the max of any *single* reaped child, not the sum; the right number for a pooled job is the cgroup's `memory.peak` ("max memory usage recorded for the cgroup and its descendants", [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)) found via `/proc/self/cgroup` (cgroup v2 only; includes page cache). CPU: `getrusage(RUSAGE_SELF)+RUSAGE_CHILDREN` user+sys over wall × cpus gives in-job CPU efficiency.

---

## What the euclid_dr1 glue does today that the epic should absorb
1. Push/pull/logs/submit verbs over one ssh alias with `sync.conf` + `PYAUTO_PULL_DIRS` (keep the verb set; Cortex already lists them in `projects.yaml`).
2. Manifest-indexed arrays (0-based line N = task N), manifest-length guards, per-part manifests ≤1000 lines (MaxArraySize), and generators that clone scripts by regex — replace with one parameterised template per stage (`--export=MANIFEST=…,STAGE=…`) instead of 49 near-copies with hard-coded paths and mail address.
3. Stage environments: JAX-CPU threads for vis_lp/SED, BLAS=1 + pool for vis_pix, separate processes, backend pre-flight guards (CPU and GPU).
4. Completion guards: FITS-exists, "exactly one vis_lp zip", seed copy into `output_sed`, PyAutoFit `.completed` short-circuit — upgrade the zip-count check to ".completed inside the zip" (the 16-of-31-file zip passed it).
5. Stage chaining: currently whole-array `afterany` + hand-built "Finished vis_lp" manifests + scontrol hold/dependency clearing — absorb as `aftercorr` per-index chaining.
6. Fix the `set -e`-less vis_lp/vis_pix scripts: the "Finished" marker is printed even when Python raises, and it fed the next-5000 manifests. Replace markers with an EXIT-trap status JSON.
7. Resource right-sizing done by hand (sacct read → scontrol MinMemoryNode/NumCPUs/CPUsPerTask/ArrayTaskThrottle on pending arrays; capacity arithmetic in a generator comment) — make it a measured, recorded step (per-stage RSS/CPU-efficiency table from sacct `.batch` rows).
8. Run-state bookkeeping split three ways (state.md stale since 09-18, dated journals, Cortex `## Runs` free-text statuses that never update) — feed the ledger from sacct/status records; keep state.md's Traps list as knowledge.
9. Progress probing of long fits via `files/search_internal/checkpoint.hdf5` (n_like, explored, shells) because logs are block-buffered — worth a verb (`PYTHONUNBUFFERED=1` would also help).
10. `du` and `tail` walk entire trees/dirs — replace with counts from status records and `tail` of one task's log.

## Slurm features we should exploit
1. `--dependency=aftercorr:<upstream>` for per-tile stage chaining (+ `--kill-on-invalid-dep=yes`).
2. `sacct -j <array> --parsable2 --noheader --units=M -o JobIDRaw,State,ExitCode,DerivedExitCode,ElapsedRaw,TimelimitRaw,AllocCPUS,ReqMem,MaxRSS,TotalCPU,CPUTimeRAW,NodeList,Start,End` (no `-X`; join `.batch`), computing seff-style CPU/mem efficiency ourselves.
3. `squeue --me -r -O ArrayJobID,ArrayTaskID,StateCompact,Reason,PriorityLong,Nice,StartTime,TimeLeft,MinMemory,NumCPUs` (or `--json`) for pending reasons/projected starts; `sprio -j` when priority is the question.
4. `sinfo -N -O Partition,NodeHost,StateCompact,CPUsState,Memory,AllocMem,FreeMem` to compute real packing headroom (exclude `*` states).
5. `--mem-per-cpu` instead of `--mem`, measured per stage (vis_lp peak ~4 GB on 8 cores), so CPU changes carry memory with them; shorter, stage-measured `--time` (and optionally `--time-min`) to help backfill.
6. `scontrol update JobId=<array> ArrayTaskThrottle=/MinMemoryNode=(MB)/NumCPUs=+CPUsPerTask=/TimeLimit=` on pending tasks — with the caveat that started (split) tasks and later requeues keep the old request; record which regime each task ran under.
7. `--signal=B:USR1@600` + bash `trap` for a pre-timeout status record / checkpoint flush; EXIT trap writing a per-task JSON (ids, node, cpus, mem, wall, exit, `.completed` probe, cgroup `memory.peak`, getrusage CPU).
8. `--nice` for campaign ordering (already used, Nice=1000), `--begin`/`scontrol hold/release` for staged rollouts (already used by hand).
9. `sreport cluster UserUtilizationByAccount -t hours` for campaign CPU-hours; `ConsumedEnergy` only if RAL has an `AcctGatherEnergyType` plugin (default off) and allocations are exclusive (they are not).
10. Do not plan on slurmrestd (not default; admin-run) — CLI `--json` over the existing ssh alias is the portable route.
