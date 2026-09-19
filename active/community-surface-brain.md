# fix: keep broadcast discussions out of awaiting-response

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Approved: 2026-09-19 (Codex conversation: "I approve")
Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/405

## Latest direction (2026-09-19)

User: "Ive done all the above, I made an extra onw hich is Errors & Bugs"

The live categories are Help & Questions, Ideas & Proposals, Bugs & Errors
(all answerable), Announcements, and Show and tell. This supersedes the
separate Q&A / Scientific analysis / Ideas / Proposals categories in the
original request below. Chooser links use help-questions, ideas-proposals,
and bugs-errors. Confirmed reproducible bugs still have linked repository
issues. GitHub category setup is verified; the former manual gate is cleared.

In agents/conductors/community/_community.py, suppress awaiting_response for Announcements and Show and tell in scan and triage, preserving the watch/context surface. Add scan and triage regression coverage in tests/test_community_conductor.py for broadcasts, Q&A, and answered/unanswered Proposals.

Branch: feature/community-surface
Validation: focused community tests for Brain; Markdown/YAML/link checks for docs and templates; static HTML and browser review for the website; independent diff review before PR creation.

## Original request

Approved community-surface handoff; original request preserved verbatim in community-surface-policy.md. This member implements the PyAutoBrain portion of that handoff and the approved plan above.
