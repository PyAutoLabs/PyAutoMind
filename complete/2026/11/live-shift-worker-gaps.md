- epic: autonomous-orchestrators (pilot 4c follow-up; issue PyAutoBrain#594)
- summary: PyAutoBrain#595. The worker prompt forbids EnterWorktree (its permission-root prompt for worktrees outside .claude/worktrees/ stalls an unattended worker) and requires `gh pr edit --add-label decision-taken` on any PR carrying a flagged decision. `_orchestrator.late_sweep`: a closed shift whose digest is posted, with a lease held or ledger ops queued, reaps, commits the ops through the one Mind writer, and appends `- late: <task> — <url> (after review-at, …)` lines to the record under `### Late arrivals`. It never spawns, re-dispatches, starts a close-out or posts a second comment; with nothing pending it is idle.
- trigger: pilot live shift 1 re-run (2026-11-06, PyAutoMind#543): worker 688a2540 blocked about 70 min on an EnterWorktree prompt until the human attached; it finished at 12:32, after review-at, and its .done and 2 ledger ops were stranded (committed by hand, Mind 8f2e2cc4); it flagged a decision without the label (autogalaxy_workspace_test#134, merged by human /prm).
- witness: PASS. Template test; late .done reaped with no spawn and then idle; a late crash is named and not re-dispatched; a closed shift with nothing pending stays idle; real-git: the late line lands under ### Late arrivals on Mind main. Control: old code fails 4 of the new tests. Brain 1638 passed; tenant firewall OK.
- heart: STALE acknowledged by the human at ship; glance tier, in-turn merge.

## Original prompt

# Live-shift worker gaps: EnterWorktree stall, late finishers stranded, unlabelled decisions

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-11-06
Issued: 2026-11-06
Epic: autonomous-orchestrators
Consequence: glance
Witness: the worker prompt forbids EnterWorktree and requires the decision-taken label on a PR with a flagged decision (tests on session_command); a .done written after review-at (digest already posted) is reaped at the next tick, its ledger ops land on Mind main, and one "- late:" line is appended to the record, with no spawn, close-out or second comment; a closed shift with nothing pending stays idle; the full Brain suite passes
Review-minutes: 10
Unattended: never
Lane: local-dev

From pilot live shift 1 re-run (2026-11-06, PyAutoMind#543): worker 688a2540 blocked about 70 minutes on an EnterWorktree permission-root prompt; it finished after review-at and its .done and ledger ops were stranded (ops committed by hand, Mind 8f2e2cc4); it flagged a decision with no decision-taken label. Human: "fix items 1-3".

<!-- filed by hand 2026-11-06; headers mirror intake's -->
