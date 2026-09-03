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
