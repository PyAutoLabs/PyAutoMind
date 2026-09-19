# fix: keep broadcast discussions out of awaiting-response

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Approved: 2026-09-19 (Codex conversation: "I approve")

In agents/conductors/community/_community.py, suppress awaiting_response for Announcements and Show and tell in scan and triage, preserving the watch/context surface. Add scan and triage regression coverage in tests/test_community_conductor.py for broadcasts, Q&A, and answered/unanswered Proposals.

Branch: feature/community-surface
Validation: focused community tests for Brain; Markdown/YAML/link checks for docs and templates; static HTML and browser review for the website; independent diff review before PR creation.

## Original request

Approved community-surface handoff; original request preserved verbatim in community-surface-policy.md. This member implements the PyAutoBrain portion of that handoff and the approved plan above.

