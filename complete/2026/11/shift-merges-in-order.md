A shift now holds a library repo for starting only while a worker on it is live, and serialises that library's merges in PR order instead of holding the library until each PR merges (M3.6j). A later PR's close-out waits behind earlier open shift PRs on the same library (no slot, no refusal); once they merge, a short update session runs `gh pr update-branch` and the normal close-out merges only on CI green at the new head; a conflict, red CI on the new head, a moved head or a third update refuses it to /prm. Later workers get a sibling note; a workspace PR waits behind its own library PR; the digest shows "waits behind" and a per-library Merge order block. Human rulings a–f (2026-11-19) are recorded in AUTONOMY.md.

Motivated by shifts 2026-11-18-pm (4 of 7 tasks unstarted) and -pm2 (2 of 4), each stalled about an hour behind a decision-taken PR awaiting /prm.

Shipped in PyAutoBrain#684 (merged 2026-11-19 by human /prm). Independent review (fresh Sonnet agent): FINDINGS, no blocker; F1 (notify in-turn merge jumping the order), F2 (two workers on one library after a re-rank), F5 (CI read on a moved head) fixed in b7c04fa; F3/F4/F6 known, listed on the PR. Full suite 2413 passed, 1 skipped. First live test: named tasks 6–7 (PyAutoGalaxy) from shift 2026-11-18-pm.

## Original prompt

# M3.6j A shift serialises library merges, not starts, so a PR awaiting /prm does not stall its library

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-11-18
Issued: 2026-11-19
Epic: autonomous-orchestrators
Consequence: judge
Witness: `python -m pytest tests/test_batch_named_tasks.py tests/test_orchestrator_closeout.py -q` passes with new tests that fail on today's main: (1) two named glance tasks on one library — the second starts once the first's PR is open, even when the first's close-out was refused for a human /prm (decision-taken, public name, judge); (2) the second's close-out does not merge while the first's PR is open; (3) once the first merges, the second's close-out updates its branch from main and merges only on CI green at the new head; (4) never two workers live on one library at once
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-18, at the end of shift 2026-11-18-pm: "I think theres an issue where the
orchestator should not get stuck and unable to do follow up tasks cause it needs my prm"

## Why

PyAutoBrain#679 (PR #680, merged 2026-11-18) frees a shift's library slot only once the task
holding it has all its PRs merged. In shift 2026-11-18-pm (7 named glance bugs, 5 on
PyAutoGalaxy, 2 on PyAutoFit) the first PyAutoGalaxy PR merged unattended (#722) and the next
started, but then PyAutoGalaxy#724 was refused for an unattended merge ("public name added or
renamed: a human /prm") and PyAutoFit#1783 likewise ("decision-taken label"). Both libraries
stayed held until review-at: 4 of 7 tasks never started, and the shift sat idle from ~16:36Z
to 17:30Z with no workers live and 3.9M of its 5M token budget unspent.

The one-per-library rule exists because concurrent library PRs collide at merge. Work does not
collide; merges do. Holding the *start* of the next task until a human /prm stalls the shift
on the one step the shift cannot do.

## Proposed shape (to be planned)

- A library is held for **starting** only while a worker on it is live (never two workers on
  one library at once).
- A library is held for **merging** while any earlier PR of this shift on it is open: the next
  task's close-out waits (no refusal, no slot taken) until that PR merges.
- When it may merge, the close-out updates the branch from `main` and requires CI green on the
  new head before merging; a conflict refuses and leaves it for /prm.
- Each later PR's worktree branches from `main`, not from the open PR (no stacked PRs).
- The digest says which PRs wait behind which /prm, so the human merges in order.
- Consider whether the next task should instead branch from the open PR's branch when it
  touches the same files — out of scope unless planning shows the update-from-main step
  conflicts too often.

## Not in scope

- Unattended merging of PRs that need a human /prm.
- Raising merge-cap or changing close-out guards other than the wait.

## Answers from the human

2026-11-19, in chat: plan approved ("approved, all six yes"). Full plan and rulings on https://github.com/PyAutoLabs/PyAutoBrain/issues/683.

(a) an unattended update session may push a merge-from-main (`gh pr update-branch`, never force) to a shift PR branch, then must end; a later session merges only on CI green at the new head. (b) the watcher may `gh pr view` blocking PRs every tick while a later PR waits, incl. carried ones. (c) an earlier PR blocks until GitHub says MERGED or CLOSED, whatever its state (dropped, red, abandoned). (d) parks on a question keep holding the library start. (e) a worker may proceed past a `worktree_check_conflict` hit naming only a listed sibling slug. (f) library repos only, and only PRs this shift knows (its outcomes + carried `behind`).
