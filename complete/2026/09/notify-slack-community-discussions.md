## notify-slack-community-discussions

- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/408
- completed: 2026-09-20
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/409
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/409

## Shipped

The GitHub for Slack app now sends new Discussions from the shared `PyAutoLabs/.github` hub to the PyAutoLabs Slack workspace's `#general` channel. `/github subscribe list features` showed `discussions` as the only enabled feature, both before and after the workspace was renamed to `pyautolabs.slack.com`. The subscription has no category filter. The public Discussion remains the source of truth.

PyAutoBrain's Community Agent runbook documents setup, event scope, live verification, and rollback. GitHub's native feature also reports accepted answers; it does not promise every reply, edit, or reaction. No custom webhook or token was added.

## Validation and close-out

[Test Discussion #21](https://github.com/orgs/PyAutoLabs/discussions/21) in Help & Questions produced one operator-observed Slack message with author, title, category, and repository context. The post-rename feature-list check confirmed the subscription persisted; no second Discussion was posted solely for that check. The exact PR head had one expected pull-request workflow run with Python 3.12 and 3.13 jobs both successful, and Git reported the feature branch wholly contained in `main` with zero unmerged commits. The human invoked `/prm` for this merge. The prior Heart RED development override is recorded on issue #408 and in the PR; it did not clear Heart or authorize a release.

## Original prompt

# Notify Slack general when a community discussion is posted

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-09-20
Consequence: judge
Review-minutes: 20
Unattended: ready

# Notify Slack general when a community discussion is posted

Type: maintenance
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: judge

## Original user request

3) Can we have a prompt so all community activity, well every time a new post goes up, it is posted on the #general chanel of SLACK which will mean everyone sees it?

## Scope

This prompt covers item 3 only. File now; do not enable an integration or post
messages until this task is started and its setup plan is approved.
PyAutoBrain owns community coordination; the event source is the .github
hub. Native app configuration may require no repository code changes.

Send a visible notification to the intended PyAutoLabs Slack workspace's
#general channel whenever a new top-level discussion is created in the shared
PyAutoLabs Discussions hub (source repository PyAutoLabs/.github), across all
five categories. People arriving from any library share this one hub.

Interpretation to confirm at setup: new top-level posts are required; every
reply, edit, reaction, repository issue, PR, commit, and CI event is not
implicitly included. Native accepted-answer notifications may be useful;
confirm whether these should remain enabled. Do not claim every reply is
covered by the native discussions subscription.

## Preferred approach

Inspect existing GitHub app installation and channel subscriptions first to
avoid duplicate delivery. Prefer the official GitHub for Slack integration:
in the confirmed #general channel, subscribe to PyAutoLabs/.github discussions.
The official integration documents created/answered discussion events.
Check and disable unwanted default issue/PR/commit/release/deployment feeds
only for this new subscription, preserving unrelated existing subscriptions.

Confirm workspace identity, channel ID, app access to .github, and who can
approve installation. Never put tokens or webhook secrets in prompts, logs,
issues, or source. Do not add @channel/@here/everyone mentions. Channel
delivery improves visibility but does not guarantee anyone reads the message.

Use custom event-driven automation only if a confirmed requirement cannot be
met natively; obtain approval for that scope increase. Any custom fallback
must handle retries without duplicate posts and render untrusted post titles
as inert text without triggering Slack mentions. Do not replay historical
activity unless explicitly requested.

## Acceptance and handoff

- With human approval, create one clearly marked test discussion and verify
  a single message arrives in the correct #general channel with a working
  link and useful author/title context; record what category context is shown.
- Verify coverage of all five categories, including future new posts by
  external users, without enabling developer workflow noise.
- Document exact enabled event types, setup owner, subscription status,
  rollback/unsubscribe steps, and any administrator-only manual actions.
- Keep public discussions as the source of truth: notification is one-way;
  do not copy private Slack replies back to GitHub.

## Verified starting references (2026-09-19)

- https://github.com/integrations/slack#customize-your-notifications
- https://github.blog/changelog/2023-03-08-introducing-the-ability-to-subscribe-to-specific-discussion-categories-on-slack/

Recheck current integration capabilities during implementation.

<!-- formalised by the Intake (Conception) Agent on 2026-09-19 from file:/home/jammy/Code/PyAutoLabs/.worktrees/community-surface-closeout/tmp/community_slack_intake.md -->
