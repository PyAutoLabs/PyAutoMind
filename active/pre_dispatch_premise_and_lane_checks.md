# Before a run is spent: check the draft's premise and its lane

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-11-10
Issued: 2026-11-12
Epic: autonomous-orchestrators
Consequence: judge
Witness: (a) the premise check replayed on the two prompts that were obsolete in the 2026-11-06-pm shift (delaunay_smoke_300s_cap, gallery_runner_missing_tiers, at the Mind commit before that shift) returns `obsolete` with its evidence, each in a few thousand tokens; (b) after the backfill, no draft in the planner pool lacks a `Lane:` header; (c) a test shows an unattended session excludes a draft whose Lane is absent
Review-minutes: 20
Unattended: needs-slicing
Lane: any

Source: the ecosystem review of 2026-11-10, findings MIND-2 and MIND-3, both confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, section B6 and Appendix A.

**What was measured.**
- In the one live shift that worked, 2 of 3 dispatched tasks were obsolete on `main`, one day after a sweep of 280 drafts. Both workers noticed and stopped, but each had been paid for as a full run. The shift worker template has no premise step, and the planner rejects only drafts flagged looks-shipped or whose Status says done. That guard looks for work that arrived and cannot see a premise that has gone away (a deleted file, a defect already fixed); its recall on the sweep was 4 of 27.
- `Lane:` is present on 12 of about 270 drafts, and an absent Lane reads as `any` by documented design (`_batch.py:113`, `_sizing.py:449-451`, `REFERENCE.md:501`). None of the 115 drafts in the planner pool carries one, and two drafts declared `Unattended: ready` have a Witness that needs RAL or an A100. Intake has inferred Lane at filing since 2026-11-03 but not from "A100" or "HPC", and the older backlog was never backfilled.

**Slice 1: a premise check (glance).** The first step of every dispatched run, before any implementation: on a fresh view of `main`, confirm that the files, functions, issues and PRs the draft names still exist and that the defect or gap can be reproduced. If not, return `obsolete` with evidence and stop. Record the result as a `Verified: <date> <sha>` header so the planner can prefer recently verified drafts. Run the same check at brief time, so the human sees "stale" before the shift starts.

**Slice 2: a Lane backfill (glance).** One scripted pass over the pool: a search for RAL, SLURM, A100, HPC, GPU, `/mnt/` and private data proposes `local-dev`, `ral` or a GPU lane; the rest get an explicit `any`. The human skims the proposals. Teach intake's inference the missing words.

**Slice 3: fail closed (judge).** In an unattended or cloud session, treat an absent Lane as unknown and exclude the draft; reject a new draft filed without one. This reverses a documented default, so it is the human's ruling.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
