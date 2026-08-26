- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/331 (closed on ship)
- shipped: 2026-08-26 — PyAutoMind PR https://github.com/PyAutoLabs/PyAutoMind/pull/332
  (merge commit `70dda35`)
- classification: bug (PyAutoMind only; Mind infrastructure — neither library nor workspace)
- summary: `scripts/status.sh --repos` sourced `scripts/pyauto_status.sh` and called a
  `pyauto-status` shell function; both went with the cross-repo git sync dashboard when it
  became a leg of the Heart-owned `$health` door (`/health status`), leaving the branch
  sourcing a file absent from the repo. Decided **delete, not repoint** — see key traps.
  The branch is gone; `--repos` now names its replacement on stderr and exits 2.
- shipped changes:
  - `scripts/status.sh`: the `source "$ROOT/scripts/pyauto_status.sh"` + `pyauto-status` +
    `exit 0` block deleted, replaced by a heredoc pointing at `/health status` and `exit 2`.
    Usage header narrowed to `[--full]`, with a comment recording where the dashboard went
    and why the branch could not be repointed.
  - `tests/test_status_script.py` (new, 4 tests): the retired flag exits non-zero and names
    `/health status`; it raises no `No such file or directory` / `command not found`; every
    file the script `source`s resolves to a real path (the root cause, generalised); a bare
    run still exits 0 and prints `== Registry ==`. Fictional-fixture-free, per the
    `tests/**` KEEP-copy rule.
- validation: 216/216 PyAutoMind tests; all four new assertions confirmed to FAIL against the
  pre-fix script extracted from `git show HEAD:scripts/status.sh`; `lifecycle.py check` OK.
  CI green on every run and every leg — Lifecycle Drift, Dashboard Refresh, and Spawn Drift
  `privacy` (`pytest tests/`); Spawn Drift's `drift` job is `skipped` by its own
  `if: github.event_name != 'pull_request'`, not a failure.
- key traps:
  - **The obvious fix — repoint at the replacement — is not available.** `pyauto-status`
    retired into `$health status`, which is an *agent-driven procedure*
    (`PyAutoHeart/skills/pyauto-status/reference.md`), not a sourceable shell function. There
    is no shell entrypoint for `status.sh` to call, so "repoint" would have meant reinventing
    the dashboard inside the Mind — the wrong organ. Deletion plus a pointer was the only
    honest option.
  - **The failure mode was silent success, not a crash.** `set -uo pipefail` has no `-e`, and
    the branch ended in `exit 0`, so a failed `source` printed two shell errors and still
    returned 0. Anything scripting the flag would have read it as working. The regression test
    asserts the non-zero exit specifically for that reason.
  - Callers were checked before deleting, as the prompt asked: nothing in PyAutoMind,
    PyAutoBrain or PyAutoHeart invokes `status.sh` with any argument. The Brain/Heart files the
    prompt named (`nightly.sh`, `bin/overnight_status.sh`, `tick.sh`, `ci_status.sh`,
    `heart-health.yml`) reference `overnight_status.sh` / `ci_status.sh` — unrelated scripts
    with similar names. `heart/checks/url_check_live.py` has its own `--repos` flag; also
    unrelated.
  - `skills/OWNERSHIP.md` already recorded the retirement and `REFERENCE.md` already pointed
    readers at `/health status`, so no doc offering the flag survived — the script's own usage
    header was the last one.
- environment note: shipped from a `web-github` session (no task worktree, no `gh`; issue and
  PR driven through the GitHub MCP surface). The session clone was shallow, which makes
  `merge-base --is-ancestor` lie across the graft boundary — `git fetch --unshallow` before
  trusting any ancestry check in that environment.

## Original prompt

# status.sh --repos sources a file that no longer exists

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Filed: 2026-08-19 (backfilled from git)
Issued: 2026-08-26

Found by the 2026-08-19 readability-pass census (#248).
@PyAutoMind/scripts/status.sh's `--repos` branch does
`source scripts/pyauto_status.sh`, and that file does not exist in `scripts/`
— `bash scripts/status.sh --repos` fails. `skills/OWNERSHIP.md` records that
`pyauto-status` was retired into the `$health status` leg (PyAutoHeart), so
the branch is probably vestigial.

Decide and fix: either delete the `--repos` branch (and any docs offering it),
or repoint it at the Heart-owned replacement. Check the callers first
(Brain `wake_up.md`, `nightly.sh`, `bin/overnight_status.sh`; Heart `tick.sh`,
`ci_status.sh`, `heart-health.yml`) to confirm none of them pass `--repos`.
