# Shared banner and navigation: PyAutoHeart

Merged https://github.com/PyAutoLabs/PyAutoHeart/pull/283 (57a4822a24e18f45ef69de5fb7c026bc24c2564f), closing https://github.com/PyAutoLabs/PyAutoHeart/issues/282.

The board now uses the shared logo banner followed immediately by prominent section links. Counts remain optional and owned by this board. Existing evidence, freshness safeguards and action payloads are preserved.

Validation: 1227 passed in 71.20s (0:01:11); ten viewport/theme browser cases; all workflow runs and every CI job on 0e3234894e760cf1b2ec02bc8bbb129155cb9803 succeeded. Heart GREEN, 100, at 2026-10-05T17:25:39Z.

Local evidence: tmp/board-navigation/ (test logs, CI verdict and renders/PyAutoHeart/ browser screenshots).


## Original prompt

# Adopt shared board navigation in PyAutoHeart

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: active
Issued: 2026-10-05
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/282
Consequence: judge
Filed: 2026-10-05

## Approved scope

Adopt Brain's shared banner/navigation in heart/dashboard.py. Place logo/banner then navigation cards, then freshness/context and content; preserve owner-supplied counts, existing anchors/actions, semantics and identity. Count-free links are valid.

Approved as part of `standard_board_banner_and_navigation.md` by the user's “sounds good, go $prm”. Depends on PyAutoBrain PR #464; do not merge before that base. Validate the full applicable repo suite plus renderer link/header tests and five-width light/dark browser checks. Preserve copy/disclosure behavior and feed contracts. Existing regeneration/publication must be verified separately from source merge. Tier judge; user explicitly authorized /prm in the active execution turn. No scientific release or compute submission.

## Original user request (verbatim)

I like the Ears format, we have the banner and logo at the top, but then remove "STALE — refresh required before judging the queue" which is unclear text. Then it has the big buttons under it with all the individual tabs you can go to and click. I want every board to now adopt this format, you prob cant always put numbers in a tbutton but thats fine, its a nice API and standarizes all boards which is a severely lacking aspect
