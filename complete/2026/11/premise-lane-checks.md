Programme task **M1.3**, slices 1–2 (epic `autonomous-orchestrators`, phase 8), findings MIND-2 and MIND-3. Shipped as PyAutoMind#559 (5617341ed) and PyAutoBrain#609 (c7e7c1c16), merged 2026-11-12. Issue PyAutoBrain#608. Slice 3, an absent Lane failing closed, is a judge ruling and is programme M2.3.

**Built:**
- `pyauto-brain batch premise <draft>`, a mechanical premise check with no LLM call.
  - It returns `ok`, `obsolete` or `unknown` with evidence.
  - It is the first step of the shift worker template, which stops on `obsolete`.
  - `batch brief --check` warns on obsolete picks.
  - `--write-verified` writes a `Verified:` header through the new `set-header` one-Mind-writer op.
- `bin/lane_backfill.py`, which proposes and applies a Lane for each pool draft. Intake now counts lane words only in a requirement context.
- **The backfill was applied** after the human approved the proposals at the block gate: 119 drafts (109 any, 8 ral, 2 wsl-data), Mind e25156929.

**Witness** (command and observed result):
- (a) `pyauto-brain batch premise --at 2026-11-06T11:20Z` returns `obsolete` for:
  - `delaunay_smoke_300s_cap`: the newest Heart smoke runs took 8.6–15.9 s against the ≥300 s claim;
  - `gallery_runner_missing_tiers`: `scripts/gallery/gallery_run.sh` was removed in 0dc177b on 2026-09-30.
- (b) After the backfill, `lane_backfill.py --mind .` finds 0 pool drafts without a Lane.
- Brain suite: 1718 passed. Mind suite: 772 passed. CI green.
- Pool premise sweep: 84 ok, 42 unknown, 1 obsolete (`remove_eden_packaging_tooling`: `eden.yaml` deleted on 2026-11-10; left for a human to retire).

**Review:** an independent Opus review returned FINDINGS:
- two false-`obsolete` routes: a nested path to create, and an upstream function;
- a bare "GPU" word picking the `gpu` lane;
- a crash reading as `obsolete`;
- a ledger wedge on a moved draft;
- the digest wording.

All were fixed. The re-review was CLEAN.

**Heart:** RED at ship (local canonical checkouts; install check F; release integrate). The live human gave a development-only override plus the merge command at the block gate.

Follow-ups: `draft/feature/pyautobrain/premise_check_followups.md`.

## Original prompt

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
