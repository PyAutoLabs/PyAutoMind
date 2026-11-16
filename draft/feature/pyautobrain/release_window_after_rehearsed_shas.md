# Release window after rehearsed SHAs: retire the laptop freeze flag, and start the nightly when it should start

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoHeart
- PyAutoHands
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: judge
Witness: (a) `git grep -n -i "freeze" -- skills/ AUTONOMY.md` in PyAutoBrain and `skills/pre_build/pre_build.md` in PyAutoHands return only the retirement note; `pyauto-heart freeze --show` prints "retired"; (b) a library PR merged during a release validation does not change what that night publishes (rehearsed SHAs, M2.4) and is named in the night's outcome as "merged after rehearsal, not in this release"; (c) the scheduled start hour of the next 7 nightly runs (`gh run list -R PyAutoLabs/PyAutoBrain --workflow nightly-release.yml --event schedule --json createdAt`) is recorded against the new trigger
Review-minutes: 15
Unattended: never
Lane: any

Source: REL-8 and REL-9 of the ecosystem review (2026-11-10), section B8. **Both unverified by the review: re-check first.**

**Why now.** M2.4 (PyAutoHands#339) made the live release build the rehearsed SHAs, so a merge during validation no longer changes what ships. Both REL-8's harm (a "quiet window" that does not exist) and REL-9's purpose (protect the window) were about that.

**REL-9, the freeze flag (anchors on origin/main 2026-11-13):** `PyAutoHeart/heart/freeze.py:58` (a laptop file); `PyAutoHands/skills/pre_build/pre_build.md:49-61` (the only setter); `PyAutoBrain/skills/prm/freeze.md` (the only enforcer, `/prm` on the holding laptop); `PyAutoBrain/AUTONOMY.md:723` keeps "return to `ref: main` plus the freeze flag" as the fallback if the SHA path breaks.
- Re-check: `grep -n "## Freeze overrides" PyAutoMind/autonomy_log.md` (review: none ever); `grep -ci freeze ~/.pyauto-heart/logs/heart.log`.
- Change: retire the flag and the `/prm` step; replace the AUTONOMY.md:723 fallback with "stop the release" (no unpinned fallback). If a window is still wanted, hold it GitHub-side (a repository variable the merge paths read), never a laptop file.

**REL-8, the start time:** `PyAutoBrain/.github/workflows/nightly-release.yml:48` (`cron: "0 2 * * *"`), measured starts 06:00–10:00 UTC; `PyAutoHeart/.github/workflows/heart-health.yml:44` (`0 5 * * *`).
- Re-check: the start-hour histogram since 2026-11-01 (command in Witness c).
- Options for the human: (1) leave it (SHAs make the delay harmless; cheapest); (2) move the cron earlier by the measured delay; (3) dispatch the nightly from the shift scheduler (M6) at a fixed time. Recommend (1) now and (3) at M6.

Tier judge: retiring a release-safety control and moving the release time are the human's.
Programme: M2 side lane (after M2.4); REL-5's laptop-state draft drops the freeze file once this lands.

<!-- drafted 2026-11-13 by the REL intake session (scratch/intake_2026-11-13) -->
