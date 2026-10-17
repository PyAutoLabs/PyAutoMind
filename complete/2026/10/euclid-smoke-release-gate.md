# euclid-smoke-release-gate

Completed: 2026-10-17
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/305
PR: https://github.com/PyAutoLabs/PyAutoHeart/pull/309

Pipeline Smoke Tests now gate readiness, and the weekly smoke sweep includes Euclid routing. Release-mode project selection and notebook sweep are unchanged. Readiness failure/success and executed shell routing fixtures passed; prerequisite pipeline smoke run 37627512732 succeeded.

## Verification and merge

User /prm authorized the merge. GitHub confirmed MERGED; git merge-base --is-ancestor proves the shipped head is in origin/main. Only PyAutoHeart has a claimed implementation branch; no sibling implementation remains. Both Python 3.12 and 3.13 jobs passed on the exact shipped head in https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/39057234022, including the tenant firewall. No skipped test legs. Issue closed as completed.

Published Heart at shipping was STALE because source moved since release rehearsal; this development merge does not assert release readiness. Live weekly cloud sweep remains unverified where applicable.

## Close-out notes

Original task worktrees are absent from this session; no worktree or data was deleted.

## Original prompt

# Make the Euclid pipeline's new CI release-blocking and add it to the weekly cloud sweep

Type: test
Target: pyautoheart
Repos:
- PyAutoHeart
Themes:
- euclid
- ci-smoke
Difficulty: small
Autonomy: safe
Priority: medium
Status: draft
Consequence: notify
Witness: `pyauto-heart readiness` goes red on a euclid smoke failure (`config/repos.yaml` `required_workflows` carries `pipelines: ["Smoke Tests"]`), the weekly cloud sweep's `PROJECTS` lists euclid, and no other repo's gating changes (readiness on a green day is unchanged).
Review-minutes: 0
Unattended: ready
Epic: euclid-dr1-prep
Filed: 2026-08-29

Follow-up split out of epic phase 2 (`euclid_strong_lens_modeling_pipeline` issue #45), which
gives that repo its first `.github/workflows/` (smoke via the Heart reusable
`smoke-tests.yml@main`, plus unit/slow test jobs). Two Heart-side wirings were deliberately
kept out of that PR because they live in a different repo:

1. `PyAutoHeart/config/repos.yaml` `required_workflows` has no `pipelines:` key, so the euclid
   gate is observed but not release-blocking. Add `pipelines: ["Smoke Tests"]` (match the
   workflow `name:` exactly) once phase 2 has merged and the workflow has a green run history
   (memory: a brand-new check with no run history reads as a "new CI failure" — verify the
   first run landed before flipping it).
2. `PyAutoHeart/.github/workflows/workspace-validation.yml` (~L134-136) hardcodes the weekly
   cloud sweep's `PROJECTS`; euclid is absent. Add it so the sweep covers the pipeline repo.

Acceptance: `pyauto-heart readiness` reflects a euclid smoke red; the weekly sweep run lists
euclid; no change to any other repo's gating.

Issued: 2026-10-17
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/305
