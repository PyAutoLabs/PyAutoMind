# Active Tasks

## search-conformance-metadata
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1666
- issued: 2026-10-07
- prompt: active/search_conformance_metadata_layer.md
- epic: search-extensibility (phase A0a(i))
- session: Claude CLI (Fable 5.1, /start_dev); https://claude.ai/code/session_01QJmrnXNQdq6HSruUt3MqVW
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/search-conformance-metadata
- repos:
  - PyAutoFit: feature/search-conformance-metadata
- tier: judge (human /prm)
- summary: tests-only metadata/serialization conformance suite over the 15 public searches; frozen golden identifier table; collects on unittest-nojax. Human ruling: identifiers stay the same, any change flagged first.

## mind-dashboard-simplify
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/500
- issued: 2026-10-07
- session: Codex; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/mind-dashboard-simplify
- repos:
  - PyAutoBrain: feature/mind-dashboard-simplify
  - PyAutoMind: feature/mind-dashboard-simplify
- plan: approved; remove requested dashboard copy, move Epics below Start here and Pending release last; retain Update button; human /prm merge

- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/501
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/491
- heart-ack: user explicitly authorized shipping on 2026-10-07 with manifest drift: workspace checkouts (manifest ↔ disk) — 3 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source
- validation: Brain 1271 passed; Mind 696 passed; generated dashboard current; copy payloads and requested layout verified
- next: human /prm; merge Brain #501 before Mind #491; no public API or scientific workspace impact
