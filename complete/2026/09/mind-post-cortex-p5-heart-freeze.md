- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/196 (closed, completed 2026-09-03)
- completed: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/197 (merged `4b873047`)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/347 (merged `67971f21`)
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/275 (merged `128d9a1d`)
- epic: mind-post-cortex (phase 5 of 5, the last — with this the epic is COMPLETE and its
  ledger is archived to `complete/archive/epics/mind_post_cortex_epic.md`)
- shipped: the library-main validation window is now a thing the organism can read. Assessment
  gap 6. A library merge landing mid-validation restales Heart and costs ~75 minutes
  (`feedback_library_merge_mid_validation_restales_heart`, 2026-08-29); `heart-ack:` recorded
  that fact per task, but nothing told a `/prm` run or a batch member "library mains are frozen
  for the next N minutes". Now something does.
  - **Heart owns the flag** (`heart/freeze.py`, new). `$HEART_STATE_DIR/freeze.json`
    (`~/.pyauto-heart/freeze.json`) carries `{reason, set_at, until, set_by}`, and the new
    `pyauto-heart freeze` verb writes, reads and clears it (`--set`, `--until`, `--clear`,
    `--show`). **Expiry is by `until`, not by discipline**: a flag past its expiry reads as
    clear and `--show` says "expired", so a forgotten set is visible rather than permanent —
    the failure mode a hand-maintained lock file always has.
  - **Real call sites, not just a verb.** `pyauto-heart validate --ingest` clears the freeze
    when it persists a validation report, because that ingest *is* the end of the window;
    `skills/review_release` gained the check-and-clear step; the Hands `skills/pre_build`
    gained the set-at-dispatch / clear-at-review step. The nightly release run is CI YAML and
    was documented rather than edited.
  - **Brain reads it, on three surfaces** — and only one of them has teeth. The `vitals`
    faculty prints `FROZEN: <reason> until <ts>` as a warning line; `batch collect`'s summary
    and the status-box renderer (`_status.py`) carry the same line as a caller-supplied fact;
    and `/prm` gained a merge-gate leg that **stops** on a library-repo PR while the freeze is
    active. Organ and workspace PRs are not gated.
  - **Heart's verdict is deliberately unchanged.** The freeze does not enter `readiness`'s
    colour or its reason list. Putting it there would make every ship and every release gate
    block on it — the opposite of "advice-with-teeth for `/prm` only" — so it stays a separate
    live read that the surfaces above go and take.
  - **The `--thaw` decision.** The prompt named one human-required question: may `/prm`
    override an active freeze? Answered on the prompt's own recommendation — yes, with the
    override logged: `/prm --thaw "<why>"` merges through an active freeze and appends one row
    to `autonomy_log.md` under a **Freeze overrides** heading created on first use. Flagged at
    the head of PyAutoBrain#347 and in issue #196 as reversible before merge; it was not
    reversed.
- verification: `pytest -q` green in all three repos on the merge heads; the Brain run in the
  task worktree was 902 passed / 1 failed, the failure being only
  `test_a_fixture_tree_finds_the_schema_its_checkout_ships` — the known worktree-anchor test
  that resolves `PyAutoCortex` to the canonical checkout and fails in any task worktree. CI on
  the pushed heads after `origin/main` was merged in: Heart Tests pytest 3.12 + 3.13, Brain
  Tests pytest 3.12 + 3.13, Hands Tests pytest 3.12 + 3.13 + 3.14 — every run, every leg green,
  filtered by head sha.
- merge order: PyAutoHeart#197 first (Brain reads the verb Heart ships), then PyAutoBrain#347,
  then PyAutoHands#275. Heart and Brain both needed `origin/main` merged into their branches
  first — Brain was 9 commits behind and phase 4's `_batch.py` changes (`derive_awaiting_review`,
  `queue_rank`, `member_outcome`, `merge_order`, the outcomes block) had landed on `main` since
  the branch was cut. Both merges were textually clean; the pre-ship `git merge-tree` scratch
  merges against p3 and p4 had predicted exactly that.
- heart at merge: `readiness --json` was RED when the PRs were opened, with three reasons
  recorded in the `active.md` row and never acked for this task — PyAutoLens CI failure,
  release validation FAILED (stage integrate), PyAutoArray open PR 11 days old. None touches
  this diff: one new Heart module and CLI verb, one ingest-side clear, skill/doc files and their
  tests; no library source and no release surface. The merge was the human's own `/prm` call,
  which is the only thing that could have unblocked it.

## Original prompt

# Heart freeze flag: make the library-main validation window visible to `/prm` and batch members

Type: feature
Target: pyautoheart
Repos:
- PyAutoHeart
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: `pyauto-heart freeze --set "release validation" --until <ts>` writes `state/freeze.json`; `pyauto-brain vitals` prints the freeze with its reason and expiry; `/prm` on a library PR while the freeze is active stops with the freeze message instead of merging (workspace/organ PRs unaffected); `batch collect`/status box show the freeze line; the flag clears itself past `--until` and on `--clear`; Heart and Brain tests cover set/clear/expiry
Review-minutes: 20
Unattended: ready
Epic: mind-post-cortex
Phase: 5
Filed: 2026-09-03
Issued: 2026-09-03

Phase 5 of `mind-post-cortex` — assessment gap 6. Two PRs: Heart (the flag
and its CLI) and Brain (`vitals` faculty, `/prm` gate leg, batch status line).

## Why

A library merge landing mid-validation restales Heart and costs ~75 minutes
(memory: `feedback_library_merge_mid_validation_restales_heart`, 2026-08-29).
`heart-ack:` is recorded per task and per shift, but nothing tells a member or
a `/prm` run "library mains are frozen for the next N minutes".

## Design

- **Heart owns the flag**: `state/freeze.json` `{reason, set_at, until, set_by}`
  written by a new `freeze` verb on the Heart CLI (`--set`, `--until`,
  `--clear`, `--show`). The release/validation drivers (`review_release`,
  `pre_build`, the nightly release run) set it at validation start and clear
  it at the end; document the exact call sites and add them.
- **Brain reads it**: the `vitals` faculty prints it as a YELLOW reason
  (`FROZEN: <reason> until <ts>`); `/prm` adds it as a gate leg before merge
  for PRs whose repo is in `LIBRARY_REPOS` (organ and workspace repos are not
  gated); the batch status box and `batch collect` summary carry one line.
  The flag is advice-with-teeth for `/prm` only — no other skill blocks on it.
- Expiry is by `until`; a stale flag past expiry reads as clear, and `--show`
  says "expired" so a forgotten set is visible.

Human-required decision to surface in the plan: whether `/prm` may override
with an explicit `--thaw` (recommended: yes, logged to `autonomy_log.md`).
