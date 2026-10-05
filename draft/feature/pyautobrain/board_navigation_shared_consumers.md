# Shared banner and navigation: Ears and shared consumers

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoEars
- PyAutoMemory
- PyAutoHeart
- PyAutoHands
- PyAutoPulse
- PyAutoNerves
- PyAutoGut
- PyAutoScientist
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Filed: 2026-10-05

## Planning anchor

`draft/feature/pyautobrain/standard_board_banner_and_navigation.md` holds the full component plan, audit and rollout acceptance. This is a proposed phase, awaiting the user's plan approval; no source change or merge authorized yet.

## Scope

After board_navigation_core merges, adopt the shared component in all eight consumer renderers listed in the parent plan, with one issue/PR per repository. Start with Ears: remove the quoted stale message, move readable timestamp/out-of-date metadata below navigation, update its browser expiry behavior, and preserve stale/unknown data semantics. Keep owner-specific destinations and actions. Use local fixtures and browser evidence to prove adoption in each board; verify regeneration/publication before claiming live. Split repo execution prompts before claims.

## Original user request (verbatim)

I like the Ears format, we have the banner and logo at the top, but then remove "STALE — refresh required before judging the queue" which is unclear text. Then it has the big buttons under it with all the individual tabs you can go to and click. I want every board to now adopt this format, you prob cant always put numbers in a tbutton but thats fine, its a nice API and standarizes all boards which is a severely lacking aspect
