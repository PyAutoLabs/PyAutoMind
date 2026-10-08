# Functional organ banner labels

Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/513
PR: https://github.com/PyAutoLabs/PyAutoBrain/pull/514
Merged: 2026-10-08
Merge commit: e20e0b0f9ef80877ccb2e4ef336cbf69c30b74da

## Delivered

Shared banners display organ functions instead of generic Board/Dashboard wording. Broca reads Assistants and follows Nerves in the shared navigation; Heart reads Tests. Logos, software names, taglines and CSS are unchanged.

## Validation

- 1,252 Brain tests passed in the CI environment. The initial activated environment exposed an existing path-resolution test assumption; removing checkout overrides resolves it without source changes.
- Tenant firewall passed; all PR CI jobs passed (Python 3.12, Python 3.13, docs).
- All 15 hero outputs were compared with the base: only the grey label text changed.
- Browser checks passed at 390, 768, 820, 1024 and 1440px; live mobile screenshots checked Heart, Cortex and Broca.
- User explicitly acknowledged Heart's nine YELLOW reasons (eight generated-drift categories plus absent rehearsal), and authorized shipping, merging and publication. No scientific library changes; workspace scientific smoke not applicable.

## Publication

All 15 public pages verified on 2026-10-08. Ears render and deploy both passed: https://github.com/PyAutoLabs/PyAutoEars/actions/runs/37835473692

| Dashboard | Label | Live verification |
|---|---|---|
| [PyAutoBrain](https://pyautolabs.github.io/PyAutoBrain/) | Orchestration | Verified; artwork preserved |
| [PyAutoMind](https://pyautolabs.github.io/PyAutoMind/) | Planning | Verified; artwork preserved |
| [PyAutoCortex](https://pyautolabs.github.io/PyAutoCortex/) | Science | Verified; artwork preserved |
| [PyAutoMemory](https://pyautolabs.github.io/PyAutoMemory/) | Knowledge | Verified; artwork preserved |
| [PyAutoEyes](https://pyautolabs.github.io/PyAutoEyes/) | Visualization | Verified; artwork preserved |
| [PyAutoEars](https://pyautolabs.github.io/PyAutoEars/) | Community | Verified; artwork preserved |
| [PyAutoHeart](https://pyautolabs.github.io/PyAutoHeart/) | Tests | Verified; artwork preserved |
| [PyAutoHands](https://pyautolabs.github.io/PyAutoHands/) | Releases | Verified; artwork preserved |
| [PyAutoPulse](https://pyautolabs.github.io/PyAutoPulse/) | Profiling | Verified; artwork preserved |
| [PyAutoInsight](https://pyautolabs.github.io/PyAutoInsight/) | Inference | Verified; artwork preserved |
| [PyAutoNerves](https://pyautolabs.github.io/PyAutoNerves/) | Configuration | Verified; artwork preserved |
| [PyAutoBroca](https://pyautolabs.github.io/PyAutoBroca/) | Assistants | Verified; artwork preserved |
| [PyAutoGut](https://pyautolabs.github.io/PyAutoGut/) | Cleanup | Verified; artwork preserved |
| [PyAutoScientist](https://pyautolabs.github.io/PyAutoScientist/) | Overview | Verified; artwork preserved |
| [PyAutoDNA](https://pyautolabs.github.io/PyAutoDNA/) | Environments | Verified; artwork preserved |

Each owner was refreshed with its existing workflow; cached-HTML consumers were regenerated before deployment. Shared navigation order was verified wherever a shared footer is present.

## Preserved work

At the user's explicit request, board-one-click-update (#504) was moved to parked.md. Its worktree and uncommitted board_update/ prototype remain untouched for later resumption.

## Evidence

Local QA and deployment receipts: `tmp/organ-banner-task-labels/` (ignored scratch evidence). No sibling prompts were retired by the scoped intake reconciliation; its unrelated similarity results remain unchanged.

## Original prompt

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
