# HPC campaign epic: what the codebase already has

This is a read-only survey. Paths are relative to `/home/jammy/Code/PyAutoLabs`. Line numbers are from the canonical `main` checkouts as of 2026-09-27.

## A. PyAutoFit (`fit/PyAutoFit/autofit`)

### A1. What `fit()` does, in order (`non_linear/search/abstract_search.py`)

`fit()` is at :602. It runs these steps in order:

1. `check_model` (:1380), then it logs the JAX device or core count (:640-657) and runs `_log_process_state()` (:716). That function uses psutil to count open files. It is the only psutil use on the main path.
2. `modify_model`. It then sets `paths.model` and `paths.unique_tag` (:659-662).
3. **`self.paths.restore()` (:664).** If `<output_path>.zip` exists, restore deletes `output_path` with rmtree, extracts the zip, and then **deletes the zip** (`paths/abstract.py:484-506`).
4. `pre_fit_output` (:737). If the fit is not complete, or `force_pickle_overwrite` is set, it calls `paths.save_all` (`paths/directory.py:373-393`). That writes these files:
   - `.identifier` (:295)
   - the parent identifier
   - `model.info`
   - `files/info.json`, when the caller passes `info`
   - `files/search.json`, the aggregator's sentinel
   - `files/model.start_point`
   - `files/model.json`
   
   Then comes `analysis.save_attributes` (dataset, etc.), then `visualize_before_fit`. When `skip_fit_output()` is set, only `save_all` runs (:676-687).
5. If `not paths.is_complete`, it calls `start_resume_fit` (:808); otherwise `result_via_completed_fit` (:1048). The completion test is the file `<output_path>/.completed` (`paths/directory.py:203-207, 570-574`).
6. `start_resume_fit` is wrapped by `configure_handler` (:88-135). That adds a `FileHandler` for `<output_path>/search.log` when `output.yaml: search_log: true`. It then does:
   - `timer.start()` (:837)
   - test-mode bypass (:840-846)
   - `_fit` for the specific search
   - a final `perform_update` with `during_analysis=False`
   - `analysis.make_result`, `save_results`, `save_results_combined`
   - **`paths.completed()` (:890)**, which touches `.completed`
7. `modify_after_fit`, then `post_fit_output` (:1119-1144):
   - If `output.search_internal` is false (the default), it **deletes `files/search_internal/`**, including the Nautilus `checkpoint.hdf5` and the timer files. If it is true, it saves `search_internal.dill` instead.
   - It then **always** calls `paths.zip_remove()`, which zips `output_path` into `<output_path>.zip` (`paths/abstract.py:363-381`). It deletes the directory only if `remove_files` is set.

**On an exception, nothing is written.** `fit()` has no `try/except/finally`. A likelihood error, OOM or SIGTERM propagates and leaves this on disk:
- the pre-fit files
- whatever full updates were written
- the search's own checkpoint
- `search.log`, whose handler is closed in the `finally` at :130-133

There is no `.failed` marker, status JSON or exit record anywhere in autofit. A grep for `.failed`, `status.json`, `run_status`, `ru_maxrss` or `memory_info` finds nothing on the fit path.

### A2. Per-update writes (`non_linear/search/updater.py`)

A full update runs every `iterations_per_full_update`, and once more at the end. It writes, in this order:
1. `files/samples.csv` and `files/samples_summary.json`, written first so a kill mid-update still leaves them (:205-248).
2. Latent samples.
3. Visualization.
4. `search.summary` and `model.results`, via `_profile_and_summarize` (:306-337).
5. `timer.update()`, which writes `.time` (:192-203).

`search.summary` (`text/text_util.py:257-356`) is prose and holds:
- Total Samples and accepted samples
- the acceptance ratio
- the log-likelihood evaluation time
- "Expected Time To Run"
- a speed-up factor
- the visualization time
- a resampling block

It is not machine-readable.

Quick updates (`non_linear/fitness.py:608-765`) write only `model.results`, which holds the max-likelihood info, plus the `fit.png` visual.

**On HPC, both cadences are off.** The autofit default is `general.yaml` `hpc: iterations_per_quick_update/full_update: 1e99`, and `abstract_search.py:254-260` swaps the `hpc:` block in under `hpc_mode`. The pipeline's `config/general.yaml:17-20` also sets `hpc_mode: true` with both at 1e99. So a running DR1 fit writes **no intermediate samples, summary or timer update**. Its only live artefacts are:
- the sampler checkpoint
- `search.log`
- the SLURM `.out` (Nautilus `verbose=True` prints its status table there)

