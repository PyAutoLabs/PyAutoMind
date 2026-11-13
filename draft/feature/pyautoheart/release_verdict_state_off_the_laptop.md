# Heart: one published verdict, with no gate state left on the laptop

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: judge
Witness: (a) `pyauto-heart readiness --dev --repos PyAutoBrain --source feed --json` on a machine with no `~/.pyauto-heart/` returns the same verdict and reasons as the laptop run within one feed refresh (both JSONs saved); (b) a test shows no reason in the dev verdict comes from checkout state (`repo_state`, `version_skew`, "behind origin"); (c) `grep -rn "HEART_STATE_DIR" heart/validate.py heart/freeze.py` names only cache paths, with the validation history read from a tracked or published location
Review-minutes: 25
Unattended: never
Lane: any

Source: REL-5 of the ecosystem review (2026-11-10), section B8. **Unverified by the review: re-check first** at source and drop or reshape what no longer holds.

**Already done (M2.1, PyAutoHeart#342).** `heart-health.yml` refreshes on library CI and Release Integrate completion; `bin/heart_feed.py` treats a feed over 6 h as STALE.

**What remains (checked 2026-11-13 on Heart 00d979a):**
- `heart/readiness.py:104-107`: the dev-ship gate "judges the dev box's local `$HEART_STATE_DIR/state.json` … The event triggers refresh the published cloud feed, which this command does not read." A cloud worker has no such file.
- `heart/validate.py:125`: `VALIDATION_HISTORY_DIR = state.HEART_STATE_DIR / "validation_history"`. The release verdict's history lives on one laptop.
- `heart/freeze.py:58`: the freeze flag is a laptop file (REL-9 proposes retiring it; see `release_window_after_rehearsed_shas.md`).
- `bin/heart_feed.py:30-35`: the published feed is organism-wide and cannot be scoped, so the door falls back to the local CLI for `--repos`.

**Re-check first:** compare `~/.pyauto-heart/release_ready.json` and `pyauto-heart readiness --dev` with the published `state.json` today; count `workflow_dispatch` runs of `heart-health.yml` since 2026-11-13 (the review counted 37 hand dispatches before M2.1).

**Change (one slice each):**
1. Publish the dev-scope inputs (per-repo main CI conclusions with their `ts`) in the cloud feed, and give `readiness --dev` a `--source feed` that scopes from it. Make that the default for unattended and cloud callers.
2. Move the validation history to an append-only tracked file written by the nightly/Release Integrate path (pattern: `timings/gates.jsonl`).
3. Drop checkout-state reasons from any verdict a worker reads.

Tier judge: it changes the source of the verdict the release gate and the merge paths read.
Programme: M4 prerequisite (a cloud worker must be able to gate); pairs with M5.2's state-store seam.

<!-- drafted 2026-11-13 by the REL intake session (scratch/intake_2026-11-13) -->
