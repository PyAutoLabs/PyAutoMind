# Prior art: status, right-sizing and failure triage for large HPC fit campaigns

Survey date 2026-09-27. Checked against the linked pages unless marked **[unverified]** (recalled, not re-checked this session).

## 1. Per-system summary

### Snakemake
- **Per task:** a `benchmark:` TSV per job with columns `s, h:m:s, max_rss, max_vms, max_uss, max_pss, io_in, io_out, mean_load, cpu_time`. The extended format adds `jobid, rule_name, wildcards, params, threads, cpu_usage, resources, input_size_mb`. psutil samples the process tree every 0.5 s for the first 30 samples and every 30 s after that ([benchmark.py](https://raw.githubusercontent.com/snakemake/snakemake/main/src/snakemake/benchmark.py)).
- **State:** one file per job, written by the job, so writers never share a file. Snakemake keeps its own run bookkeeping in `.snakemake/` (metadata and incomplete markers), and `--rerun-incomplete` reruns jobs whose outputs are marked incomplete **[unverified detail]**.
- **Retries/resources:** `--retries` or a per-rule `retries`. Resources can be callables of `attempt`, so memory can grow on each retry. The standard resources are `mem_mb`, `runtime`, `disk_mb` and `tmpdir`. Group jobs bundle several rules into one submission, and Snakemake sums the parallel components' resources for that submission ([rules docs](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html)).
- **Slurm executor plugin:** each workflow run gets a UUID as the Slurm job name, so `sacct` queries only cover that run. The first status check comes about 40 s after submission, and the interval backs off to 180 s. `runtime` maps to `--time`, `mem_mb` to `--mem` and `cpus_per_task` to `--cpus-per-task`. Other features:
  - `--slurm-array-jobs` submits arrays, with `--slurm-array-limit` as the cap.
  - Nodes where jobs failed are added to `--exclude` on later submissions.
  - Logs of failed jobs are kept for 10 days and logs of successful jobs are deleted.
  - `--slurm-efficiency-report` with `--slurm-efficiency-threshold` writes an efficiency report.

  Source: [plugin catalog](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html).
- **Digest:** `--report` builds a self-contained HTML report **[unverified detail]**.

### Nextflow (+ nf-core, Seqera Platform)
- **Per task:** the trace file (`-with-trace`, `trace.txt`, tab-separated) has one row per task. Typical columns are `task_id, hash, native_id, name, status, exit, submit, duration, realtime, %cpu, peak_rss, peak_vmem, rchar, wchar`, and more fields can be configured. The metrics come from shell tools (`ps`, `awk`, and so on) inside the task wrapper, and the docs call them estimates ([reports](https://docs.seqera.io/nextflow/reports), [tracing](https://docs.seqera.io/nextflow/tracing), [metrics](https://www.nextflow.io/docs/latest/metrics.html)).
- **State:** a single head process writes the trace. Each task writes its own small files (`.exitcode`, `.command.trace`) in its own hashed work directory, and the head collects them. So the many-writer problem is avoided through **one directory per task**. `-resume` reuses cached task hashes **[unverified detail]**.
- **Retries:** `errorStrategy` takes `terminate`, `finish`, `ignore` or `retry`, bounded by `maxRetries` and `maxErrors`. The canonical pattern is `memory { 2.GB * task.attempt }` with `errorStrategy { task.exitStatus in 137..140 ? 'retry' : 'terminate' }` ([2016 blog](https://www.nextflow.io/blog/2016/error-recovery-and-automatic-resources-management.html)).
  - Since 24.10, `task.previousTrace` exposes the previous attempt's trace. A retry can then size itself from measured usage (for example `task.previousTrace.memory * 2`) instead of multiplying a guess ([process docs](https://nextflow.io/docs/stable/process.html)).
  - `resourceLimits` caps the escalation, for example at the largest node ([directives](https://docs.seqera.io/nextflow/reference/process/directives)).
- **nf-core convention:** in `base.config`, `errorStrategy = { task.exitStatus in ((130..145) + 104 + (175..177)) ? 'retry' : 'finish' }` with `maxRetries = 1`. The labels scale linearly with `task.attempt`: `process_low` is 2 CPU / 12 GB / 4 h times the attempt, `process_medium` 6 / 36 GB / 8 h, and `process_high` 12 / 72 GB / 16 h ([base.config](https://raw.githubusercontent.com/nf-core/tools/main/nf_core/pipeline-template/conf/base.config)). **Exit-code classes (signal-range exits → retry, anything else → finish) are the triage rule.**
- **Digest:** there are three digests:
  - The execution report (Summary, Resources, Tasks) plots CPU, memory, time and I/O distributions per process.
  - The timeline shows scheduling delay against run time.
  - Seqera Platform (Tower, via `-with-tower`) streams task events to a central service and generates per-process resource recommendations from observed usage. Seqera claims savings of up to 87% ([Seqera blog](https://seqera.io/blog/optimizing-resource-usage-with-nextflow-tower/)).

### Parsl
- **Per task:** an SQLite monitoring DB with task and try state transitions and per-task resource samples; the default `resource_monitoring_interval` in the doc example is 10 s. `parsl-visualize` serves a web dashboard: the DAG, task states, and CPU/memory use over time ([monitoring docs](https://parsl.readthedocs.io/en/stable/userguide/advanced/monitoring.html)). The table names (`workflow, task, try, status, resource, node, block`) are **[unverified]**.
- **Many writers:** workers never touch the DB. Messages travel over "radios" (UDP, HTEX channel, or filesystem) to a single DB-manager process, which is **the only SQLite writer**. The **filesystem radio is maildir-style**: the writer creates the message in `tmp/` and renames it atomically into `new/`, and the receiver reads and deletes from `new/`. Its docstring says it is "likely to give higher shared filesystem load compared to the UDP radio, but should be much more reliable" ([filesystem.py](https://raw.githubusercontent.com/Parsl/parsl/master/parsl/monitoring/radios/filesystem.py)).

### FireWorks
- **State:** a central MongoDB (LaunchPad). The states are READY, WAITING, RESERVED, RUNNING, COMPLETED, FIZZLED, DEFUSED, PAUSED and ARCHIVED **[state list partly unverified]**. When a task raises an exception it is marked FIZZLED, and its dependants are blocked. Exception details go into the launch's `stored_data`, can be copied into `_exception_details` on rerun, and failed work is rerun with `rerun_fws`.
- **Liveness:** a running task pings the LaunchPad every hour, and `lpad detect_lostruns` marks a run FIZZLED after 4 h without a ping ([failures tutorial](https://materialsproject.github.io/fireworks/failures_tutorial.html)).
- **Offline mode (directly relevant):** compute nodes with no database access write `FW_ping.json` and `FW_action.json` **into their own launch directory**. A login-node `lpad recover_offline`, run periodically, reads them into the DB, and the DB may be down in the meantime ([offline tutorial](https://materialsproject.github.io/fireworks/offline_tutorial.html)). This is the "one file per task plus a periodic collector" pattern.

### Balsam (ALCF)
- **State:** a central REST server with a Python client (`Job.objects`), plus per-site agents. The success path is `CREATED → AWAITING_PARENTS → READY → STAGED_IN → PREPROCESSED → RUNNING → RUN_DONE → POSTPROCESSED → STAGED_OUT → JOB_FINISHED`. The failure states are `RUN_ERROR` (non-zero return code), `RUN_TIMEOUT` (killed mid-run), `RESTART_READY` and `FAILED`, and **user error and timeout handler hooks** decide between retry and fail ([Balsam jobs](https://balsam.readthedocs.io/en/latest/user-guide/jobs/)). The lesson is an explicit state machine that keeps timeout separate from error, each with its own handler.

### MLflow / Weights & Biases
- **MLflow:** per-run params, metrics (a time series per key) and artifacts, stored on a tracking server or a local `mlruns` file store. System metrics are opt-in (`MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING`) and cover CPU%, memory, GPU, network and disk under a `system/` prefix. Sampling runs every 10 s, tunable with `..._SAMPLING_INTERVAL` and `..._SAMPLES_BEFORE_LOGGING` ([MLflow system metrics](https://mlflow.org/docs/latest/ml/tracking/system-metrics/)).
- **W&B:** `WANDB_MODE=offline` writes everything, system metrics included, to a local run directory. `wandb sync ./wandb/offline-run*` is idempotent and safe to run from cron. System metrics are sampled every 2 s and averaged over 30 s ([W&B offline](https://docs.wandb.ai/support/models/articles/how-do-i-run-wandb-offline), [Alliance doc](https://docs.alliancecan.ca/wiki/Weights_&_Biases_(wandb)/en)).
- **Lesson:** "write locally per run, sync idempotently later" is the standard answer for firewalled compute nodes. Both tools are built for dashboards of tens to hundreds of runs, not for a 5,000-task status digest, and neither knows about Slurm.

### Slurm itself
- **`sacct` (the source of truth after a job ends):** `MaxRSS` is per step, so look at the `.batch` step. The other fields:
  - `TotalCPU` (user plus system time) can miss child CPU time on signal kills.
  - `Elapsed`, `ReqMem`, `AllocCPUS` and `Timelimit`.
  - `State` includes `OUT_OF_MEMORY`, `TIMEOUT`, `NODE_FAIL` and `PREEMPTED`.
  - `ExitCode` is `code:signal`, and `DerivedExitCode` is the highest step exit.

  `--parsable2` gives machine-readable output, `--array` expands tasks, and `-X` restricts output to allocations. The manual warns: **"Do not run sacct … from loops in shell scripts"** because the RPCs load slurmdbd ([sacct](https://slurm.schedmd.com/sacct.html)). So use one batched query per collector cycle.
- **`sstat`:** live `MaxRSS`/`AveCPU` for a running step. It needs `jobacct_gather` and the `.batch` step id ([sstat](https://slurm.schedmd.com/sstat.html)).
- **`seff` / Princeton `jobstats`:** `seff` computes efficiency after the job from sacct. `jobstats` uses Prometheus exporters, stores a summary per job at job end (traditionally in `AdminComment`, now optionally MariaDB), and prints CPU, memory and GPU efficiency bars with **actionable notes** such as "request less memory" ([jobstats](https://github.com/PrincetonUniversity/jobstats)).
- **`scontrol update` on pending jobs:**
  - `TimeLimit` can be set or changed with `+`/`-` while the job is pending, but "only a privileged user can increase a running or suspended job's TimeLimit".
  - Memory can only be reduced on a running job.
  - Array elements are addressed as `JobID_TaskID`, and the bare array job id addresses all of them.

  Sources: [scontrol](https://slurm.schedmd.com/scontrol.html), [job arrays](https://slurm.schedmd.com/job_array.html). `--array=0-N%K` throttles concurrency. `MaxArraySize` defaults to 1001 and can be raised to 4,000,001, so a 5,000-task array needs a site with a raised limit or several arrays. Changing the throttle with `scontrol update ArrayTaskThrottle=` works in practice (seen on RAL) but is not documented on the job-array page. Whether users may *increase* NumCPUs or memory on pending jobs is **site-policy dependent [unverified]**.
- **Backfill:** "Backfill scheduling is difficult without reasonable time limit estimates". `bf_max_job_user` caps how many of one user's jobs start per backfill cycle ([sched_config](https://slurm.schedmd.com/sched_config.html)). Tight walltimes backfill better, and over-asking delays starts.
- **slurmrestd:** a JWT-authenticated REST interface (`X-SLURM-USER-NAME`/`X-SLURM-USER-TOKEN`) that includes slurmdbd accounting endpoints ([rest](https://slurm.schedmd.com/rest.html)). It is an alternative to parsing sacct, but whether a site exposes it varies.

### XALT
- A site-level exec tracker. Each run produces a JSON record, transmitted either as a file or through syslog, and an hourly cron job with a lock (`xalt_file_to_db.py`) loads the records into a DB with tables `XALT_RUN`, `XALT_LINK`, `XALT_OBJECT` and so on ([XALT file transport](https://xalt.readthedocs.io/en/latest/070_loading_json_by_file.html), [XALT](https://xalt.readthedocs.io/en/latest/)). It is the same file-per-record plus periodic single-writer loader pattern at site scale. XALT also shards its JSON directories **[unverified detail]**.

### HyperQueue, Dask-jobqueue, Ray, Globus Compute (brief)
- **HyperQueue:** a user-space server/worker meta-scheduler that runs inside Slurm allocations. It supports task arrays and per-task resource requests, including alternative requests in job definition files. `--max-fails=X` aborts the rest of a job after X failures, and a crashed worker's task is rescheduled with a new instance ID. **Only failed tasks can be resubmitted** with `hq submit --array=$(hq job task-ids <id> --filter=failed)` ([HQ failure](https://it4innovations.github.io/hyperqueue/stable/jobs/failure/)). A journal file lets the server resume ([HQ jobs](https://it4innovations.github.io/hyperqueue/stable/jobs/jobs/)). It is relevant if the Slurm array cap or scheduler load becomes the bottleneck, because it packs many fits into fewer Slurm jobs.
- **Dask-jobqueue / Ray / Globus Compute:** these are pilot-job or remote-function frameworks with in-memory central schedulers and dashboards. They keep state in memory, not in a durable per-task record, so after a crash they are weaker sources of truth for a multi-day campaign **[general characterisation, not re-verified]**.

### Walltime and memory prediction literature
- Tsafrir, Etsion and Feitelson, "Backfilling using system-generated predictions rather than user runtime estimates", *IEEE TPDS* 18(6), 2007. They predict a job's runtime from the user's recent similar jobs (the mean of the last two) and raise the prediction when a job outlives it. The result is better backfill than with user estimates ([patent/summary](https://patents.google.com/patent/US8261283B2/en)).
- Gaussier et al., "Improving backfilling by using ML to predict running times", SC15. Its loss function penalises under-prediction asymmetrically ([ACM](https://dl.acm.org/doi/10.1145/2807591.2807646)).
- Rodrigues et al., "Helping HPC users specify job memory requirements via machine learning" ([arXiv:1611.02905](https://arxiv.org/pdf/1611.02905)).
- **Takeaway:** fitting a distribution to calibration runs and requesting a **high quantile plus margin**, not the mean, is the established approach. Under-prediction costs a whole rerun, while over-prediction only costs backfill priority.

## 2. Comparison table

| System | Per-task record | Storage / aggregation | Many-writer strategy | Retry / failure classes | Resource hints | Digest |
|---|---|---|---|---|---|---|
| Snakemake | benchmark TSV (RSS/USS/PSS, CPU time, I/O, wall) | file per job; head polls sacct by run UUID | one file per job; head is sole aggregator | `--retries`, `attempt`-scaled resources, `--rerun-incomplete`, bad-node exclusion | `mem_mb`/`runtime`/`cpus_per_task`, efficiency report | HTML `--report`, efficiency report |
| Nextflow | trace row (status, exit, realtime, %cpu, peak_rss, I/O) | head writes trace; per-task files in hashed work dirs | dir per task; single head writer | `errorStrategy` closure on `exitStatus`, `task.attempt`, `task.previousTrace`, `resourceLimits` | nf-core labels × attempt; Seqera recommendations | HTML report, timeline, trace TSV, Seqera UI |
| Parsl | task/try states + resource samples | SQLite written by one DB manager | radios → single writer; maildir tmp/→new/ rename | per-app retries **[unverified]** | per-task monitoring | `parsl-visualize` web UI |
| FireWorks | launch record, stored_data, exceptions | MongoDB; offline JSON files + `recover_offline` | offline files per launch dir, cron collector | FIZZLED, `detect_lostruns` (ping timeout), `rerun_fws` | queue adapters | `lpad` queries/web GUI |
| Balsam | job state + history | central REST/DB | clients talk HTTPS to server | RUN_ERROR vs RUN_TIMEOUT hooks → RESTART_READY/FAILED | per-job node/rank packing | API/CLI |
| MLflow / W&B | metrics time series, system metrics | server or local store; offline + `sync` | per-run dir, idempotent sync | none (not schedulers) | none | web dashboards |
| Slurm sacct/sstat/jobstats | State, ExitCode, MaxRSS, TotalCPU, Elapsed | slurmdbd | n/a (authoritative) | OOM / TIMEOUT / NODE_FAIL / PREEMPTED states | seff/jobstats efficiency notes | `seff`/`jobstats` text |
| XALT | JSON per exec | file/syslog → cron loader → DB | file per record, locked single loader | n/a | n/a | SQL reports |
| HyperQueue | task state per instance | server + journal | server-mediated | `--filter=failed` resubmit, `--max-fails`, crash reschedule | per-task resource requests | `hq job info/list` |

## 3. Lessons for our design

### Adopt
1. **Each fit writes status files in its own output directory, and no two fits share a file.**
   - Write each status snapshot as a JSON file to a temp name, then rename it into place, so readers only see whole files. This is the maildir/Parsl filesystem-radio pattern ([Parsl](https://raw.githubusercontent.com/Parsl/parsl/master/parsl/monitoring/radios/filesystem.py)); Nextflow's per-task work dir and FireWorks' offline `FW_ping.json` do the same.
   - Keep the file tiny (well under 4 KB) and the rewrite interval coarse (≥60 s). At 5,000 writers that is about 80 metadata operations per second.
   - Close-to-open consistency means a reader on another node sees the rename after its attribute cache expires. The collector should tolerate records that are a few seconds to about a minute stale ([nfs(5)](https://www.man7.org/linux/man-pages/man5/nfs.5.html), [CITI CTO note](http://www.citi.umich.edu/projects/nfs-perf/results/cel/dnlc.html)).
2. **One periodic collector is the only aggregator.** It scans the sharded run directories, makes **one batched `sacct --parsable2 --array -j <arrayids>` call** per cycle, and writes a single digest (JSON plus a Markdown summary) that the agent reads in one call. FireWorks (`recover_offline`), XALT (cron loader) and Snakemake (UUID-scoped sacct polling) all use this shape. The sacct manual's warning against per-job loops ([sacct](https://slurm.schedmd.com/sacct.html)) is why the call is batched.
3. **Two sources of truth, joined.** Slurm accounting is authoritative for the job's fate (State, ExitCode, MaxRSS on `.batch`, Elapsed, TotalCPU). The per-fit file is authoritative for science progress (stage, iterations, best logL, ETA). A fit whose file says RUNNING while sacct says TIMEOUT or OUT_OF_MEMORY is the key triage signal. The runner cannot write its own obituary when it is SIGKILLed.
4. **An explicit state machine, with timeout, OOM, bad-input and missing-seed kept apart** as separate classes, each with its own handler. This follows Balsam's RUN_ERROR/RUN_TIMEOUT hooks ([Balsam](https://balsam.readthedocs.io/en/latest/user-guide/jobs/)) and nf-core's exit-code classes ([base.config](https://raw.githubusercontent.com/nf-core/tools/main/nf_core/pipeline-template/conf/base.config)). Slurm TIMEOUT and OUT_OF_MEMORY become retry-with-more-resources, and Python exceptions or input-validation failures become finish-and-report.
5. **Retries sized from measurement, not a multiplier.**
   - Use `task.previousTrace`-style sizing ([Nextflow process](https://nextflow.io/docs/stable/process.html)): the next request is the observed MaxRSS or elapsed time times a margin.
   - Cap requests at a `resourceLimits`-style ceiling.
   - A retry rebuilt from scratch doubles its walltime budget, while a resumed fit only needs the remaining time. Distinguish the two because PyAutoFit can resume.
6. **Resubmit only the failed subset**, as `hq … --filter=failed` does ([HyperQueue](https://it4innovations.github.io/hyperqueue/stable/jobs/failure/)). The collector writes `failed_<class>.txt` index lists, and resubmission is a new `--array=<list>%K` sized for that class.
7. **A calibration pilot and quantile walltime.** Run about 1–2% of objects, stratified by input size, and fit runtime and memory against size. Request something like p95 plus 20% walltime per size bin, following Tsafrir 2007 and the SC15 asymmetric-loss work ([ACM](https://dl.acm.org/doi/10.1145/2807591.2807646)). Tight limits backfill better ([sched_config](https://slurm.schedmd.com/sched_config.html)). This is the planning-time version of Seqera's resource recommendations.
8. **Fix pending tasks in place instead of resubmitting.** `scontrol update JobId=<array> ...` can *lower* memory or CPUs on pending tasks and adjust `ArrayTaskThrottle` ([scontrol](https://slurm.schedmd.com/scontrol.html)). Users cannot raise TimeLimit on running jobs, so walltime must be right before tasks start.
9. **Efficiency notes in the digest**, jobstats-style ([jobstats](https://github.com/PrincetonUniversity/jobstats)): "requested 64 GB, p95 used 4 GB → recommend 8 GB". This gives the agent an actionable line, not raw numbers.
10. **Validate each stage's outputs before the next stage starts**, with a checksum or schema check. Record the result in the status file, so a "missing seed" can be seen as a stage-2 failure caused by stage 1. This is Snakemake's incomplete-marker idea applied per stage.

### Avoid
- **SQLite (in any mode) on NFS as the shared status store.** WAL "does not work over a network filesystem" because it needs shared memory ([sqlite WAL](https://www.sqlite.org/wal.html)). Rollback-journal mode depends on NFS locking, which "has led to database corruption" ([sqlite over net](https://www.sqlite.org/useovernet.html)). SQLite is fine only as the collector's private output on local disk or as a single writer.
- **Appending to one shared JSONL/CSV from many nodes.** `O_APPEND` is not atomic across NFS clients, so writes from different nodes can interleave or be lost. Use one append-only JSONL *per fit* if history is wanted.
- **Per-fit `sacct`/`squeue`/`sstat` calls from the agent or the fits** ([sacct](https://slurm.schedmd.com/sacct.html)).
- **Blind `× attempt` escalation** like nf-core's (for example a 16 h × 2 request). It wastes quota and hurts backfill when the real cause is a bad input. Escalate only on TIMEOUT or OOM classes.
- **Central live services** (MongoDB, a REST server, W&B/MLflow servers) as a hard dependency of compute nodes. Compute nodes are often firewalled. If one is used, use it only through offline files plus an idempotent sync (FireWorks offline, `wandb sync`).
- **Relying on Slurm `TotalCPU` for signal-killed jobs**, which can miss child CPU time ([sacct](https://slurm.schedmd.com/sacct.html)). Prefer the fit's own CPU-time report where one exists.
- **Assuming arrays beyond 1,000 tasks:** check the site's `MaxArraySize` (default 1001) and split campaigns into chunks ([job arrays](https://slurm.schedmd.com/job_array.html)).
