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
Consequence: judge
Review-minutes: 20
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
