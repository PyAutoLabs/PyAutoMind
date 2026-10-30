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
