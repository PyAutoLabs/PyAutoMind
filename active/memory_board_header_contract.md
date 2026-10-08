# memory-board-header-contract

Type: bug
Target: PyAutoMemory
Repos: PyAutoMemory
Difficulty: easy
Consequence: notify
Autonomy: safe
Priority: high
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/126
Parent: inference-sampler-literature (Memory#124; PR125)

## Intent

Unblock the approved literature phase by repairing Memory's pre-existing shared-header assertion regression, reproduced on origin/main 3ce9948. tests/test_board.py::test_paper_links_and_issue_actions expects the retired `markdown version` header anchor; Brain's canonical section_layout converts the Markdown source link into an accessible icon with aria-label=Markdown version. Follow the current shared contract, retain checks for the repository front door and paper/issue actions, and do not change production rendering. Use an isolated prerequisite branch coordinated under the existing owned literature claim. No unrelated changes, compute or release.

## Plan

- Reproduce the single failing test on exact origin/main and inspect authoritative Brain shared-header output.
- Change only the stale test expectations to assert the current accessible Markdown source link and GitHub Page link.
- Run targeted/full Memory tests, validate, structure and existing gates; obtain independent review before shipping.

Detailed: edit tests/test_board.py::test_paper_links_and_issue_actions; assert semantic link targets/labels using HTML parsing or the shared stable markup rather than obsolete plain anchors. Keep every existing paper, queue and issue assertion. Tier: notify — merge mode: human-authorized in-turn merge on independent CLEAN review and all green checks, as an approved prerequisite.

## Authorization and original request

Human original request: "prm, and continue through all phases autonomously to the end".
Root delegated prerequisite: "investigate Memory PR125 CI failure tests/test_board.py188 stale markdown link assertion ... Use bug skill then start-dev plan/survey/worktree route for narrow fix, user autonomous all-phase authority covers prerequisite ... separate branch/issue ideally ... no commit/push/merge".

Coordination authorization: root explicitly authorized a separate prerequisite prompt/issue and isolated branch/worktree recorded under the existing inference-sampler-literature owned claim. Both are owned by this same root session; preserve the literature diff.
