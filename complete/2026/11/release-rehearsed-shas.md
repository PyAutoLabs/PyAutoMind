Programme **M2.4** (epic `autonomous-orchestrators`, phase 9). Shipped as PyAutoHands#339 (4d68b445e), merged 2026-11-13. Issue PyAutoHands#337.

**Human ruling (M1 gate, 2026-11-12):** a release publishes exactly the rehearsed commits, even if main moved. The Colab bump moves off main.

**Built:**
- `release.yml` takes `rehearsal_run_id` and `commit_shas`.
- `resolve_commits` reads the rehearsal record (`rehearsal.json`). It refuses if the record is missing or mismatched, or if a SHA is not on `origin/main`.
- The release checks out and tags exactly those SHAs, and verifies the tag on origin.
- The Colab bump goes to `release/<version>` with a PR into main.
- The caller contract is in `docs/internals.md`.
- The partners merged in the same sitting: Brain#620 (callers) and Heart#342 (ancestry).

**Witness:**
- Hands suite: 631 passed. 4 pre-existing environmental `test_tombstone` failures.
- yamllint clean.
- Offline dry run: a release tags the rehearsed SHAs while main is 2 ahead, and refuses a PR-head SHA.

**Review:** 3 rounds, all fixed, then CLEAN. The findings were: the Brain callers must merge together, a missing off-main guard, no owner for the release branch, and contract gaps.

**Heart:** RED at ship. The human gave an override plus the merge command.

Follow-up: workspaces still use `ref: main`, recorded in `draft/maintenance/pyautobrain/m2_build_followups.md`.

## Original prompt

# Release: build the commits that were rehearsed, not `main` at release time

Type: feature
Target: PyAutoHands
Repos:
- PyAutoHands
- PyAutoBrain
Difficulty: medium
Autonomy: human-required
Priority: high
Status: issued
Filed: 2026-11-10
Issued: 2026-11-12
Epic: autonomous-orchestrators
Consequence: judge
Witness: a rehearsal followed by a release dry run in which a commit is pushed to one library's `main` between the two: the release leg's log shows it checking out the rehearsed SHA (or stopping with "main moved since rehearsal"), and for a real release `gh api repos/PyAutoLabs/<lib>/compare/<rehearsed sha>...<tag>` returns `identical` for every library
Review-minutes: 20
Unattended: never
Lane: any

Source: the ecosystem review of 2026-11-10, finding REL-4, confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, section B8 and Appendix A. Verifier notes: `verdicts/REL-4.json`.

**What happened on 2026-11-09.** The nightly passed its GREEN gate on the `main` HEADs captured after the rehearsal. The rehearsal (09:18 to 09:37Z) and the live run's own TestPyPI leg both built PyAutoArray `e2b05f004`. PyAutoArray #681 and #683 merged at 10:43:57Z and 10:44:01Z. The release leg checked out `main` again at 10:58:29Z and tagged and published `6ae33d433`, four commits and ten files ahead of what was rehearsed. One minute later PyAutoGalaxy and PyAutoLens `main` failed all three unit-test legs against the new PyAutoArray. The exposure runs from the rehearsal checkout to the release checkout, about 100 minutes that night.

With one human merging, this is rare. With many workers merging through the working morning, when the nightly actually runs, it becomes routine.

**The change.**
1. Add a commit-SHA input per library to `PyAutoHands/.github/workflows/release.yml` (the release legs use `ref: main` at `:96-111` and `:469-484` today).
2. Have the driver pass the rehearsed SHAs. `nightly.sh:408-423` already captures `commit_shas.json`.
3. Check out by SHA. When `main` has moved, either release the rehearsed SHA or stop; the human rules which.
4. Put the Colab-bump commits on the tag or a release branch, not on `main`.

Once this lands, the freeze flag is no longer needed to keep a release honest, and a merge during validation no longer makes the night STALE (2 blocked nights so far).

`judge` because it changes what a release publishes; the human approves the design and the first release made with it.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
