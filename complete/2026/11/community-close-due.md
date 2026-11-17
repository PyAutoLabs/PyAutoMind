- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/658
- prs: https://github.com/PyAutoLabs/PyAutoBrain/pull/662, https://github.com/PyAutoLabs/PyAutoEars/pull/32, https://github.com/PyAutoLabs/PyAutoMind/pull/580 (merged 2026-11-17)
- user-facing: true — motivated by hub #37 (closed under the policy by hand, 2026-11-17)
- heart-red-override: shipped under the live human's development override 2026-11-17 ("yes, override for PyAutoLabs/PyAutoBrain#658"); RED reason "PyAutoMind: Tenant Firewall Gate failure on main" (generated-hook drift in Brain/Heart/Hands, unrelated, still open); merge on the human's separate /prm with all checks green.
- what shipped: Mind policy/community_close_due.md (21 days, we spoke last and asked for something, never threads awaiting us, approve the batch once per session, no automation); Ears optional snapshot fields awaiting_contributor_since / close_due with tests and REFERENCE.md contract; Brain scan "Close due (21d)" section with the prefilled message, settled/historical follow-ups collapse to one count line even when the snapshot is stale, no "Delivery: unknown" rows for Announcements / Show and tell.
- follow-up: the Ears close-due label renders after the next Ears collection; issue-templates-route-bugs-to-hub (item 5) remains in planned.md, blocked on claims.

## Original prompt

# Community: 21-day close policy, close-due scan section, and quiet historical follow-ups

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoEars
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Community: https://github.com/PyAutoLabs/.github/discussions/37
Filed: 2026-11-17
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/658

Approved by the human in the /community chat on 2026-11-17 (items 1-4; item 5 is the
sibling prompt draft/maintenance/workspaces/issue_templates_route_bugs_to_hub.md).

## Request (verbatim from the session)

(1) Brain community scan (agents/conductors/community, _ears_feed) must not print Ears
historical follow-ups (historical_follow_up_at set, follow_up inactive) as "Follow-up:
unknown" rows — show only a quiet count; also suppress "Delivery: unknown" rows for
broadcast categories (Announcements, Show and tell). (2) New Mind policy: 21-day close — a
thread (Discussion or external issue) where the maintainer commented last and is waiting on
the contributor, open, with no external reply for 21 days, is closed with a standard
message: "Hi @user, we're closing this for now because we haven't heard back in three weeks.
Nothing is lost. If you're still <context>, reopen this discussion or just reply here ... and
we'll pick it up again." (issues: 'reply here' since issue authors can't reopen a
maintainer-closed issue). Never applies to threads awaiting us. Brain community skill
references it. (3) Ears snapshot: additive optional field awaiting_contributor_since /
close_due (>=21 days) with tests, REFERENCE.md contract note. (4) Brain community scan:
"Close due (21d)" section with prefilled standard message; human approves the batch once per
session, then the session posts+closes (addDiscussionComment + closeDiscussion reason
OUTDATED / gh issue close). No GitHub Action, no unattended closing.

## Evidence

- 2026-11-17 scan listed 25 settled threads (PyAutoLens#631, PyAutoFit#36 from 2019, ...) as
  "Follow-up: unknown". Ears' snapshot had them correctly as historical
  (`historical_follow_up_at`, `review_needed: false`); Brain's `_ears_feed.py` (~line 173)
  sets `review_needed=None` for every row when the snapshot is stale or cached, which turns
  settled history into unknown.
- First manual application of the policy: discussion #37 closed 2026-11-17 (27 days silent).
