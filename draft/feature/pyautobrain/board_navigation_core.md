# Shared banner and navigation: Brain, Mind and Cortex

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Filed: 2026-10-05

## Planning anchor

`draft/feature/pyautobrain/standard_board_banner_and_navigation.md` holds the full component plan, audit and rollout acceptance. This is a proposed phase, awaiting the user's plan approval; no source change or merge authorized yet.

## Scope

Implement the shared navigation-card renderer and CSS in board/_theme.py; adopt in board/_board.py, agents/conductors/intake/_intake.py and agents/conductors/cortex/_cortex.py. Preserve hero identity, 1240px sizing, prose measure, semantics, copy payloads and stable links. Cards directly follow the banner; counts are optional and missing is not zero. Document the owner-supplied component contract and 13-board rollout matrix. Add focused rendering and browser checks. Suggested branch feature/board-navigation-core. This is the dependency for downstream phases; human /prm before dependent consumers ship.

## Original user request (verbatim)

I like the Ears format, we have the banner and logo at the top, but then remove "STALE — refresh required before judging the queue" which is unclear text. Then it has the big buttons under it with all the individual tabs you can go to and click. I want every board to now adopt this format, you prob cant always put numbers in a tbutton but thats fine, its a nice API and standarizes all boards which is a severely lacking aspect
