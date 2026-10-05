# Standard board banner and navigation rollout

All 13 published boards now use the shared logo banner followed by prominent section navigation. Counts are optional, and each board retains its own evidence and action meanings. Ears no longer shows the unclear "STALE — refresh required before judging the queue" wording; it shows a readable last-checked timestamp and a plain explanation below the cards when needed.

## Merged implementation

- PyAutoBrain#464: shared API and Brain, Mind, Cortex adoption.
- PyAutoEars#12: https://github.com/PyAutoLabs/PyAutoEars/pull/12
- PyAutoMemory#116: https://github.com/PyAutoLabs/PyAutoMemory/pull/116
- PyAutoHeart#283: https://github.com/PyAutoLabs/PyAutoHeart/pull/283
- PyAutoHands#299: https://github.com/PyAutoLabs/PyAutoHands/pull/299
- PyAutoPulse#15: https://github.com/PyAutoLabs/PyAutoPulse/pull/15
- PyAutoNerves#186: https://github.com/PyAutoLabs/PyAutoNerves/pull/186
- PyAutoGut#22: https://github.com/PyAutoLabs/PyAutoGut/pull/22
- PyAutoScientist#43: https://github.com/PyAutoLabs/PyAutoScientist/pull/43
- PyAutoEyes#17: https://github.com/PyAutoLabs/PyAutoEyes/pull/17
- PyAutoInsight#5: https://github.com/PyAutoLabs/PyAutoInsight/pull/5

## Validation and publication

1,186 core tests and 2,655 consumer tests passed. Every CI workflow and job on each PR head passed before merging. Browser evidence covers five viewport widths and light/dark for all owners, plus keyboard section navigation. The Ears browser suite also checks clipboard actions, expiry and overflow. Heart was GREEN before shipping.

All 13 live Pages URLs were fetched after publication and contain the shared navigation. Cortex was explicitly regenerated through its existing dashboard refresh workflow. Local raw evidence is retained at `tmp/board-navigation/`, including CI results, test logs, rendered pages, screenshots and `live-status.json`.

Core and consumer issues closed; claims released; dashboards regenerated as part of this close-out. Existing prompt panels retain their payloads and remain a separate task.

## Original prompt

# Shared banner and navigation: Eyes and Insight

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoEyes
- PyAutoInsight
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Filed: 2026-10-05

## Planning anchor

`draft/feature/pyautobrain/standard_board_banner_and_navigation.md` holds the full component plan, audit and rollout acceptance. This is a proposed phase, awaiting the user's plan approval; no source change or merge authorized yet.

## Scope

After core PR PyAutoBrain#464 (merged; `complete/2026/10/board-navigation-core.md`), adapt Eyes and Insight independent renderers to the same banner, card navigation and sizing contract. Preserve gallery/inference data, actions and identity. Resolve the independent outer-width and overflow integration needed for usable cards on compact screens; verify with loaded gallery assets and populated tables. Preserve Eyes local untracked dataset/, output/ and scripts/; use isolated worktrees. One issue/PR per repository; split repo execution prompts before claims. Verify all 13 board entries and remaining publication state for the final rollout report.

## Original user request (verbatim)

I like the Ears format, we have the banner and logo at the top, but then remove "STALE — refresh required before judging the queue" which is unclear text. Then it has the big buttons under it with all the individual tabs you can go to and click. I want every board to now adopt this format, you prob cant always put numbers in a tbutton but thats fine, its a nice API and standarizes all boards which is a severely lacking aspect