### A3. Timer (`non_linear/timer.py`)

- `Timer(paths.search_internal_path)` is built at `abstract_search.py:538-554`.
- It writes `files/search_internal/.start_time` once, on first start (it survives resume, :27-40).
- It writes `.time` (elapsed seconds) on each `update()` (:42-55).
- Both live **inside `search_internal/`**. That folder is deleted at completion by default, and `hpc/sync pull` excludes it, so the local mirror never sees the timer.
- The elapsed time survives only as `samples_info["time"]` (Nautilus `search.py:706-713`; Dynesty `dynesty/search/abstract.py:318-327`) inside `files/samples_info.json`, and in the speed-up line of `search.summary`.
- Resumes are not recorded: there is no per-attempt timing and no walltime accounting.

### A4. Resume

- **Identity.** The output path is `output_path/[test-mode segment]/path_prefix/unique_tag/name/<identifier>` (`paths/abstract.py:327-349`). The identifier is a hash of the search and the model (plus `unique_tag`) (:270-293). A killed job resubmitted with the same script and data maps to the same folder.
- **Nautilus.** It resumes from `files/search_internal/checkpoint.hdf5` (`nest/nautilus/search.py:316-329, 389-396`). The checkpoint is passed as `filepath=` to the sampler, so Nautilus writes it on its own schedule. The `_fit` loop runs `search_internal.run(n_like_max=chunk)` in chunks of `iterations_per_full_update`, with a floor of 3×n_live (:580-633). At the end, `output_search_internal` removes the checkpoint (:675-704).
- **Likelihood check on resume.** `general.yaml test: check_likelihood_function: true` recomputes a previous sample's likelihood on resume.
- **Completed fits are skipped.** They return `result_via_completed_fit` and re-zip (and remove, under `hpc_mode`) in `post_fit_output`.
- **Hazard 1: restore is destructive and not concurrency-safe.** `restore()` deletes the output dir *before* extracting, and deletes the zip *after* extracting (`paths/abstract.py:484-506`). Two jobs that open the same completed stage at the same time can race: in DR1, the vis_pix and SED jobs both read the vis_lp result, and the pipeline's `scripts/initial_lens_model.py:408-411` calls `search.paths.restore()` explicitly. One job deletes the zip while the other is reading it. This matches the ledger note "SED task 192 will find no vis_lp seed zip".
- **Hazard 2: the zip is not atomic.** `zip_directory` (`tools/util.py:76-84`) writes straight to `<path>.zip`, unlike `open_atomic` at :94. A walltime kill during the final zip leaves a truncated zip. On the next run, `restore()` deletes the good directory and then raises `BadZipFile`. The completed fit is lost.

### A5. `hpc_mode` / `remove_files`

- `hpc_mode: true` forces `remove_files=True` (`paths/abstract.py:180-187`), sets `silence=True` (`abstract_search.py:266-267`), and swaps in the `hpc:` update cadences.
- `remove_files` only decides whether `output_path` is deleted after zipping. The zip is always made.
- `preserve_in_zip` (`paths/abstract.py:383-443`) exists so that files written after completion get into the zip. It also deletes the loose copies under `remove_files`.
- **What breaks:** any reader of loose files (`output/.../files/*.json` or images) after completion. The aggregator copes by extracting zips (A6). The pipeline's `scripts/tools/build_inspect.py:35,129` reads zip members directly.
- `output.log_to_file` / `log_file` in `general.yaml` are **dead keys**: no `.py` in the tree reads them. The real log switch is `output.yaml search_log`.

### A6. Aggregator (`aggregator/aggregator.py`)

`from_directory` (:177) runs a single `os.walk` over the whole tree.
- It recognises a search output by `files/search.json`, or by a legacy `metadata` file (:104-115).
- It **extracts each `*.zip` as it meets it**, either beside the zip (which doubles the disk used) or into a temporary directory when `unzip_temporary=True` (:245-296).
- It skips a zip whose sibling directory already carries `.completed`.
- `completed_only` filters on `.completed`.
- **Cost:** O(files), plus a full extraction of every zip, on every call. There is no index or cache beyond "already extracted".
- The SQLite route (`database/aggregator/aggregator.py:389` `add_directory`, `database/aggregator/scrape.py`) is the scalable alternative, but nothing on the HPC path uses it.
- `workflow/{csv,png,fits}_make.py` in the pipeline use `Aggregator.from_directory(..., completed_only=True, unzip_temporary=True)`.

