# run_smoke.py: three runner variants across 10 repos, no sync mechanism

Type: maintenance
Target: ci
Repos:
- @PyAutoHands
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

> **Re-scoped 2026-08-05.** The original finding below is preserved for history
> but its two headline claims are now measured to be wrong: step 1 is already
> done, and "9 copies in 5 revisions" conflates three structurally different
> programs. Read the correction block first — it is the current statement of
> the task.

## Original finding (2026-07-25, during the notebook skip-guard fix)

Every workspace's PR smoke gate runs its own copy of
`.github/scripts/run_smoke.py`. There are **9 copies across the workspace
repos in 5 distinct revisions** — they have already drifted:
autofit_workspace + autolens_workspace share one revision; HowToLens +
HowToGalaxy + autofit_workspace_test share another; autogalaxy_workspace,
autogalaxy_workspace_test, autolens_workspace_test and autocti_workspace_test
are each unique. PyAutoHeart's reusable smoke-tests.yml deliberately leaves
the runner in the workspace, but nothing keeps the copies aligned.

Immediate consequence: PyAutoHands#198 taught the authoritative executor
(`autohands/build_util.py::execute_notebook`) to treat a clean `SystemExit: 0`
notebook exit as a PASS (the optional-dep skip-guard idiom), but the 9 smoke
copies still carry their own `execute_notebook` and keep reporting the
spurious FAIL until each adopts it. Adoption is ~2 lines per repo (they
already import `env_config` and `build_util.py_to_notebook` from PyAutoHands);
the exact snippet + full copy inventory is documented in
PyAutoHands `docs/internals.md`.

## Correction (2026-08-05, measured during the jupyter-guard fix)

Measured across the checkouts, not inferred. There are **10** copies, not 9,
and they are **three different programs**, not five revisions of one:

| Variant | Repos | Lines | Notebook leg | `is_clean_skip_exit` |
|---|---|---|---|---|
| **workspace** | autofit_workspace, autogalaxy_workspace, autolens_workspace | ~266 | yes | **already adopted** |
| **workspace_test** | autofit_workspace_test, autogalaxy_workspace_test, autocti_workspace_test | 113 | no | n/a |
| **workspace_test + timeout** | autolens_workspace_test | 193 | no | n/a |
| **HowTo** | HowToLens, HowToGalaxy, HowToFit | 75 | no | n/a |

Consequences for the original task, in order of how much they change it:

1. **Step 1 is done, and was never applicable beyond three repos.** The
   skip-guard is adopted in all three notebook-capable copies. The other seven
   have no `execute_notebook` at all — they never shell out to `jupyter`, so
   there is no spurious FAIL for them to fix. The acceptance criterion "a
   notebook exiting via the skip-guard passes every workspace's PR smoke gate"
   is already met, because only three gates run notebooks.
2. **The variants differ by feature, not only by drift.** `workspace_test`
   exposes `load_smoke_scripts`/`run_one` and no notebook machinery;
   `autolens_workspace_test` additionally carries `TIMEOUT_SECS`
   (`BUILD_SCRIPT_TIMEOUT`) and a `_kill_group` process-group kill that no
   other copy has. That is a capability, not staleness — a naive
   "make them byte-identical" would delete it.
3. **The HowTo tier is already the proposed end-state.** Those three are
   75-line delegators (`PROJECT = "howtolens"`, straight into PyAutoHands
   `build_util`) — the thin-wrapper design step 2 asks whether to build
   already exists in-tree as a working precedent to copy.
4. Real remaining drift inside the workspace variant is now **two lines**:
   autofit_workspace and autolens_workspace are byte-identical; autogalaxy's
   only divergence is an unused `_BUILD_DIR` intermediate variable. The
   jupyter-guard fix (autolens_workspace#470) landed the identical patch in all
   three, so it did not widen this.

## Task (re-scoped)

1. ~~Roll the 2-line skip-guard adoption across the copies.~~ **Done** — verify
   and close out, do not redo.
2. Decide the shared-module question **per variant**, not globally, using the
   HowTo delegator as the reference shape:
   - Is one PyAutoHands-owned runner with per-repo config the right target, or
     two (notebook-capable and script-only)?
   - Does `autolens_workspace_test`'s timeout/kill behaviour get promoted to
     everyone, or does that repo keep a documented divergence? **Answer this
     before writing any code** — it is the only place consolidation destroys
     behaviour.
3. Implement whichever shape is chosen, one PR per repo.
4. Drop the vestigial `_BUILD_DIR` line in autogalaxy_workspace if the
   workspace variant is not being replaced wholesale.

## Acceptance

- A stated, written decision on the timeout/kill divergence — promoted or
  documented-as-intentional — before any repo is touched.
- Each variant is either a thin wrapper over a PyAutoHands-owned module, or
  carries a documented reason why it diverges.
- No repo loses behaviour it has today; `autolens_workspace_test` still
  enforces its per-script timeout.
