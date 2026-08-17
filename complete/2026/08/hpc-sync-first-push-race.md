- completed: 2026-08-17
- issue: none — worked straight from the draft prompt
- repos:
  - autolens_assistant
  - autofit_assistant
  - autogalaxy_assistant
  - PyAutoBrain
- prs:
  - https://github.com/PyAutoLabs/autolens_assistant/pull/112
  - https://github.com/PyAutoLabs/autofit_assistant/pull/29
  - https://github.com/PyAutoLabs/autogalaxy_assistant/pull/15
  - https://github.com/PyAutoLabs/PyAutoBrain/pull/228
- merge-commits: autolens_assistant `4b4d8a7` · autofit_assistant `8acfbe1` ·
  autogalaxy_assistant `c06f190` · PyAutoBrain `b909804` (all 2026-08-17)
- summary: `hpc/sync push()` fired the `CODE_DIRS` rsyncs in parallel before
  anything created `${HPC_BASE}/${PROJECT_NAME}`. rsync only creates the last
  path level, so on a first push all of them died with `mkdir failed: No such
  file or directory` — then the `[root files]` rsync created the base dir, so
  `dataset/` synced and the command exited 0. Fixed by `ssh mkdir -p` before the
  parallel rsyncs, plus per-PID `wait` so a failed background rsync is no longer
  swallowed. Landed in all three assistants carrying the script.
- validation: fake-HPC harness (real rsync, stubbed ssh) — reproduced the exit-0
  failure per repo, then confirmed the full tree transfers; injected failure now
  exits 1 and stops `push-submit` before `sbatch`; re-push, `--no-data` and
  `status` unchanged.
- release: n/a — assistant repos, no package release.

## The silence was the bug, not the mkdir

The missing `mkdir` is a one-line fix. What made it cost a GPU job was that
`push()` backgrounded each rsync with `&` and then called bare `wait`.

**`wait` with no arguments reports its own status, not the jobs'.** So under
`set -euo pipefail` five failed rsyncs still left `$?` at 0. The `[root files]`
rsync that ran next happened to create the base directory, so `dataset/` — the
slow, visible part — synced perfectly. Every signal a human reads said success.

The failure surfaced only later, as `sbatch` unable to find `hpc/batch_gpu`
(job 330464, slope_hierarchy first push, 2026-07-16).

So the fix is two changes, and the second is the durable one: collect the PIDs,
`wait` on each, name the directory that failed, and return 1. A first push that
half-lands now stops `push-submit` before it queues work against an incomplete
tree, instead of deferring the error to SLURM.

## It was three repos, not one

The prompt named `autolens_assistant`. `hpc/sync` is cloned across the
assistants, so the same defect sat in two more:

- `autofit_assistant` — blob `1560e64`, **byte-identical** to the file the bug
  was reported against.
- `autogalaxy_assistant` — differs only in `CODE_DIRS` (no `slam_pipeline`);
  `push()` identical, upstream patch applied with no conflicts.
- `autocti_assistant` — has `hpc/` but no `sync` script. Unaffected.

Each was reproduced independently before fixing rather than assumed from the
shared ancestry. Worth remembering for the next `hpc/` change: the script has
three live copies and no shared source.

## Trap: the fix is invisible to the repo's own CI

Nothing in these repos tests `hpc/sync` — it needs a real SSH endpoint. The
whole verification was a local harness that stubs `ssh` (runs the command
locally) and wraps **real** rsync with a `HOST:path` → `path` rewrite, so
rsync's actual one-level-mkdir behaviour is exercised rather than mocked. That
distinction is the point: a mocked rsync would have "passed" against the buggy
script.

`hpc/sync` is also mode `100644` in `autolens_assistant` but `100755` in the
other two — noticed while patching, left alone as out of scope.

## Detour: a red `boundary` check that was not ours

`autolens_assistant#112` opened onto a failing `clone-boundary` job —
`CHOOSING_YOUR_AI_TOOL.md` unclassified. It predated the branch (it arrived in
`64018f8`, "Release 2026.8.17.1", the PR's own base commit) and so was failing
**every** PR against the repo, and blocking every future assistant birth.

The classification was already decided: `modes/maintainer.md`, the prose that
owns the boundary, files the file under `**Mixed**` alongside `llms-chat.txt`.
Only PyAutoBrain's `_clone.py` lacked the pattern — the two sources had drifted.
Fixed in `_SHARED_MIXED` (PyAutoBrain#228), which is a one-repo change; no
`maintainer.md` edit was needed.

Useful mechanism found while doing it: `clone-boundary.yml` honours a
`Brain-ref: <branch>` line in the PR body, running the boundary against that
PyAutoBrain ref instead of `main`, so paired PRs can both be green before an
ordered merge. Note that **editing a PR body does not re-trigger
`pull_request`** — the declaration only takes effect on a fresh event.

## Original prompt

# hpc/sync first-push race — parallel rsyncs before remote base dir exists

Type: bug
Target: autolens_assistant
Repos:
- autolens_assistant
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Bug in autolens_assistant hpc/sync: on the FIRST push to a new remote project, push() launches the CODE_DIRS rsyncs in parallel before anything has created the remote base directory, so all of them fail with 'mkdir failed: No such file or directory' (rsync only creates one path level). The '[root files]' rsync then creates the base dir, so dataset/ syncs and the overall command exits 0 — the failure is silent until sbatch can't find hpc/batch_gpu. Fix: ssh mkdir -p the remote project dir before the parallel rsyncs (or add --mkpath). Found during slope_hierarchy first push (job 330464 postmortem, 2026-07-16).

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from user-intake -->
