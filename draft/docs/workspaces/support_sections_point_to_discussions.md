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
Status: formalised
Consequence: glance
Witness: each of the seven repos' README "Community & Support" section carries the two policy sentences (Discussions hub first, issues for bug reports with a reproducer, Slack for collaborators) and a `.github/ISSUE_TEMPLATE/config.yml` whose contact links open the hub, with one `bug_report.md` template asking for snippet, traceback and versions; `blank_issues_enabled` stays true.
Review-minutes: 10
Filed: 2026-09-17

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
  occasionally by hand) and two `contact_links`: "Ask a question / get help"
  and "Propose a feature" → the hub (`https://github.com/orgs/PyAutoLabs/discussions`,
  categories Q&A and Ideas).
- `.github/ISSUE_TEMPLATE/bug_report.md`: title prefix `bug:`, label `bug`,
  sections Reproducer / Traceback / Versions (`pip show autolens autogalaxy
  autofit autoarray autonerves`) / Expected vs actual — the five signals the
  Ears' triage looks for.

Order: PyAutoLens first (the hub lives there), then the other three
libraries, then the three workspaces. The docs sites' own Support pages
(`docs/` in each library) get the same paragraph in the same PR where one
exists.
