# Adopt the shared orchestration panel on remaining boards

Type: feature
Target: PyAutoEars
Repos: PyAutoEars, PyAutoHands, PyAutoMemory, PyAutoPulse, PyAutoInsight, PyAutoNerves, PyAutoGut, PyAutoEyes, PyAutoScientist
Difficulty: large
Autonomy: supervised
Priority: normal
Status: active
Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/PyAutoEars/issues/15
Consequence: judge
Review-minutes: 20
Unattended: needs-slicing

## Original user request (verbatim)

ok do those next tasks

## Approved scope

Bounded consumer phase of `draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md`, whose original request and combined plan remain authoritative and approved. The core component, thirteen organ headings and prose cleanup have shipped. Do not reimplement them. Brain, Mind, Cortex and Heart already use the shared panel.

## Plan

1. Adopt Brain's shipped `orchestration_panel` in Ears, Hands, Memory, Pulse, Insight, Nerves, Gut, Eyes and Scientist. Preserve the approved single-line organ heading, omit explanatory subtitles, and place after banner/navigation.
2. Reuse existing whole-domain prompt payloads on Ears/Pulse/Insight. For boards without a general prompt, add a bounded owner-specific ongoing-chat prompt grounded in existing workflows. Keep distinct release, repair, recovery and figure actions and all approval boundaries.
3. Supply visible trusted work links derived from the body map or domain project registry; copy and exact preview include the same links. Preserve Ears Open Community Hub as a companion destination. Multi-project defaults include named registered destinations without arbitrary project selection; optional direction never changes trusted routing.
4. Remove only superseded panel-specific controls/JS; retain unrelated clipboard actions. Reuse shared focus input, exact preview, clipboard feedback/fallback and length budget. Preserve domain data/feed contracts.
5. Add Scientist README/documentation entry links to Brain's canonical standards. Do not move the RTD source. Generated agent guidance belongs to the separate Mind phase.
6. Update meaningful owner renderer tests, run affected suites and common clipboard witness, render all nine boards, and validate mobile/tablet/desktop in both themes without page-wide overflow. Record adoption evidence and open one tested PR per owner. Publication is checked after authorized merges, not assumed from source.

## Branch survey

All nine canonical repos are on main. Eight are clean; Eyes has user-owned untracked dataset/, output/ and scripts/ which remain untouched. No current active task claims these repos. Source edits use isolated worktrees on feature/orchestration-panel-consumers.

## Delivery

Workspace workflow using the already-merged Brain API. Tier: judge; merge mode: human /prm. No new behavior outside the approved parent initiative.

## PRs opened — 2026-10-06

Nine tested panel PRs open. 1,441 owner tests and 72 browser layouts plus integrated clipboard/fallback/budget flows passed; independent review CLEAN. Generated standards guidance included on each branch. Human /prm, then regenerate and verify live publication.

| Repository | PR |
|---|---|
| PyAutoEars | https://github.com/PyAutoLabs/PyAutoEars/pull/16 |
| PyAutoHands | https://github.com/PyAutoLabs/PyAutoHands/pull/303 |
| PyAutoMemory | https://github.com/PyAutoLabs/PyAutoMemory/pull/118 |
| PyAutoPulse | https://github.com/PyAutoLabs/PyAutoPulse/pull/19 |
| PyAutoInsight | https://github.com/PyAutoLabs/PyAutoInsight/pull/8 |
| PyAutoNerves | https://github.com/PyAutoLabs/PyAutoNerves/pull/188 |
| PyAutoGut | https://github.com/PyAutoLabs/PyAutoGut/pull/24 |
| PyAutoEyes | https://github.com/PyAutoLabs/PyAutoEyes/pull/20 |
| PyAutoScientist | https://github.com/PyAutoLabs/PyAutoScientist/pull/45 |

CI was judged once at each exact head: no failures observed; pending, skipped and absent checks are not green. The corresponding CI snapshots and local validation artifacts are preserved in the session scratch evidence. No timers, watchers or automatic merge subscriptions remain.
