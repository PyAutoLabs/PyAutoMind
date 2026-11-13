Programme **M2 finish** (epic `autonomous-orchestrators`, phase 9). Shipped as PyAutoHands#340 (9f7c70327), PyAutoHeart#345 (00d979a20) and PyAutoBrain#621 (e7d8eb29d), merged 2026-11-13. Issues PyAutoHeart#343 and #344.

- **#343, repos Heart does not poll** (human ruling 2026-11-13): they are not Heart-gated. `readiness --dev` lists them as gate-deferred and shown. At merge, the PR checks must include at least one completed check, all green (watcher `pr_health`, `/prm` and AUTONOMY leg 4). Replay: the parked share falls from 36.9% to 4.7%.
- **#344, Stage 3** (human ruling 2026-11-12):
  - One retry, for FAILED scripts only. The attempt's new output is cleaned first, and a pass on retry is recorded as flaky.
  - A quarantine needs a bug ref, expires after at most 7 days, allows at most 3 active, and reads YELLOW.
  - A rehearsal that skipped a script whose entry is gone reads RED.
  - REL-3 was re-checked and holds.

**Witness:**
- Heart suite: 1454 passed. Brain suite: 1822 passed. Hands suite: 639 passed. CI green on all three PRs.
- **Gate:** Heart's scoped dev-ship verdict was GREEN at 14:00Z for Heart, Hands and Brain. No RED override was needed: the first ship through the M2.1 gate.

**Review:** three rounds of FINDINGS, then CLEAN.

**Human rulings at the gate, 2026-11-13:**
- ship;
- a quarantine-only YELLOW may let the nightly ship (to build: `draft/feature/pyautobrain/nightly_ships_on_quarantine_only_yellow.md`);
- no retry for timeouts.

Follow-ups: `draft/maintenance/pyautobrain/m2_build_followups.md` items 9–11.
