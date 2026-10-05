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

After board_navigation_core merges, adapt Eyes and Insight independent renderers to the same banner, card navigation and sizing contract. Preserve gallery/inference data, actions and identity. Resolve the independent outer-width and overflow integration needed for usable cards on compact screens; verify with loaded gallery assets and populated tables. Preserve Eyes local untracked dataset/, output/ and scripts/; use isolated worktrees. One issue/PR per repository; split repo execution prompts before claims. Verify all 13 board entries and remaining publication state for the final rollout report.

## Original user request (verbatim)

I like the Ears format, we have the banner and logo at the top, but then remove "STALE — refresh required before judging the queue" which is unclear text. Then it has the big buttons under it with all the individual tabs you can go to and click. I want every board to now adopt this format, you prob cant always put numbers in a tbutton but thats fine, its a nice API and standarizes all boards which is a severely lacking aspect
