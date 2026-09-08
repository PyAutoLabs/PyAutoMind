## batch-no-park-at-ship
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/363
- completed: 2026-09-07
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/365 (merge 6383373f)
- summary: |
    Doctrine change in `PyAutoBrain/AUTONOMY.md`, dated 2026-09-07: under an explicit `--auto` launch an
    effective-`supervised` run reaching the ship checkpoint no longer parks (`awaiting-input`, question on
    the issue); it resolves to decide-and-flag — PR opened, never merged, the decision flagged in the PR body
    under the existing one-per-PR rule — because every autonomous run already ends at PR-open with merge human,
    so the PR review IS the approval the supervised level exists to provide. The decide-and-flag section is
    rescoped from "batch launches only" to every explicit `--auto` launch; every limit stays (one flagged
    decision per PR; rejected alternative + one-command revert; never public API / default / error contract /
    external reporter's file; never `judge` tier; `decision-taken` label). Interactive supervised runs keep
    park-and-ask; `human-required`, `Unattended: never` and `Blocked-by:` are unchanged. Second revert
    condition: one supervised `--auto` PR the human would have wanted stopped before it existed returns the
    checkpoint to park-and-ask.
- planner: |
    `agents/conductors/batch/_batch.py` admits `supervised` members and rejects only `human-required`
    ("autonomy human-required — would park at ship"); supervised members are marked
    `(supervised — decide-and-flag at ship)` in the BatchDecision. `skills/start_dev/start_dev.md` (`--auto`
    supervised bullet) and `skills/batch/batch.md` (rejection vocabulary) match the doctrine.
- witness: |
    `pyauto-brain batch plan` on the 2026-09-07 backlog, 45-min budget: before 4 members with 91
    "autonomy supervised — would park at ship" rejections; after 10 members, zero supervised rejections,
    17 human-required still rejected; `draft/bug/autonerves/xla_gpu_autotune_level_0_default_slows_fp64_gemm.md`
    taken as a member. Posted as a PR comment.
- tests: |
    `tests/test_batch_plan.py::test_human_required_work_is_never_dispatched` (was
    `test_only_safe_work_is_dispatched`); new `tests/test_autonomy_doctrine.py` pins the levels-table cell,
    the extension paragraph and both revert conditions. 922 passed in the worktree; the one failure is the
    known worktree-only Cortex fixture (`draft/bug/pyautobrain/cortex_test_worktree_symlink.md`).
- evidence: |
    2026-08-31 batch: PyAutoFit#1554 and PyAutoMemory#76 took decide-and-flag and gave one review surface;
    PyAutoHands#272, PyAutoFit#1552 and euclid#47 parked and each needed a separate judgement before a PR
    existed. 2026-09-07: `/batch` rejected all five prompts the human named, three of them supervised.
- follow-ups: |
    The three supervised prompts rejected on 2026-09-07 (mge_jit_regression_rebaseline, xla_gpu_autotune
    default, scheduled_runs_delivered_hours_late) and `draft/feature/pyautobrain/batch_slice.md` are now
    admissible to the next batch. Sibling task prm-shadow-row-notify-tier (PyAutoBrain#364) shipped in the
    same session.

## Original prompt

# Retire parked-at-ship under `--auto`: supervised resolves to decide-and-flag

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: never
Filed: 2026-08-31
Issued: 2026-09-07

Human direction (2026-08-31, verbatim):

"""
I dont really want these parked at ship judgements, ideally we send off a batch
and then dont think about it again, the parked thing is an annoying middle
ground which requires human time.
"""

Doctrine change to AUTONOMY.md (human-required — this is a gate edit, to be made
with the human in the loop, not by an unattended run):

Under an explicit **`--auto` launch**, an effective-`supervised` run reaching the
ship checkpoint does not park. It resolves to **decide-and-flag**: open the PR
(never merge), and flag the decision in the PR body per the existing one-per-PR
rule. The contract already ends every autonomous run at PR-open with merge left
to the human, so **the PR review IS the human approval the supervised level
exists to provide**. A mid-run park is a redundant second checkpoint: it costs
the human a GitHub-issue round-trip before a PR even exists, and then asks them
for the same judgement again at merge.

Evidence, 2026-08-31: two supervised-capped `--auto` runs took the
decide-and-flag branch (PyAutoFit#1554, PyAutoMemory#76) and produced exactly
the desired experience — everything at a PR, one review surface; three runs took
the park branch (PyAutoHands#272, PyAutoFit#1552, euclid#47) and each required a
separate human judgement before a PR existed.

Scope: `--auto` launches only — interactive supervised runs keep the park
behaviour, because there the human is present and the round-trip is free.
`human-required` and `Unattended: never` are unchanged and never run unattended.
`Blocked-by:` unchanged.

Witness: AUTONOMY.md's supervised ship-checkpoint section states the rule with a
dated entry and a revert condition, and the next `--auto` run with a
supervised-capped member ends with a PR, not a park.
