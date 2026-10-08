## broca-pages
- issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/3 (closed)
- completed: 2026-10-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBroca/pull/4 (merged c5af0a2a)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/512 (merged c843f078)
- summary: Broca dashboard published at https://pyautolabs.github.io/PyAutoBroca/ with GitHub Pages Actions; shared board navigation includes Broca.
- deployment: https://github.com/PyAutoLabs/PyAutoBroca/actions/runs/37786032633 — build and deploy succeeded. Only rendered site/index.html is uploaded; no source/records/transcripts served in the Pages artifact. PRs build but never deploy. Main pushes/manual dispatch publish without running benchmarks or refreshing collection receipts.
- validation: Broca 19 local tests; Brain 95 theme/policy tests. All final-head applicable CI green: Broca push and PR test runs, Pages build, Brain Python 3.12/3.13. Live HTTP verification confirms four assistants, check-in panel and unchanged evidence timestamp 2026-10-08T12:58:48Z.
- authorization: user requested Pages via Actions following public visibility and all-merges authorization; existing coordinated Brain changes and exact Heart YELLOW acknowledgement reused, no new warning set.
- limits: Update control remains unavailable until a true evidence-collection service exists; publication is not collection. Other boards acquire the navigation link at their next render.
- cleanup: merged branch ancestry verified; task lifecycle closed and dashboard regenerated; local worktrees/branches removed after registry release. Deployment verification preserved under .artifacts/broca-pages.

## Original prompt

# Publish Broca dashboard with GitHub Pages Actions
Type: feature
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/3
Target: pyautobroca
Consequence: judge
Autonomy: human-required

## Original request (verbatim)

> pages now use actions if that helps

## Approved context

The user requested public Broca visibility, authorized all merges in this session,
and now explicitly requests Pages publication. Implement and deploy the minimal
Actions publication path for the existing reviewed dashboard. The user already
allowed coordinated Broca-related Brain/Mind changes preserving other tasks.

## Plan

- @PyAutoBroca: add .github/workflows/pages.yml; validate records, render saved
  evidence with Brain shared theme into a dedicated site directory, upload the
  Pages artifact, deploy only on main/manual requests. PRs validate build without
  deploying. Do not collect data, run models, refresh receipts or publish raw repo
  contents. Update README/AGENTS hosting status and include a workflow contract test.
- @PyAutoBrain: move Broca from unhosted registration to public board navigation
  after the site is deployable; update matching theme registration test/docs.
- Configure/verify GitHub Pages Actions, run applicable tests, ship the changes,
  merge after all applicable CI passes under the user's merge/deploy authorization,
  dispatch publication if needed, verify the live root serves the Broca dashboard.
- Update Mind lifecycle and clean worktrees. No benchmark execution or scheduling.

Tier: judge — merge mode: human authorization already given for all merges and this deployment.
