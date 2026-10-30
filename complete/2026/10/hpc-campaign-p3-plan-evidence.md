- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1745
- completed: 2026-10-30
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1747
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1747
- epic: hpc-campaign (phase 3; ledger draft/research/autofit/hpc_campaign_epic.md)
- summary: `autofit/campaign/evidence.py` (readers for profiling-summary@3, walltime-validation@1,
  inference-summary@2 by path/URL; opaque stage keys under `evidence:`; grades measured-current / provisional /
  analogue / superseded / estimated / unsupported; "optimal" only with a current, key-scoped Pulse designation),
  `plan.py` (`campaign plan` → plan.md + plan.json, every number graded with record ids; CPU right-size below
  0.6 efficiency; mem = pilot max RSS ×1.25 in 4 GB steps; wall p95+25 % in 15-min steps, censored flag, size
  bins; cores-mismatch scaling graded estimated; max-of-best-grade evidence choice; throttle 50 % of stated idle
  CPUs; ETA upper bound), `pilot.py` (stratified 1–2 % `pilot.json`, never submitted).
- witness: W3 — graded 5,000-lens Euclid VIS plan in Workspace/Science/scratch/hpc_campaign_p3_w3/ (vis_lp 4 CPU /
  8 GB / 5:00, vis_pix 8 / 20 GB / 10:45, SED 2 / 8 GB / 4:00 censored; ≈108k CPU-h; ETA ≤ 63.5 h; 0
  measured-current — no Euclid walltime/inference records; gaps listed for the likelihood-lifecycle ledger).
- tests: campaign 128; full PyAutoFit suite 4,120; smoke autofit 10/0; CI unittest 3.12/3.13/nojax + docs green.
  Independent review FINDINGS (cores mismatch, first-match evidence, cost fallback, ungraded numbers, designation
  scope) fixed in 32a9305d2.
- heart: shipped and merged under the human-authorized Heart RED development override (autonomy_log
  red-override row 2026-10-30); merge by separate human /prm with all CI green.

## Original prompt

Issued: 2026-10-30
Epic: hpc-campaign
Phase: 3
Blocked-by: phase 2 (COMPLETE 2026-10-30)
Concurrent-with: hpc-campaign phase 4 (owns campaign/carbon.py, report.py); this task owns campaign/evidence.py, plan.py, pilot.py; shared campaign/__main__.py — p3 merges first
Consequence: judge
Autonomy: human-required
Witness: W3 — graded 5,000-lens Euclid VIS plan (vis_lp → vis_pix → SED) from live Pulse/Insight JSON, in Workspace/Science/scratch/hpc_campaign_p3_w3/

# HPC campaign phase 3 — evidence readers, plan, pilot

Original request (human, 2026-10-30): "do both" (hpc-campaign phases 3 and 4, in parallel), after
"Ctoninue the PyAutoLEns II HPC runs and Results".

Lane prompt: Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/PROMPT_hpc_campaign.md §Phase 3.
@PyAutoFit: readers for profiling-summary@3, walltime-validation@1, inference-summary@2 (path/URL; opaque
match keys under `evidence:`); evidence grades on every number; never "optimal" without a Pulse designation
record; `campaign plan` (plan.md + plan.json); `campaign pilot` (stratified 1–2 % manifest, never submitted
here). Done: DR1 repack numbers reproduced from a sacct fixture; W3.
