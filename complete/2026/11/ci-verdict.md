Programme **M4.6**, part 1 (epic `autonomous-orchestrators`, phase 11). Shipped as PyAutoBrain#629 (7e2d16f71), merged 2026-11-14 on the human's command. Issue PyAutoBrain#628.

**Re-check** (posted on #628): FB-4 partly holds, and FB-5, REL-6 and FLOW-3 hold. A fourth CI judgement was found in the batch collector.

**Built:** `pyauto-brain ci-verdict <owner/repo>#<n>`.
- Judges every check-run, run, job and commit status for the REST head sha.
- Exit 0 GREEN, 2 PENDING, 1 RED. Mergeability is part of the verdict, and an empty sha is refused.
- `/prm` step 2 and the close-out template run it. `pr_health` delegates its judgement to it, so the watcher's network surface is unchanged.

**Also fixed:** a time-bomb test (`test_batch_green` full brief run). It dated a fake Heart reading at a fixed 2026-11-13 time, so it went red on main after 01:30Z on 11-14. It now pins `--at NOW`; no assertion changed.

**Witness:**
- 37 new tests, offline.
- Brain suite: 1973 passed.
- CI green.
- Live read-only checks: Brain#626 GREEN, Mind#567 GREEN with the skipped leg named, fork PR Array#675 GREEN, Galaxy#697 RED.

**Review:** CLEAN.

Follow-ups: `draft/maintenance/pyautobrain/ci_verdict_followups.md`; the dependants'-tests half is `draft/feature/pyautobrain/dependants_tests_after_library_merge.md`.
