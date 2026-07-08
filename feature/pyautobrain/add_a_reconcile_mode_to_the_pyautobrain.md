# Add a reconcile mode to the PyAutoBrain intake agent

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised

Add a reconcile mode to the PyAutoBrain intake agent. It audits the PyAutoMind backlog for prompts describing already-shipped work whose status has gone stale, because a prompt's Status header is not a reliable completeness signal (formalise preserves an existing Status verbatim, so a shipped task can still read Status: planned). For each backlog prompt, cross-reference against complete.md prompt-path references and section headers, issued/ basenames, and optionally the target repo git log / merged PRs, then report a confidence-ranked list of suspected-complete prompts for a human to retire — never move or delete files automatically. Complements census/dashboard/formalise. Touches intake agent code in PyAutoBrain and reads PyAutoMind.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake -->
