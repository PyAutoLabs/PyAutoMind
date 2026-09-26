# Completed: PyAutoLens community surface

Merged: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/746
PR: https://github.com/PyAutoLabs/PyAutoLens/pull/747

## Shipped

Updated Community & Support documentation and issue templates to route community questions, proposals, and suspected errors to the shared Discussions hub; confirmed reproducible bugs retain repository issues.

Uses the human-approved five categories: Announcements, Help & Questions, Ideas & Proposals, Bugs & Errors, and Show and tell.

## Validation and close-out

All workflows and jobs for the exact PR head were audited before merging; required jobs passed, with only conditional skips inside successful workflows. Independent review was CLEAN. Git ancestry confirms the feature head is contained in origin/main with zero unmerged commits. Human authorized merging all PRs on 2026-09-19.


Only this repository member is complete. The shared community-surface worktree remains because Mind, Lens workspace, website, and organization-profile PRs are still open. The policy and migration umbrella tasks remain active.

## Original prompt

# docs: direct community support to the Discussions hub

Type: docs
Target: pyautolens
Repos:
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: high
Approved: 2026-09-19 (Codex conversation: "I approve")
Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/746

## Latest direction (2026-09-19)

User: "Ive done all the above, I made an extra onw hich is Errors & Bugs"

The live categories are Help & Questions, Ideas & Proposals, Bugs & Errors
(all answerable), Announcements, and Show and tell. This supersedes the
separate Q&A / Scientific analysis / Ideas / Proposals categories in the
original request below. Chooser links use help-questions, ideas-proposals,
and bugs-errors. Confirmed reproducible bugs still have linked repository
issues. GitHub category setup is verified; the former manual gate is cleared.

Update README Community & Support and existing docs support pages with the exact policy paragraph. Add .github/ISSUE_TEMPLATE/config.yml with question, feature idea and implementation proposal links, blank issues enabled; add bug_report.md requesting reproducer, traceback, versions and expected/actual behavior. Preserve collaborator Slack details; remove invitations to file support questions as issues.

Branch: feature/community-surface
Validation: focused community tests for Brain; Markdown/YAML/link checks for docs and templates; static HTML and browser review for the website; independent diff review before PR creation.

## Original request

Approved community-surface handoff; original request preserved verbatim in community-surface-policy.md. This member implements the PyAutoLens portion of that handoff and the approved plan above.
