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
