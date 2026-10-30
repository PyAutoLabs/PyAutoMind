- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1740
- completed: 2026-10-30
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1741
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1742
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1741
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1742
- epic: hpc-campaign (phase 2; ledger draft/research/autofit/hpc_campaign_epic.md)
- summary: New `autofit/campaign/` (stdlib + PyYAML, no Slurm at import). **2a (#1741):** `campaign.yaml`
  loader/validator (stages, manifest chunks ≤ site max_array_size, --mem-per-cpu, aftercorr deps, success
  checks, propose-only retry, autonerves site layer); Scheduler protocol + Fake/Local/Slurm adapters (batched
  sacct/squeue/sinfo via injectable runner; sbatch with aftercorr, --kill-on-invalid-dep=yes,
  --signal=B:USR1@600); partition lint on validate/submit/update_pending — CPU-only never on a GPU partition,
  mixed `ral,gpu`/`gpu,ral` always refused, timing-leg exemption (≤8 CPUs, ≤%2, no pending GPU jobs) fails
  closed; atomic job ledger. **2b (#1742):** collector (sacct + status records joined by job/task ids),
  digest.json + ≤2 KB digest.md + tasks.jsonl + failed_<class>.txt, propose-only resubmits (timeout p95+25 %,
  OOM peak×1.5, site-capped; `submit --proposal` is the human act), retro mode from a sacct dump.
- witness: W2 — retro over the F4a DR1 sacct dump: 61,078 Slurm tasks, 709.8k CPU-h (29 % failed/repeated),
  sed 12 % timeouts, memory requests 2–4× p95 peak, 568 CPU tasks on `gpu` (09-30 incident); in
  Workspace/Science/scratch/hpc_campaign_p2_w2/ (never committed).
- tests: full PyAutoFit suite 2a 4,082 / 2b 4,098 passed; CI unittest 3.12/3.13/nojax + docs green on both;
  smoke autofit green. #1742 retargeted from the 2a branch to main after #1741 merged (same head, CLEAN).
- decisions flagged: mixed partition lists always refused; cancelled/requeued/preempted stay campaign strings
  (possible RunState.CANCELLED follow-up); only digest.md capped at 2 KB.

## Original prompt

Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1740
Epic: hpc-campaign
Phase: 2
Blocked-by: phase 1 (COMPLETE 2026-10-29)
Concurrent-with: results-library phase 1 (ruling F11 — two PyAutoFit worktrees; this task owns `autofit/campaign/` only and imports `non_linear/status/states.py` read-only)
Consequence: judge
Autonomy: human-required
Witness: W2 — `python -m autofit.campaign retro --sacct` over the F4a dump `Workspace/Science/active/euclid_dr1/inspect/sacct_retrospective_2026-10-28/sacct_jnightin_20260901_20261028.psv` filtered to the DR1 WorkDirs; digest + figures (dataviz skill) in `Workspace/Science/scratch/hpc_campaign_p2_w2/`; never committed to a public repo.

# HPC campaign phase 2 — campaign core, scheduler adapters, collector, partition lint, retrospective mode

Original request (human, 2026-10-30): "Ctoninue the PyAutoLEns II HPC runs and Results"

Ledger: `draft/research/autofit/hpc_campaign_epic.md` (Hard constraint; rulings F4, F5).
Report: `hpc_campaign_epic_report.md` §3.2 (campaign.yaml, digest schema).
Lane prompt: `Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/PROMPT_hpc_campaign.md` §Phase 2.

@PyAutoFit scope (`autofit/campaign/`, stdlib + PyYAML, no Slurm at import):
- `campaign.yaml` loader/validator (stages, manifest, chunking ≤ max_array_size, resources, `after`,
  `success`, propose-only `retry` (F5), `site:` from PyAutoNerves `site.yaml`).
- `Scheduler` protocol + `FakeScheduler`, `LocalScheduler`, `SlurmScheduler` (batched sacct/squeue/sinfo,
  sbatch generation with aftercorr, --kill-on-invalid-dep=yes, --mem-per-cpu, --signal=B:USR1@600).
- Partition lint: refuse `gpu` in a partition list for a no-gres script unless all three exemption
  conditions hold at submit time; `gpu_only` partitions never packed with CPU tasks.
- Collector → `digest.json` + `digest.md` (≤2 KB), `failed_<class>.txt`, propose-only resubmits.
- Retrospective mode `campaign retro --sacct <dump> [--status-root]`.
- CLI `python -m autofit.campaign {validate,submit,status,resubmit,retro}`.

Done: FakeScheduler end-to-end with injected timeout/oom/exception/missing-seed; digest size test; lint
tests for every branch incl. `ral,gpu` and `gpu,ral`; synthetic sacct retro; W2 witness (F4a authorised).