### A7. Parallelism and resources

- `number_of_cores` is a constructor argument on the search (`abstract_search.py:156, 271-300`). The config has only `parallel.warn_environment_variables`.
- Pools are created by `make_pool` / `make_sneaky_pool` / `make_sneakier_pool` (:1632-1685). They use `fork_context()` (`non_linear/parallel/context.py:5-33`).
- Nautilus wraps its pool with a liveness-polling wrapper that detects dead workers (`nautilus/search.py:64-148`).
- **Memory measurement exists only as a GPU pre-flight guard in MultiStartGradient:** `_memory_budget_bytes` (JAX `memory_stats` → psutil `virtual_memory`) and `analysis.batched_memory_bytes` (`analysis/analysis.py:338`). It lives at `mle/multi_start_gradient/search.py:791-870` and is skipped on CPU.
- Nothing records peak RSS, CPU time or device memory for a fit.

### A8. Progress / ETA

Samplers expose progress only internally:
- Nautilus: `n_like`, `n_live`, `log_z` in `samples_info_from` (`nautilus/search.py:706-713`), plus `n_eff`/`f_live` targets.
- Dynesty: `ncall`, `logz`.

These reach disk only at a full update, or as the final `samples_info.json`. No ETA is computed: "Expected Time To Run" is total samples × likelihood time *after* the fact. There is no live progress file.

## B. PyAutoNerves (`organs/PyAutoNerves/autonerves`)

1. `Config(*config_paths, output_path)` (`conf.py:83-119`) takes an ordered list of config directories. The first one wins, and later ones are fallbacks. Lookup is `conf.instance["general"]["hpc"]["hpc_mode"]`.
2. A module-level singleton, `default = Config(cwd/"config", output_path=cwd/"output/")` (`conf.py:292-296`), is created at import. `instance = default`.
3. `push(new_path, output_path=None, keep_first=False)` (`conf.py:210-276`):
   - It prepends a layer. With `keep_first`, the layer goes second.
   - It raises if the path does not exist or holds no yaml/json/ini.
   - It is a **no-op when the path is already first** (:251-257; memory `cfgPush`).
   - It re-runs `configure_logging`.
4. `register(file)` (:278-287) pushes `<package>/config` with `keep_first=True`. `autofit/__init__.py:5` and `autolens/__init__.py:153` do this. The resulting order is **[workspace `./config`, lens defaults, …, fit defaults]**.
5. A "site" layer, such as `site.yaml` or a `config_ral/` directory, would be one more `push`. Nothing like it exists today. Cluster facts currently live in `hpc/sync.conf` (bash, gitignored) and in the submit scripts.
6. `test_mode.py` holds environment-variable switches only:
   - `PYAUTO_TEST_MODE` (levels 0-3, :5-14)
   - `PYAUTO_SKIP_FIT_OUTPUT`, `PYAUTO_SKIP_VISUALIZATION`, `PYAUTO_SKIP_CHECKS`, `PYAUTO_SKIP_LATENTS`
   - `PYAUTO_SMALL_DATASETS`, `PYAUTO_DISABLE_JAX`
   - `with_test_mode_segment(base)` (:190), which adds a test-mode segment to the output path
7. The version handshake is `workspace.check_version(library_version, workspace_root)` (`workspace.py:175-240`). The floor comes from `general.yaml version.minimum_library_version`, then `workspace_version`, then `version.txt`. It raises if the installed library is older, and warns if it is stale. Bypass with `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`.
8. `output.should_output(name)` (`output.py:10`) reads `output.yaml`, e.g. `search_log`.
9. Nerves has no notion of run identity, job id, or a machine profile.

## C. PyAutoCortex (`organs/PyAutoCortex`)

### `projects.yaml` schema (header :12-42)

It uses a closed, restricted YAML subset. The fields are:
- `remote`, `local_path`, `ral_root`, `mirror`
- `sync_cli`: the path of the project's sync CLI, e.g. `hpc/sync`
- `sync_verbs`: a flow list
- `ledger`: the project's own state file
- `assistant`, `witness_file`
- `partition`: `gpu | ral | both`
- `status`, plus an optional `note`

