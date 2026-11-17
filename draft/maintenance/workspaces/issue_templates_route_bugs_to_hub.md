# Issue choosers: route bug reports to Bugs & Errors on the hub (drop the bug_report template)

Type: maintenance
Target: workspaces
Repos:
- PyAutoArray
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- .github (org default bug_report.yml)
Difficulty: small
Autonomy: supervised
Priority: medium
Consequence: judge
Filed: 2026-11-17

Approved by the human in the /community chat on 2026-11-17 (item 5).

## Request

Replace the bug_report.md issue template in PyAutoLabs library/workspace repos with a contact
link to Bugs & Errors (https://github.com/orgs/PyAutoLabs/discussions/categories/bugs-errors),
blank_issues_enabled false, per the where-to-file policy. Motivation: autofit_workspace#182, an
unedited bug template from a new account (closed 2026-11-17).

## Notes for planning

- This reverses a deliberate 2026-09 choice recorded in `policy/community_surface.md` §2
  ("one bug-report template ... blank issues stay enabled because the development flow files
  by API and the maintainer occasionally by hand"). Update that paragraph in the same change.
  The API is unaffected by `blank_issues_enabled`; confirm with the human whether disabling
  blank issues in the web chooser is acceptable for maintainer hand-filing.
- The config.yml files are generated from the community-surface sentences; edit the generator
  source, not each file by hand, if one exists.
- Blocked on 2026-11-17 by claims: PyAutoGalaxy (galaxy-duplicate-pytree-registration),
  PyAutoFit (ep-projected-model-shared-prior), autolens_workspace (cluster-regime-narrative).
