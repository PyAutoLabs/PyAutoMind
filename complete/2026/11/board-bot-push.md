M2.2 follow-up item 12 (human ask, 2026-11-16). Shipped as PyAutoHeart#350 (942fd53d9) and PyAutoHands#342 (3f606a75e), merged 2026-11-16 after an independent review returned CLEAN, with Heart tests run on the branch head and Hands CI 3/3 GREEN. Issue PyAutoHands#341.

**Built:** every push to Heart's and Hands' own `main` now authenticates as the pyautolabs-bot App:
- Heart: the board block and timing record, and the token-push sidecar.
- Hands: the release-board strip.

Each uses a repo-scoped App token with contents write. Checkouts no longer save `GITHUB_TOKEN`, and the workflow grants drop to contents read.

**Then:** the lead applied the M2.2 merge gate rulesets to both repos (Heart 27363731, Hands 27363737; bypass: org admin plus the App only; `ACTIONS_BYPASS_REPOS` emptied in `m2_rulesets/apply.sh`). **All 14 repos now carry the ruleset.** Witness: Heart's dispatched daily run committed as `pyautolabs-bot[bot]` at 10:04:58Z under the ruleset. Hands' run had nothing to commit.

**Lesson:** a commit message that quotes the CI-skip marker skips that PR's CI. Hands#342 needed an empty commit to run its checks.