The **`euclid_dr1` row is at :104-116**:
- `local_path /mnt/c/Users/Jammy/Science/euclid_dr1`, `ral_root /mnt/ral/jnightin/euclid_dr1`, `mirror none`
- `sync_cli hpc/sync`
- 17 sync verbs: push, pull, logs, sync, push-data-init, pull-full, status, submit, push-submit, jobs, sacct, cancel, wait-and-pull, tail, du, check, clear-logs
- `ledger wiki/project/state.md`, `assistant autolens_assistant`, `witness_file results/**/*.json`, `partition ral`
- It was cloned from the pipeline on 2026-09-11.
- REFERENCE.md:121 says `witness_file` is "kept for the projects' own tooling; the Cortex no longer scores it".

### Ledger (`projects/euclid_dr1.md`)

- The header is `Project:` and `Issue:`.
- `## Now` is 2-3 prose lines, rewritten.
- `## Runs` has one line per job: `- <jobid> — open|running — <partition> — <date> — <what>`. The regex is at `scripts/cortex.py:92`.
- `## Log` is dated and newest first. Each entry is `- <date> — run|result|lesson|note — <text>`.
- The DR1 ledger has about 30 runs. Job-level facts such as array ranges, manifests, CPU, memory and walltime, dependencies and holds all live only in the free-text `<what>`.
- **Granularity is the SLURM job.** Per-array-task outcomes appear only as prose, e.g. "971 of 1000; 29 hit the 18-hour walltime", "992 lenses whose … log ended Finished vis_lp".

### Verbs (`scripts/cortex.py`, usage at :25-37, parser at :857-927)

- `run <key> <jobid> "<what>"` adds an `open` run and a `run … submitted` log entry (:594-610).
- `running` flips a run to `running` (:621).
- `done [--failed] [--wall H:MM] [--note]` removes the run and logs `finished`/`failed` (:632-651).
- `log --kind note|result|lesson` and `now` write prose.
- There are also `new`, `issue`, `link`, `retire` and `check`.
- `RUN_STATES = ("open","running")`, and "there is no third state" (:61-63). The run contract is binary plus a log line.

### Machine-readable state

There is almost none. Only:
- `checkin.yaml` (`refreshed:`)
- `census --json` in the Brain conductor

A richer layer existed and was **retired**. `docs/schema_decisions.md` decisions 39-41 and 51 defined a `.cortex/pull.json` manifest (`checkpoints: {run_dir: {bytes, mtime}}, runs: {jobid: {...}}`) and PASS/FAIL/UNOBSERVABLE scoring legs. Decision 60 (:430-440, 2026-09-12) cut all of it back to "one ledger per project" and dropped `collect`, the scoring legs and the pull manifest. "Nothing in a ledger is inferred from results" (`cortex.py:16-18`). Only the human writes `result`/`lesson` entries.

## D. PyAutoBrain (`organs/PyAutoBrain`)

- **Cortex skill:** `skills/cortex/cortex.md`. **Conductor:** `agents/conductors/cortex/_cortex.py` (1448 lines).
  - `pull` runs only on the laptop. For each active project it runs `<local_path>/<sync_cli> pull`, then `<sync_cli> jobs` (squeue), and prints the output **verbatim**. It parses nothing, flips no state and writes nothing (cortex.md:26-43).
  - `checkin` works on any surface. It stamps `checkin.yaml`, renders `dashboard.md/.html`, pushes a `claude/checkin-<date>` branch, and prints Now, Runs and the last five entries per project (cortex.md:48-73).
  - The agent may run `running`/`done` from the jobs output as "cluster facts" (:80-89).
  - Rules: never submit unless asked (:120-124); only the project's own CLI reaches a cluster (:130-131); "The door runs once and ends. No timer, no subscription, no cron, no loop" (:132-133).
- **No allowlist or permission classifier for scheduler commands.** `sbatch`, `squeue`, `scontrol` and `scancel` appear in the organs only in `agents/conductors/profiling/_profiling.py:263,374`, where they are printed dispatch strings. `.claude/settings.json:37-60` has two PreToolUse hooks:
  - the PyAuto API gate (`lens/autolens_assistant/.claude/hooks/validate_pyauto_code.py`)
  - the Mind commit guard
  
  plus the end-at-deliverable matcher. None of them inspects `ssh`, `hpc/sync` or `scontrol`. `scontrol hold/release/update` has been used by hand (ledger 2026-09-26; memory `RALpack`).
