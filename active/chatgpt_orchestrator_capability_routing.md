# Capability-route ordinary ChatGPT orchestration

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoScientist
Difficulty: large
Autonomy: supervised
Priority: high
Status: issued
Issued: 2026-09-20
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/410

## Request

Investigate and implement a PyAutoScientist development route in which ordinary
ChatGPT Chat remains the top-level scientist-facing orchestrator, PyAutoMind
retains intent/lifecycle state, and PyAutoBrain retains reasoning/routing/safety.

Use the repository and GitHub capabilities exposed by the current Chat
conversation for as much development as they can honestly perform. Escalate to
Codex/Work, a local shell, GitHub Actions, HPC, or another supported execution
environment only for the smallest coherent phase that genuinely requires
capabilities absent from Chat.

Do not add ChatGPT as an organ, do not create a second task-state system, do not
automate the ChatGPT web client, steal session credentials, or pretend an
interactive Chat session is an API.

The architecture must be harness-independent: reason about capabilities and
required evidence rather than scattering provider-name conditionals. Preserve
all existing autonomy, test/smoke/scientific-validation, independent-review,
Heart, PR-review, human-merge, release and lifecycle gates.

The detailed investigation, architecture decision, representative-task audit
and implementation plan are recorded on PyAutoBrain issue #410.
