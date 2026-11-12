# M2 builds: follow-ups found in review (2026-11-12)

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoHeart
- PyAutoHands
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: one test or recorded check per item; after the M2 merge, one `heart-refresh` dispatch run id recorded from a library merge
Review-minutes: 10
Unattended: never
Lane: any

Source: the independent reviews of Heart#340, Brain#614 and Hands#337 (programme M2). None blocks the M2 merge.

1. **Witness after merge:** record one `heart-refresh` `repository_dispatch` run on PyAutoHeart triggered by a library merge (confirms the App token can dispatch), and pull the canonical Heart checkout so `readiness --dev` exists locally.
2. **Repos Heart does not know** (e.g. `Jammy2211.github.io`) are a usage error → the dev gate parks forever. Decide: add to `excluded:` (STALE) or to a "not Heart-gated" list.
3. **Hands `release.yml` workspaces still check out and tag `ref: main`** (lines ~480, ~1054, ~1065); the Colab links point at those tags.
4. `skills/intake/intake.md` step 1 does not mention `--lane` (intake now refuses a Lane-less draft).
5. `queue_retire_text` collapses 3+ blank lines across all of queue.md (cosmetic).
6. Heart `ci_status.py:492` `write_and_summarise` looks unused.
7. Hands `release.yml` does not yet send `heart-refresh`.
8. A machine-readable override column in `autonomy_log.md` (so the M2.1 replay need not parse prose).

<!-- filed 2026-11-12 by the programme lead session -->
