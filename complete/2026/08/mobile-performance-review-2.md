- completed: 2026-08-26
- issue: none — like the review it follows, this began as an environment review
  in a mobile session rather than a filed prompt, so it carries no `active/`
  entry to fold. Recorded because the work shipped.
- prs:
  - https://github.com/PyAutoLabs/PyAutoMind/pull/342 (merged, `4998a95c`)
  - https://github.com/PyAutoLabs/PyAutoBrain/pull/295 (merged, `ff553c08`)
- classification-note: two repos. No gate order — `firewall_gate.yml` is
  path-filtered to `scripts/repos_sync.py`, which neither PR touches, so the
  Brain-before-Mind order the previous review needed did not apply. Merged
  Mind first to keep source ahead of its generated copy.
- classification: bug (organism infrastructure; Mind + Brain)
- summary: |
    A second pass over `complete/2026/08/mobile-performance-review.md`. Python
    3.12 is now the session default — that review's fix held — but three
    defects underneath it were still live, and **both mitigations it shipped
    had holes**. The headline: the SessionStart hook has still never fired in a
    multi-repo session, and the fan-out written to fix that had never been
    installed by anyone, because writing it required the hook to already be
    running.

## What was still true

1. **The hook never fires in a multi-repo session** — proved, not inferred.
   `~/.claude/session-env/<session-id>/` holds an env file per session that ran
   the hook. Two earlier single-repo sessions in this container each have one;
   the multi-repo session's directory is **empty**. Corroborated by both clones
   still being shallow three minutes in, until an unrelated verb happened to
   call `session_bootstrap.sh`.

   The workspace-root fan-out was **unreachable by construction**. Writing it
   requires the hook to be running; the hook only runs where Claude Code
   registers it — a session whose project dir *is* a repo, i.e. a single-repo
   one; and `install_workspace_settings` returned early in exactly that case as
   "nothing to add". The one session type that could seed the container never
   did, and the session that needed the seed never ran the hook to write it.
   It now installs from any session, targeting `$WORKSPACE_ROOT` derived from
   the checkout, skipping only a root that is itself a repo or is not writable.

2. **Both natural test commands failed, and neither looked environmental.**
   With no env file there is no PATH export, so shells resolved
   `/usr/local/bin/python3` (no pytest) and uv's *isolated* `pytest` (no
   PyYAML). The second is the dangerous one: four collection `ImportError`s
   naming `yaml`, in a workspace whose suite was green — it reads as broken
   source.

   | Command | Before | After |
   |---|---|---|
   | `python3 -m pytest` | `No module named pytest` | 232 passed |
   | `pytest` | 4 collection `ImportError`s | 223 passed |

   `point_system_default` was being handed `readlink -f "$VENV/bin/python"` —
   resolving the venv straight through to the base interpreter, satisfying the
   version question and losing everything else.

3. **Tests ran on one of four cores.** No single slow test — 554
   subprocess-heavy ones, the top fifteen summing to ~27s of 96s.
   `pytest-xdist` joins `BASE_DEPS`: PyAutoBrain 96s → 28s, PyAutoMind 10s →
   3.7s, all passing either way.

4. **`--check` reported `pytest: 3.12 OK` for the unusable pytest.** It asked
   the version — necessary, not sufficient — and so answered a question it had
   not asked, the same class the previous review fixed elsewhere. It now also
   asks whether the interpreter can import what the suite needs.

## Key traps

- **The fix did the disease, and destroyed the container's interpreter.** The
  wrapper was first written with `cat >"$dest"`. `/usr/local/bin/python3` is a
  *symlink*, and a redirect opens the link's **target** — so it overwrote
  `/usr/bin/python3.12` itself with the wrapper. The venv's own python symlinks
  to that same file, so the wrapper then exec'd itself: every `python3` in the
  container spun at 100% CPU and the interpreter was gone. Recovered with
  `uv python install 3.12`. The fix is `rm -f` before writing, plus a chain
  walk (`links_through`) refusing a target that reaches the destination by the
  other route. Both guards were confirmed to FAIL with the fix removed.

- **A symlink cannot be the wrapper.** The first attempt at pointing the system
  default at the venv was `ln -s`. CPython resolves a symlinked executable
  *before* looking for `pyvenv.cfg`, so it lands on the base interpreter's
  prefix — the venv is lost again, silently, in the same shape as the bug being
  fixed. Only an `exec` wrapper keeps it. Pinned by a test asserting the
  destination is **not** a symlink.

- **The endpoint comparison was too aggressive.** The first loop guard compared
  `readlink -f` of target and destination — but a venv's python legitimately
  *resolves* to the same base interpreter a system default points at, so it
  refused every safe rewrite. The question that matters is narrower: is the
  path being rewritten a *link in the target's own chain*.

- **`--system-site-packages` is what makes the swap safe.** Pointing `python3`
  at an isolated venv would trade one set of missing modules for another. The
  venv is now a strict superset of the base interpreter, verified both ways.

## Validation

232 PyAutoMind tests and 554 PyAutoBrain tests, `ruff`, `lifecycle.py check`
and `repos_sync.py --check` all clean. 8 new tests across the hook's new legs;
every guard was confirmed to FAIL against the pre-fix behaviour before being
trusted. Heart was unreachable (PyAutoHeart not checked out and `add_repo`
blocked), so `ship_library.md` step 3's documented fallback stood in: per-repo
`pytest -x`, any failure treated as RED.

CI: PyAutoMind's only PR check on this diff is `spawn_drift.yml` (no path
filter; the other three are correctly filtered out) — its `privacy` job runs
`pytest tests/ -q` over the whole directory, so the new tests were covered.
PyAutoBrain ran `tests.yml` green on both 3.12 and 3.13 legs.

## Follow-up

**PyAutoHeart and PyAutoHands carry stale generated copies of the hook.**
`repos_sync.py --write` regenerated two of four because only two repos were
attached, and `add_repo` for the other two was refused by the session's
permission classifier. Not gated by either PR's CI (`firewall_gate.yml` is
path-filtered to `scripts/repos_sync.py`), so this is silent drift until
someone runs `--check` in a full workspace. The previous review logged the same
lesson: **a drift check over N repos is only as strong as the number of them
your session can see.** Twice now, so the constraint is the session shape, not
an oversight.

`draft/feature/pyautobrain/board_without_gh.md` is unaffected — its premise
still holds. Its `(verify)` row on the GitHub token was re-checked this session:
`$GH_TOKEN` is set and a direct REST call still returns "GitHub access is not
enabled for this session".
