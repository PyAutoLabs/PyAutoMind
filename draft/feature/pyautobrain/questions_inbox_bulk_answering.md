# Questions inbox: parked questions wait in one list the human works through in bulk

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Consequence: judge
Priority: high
Status: draft
Filed: 2026-11-14
Epic: autonomous-orchestrators (programme M3.4 companion)
Lane: any

## Why

Human, 2026-11-14, during M3.1 shift A: two workers parked with questions (autolens_workspace#669, #670) and the bot @-mentioned them mid-run. Their view: when a task stops on a question, it is more natural to put it in a separate queue that they go through "whenever, but normally after the run when I have time to go over them in bulk". Notifications are fine, but the flow is that they tend to the list when they choose, not that they respond to a notification. Open GitHub issues are fine as the place the question lives.

## What

1. **One inbox across shifts.** Every parked question (`question:` in a worker's `.done`, PARKED-ON-ISSUE) lands in a single list that persists after the shift, e.g. a Mind `questions.md` or a dashboard section. Each entry gives the task, a one-line ask, the options the worker offered, the issue link, the shift it came from and its age. The shift digest links to the inbox rather than repeating the asks.
2. **Calm notifications.** Keep the push, but make it informational: one line, "1 question added to your inbox", with no call to act. Per shift, bundle them, or send them only at shift end. The human chooses after trying it.
3. **Answering resumes the work.** The human answers on the issue, in the dashboard, or in a chat (M3.4 cockpit). The answered task becomes startable again: it re-enters the planner with the answer attached to its prompt, so the next shift or session continues it without the human re-explaining. Unanswered entries never block a shift.
4. **Bulk sitting.** A chat command such as "go through my questions" walks the inbox one entry at a time. It records each answer on its issue and marks the entry answered, deferred or dropped.

5. **On the Mind dashboard.** The inbox is a section of the PyAutoMind dashboard: each open question shows its ask, options, issue link and age, with an answer, defer or drop control using the dashboard's existing input route (design C: an Issues-token `dashboard-input` issue, validated and committed by the bot).
6. **Reminders from the cockpit.** The M3.4 chat mentions the inbox count at shift end, or when the human attaches, and offers a bulk sitting. It reminds; it never demands.

## Witness

- Offline: a replayed shift with two parked workers produces two inbox entries, one calm notification and a digest link. An answered entry makes the task plannable again, with the answer in its prompt.
- Live: after one shift the human clears the inbox in one sitting, and the next shift picks up an answered task.
