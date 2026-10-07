# Simplify Mind dashboard text and section order

Type: maintenance
Difficulty: small
Priority: normal

Update @PyAutoBrain's Mind dashboard renderer and regenerate @PyAutoMind's dashboard outputs.

## Original request

Remove "Issued — each has an open GitHub issue and usually a branch."

Remove "Library PRs the ledger records as merged but not yet released, and the in-flight tasks waiting on each. Rendered from the ledger — active.md and the complete/ records — never a live GitHub query; the Brain board's pending-release search is the fresh view, this is what the Mind believes."
remove "234 unstarted prompts and 2 awaiting human review. Unstarted prompts are sorted most-pickable first (priority, then size). 47 of them belong to an epic and are listed only under Epics below."

Remove all the descriptipve text inside Backlog like that within Human review.

remove "The 50 newest things to happen to the work in hand, newest first — issued, filed, flagged for review. Every other section on this page is laid out by state, which is exactly why none of them can answer “what has been happening?”. Shipped work is not here: it is read from complete/index.md, and a thousand records deep it would crowd out everything anyone can still act on. Showing the newest 10; … opens the next 10."

remove "Issued — each has an open GitHub issue and usually a branch."

Move Pending Release down to bottom.

Move Epics up to below "start Here"

Remove "📋 Refresh this page — reconcile finished prompts, then regenerate" which should just be the update button added above now.

Remove "markdown version · GitHub Page No batch in flight."

## Implementation plan

- Edit `agents/conductors/intake/_intake.py`: remove the requested explanatory text in HTML and Markdown, including Backlog/Human review introductions and Recent's explanatory paragraph; remove the redundant refresh task and top metadata links; suppress the empty-batch status while retaining active batch information and the existing Update button.
- Order sections and navigation: Start here, Epics, In flight, Planned, Backlog, Recent, Pending release. Keep task rows, controls, counts and pagination working.
- Run existing focused dashboard tests, adjusting expectations only where required by the requested presentation; regenerate `dashboard.html` and `dashboard.md` through the supported intake command and inspect the rendered output.
- Proposed branch: `feature/mind-dashboard-simplify`. Tier: undeclared — merge mode: human /prm.

## Initial branch survey

Both canonical repos are clean on `main` and current with origin. No registered claim conflicts. The worktree helper reports existing unregistered Brain/Mind worktrees on `pending-release-published-only` and `pending-release-catchup`; leave these untouched and use isolated task worktrees after approval.
