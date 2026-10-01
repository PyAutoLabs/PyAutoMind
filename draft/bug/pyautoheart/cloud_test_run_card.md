# Show cloud-observed workspace tests on the Heart board
Type: bug
Difficulty: small
Autonomy: human-required

## Original request
> fix this One display inconsistency remains: the test-run card says “unobserved,” although workflow logs confirm ingestion. Older dev-box observations also remain advisory., do it end to end without asking me anything

## Evidence and scope
@PyAutoHeart published board 2026-10-01T19:55:48Z is GREEN/100 but the Test run section is unobserved. The same workflow log says `test_run ready 1405p/0f/122s @ cloud#36909756099`. `heart/dashboard.py` leaves `test_run` in `LOCAL_ONLY_FAMILIES`, which unconditionally masks the measured snapshot. The dev-box observation was last published 3d ago; worktree drift, script timing and profiling drift remain local-only. Refresh those through the existing `pyauto-heart tick` and `publish` door after merge, preserving privacy scrub and user worktrees.

## Plan approved in chat
The user explicitly requested end-to-end completion without asking. For the display fix: remove test_run from the local-only list, let the existing measured renderer surface its ready/failure/unknown state, and keep an unobserved placeholder when no test-run evidence exists. Update focused board tests for measured and missing evidence, including nonfabricated counts. Run Heart suite and tenant firewall, open PR, judge every CI leg, merge if green, close issue and Mind task, and publish/check the live board. No score, threshold, skip or weight changes. Older dev-box sections remain advisory with age shown and are refreshed only through sanctioned publish.

## Branch survey
Heart canonical clean main after fast-forward; no other Heart claim. Mind canonical branch belongs to another session; isolated ledger is codex/cloud-test-run-card. Source branch feature/cloud-test-run-card from origin/main.
