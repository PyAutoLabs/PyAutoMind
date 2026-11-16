# ci-verdict: follow-ups from the M4.6 review

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-14
Epic: autonomous-orchestrators
Consequence: glance
Witness: one test per item; `/prm` merges with `--match-head-commit <judged sha>`
Review-minutes: 10
Lane: any

Source: independent review of PyAutoBrain#629 (programme M4.6). None blocked the merge.

1. `/prm` (`skills/prm/prm.md` ~121): `gh pr merge` should pin `--match-head-commit <sha>` — the sha `ci-verdict` judged — so a push between verdict and merge cannot merge an unjudged head.
2. Zero checks seconds after a push reads RED `no-checks`; make it PENDING for a short grace window after the head commit time.
3. Rows carry no job id / log URL; `/prm` says fetch the failing job's log at once — include them.
4. `mergeable_state == has_hooks` (GitHub Enterprise only) reads RED; treat as clean.
5. The batch collector (`_batch.py` `leg_green`, `headRefOid` at ~1068) is a fourth CI judgement — point it at `ci_verdict.judge` and the REST head sha.

<!-- filed 2026-11-14 by the programme lead session -->
