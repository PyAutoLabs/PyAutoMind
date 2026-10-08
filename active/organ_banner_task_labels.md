# Organ banner task labels

Consequence: judge
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/513

## Original request

For the dashboards, I want to update the banner images at the top, but I only want to update thw words in grey and not the logo, software name or words underneath. I like that each word describes what task it does (e.g. Insight -> Inference), Ears -> Community, the only problem is I dont want words like "Board", "Dasdboard", and I dont want it to just be "Dashboard" like it is on many (e.g. Cortex). The word should be what the organ does (So for Cortex -> Science).

## Scope and proposed plan

@PyAutoBrain owns the shared HTML banner in `board/_theme.py::hero`. Change only its grey `kind` label to an organ-specific functional label. Preserve SVG marks, wordmarks, taglines, colours and layout. Existing renderer calls remain compatible. Move Broca immediately after Nerves in the shared dashboard navigation, using `config/policy.yaml` → `board.boards`; preserve other entries' relative order.

Approved labels: Brain: Orchestration; Mind: Planning; Cortex: Science; Memory: Knowledge; Eyes: Visualization; Ears: Community; Heart: Tests; Hands: Releases; Pulse: Profiling; Insight: Inference; DNA: Environments; Nerves: Configuration; Broca: Assistants; Gut: Cleanup; Scientist: Overview.

User correction (verbatim):

Broca should be Assistants and also move it after Nerves, Heart should be Tests

Add a functional label to the existing organ metadata and use it for the banner label, retaining the legacy `kind` argument for consumer compatibility. Update the banner contract in `docs/board-navigation.md`. Verify representative hero output differs only in the label and visually inspect long labels at mobile and desktop sizes. Identify consumer regeneration/publication requirements before claiming live deployment.

Branch proposed: `feature/organ-banner-task-labels`. Library workflow for the shared Brain implementation. Tier: judge; merge mode: human /prm.

## Execution state

User approved the corrected plan, then explicitly authorized parking board-one-click-update, merging and publishing. The update task is parked with its worktree and edits preserved. Task worktree: `.worktrees/organ-banner-task-labels/PyAutoBrain`; branch: `feature/organ-banner-task-labels`.

Heart YELLOW acknowledgement: user explicitly answered “Acknowledge; ship, merge and publish” after these exact warnings were presented:

- manifest drift: end-at-deliverable blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
- manifest drift: generated hooks (session-start + end-at-deliverable) — 3 mismatch(es) vs PyAutoMind/repos.yaml
- manifest drift: hub organism blurb (organs present) — 2 mismatch(es) vs PyAutoMind/repos.yaml
- manifest drift: organism-map blocks (generated) — 7 mismatch(es) vs PyAutoMind/repos.yaml
- manifest drift: public front-door organ tables (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml
- manifest drift: root AGENTS.md routing table (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
- manifest drift: shared-standards blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
- manifest drift: where-to-file blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
- release validation incomplete: no rehearsal for current source
