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

## Planning state

No source edited. User approved the corrected plan and label mapping with “continue” on 2026-10-08. Brain is currently claimed by `board-one-click-update` (PyAutoBrain issue #504); `worktree_check_conflict` reports a hard conflict. Do not create a competing implementation worktree until the claim is resolved. Heart entry verdict: STALE (release STALE; monitoring RED); planning permitted by start_dev.