- `AUTONOMY.md:438-440` says a science member is never `--auto`, and a run is submitted only when the human asks.
- `skills/MODEL_DELEGATION.md:103-105` says Cortex work enters through the declared assistant.
- There is no Slurm or HPC helper library in Brain, Hands or Heart.

## E. autolens_assistant and euclid_strong_lens_modeling_pipeline

### `lens/autolens_assistant`: the hpc/sync template's home

- `hpc/sync` (600 lines of bash) is driven by `hpc/sync.conf` (HPC_HOST, HPC_BASE, PROJECT_NAME, PULL_DIRS…).
  - Transfer verbs: push, pull, logs, sync, push-data-init, pull-full, status.
  - Job verbs: submit, push-submit, jobs, sacct, cancel, wait-and-pull.
  - Inspect verbs: tail, du, check, clear-logs.
- `pull` rsyncs the SLURM logs, then each PULL_DIR with `--exclude=search_internal`, then **unzips every new zip locally** (:230-267). `submit` runs `ssh host "cd batch_<type> && sbatch <script>"` (:317-335). `wait-and-pull` is a blocking foreground poll (:375).
- In the template, `submit` takes **no extra sbatch args**. Its dispatcher passes only `$2 $3` (:585).
- `hpc/template.py` (263 lines) is the pipeline-script interface (`parse_fit_args`, `--use_cpu`, `--number_of_cores`).
- `hpc/batch_cpu/template` and `hpc/batch_gpu/template` are SLURM array templates. Each has one dataset per task, pins thread counts, and ends with an unconditional `echo "Finished dataset"`.
- `hpc/sync.conf.example` and `hpc/sync_jump.conf.example` configure the jump host.
- Wiki and skills:
  - `wiki/core/operations/hpc.md`: CPU regimes (JAX vs Numba sparse), JAX on GPU, batch arrays, "Persisting outputs" (resume by `unique_id`), gotchas (Numba cache, `output/` clashes, inversion memory about 32 GB for a 50×50 mesh).
  - `wiki/core/operations/hpc_infrastructure.md`: the directory structure, the template, GPU vs CPU templates with a checklist, and hpc/sync.
  - `skills/euclid_hpc_runs.md`: configure sync, adapt the batch template and submit, combine results.
  - `skills/start-new-project.md:317-330`: an optional HPC step that scaffolds `hpc/` and `sync.conf`.
  - `skills/euclid_setup_pipeline.md` and `wiki/project/_profile_template.md` mention HPC access.

### `lens/euclid_strong_lens_modeling_pipeline`

- It has its own `hpc/sync` (696 lines), which has **diverged** from the template:
  - `restrict_pull_dirs` (:142)
  - `submit … [sbatch arg …]` passthrough, e.g. `--array` and `--export=ALL,…` (:353-407, dispatcher :677)
  - `SSH_BULK` with an AES-GCM cipher
- `hpc/README.md` covers the route table and measured per-lens times:
  - GPU: 1h14-1h44
  - two-stage CPU: 3h17
  - SED: 8c/64 GB/12 h
- Submit scripts:
  - `batch_cpu/`: initial_lens_model{,_two_stage,_vis_lp,_vis_pix}, sersic_waveband, build_inspection_bundle, positions_gate, jax_fork_control
  - `batch_gpu/`: initial_lens_model, full_model, sersic_waveband
- **Stage gate:** `scripts/initial_lens_model.py:395-420` checks that vis_lp is complete (`restore()` + `is_complete`) before vis_pix, and otherwise raises `RuntimeError`.
- **Completion witness bug:** `batch_cpu/submit_initial_lens_model_vis_lp` has **no `set -e`**. Its last lines run `python3 … --stage=vis_lp` and then an unconditional `echo "Finished vis_lp: $dataset"`. A Python exception still prints "Finished vis_lp"; only a walltime kill suppresses it. The DR1 ledger selected the 356390-356450 vis_pix manifests by "log ended Finished vis_lp". Only `_two_stage` uses `set -e` (:74).
- **Run manifests** (`hpc/run_manifests/*.txt`, referenced in the ledger) live in the euclid_dr1 science checkout. That checkout is outside this workspace and was not read.
- **Aggregation:**
  - `scripts/build_inspection_bundle.sh` runs 10 stages and reads the result zips in place via `scripts/tools/build_inspect.py`.
  - `workflow/{csv,png,fits}_make.py` use the aggregator.
  - `scripts/tools/{positions_gate,rewrite_positions,diagnose_latent*,compare_catalogues}.py` are other tools.
  - There is **no status or summary script** that turns logs or `.completed` markers into a per-lens table.

