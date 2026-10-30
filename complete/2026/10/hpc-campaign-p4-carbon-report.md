- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1746
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/208
- completed: 2026-10-30
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1748
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/209
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1748
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/209
- epic: hpc-campaign (phase 4; ledger draft/research/autofit/hpc_campaign_epic.md)
- summary: `autofit/campaign/carbon.py` — Green Algorithms estimate, four cases (low / central usage basis /
  allocation u=1 / high), ranges from site low/high, CI bounds = spread across bases (F6), successful vs
  failed/repeated vs in-progress split, per-task values, `forecast()` for planned stages, no GA default
  fallbacks, NESO fetch + `--begin-hint` opt-in and cached; `report.py` — `campaign report` (compute, energy +
  carbon, failure census, stage tables, results counts, paper paragraph: "estimate", range, CI basis, exclusions,
  never "saving"). PyAutoNerves: optional `carbon_intensity` table + `Site.ci(basis)`; ral.yaml regional 188
  (81–308), national 129 (51–231), DESNZ 177, all unverified; ci_basis value required.
- witness: W4 — DR1 from the W2 retro digest, Workspace/Science/scratch/hpc_campaign_p4_w4/: ≈3.5 MWh (1.7–6.0),
  ≈651 kgCO2e (221–1,119) regional basis; 30 % of finished-work energy failed/repeated; ~2× the §1.4 forecast from
  workload (22k vis_lp, 23k SED tasks vs 5k), not the model.
- tests: campaign 151 (stacked); full PyAutoFit suite 4,143; Nerves 284; smoke autofit 10/0; CI all green.
  §1.4 worked example reproduced exactly. Independent review FINDINGS (null CI basis crash, zero-energy report
  crash, running counted as failed, --ci label, missing source) fixed in 8e7a1f5b4 / dba2819. #1748 retargeted to
  main after #1747 merged.
- open ruling: CI high bound uses the base spread, so RAL high = central (188); regional p95 (308) unused.
- heart: shipped and merged under the human-authorized Heart RED development override; merge by separate /prm.

## Original prompt

Issued: 2026-10-30
Epic: hpc-campaign
Phase: 4
Blocked-by: phase 2 (COMPLETE 2026-10-30)
Concurrent-with: hpc-campaign phase 3 (owns campaign/evidence.py, plan.py, pilot.py); this task owns campaign/carbon.py, report.py + PyAutoNerves site CI keys; shared campaign/__main__.py — rebases after p3
Consequence: judge
Autonomy: human-required
Witness: W4 — DR1 carbon estimate (central + range, both bases, CI basis named, labelled estimate) from the W2 retro digest, in Workspace/Science/scratch/hpc_campaign_p4_w4/

# HPC campaign phase 4 — carbon and campaign report

Original request (human, 2026-10-30): "do both" (hpc-campaign phases 3 and 4, in parallel), after
"Ctoninue the PyAutoLEns II HPC runs and Results".

Lane prompt: Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/PROMPT_hpc_campaign.md §Phase 4;
report §1.4 (draft/research/autofit/hpc_campaign_epic_report.md).
@PyAutoFit: Green Algorithms model, usage (central) + allocation (upper) bases, site low/high ranges, CI basis
named, optional cached NESO fetch (offline default), `--begin` hint off by default, successful vs failed/rerun
split, per-object values; `campaign report` from a live or retro digest with a paste-ready paper paragraph
("estimate", range, CI basis; no "savings" wording). @PyAutoNerves: CI keys in site schema + site/ral.yaml.
Done: §1.4 DR1 fixture reproduced within rounding; W4.
