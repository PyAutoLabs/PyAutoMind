## hpc-campaign-p1-status-record
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1735
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/206
- completed: 2026-10-29
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1738
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/207
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/179
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/207
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1738
- epic: hpc-campaign (phase 1; ledger draft/research/autofit/hpc_campaign_epic.md)
- summary: Per-fit status record in new `autofit/non_linear/status/`: `states.py` (RunState,
  FailureClass, Product — the shared vocabulary), atomic `<output_path>.status.json` (≤2 KB, cadence
  `hpc.status_interval_s` 60), append-only `.status.jsonl` (resumed fit = attempt 2), failure record
  (`failed` + failure_class + `.traceback.txt`, exception re-raised), SIGUSR1 → checkpoint flush +
  `timeout_pending`, SIGTERM same then exit 143; `progress()` for Nautilus/Dynesty/Emcee/BFGS/LBFGS;
  `hpc.status: false` writes nothing. PyAutoNerves site layer: `site.yaml` schema with ranges and
  `unverified`, `Config.push_site`, shipped `site/ral.yaml` (`gpu` gpu_only; `Site.check_cpu_job`
  rejects gpu, ral,gpu, gpu,ral). autofit_workspace: cookbook `search.py` Status Record / Batch Job
  Time Limits / Turning It Off + `general.yaml` keys.
- tests: Fit suite green; merge result main+#1736+#1738 3,976 passed; Nerves 280 passed; smoke
  autofit+autolens_test 47/47 on the combined worktree; CI green on all legs of all three PRs.
- traps: the docs' `exec python ...` advice (so a `--signal=B:USR1` reaches the fit) is untested on a
  real Slurm job. autofit_workspace was merged once #1738 merged (library-first gate), before release.
- next: hpc-campaign phase 2 (campaign core + Slurm/Local/Fake adapters + collector + partition lint +
  retrospective sacct mode).

## Original prompt

# HPC campaign phase 1: per-fit status record, failure record, shared state vocabulary (PyAutoFit) and site config (PyAutoNerves)

Type: feature
Target: autofit
Repos:
- PyAutoFit
- PyAutoNerves
- autofit_workspace
Themes:
- hpc
- results
Difficulty: large
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Witness: a local Nautilus fit writes `<output_path>.status.json` (≤2 KB, atomic) at start, at cadence, on completion; killed-and-resumed shows `attempt: 2` in `status.jsonl`; an exception in `fit()` writes `state: failed` + `failure_class` + a traceback file and re-raises; SIGUSR1 flushes the checkpoint and writes `timeout_pending`; `hpc.status: false` changes nothing; `autofit.non_linear.status.states` imports cleanly; PyAutoNerves `Config.push_site("ral")` loads an example `site/ral.yaml` with `gpu` marked `gpu_only` and unconfirmed values `unverified: true`; `autolens_workspace_test` smoke green
Review-minutes: 45
Unattended: never
Epic: hpc-campaign
Phase: 1
Parent: draft/research/autofit/hpc_campaign_epic.md
Blocked-by: results-library phase 0 PR 0a — for merge order only (both touch `abstract_search.py`); development starts now
Filed: 2026-10-28
Issued: 2026-10-28
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1735 ; https://github.com/PyAutoLabs/PyAutoNerves/issues/206

Phase 1 of the `hpc-campaign` epic (ledger `draft/research/autofit/hpc_campaign_epic.md` §"Phases (amended
2026-10-28)"; report `hpc_campaign_epic_report.md` §3.2 schema, issues #C/#D/#E). Scoping review:
`/mnt/c/Users/Jammy/Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/REVIEW.md`
§C.1, §D.4. Rulings F1 (failure record moved here), F6 (site constants as ranges, `unverified`), F11.

Ground against PyAutoFit `main` at or after `8740092dc`: `abstract_search.py` `fit()`, `_complete_fit`,
`post_fit_output`; `run(ctx)`/`FitContext` (#1689–#1692, `fit_context.py`, `execution.py`);
`checkpoint.py`, `internal_state.py`, `runtime.py`; `config/general.yaml` `hpc.*`, `output.*`. The plan
quotes the current lines.

## PyAutoFit — `autofit/non_linear/status/`

- `states.py`: run states `pending, running, completed, failed, timeout_pending, skipped` (collector-only
  `timeout, oom, node_fail`), failure classes `exception, bad_input, missing_seed, upstream_incomplete`,
  product names. The single vocabulary both epics import.
- `StatusWriter`: atomic `<output_path>.status.json` (≤2 KB) at start, every `hpc.status_interval_s`
  (default 60), on USR1/TERM, completion and failure; `status.jsonl` attempt history; beside the zip so it
  survives `remove_files`.
- **Failure record** on exception in `fit()`/`run(ctx)`: `state: failed`, `failure_class`, traceback file,
  re-raise.
- `progress()` protocol (Nautilus, dynesty, emcee, MLE); resource probe (cgroup v2 `memory.peak` →
  `getrusage`; NVML when a GPU is allocated; CPU model; `SLURM_*` via a generic env mapping); SIGUSR1 →
  checkpoint flush + `timeout_pending`; SIGTERM same then exit 143. Records the `dataset_identity.json` path
  when present.

## PyAutoNerves — `site.yaml`

Schema (partitions with `gpu_only`, `cores_per_node`, `mem_per_node_mb`, `max_time`, `max_array_size`,
`tdp_w_per_cpu`, `cpu_is_thread`, `gpu_model`, `gpu_tdp_w`; `pue` range; `grid_region`; `ci_basis`;
`energy_accounting`), `Config.push_site(name)`, validation, example `site/ral.yaml` (`unverified: true`
where unconfirmed). Nerves imports no autofit.

## autofit_workspace

`hpc/` guide section on the status record and the resume contract (after the library PR merges).

## Worktree file ownership (review §D.4, ruling F11)

This lane: `autofit/non_linear/status/`, `config/general.yaml` new `hpc.status_*` keys, later
`autofit/campaign/`. Shared touchpoint `non_linear/search/abstract_search.py` and `fit_context.py`:
**merges after results-library PR 0a**. Ships `pending-release`.