## F. `organs/PyAutoMind/policy/end_at_deliverable.md`

A session ends when it reports its deliverable. It must never arm anything that outlives the turn to wait for CI, a review or a merge:
- `send_later`
- `subscribe_pr_activity`
- `CronCreate`
- `ScheduleWakeup`
- `/loop`
- `RemoteTrigger` create/update/run

The rule is "judge once, report, stop". A PreToolUse matcher hook enforces it (`.claude/settings.json`, `end_at_deliverable_hook.sh`). The Cortex door restates it: "no timer, no subscription, no cron, no loop".

For monitoring designs this means any watching must be done by something **on the cluster**. That means SLURM itself (`--dependency`, epilog), the fit writing its own status file, or a cron on RAL owned by the human. An agent can only read that state once per human-initiated check-in. `hpc/sync wait-and-pull` is a foreground poll that the hook does not catch, but it breaks the spirit of the rule if an agent runs it.

## Gaps

- **Per-fit status record.** No file says whether a fit is running, completed or failed, what attempt it is on, or its job id and task id. `.completed` is the only machine signal, and it is buried in the zip under `hpc_mode`. With 1e99 update cadences a running fit writes nothing structured. A small atomic `files/status.json`, written at start, at chunk boundaries and in a `finally`, belongs in PyAutoFit, next to `Timer` and `paths.completed()`.
- **Resource measurement.** No peak RSS, CPU time, GPU memory or per-attempt wall clock is recorded. The timer lives in `search_internal/`, which is deleted and not pulled. `samples_info.time` survives only in the final JSON. SLURM `sacct` (MaxRSS, Elapsed, State, ExitCode) is only printed verbatim. Nothing captures it per task, even though over-reserving (64 GB reserved vs 4 GB peak, memory `RALpack`) is the main cost lever.
- **Failure recording.** `fit()` has no exception handler, so there is no `.failed` or traceback artefact. The batch templates echo "Finished" unconditionally (the vis_lp script has no `set -e`). The Cortex has `done --failed` per job only, with no per-task outcome, exit code or reason class (walltime, OOM, exception, bad input).
- **Stage-output validation.** The only checks are the pipeline's vis_lp→vis_pix `is_complete` check and the aggregator's `completed_only`. Nothing validates zip integrity, because `zip_directory` is non-atomic and `restore()` deletes the directory before extracting. Nothing validates expected members (samples_summary, result files) or seeds for downstream stages such as SED. `restore()` is also not safe against concurrent readers of a shared upstream result.
- **Resume guarantees.** Resume depends on the sampler checkpoint in `search_internal/`, the identifier hash, and a correct `restore()`. There are no guarantees against:
  - truncated zips from a walltime kill during zipping
  - partial checkpoints
  - two jobs sharing one identifier
  - resumed attempts not being counted
  
  There is also no "requeue-safe" contract for SLURM `--requeue`/`--signal`, such as a SIGTERM handler that flushes a checkpoint.
- **Campaign-level aggregation.** Campaign facts live in prose (the Cortex ledger `<what>` strings) plus manifests in the science repo. Nothing joins manifest entries with SLURM task state, fit status and result presence into a per-lens table. The aggregator walks and extracts the whole tree on every call. The machine-readable pull manifest (Cortex decision 51) was retired in decision 60. The two `hpc/sync` copies (template vs pipeline) have drifted, and no status or summary verb exists in either.
- **Governance.** No action allowlist or classifier exists for scheduler-mutating commands (`sbatch`, `scancel`, `scontrol hold/release/update`) run over `ssh`/`hpc/sync`. The only rules are prose ("never submit unless asked").
- **Site config.** No Nerves layer carries cluster facts (partitions, memory per node, walltime, scratch paths). They are spread across `sync.conf`, the submit-script headers and memory notes.
