# Release: the post-release tail runs in the workflow, and a red tail does not read as a failed release

Type: feature
Target: PyAutoHands
Repos:
- PyAutoHands
- PyAutoMind
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: glance
Witness: (a) after the next live release, `gh pr list --search "label:pending-release" --state merged` across the published set shows no PR whose merge commit is an ancestor of the tag (job summary of `clear_pending_release_labels` saved); (b) the live release run sends `heart-refresh` (one `heart-health.yml` run id with event `repository_dispatch` after the tag); (c) a release whose publish jobs passed but whose post-publish smoke failed is reported by the driver as "shipped, post-publish check red: <job>" (test on `nightly.sh` outcome parsing)
Review-minutes: 15
Unattended: never
Lane: any

Source: REL-7 of the ecosystem review (2026-11-10), section B8. **Unverified by the review: re-check first.**

**What exists (Hands 9f7c703):** `.github/workflows/release.yml:863-917` already has `clear_pending_release_labels` (since 43d168d, 2026-10-07): it runs `lifecycle.py clear-released --remove-labels` without `--apply`, so the Mind half stays with `PyAutoHeart/skills/review_release/review_release.md:137-178` (step 6, a human session). The review quotes a pass where the label job dropped 0 of 28.

**Re-check first:** read the step summaries of the last three live `release.yml` runs: did the job drop labels? If it drops none, find why (token repos, the ancestor test, the label name) before anything else.

**Change:**
1. Fix whatever the re-check finds in the label job; keep `continue-on-error`.
2. Send `repository_dispatch: heart-refresh` from the release workflow after the tag (open item 7 of `draft/maintenance/pyautobrain/m2_build_followups.md`: fold it in here, or close it there).
3. Split the run's result: publish jobs decide "shipped"; post-publish jobs (wiki-currency "Install the released stack", Colab bump, notes) report separately. `nightly.sh` reads the publish jobs, and names a failing post-publish job (today `PyAutoBrain/agents/conductors/release/nightly.sh:459-475` infers "shipped" from the tag and pages "the post-release smoke leg is the usual cause").
4. Not here: writing Mind `main` from the workflow. The Mind half of the chain waits on M4.3 (one network write path to Mind `main`); note that in review_release step 6.

Overlaps `draft/feature/pyautobrain/nightly_outcome_record_and_same_night_bug_tasks.md` slice 1 (shipped/partial/not-shipped via PyPI + tags): build whichever lands second on top of the first.
Tier glance: nothing here changes when or what a release publishes.

<!-- drafted 2026-11-13 by the REL intake session (scratch/intake_2026-11-13) -->
