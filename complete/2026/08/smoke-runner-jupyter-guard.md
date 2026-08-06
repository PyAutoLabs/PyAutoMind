The workspace smoke runners' notebook leg aborted the whole run when `jupyter`
was missing. `.github/scripts/run_smoke.py::execute_notebook` shelled out to a
bare `jupyter` argv with no `FileNotFoundError` guard, so the exception escaped
`main()`: raw traceback at the **first** notebook entry, no
`=== Smoke test summary ===` line, every remaining entry silently uncovered.
The script leg was never affected — it invokes `sys.executable`, which always
exists.

The framing that made this worth fixing properly: it is a **contract break**,
not a missing optional tool. The runner is documented in two places (its own
module docstring, each workspace's `AGENTS.md`) to continue through failures and
always end with the summary line. CI never saw it because the runner images
always ship jupyter, so it only bit a local sweep — where it looked like a crash
and quietly discarded coverage.

## PRs

- autolens_workspace#471 → `ac8da5e0` (issue autolens_workspace#470 closed)
- autofit_workspace#133 → `eef1d887`
- autogalaxy_workspace#206 → `fc47cbc2`
- PyAutoMind#139 (Mind state: route + the copy-drift re-scope below)

All four on branch `claude/smoke-runner-jupyter-guard-3sxcc0`. All checks green
before merge (smoke 3.12 + 3.13 and navigator ×3 on each workspace; drift on
Mind).

## The fix

`JUPYTER_MISSING_RC = 127` + a message constant; `try/except FileNotFoundError`
around the `subprocess.run`, **nested inside the existing `try/finally`** so the
staged notebook copy and temp dir are still cleaned up; `run_notebook` returns
early on that rc.

Two ordering decisions that are the whole point of the fix and should not be
"simplified" later:

1. The early return sits **before** the `is_clean_skip_exit` branch. That helper
   matches on `CellExecutionError` so it could not currently launder a missing
   tool into a PASS — but the ordering makes that structural rather than
   incidental.
2. It **skips the regenerate-and-retry**. Regenerating a notebook cannot help
   when the executor itself is absent; without this the run just emits the
   message twice.

## Scope decision (the prompt demanded one explicitly)

**Fixed the three copies; deliberately did not consolidate.** `run_smoke.py`
exists in **10** workspace repos, but only autofit_workspace,
autogalaxy_workspace and autolens_workspace carry the notebook leg
(`grep -c '"jupyter",'` → 1; 0 for the other seven, which have no
`execute_notebook` and so cannot hit this bug). Consolidation is owned by
`draft/maintenance/ci/run_smoke_copy_drift.md`; folding it in would break
*one prompt = one task = one PR* and couple a correctness fix to a cross-repo
refactor.

Drift did not widen: autofit_workspace and autolens_workspace were byte-identical
before and remain so (identical patch). autogalaxy_workspace's **entire**
divergence is an unused `_BUILD_DIR` intermediate variable (2 lines, unrelated
to this code path), left alone rather than quietly de-drifted inside a bug fix.

## Verification

jupyter was genuinely absent in the cloud container, so the bug was reproduced
before anything was touched (`FileNotFoundError: [Errno 2] No such file or
directory: 'jupyter'` out of `subprocess.run` at `run_smoke.py:116`, second
notebook entry never reached). Then the real runner in each repo:

| repo | exit | notebook entries | entries counted | summary line | escaped traceback |
|---|---|---|---|---|---|
| autofit_workspace | 1 | `[FAIL (exit 127)]` ×2 | 10/10 | yes | 0 |
| autogalaxy_workspace | 1 | `[FAIL (exit 127)]` ×2 | 15/15 | yes | 0 |
| autolens_workspace | 1 | `[FAIL (exit 127)]` ×2 | 37/37 | yes | 0 |

Normal path proven untouched with a stub `jupyter` on `PATH` exiting 3 — the
runner reported 3, not 127, and still took the regenerate-and-retry path.

**Do not oversell that table:** the PyAuto libraries are not installed in that
container, so every *script* entry also failed on `ImportError`. Unrelated to
the change — and the ideal evidence, since it exercises the
continue-through-failures path the fix defends. It is **not** evidence the
scripts are broken. Green CI (which has the libraries) is the complementary
half: it proves the notebook leg still executes normally with the guard in
place.

## Findings worth keeping

- **Why this survived.** `regenerate_notebook` shells out to `ipynb-py-convert`
  and raises the same `FileNotFoundError`, but its caller already wraps it in
  `except Exception`. Guarded retry, unguarded primary — the asymmetry is
  exactly why nobody noticed.
- **`draft/maintenance/ci/run_smoke_copy_drift.md` was re-scoped in the same
  session**, because measuring the copies showed both its headline claims were
  wrong. Its step 1 ("roll the 2-line skip-guard adoption across the 9 copies")
  is already done where meaningful and meaningless elsewhere; and "9 copies in
  5 revisions" conflates **three structurally different programs** — the
  ~266-line workspace runner (scripts + notebooks), the 113-line
  `workspace_test` script runner, and the 75-line HowTo delegator (10 copies,
  not 9). Two consequences were written into that prompt:
  - `autolens_workspace_test` carries `TIMEOUT_SECS` / `_kill_group` that no
    other copy has. That is a **capability**, so a naive byte-identical
    consolidation would delete behaviour — the re-scoped task now requires that
    call be made and written down *before* any code is written.
  - The HowTo tier is already a thin PyAutoHands delegator, i.e. the end-state
    that prompt proposes exists in-tree as a precedent to copy.
- **Prompt provenance trap.** The originating draft
  (`draft/bug/workspaces/bug_in_the_workspace_smoke_runners_the.md`) lives on the
  **unmerged** branch `claude/health-agent-full-run-myysos`, not on `main`, so it
  was copied into `active/` rather than `git mv`-ed across branches. That draft
  is now stale — whoever merges that branch should drop it rather than re-filing.

## Environment

Cloud session, no worktree and no `gh` CLI: worked in the canonical
`/home/user/<repo>` checkouts on the mandated branch; issue and PRs via the
GitHub MCP surface.

## Original prompt

# Bug in the workspace smoke runners: the notebook leg aborts

Type: bug
Target: workspaces
Repos:
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- workspaces
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Bug in the workspace smoke runners: the notebook leg aborts the whole run when jupyter is missing. In autofit_workspace, autogalaxy_workspace and autolens_workspace, .github/scripts/run_smoke.py execute_notebook calls subprocess.run with a bare 'jupyter' argv and no FileNotFoundError guard, so on a machine without jupyter the exception escapes main(): the run dies with a raw traceback, prints no === Smoke test summary === line, and every remaining entry is silently uncovered. The script leg is unaffected because it invokes sys.executable, which always exists. CI never sees this because the runner images always have jupyter, so the gap only bites a local developer sweep — where it looks like a crash rather than a missing optional tool, and quietly discards coverage. Observed on 2026-08-05 running the runner locally in all three workspaces. Fix by catching FileNotFoundError in execute_notebook and returning a clear per-entry failure or skip, so the runner keeps its documented contract of continuing through failures and always ending with the summary line. The same file is duplicated across nine repos but only these three run the notebook leg.

<!-- formalised by the Intake (Conception) Agent on 2026-08-05 from user-intake -->
