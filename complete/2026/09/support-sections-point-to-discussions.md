# Completed: community support doors across seven repositories

Merged: 2026-09-19

All seven approved support members merged: PyAutoLens#747, PyAutoGalaxy#627,
PyAutoFit#1640, PyAutoArray#563, autolens_workspace#570,
autogalaxy_workspace#248, and autofit_workspace#162. Their individual
community-surface completion records hold validation and pending-release duties.
The exact shared policy paragraph and the three live category links shipped.
This retires the duplicate umbrella; it does not retire historical-thread migration.

## Original prompt

# Point every user-facing "Community & Support" section and issue chooser at the Discussions hub

Type: docs
Target: workspaces
Repos:
- PyAutoLens
- PyAutoGalaxy
- PyAutoFit
- PyAutoArray
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
Themes:
- docs-hub
- community
Difficulty: small
Autonomy: supervised
Priority: high
Status: blocked
Blocked-by: PyAutoLens#746, PyAutoGalaxy#626, PyAutoFit#1639, PyAutoArray#562, autolens_workspace#569, autogalaxy_workspace#247, autofit_workspace#161
Consequence: glance
Witness: each of the seven repos' README "Community & Support" section carries the two policy sentences (Discussions hub first, issues for bug reports with a reproducer, Slack for collaborators) and a `.github/ISSUE_TEMPLATE/config.yml` whose contact links open the hub, with one `bug_report.md` template asking for snippet, traceback and versions; `blank_issues_enabled` stays true.
Review-minutes: 10
Filed: 2026-09-17

Execution: split into the seven `active/community-surface-*.md` support
tasks on 2026-09-19, one issue and PR per repo (references above). Do not
start a duplicate task from this umbrella prompt. Retire it once all seven
PRs are merged. The live categories were verified on 2026-09-19:
`help-questions`, `ideas-proposals`, and `bugs-errors` are all answerable.
The former category-creation gate is cleared; links must use these slugs.
## Merge progress (2026-09-19)

The four library members and the Galaxy/Fit workspace members have shipped;
their records are `complete/2026/09/community-surface-*.md`. Do not reimplement
those six members. Only autolens_workspace#570 remains awaiting its smoke CI
and merge; retire this umbrella once that seventh member has shipped.
The approved contact links now target Help & Questions, Ideas & Proposals,
and Bugs & Errors, superseding the category names below.

## Original scope

Spawned by `policy/community_surface.md` (PyAutoMind#403), decision 4. Today
every README says "For installation issues, bug reports, or feature requests,
please raise an issue on the GitHub issues page" and none of the repos has an
issue chooser (`PyAutoLens/.github/` holds only `copilot-instructions.md` and
`workflows/`), so a user's only door is the tracker the policy is moving them
out of.

Per repo, one small PR:

- README `## Community & Support` → the policy's paragraph, verbatim:
  > Questions, help with your code or your analysis, and ideas: the
  > [PyAutoLabs Discussions](https://github.com/orgs/PyAutoLabs/discussions).
  > Bug reports with a reproducer (a snippet, the traceback, your versions):
  > an issue on the library's tracker. The Slack is for collaborators, by
  > invitation.
  Keep the Slack sentences that follow; drop the "raise an issue" line.
- `.github/ISSUE_TEMPLATE/config.yml`:
  `blank_issues_enabled: true` (the dev flow files by API; the maintainer
  occasionally by hand) and three `contact_links`: "Ask a question / get help"
  → Help & Questions; "Suggest an idea / propose an implementation" → Ideas &
  Proposals; "Report an error / investigate a bug" → Bugs & Errors. All are
  categories on `https://github.com/orgs/PyAutoLabs/discussions`.
- `.github/ISSUE_TEMPLATE/bug_report.md`: title prefix `bug:`, label `bug`,
  sections Reproducer / Traceback / Versions (`pip show autolens autogalaxy
  autofit autoarray autonerves`) / Expected vs actual — core context signals the
  Ears' triage looks for.

Order: PyAutoLens first, then the other three
libraries, then the three workspaces. The docs sites' own Support pages
(`docs/` in each library) get the same paragraph in the same PR where one
exists.
