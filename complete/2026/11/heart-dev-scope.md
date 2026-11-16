Programme **M2.1** (epic `autonomous-orchestrators`, phase 9). Shipped as PyAutoHeart#342 (4ffd239f0), merged 2026-11-13. Issue PyAutoHeart#340.

**Human ruling (M1 gate, 2026-11-12):** a dev ship is blocked only by reasons inside the repos it touches, plus their library CI and dependants. A feed older than 6 h is re-checked or parks. STALE never passes. Event triggers refresh the feed.

**Built:** `pyauto-heart readiness --dev --repos A,B`.
- **Blocks:** red main CI of each declared CI workflow (`dev_ship.ci_workflows`) in the touched repos and the libraries downstream of them.
- **STALE:** unfinished or unrecorded runs, unpolled repos, feeds over 6 h old or timestamped in the future, and evidence with no conclusion.
- **Shown, never blocking:** ops workflows and release-scope workflows.
- `ci_status` fetches declared workflows that fall off the 30-run page.
- `heart-health.yml` runs on `repository_dispatch: heart-refresh` and on Release Integrate completion. `lib-tests.yml` sends the refresh.
- **M2.4 partner:** `rehearsal_ancestry`. A rehearsal whose SHAs are ancestors of main stays fresh.

**Witness:**
- Heart suite: 1423 passed.
- Replay of 268 logged ships: 6 (2.2%) red-blocked, plus STALE for repos Heart does not poll (90 ships, 34%). The human ruled that these repos become not Heart-gated, with a PR-check guard, as the next task.
- After merge, `pyauto-heart readiness --dev --repos PyAutoBrain` returned STALE: "Heart snapshot 13.0 h old, over the 6 h maximum".

**Review:** 4 rounds, all fixed. The findings were: organ CI dropped, unpolled repos read as GREEN, a future timestamp read as fresh, the age limit could be switched off, an ops workflow could block, an older red workflow was hidden by a newer green one, and missing workflows were skipped. The final review was CLEAN.

**Heart:** RED at ship. The human gave a dev-only override plus the merge command at the M2 gate.

Follow-ups: `draft/maintenance/pyautobrain/m2_build_followups.md`.

## Original prompt

# Heart: a branch-scoped verdict for development ships, and a maximum feed age at the door

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBrain
Difficulty: medium
Autonomy: human-required
Priority: high
Status: issued
Filed: 2026-11-10
Issued: 2026-11-12
Epic: autonomous-orchestrators
Consequence: judge
Witness: (a) the 228 `autonomy_log.md` rows since 2026-09-01 replayed through the new dev-ship scope: the share that would still have needed an override is printed, and only rows whose RED reason lies inside the branch's own repos or their dependants remain; (b) a test shows `bin/heart_feed.py` reports STALE, not the old colour, for a feed older than the configured maximum; (c) a library CI run completing on `main` triggers `heart-health.yml` (one run id shown)
Review-minutes: 30
Unattended: never
Lane: any

Source: the ecosystem review of 2026-11-10, findings REL-1 and DASH-3, both confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, sections B4 and B8 and Appendix A.

**What was measured.** Since 2026-09-01 the first table of `autonomy_log.md` has 228 rows. Heart was RED on 188 to 191 of them (82 to 84%) and GREEN on none. The human typed 162 development overrides on 33 days. About three quarters of the RED rows quote `release validation FAILED`, an organism-wide reason that never sees the branch being shipped. The log cannot record a wrong override: the outcome is written when the PR opens and never updated. Separately, the published feed that the `start_dev` door reads is refreshed once a day plus hand dispatches: its mean age is 11.4 hours and it is older than 12 hours for 44% of the time. The door prints the age and applies no maximum.

One colour is answering two questions. "May this branch merge?" and "May `main` be published?" need different evidence.

**Slice 1 (small, no doctrine change): a fresh feed.**
- Trigger `heart-health.yml` from library CI completing on `main` and from the release workflow, keeping the daily cron as a backstop.
- Give `PyAutoBrain/bin/heart_feed.py` a maximum feed age (about 6 hours), above which the door reports STALE.

**Slice 2 (the human's ruling): a dev-ship reason scope.**
- In `heart/readiness.py`, give the development ship check its own scope: enforce only library CI on `main` for the repos a branch touches and their dependants. Show release-validation, install-verification, version-floor, organ-workflow and checkout-state reasons at a ship without enforcing them. Keep every reason for releases.
- Reword the ship leg in `PyAutoBrain/AUTONOMY.md` to match, and update `ORGANISM.md:95-96`, which still says the Brain triggers Build only on GREEN.
- Record the override reason in a machine-readable column, and let the row be amended when an override turns out wrong.

Slice 2 changes doctrine, so it is `judge`: the human rules on the scope and the wording before anything merges. Slice 1 can ship first at `glance`.

Nothing covers this today: a search of `draft/`, `active/` and `complete/2026` for a dev-ship or branch scope found no prompt.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
