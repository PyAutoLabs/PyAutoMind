# Shift watcher: findings from the M1 exit-test shadow shift (2026-11-13-am)

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: glance
Witness: (1) a fake-clock test with a 28-minute gap between ticks inside the window reports stall minutes ≥ 28 in the digest and the pilot.jsonl row; (2) a shadow/unattended plan runs the cheap premise check on its picks and drops (or flags) an `obsolete` draft; (3) a pick whose draft has no `Review-minutes:` shows the sizing-faculty estimate, not `~0`
Review-minutes: 10
Unattended: never
Lane: any

Source: the M1 exit-test shadow shift `batches/2026-11-13-am.md` (digest PyAutoMind#561, ledger 790ded32). The exit test passed (digest and pilot.jsonl row agree with GitHub and the workers); these are what it showed.

1. **Missed ticks are not stall time.** The laptop slept 09:31–09:59Z (no ticks); the row's `stall_minutes` is 0 and the digest says nothing.
2. **Planning ignores the premise check.** `remove_eden_packaging_tooling` (obsolete since `eden.yaml` was deleted 2026-11-10) was proposed; the check runs only at worker start (programme M1.3). Run it at plan time too (it is cheap, no LLM).
3. **Review-minute estimates show `~0`** for every pick in the digest.

<!-- filed 2026-11-13 by the programme lead session -->
