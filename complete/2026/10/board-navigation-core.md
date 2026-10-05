# Shared board banner and navigation

Merged PyAutoBrain#464 (3cdd3c7792e9e6d7a6edc25d06a85fa6133ec9d9), closing PyAutoBrain#463.

The shared theme now renders accessible section cards immediately after the logo banner, with optional owner-supplied counts and context. Brain, Mind and Cortex use the component. Responsive sizing, operational meanings and copy prompts are preserved. The remaining ten boards have separate active migration tasks.

Validation: 1,186 tests; strict docs build; tenant firewall and discovery checks; 30 browser viewport/theme cases including keyboard navigation. Every Docs and Brain Tests CI job passed on bb858130adf0885e018b3d78cdd52be0ccd47a33. Heart refreshed GREEN (100), 2026-10-05T17:07:28Z.

Evidence: tmp/board-navigation/core-evidence/ (local raw evidence), docs/board-navigation.md and its committed screenshots in Brain.

## Original prompt

# Shared banner and navigation: Brain, Mind and Cortex

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: active
Issued: 2026-10-05
Consequence: judge
Filed: 2026-10-05

## Planning anchor

`draft/feature/pyautobrain/standard_board_banner_and_navigation.md` holds the full component plan, audit and rollout acceptance. This is a proposed phase, awaiting the user's plan approval; no source change or merge authorized yet.

## Scope

Implement the shared navigation-card renderer and CSS in board/_theme.py; adopt in board/_board.py, agents/conductors/intake/_intake.py and agents/conductors/cortex/_cortex.py. Preserve hero identity, 1240px sizing, prose measure, semantics, copy payloads and stable links. Cards directly follow the banner; counts are optional and missing is not zero. Document the owner-supplied component contract and 13-board rollout matrix. Add focused rendering and browser checks. Suggested branch feature/board-navigation-core. This is the dependency for downstream phases; human /prm before dependent consumers ship.

## Original user request (verbatim)

I like the Ears format, we have the banner and logo at the top, but then remove "STALE — refresh required before judging the queue" which is unclear text. Then it has the big buttons under it with all the individual tabs you can go to and click. I want every board to now adopt this format, you prob cant always put numbers in a tbutton but thats fine, its a nice API and standarizes all boards which is a severely lacking aspect
