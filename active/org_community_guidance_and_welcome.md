# Make organization-wide community guidance visible and canonical

Type: docs
Target: PyAutoScientist
Repos:
- PyAutoScientist
- .github
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/30
Approved: 2026-09-19 — user: "go"

## Original user request

Do 1 and 2 and then also update this https://github.com/PyAutoLabs/PyAutoScientist/blob/main/CONTRIBUTING.md and check any other repo level files. I guess if feasible these files should move from PyAutoScientist to PYAutoLabs but only if they can go org level

## Referenced requests

1. Pin a welcome discussion making clear that PyAutoLabs Discussions is the
   shared hub for every library, workspace, and tutorial, including arrivals
   redirected from another repository.
2. Pin a short issue above each eligible repository's issue list directing
   questions and ideas to that hub, while retaining confirmed reproducible
   defects on the appropriate repository tracker.

## Approved plan

- Inventory existing pins and public non-archived PyAutoLabs repositories
  with Issues enabled. Reuse existing equivalent welcome/pointer posts;
  do not evict other pins, enable disabled Issues, touch private repositories,
  or change subscriptions. Report exceptions rather than altering settings.
- Publish a global welcome discussion on the .github-backed organization
  hub with an explicit all-repositories welcome and the five live categories.
- Publish and pin a concise issue in each eligible repository pointing to
  the hub and the canonical contribution guide. Record all post URLs; no
  mass mentions and no duplicate notices. Distinguish these permanent
  signposts from unfinished development issues for community triage.
- Make PyAutoLabs/.github/CONTRIBUTING.md the actual shared guide (currently
  only a pointer to PyAutoScientist). Rewrite contribution entry points:
  Discussions first for help, scientific questions, ideas and proposals;
  repository issues for confirmed reproducible bugs or agreed implementation.
  Conventional non-AI pull requests remain welcome. PyAutoScientist is an
  optional experimental ecosystem, not a prerequisite for contribution.
- Move the existing Code of Conduct content unchanged into
  PyAutoLabs/.github/CODE_OF_CONDUCT.md, preserving attribution and reporting
  contact. Add org-default SUPPORT.md using the established support policy.
- Replace PyAutoScientist CONTRIBUTING.md and CODE_OF_CONDUCT.md with clear
  compatibility pointers to the organization source; preserve old URLs.
  Update its README's obsolete canonical-policy-home claim and linked
  contribution entry points without touching generated organ tables.
- Inspect other root/.github/docs community-health files and existing local
  overrides. Preserve genuine repo-specific instructions; old shared pointers
  continue through compatibility files rather than requiring a mass rewrite.
- Do not move LICENSE, AGENTS.md or CLAUDE.md: no org default inheritance.
  Keep AI_POLICY.md at its existing canonical source with explicit pointers,
  because GitHub does not auto-inherit that custom filename. Do not rewrite
  the substantive AI or conduct policies under this contribution-routing task.
- Validate Markdown links, no circular pointers, default-vs-local precedence,
  retained old URLs, pinned visibility and category links. Publish the .github
  canonical files before dependent link changes. One issue/PR per changed
  repo through start-dev, with public pin actions recorded in the task ledger.

## Scope boundary

Slack notifications remain a separate filed prompt and are not enabled here.
Historical issue-to-discussion conversion is not part of this task. Pins do
not close or relabel other issues. Do not claim root files are copied into
clones by GitHub defaults; they are displayed by GitHub only.

## Verified GitHub capability

https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file

Supported shared defaults include CONTRIBUTING.md, CODE_OF_CONDUCT.md,
SUPPORT.md and SECURITY.md. Local files override defaults. LICENSE cannot
be inherited. Existing security reporting policies must be retained; no new
security reporting promise is invented by this task.
