# Publish Broca dashboard with GitHub Pages Actions
Type: feature
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
