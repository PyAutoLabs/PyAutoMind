Ten repos each carried their own `.github/scripts/run_smoke.py` — the file
PyAutoHeart's reusable `smoke-tests.yml` invokes from inside each workspace, so
one must exist per repo. What was duplicated was not the file's existence but
its **driver loop**: read the allowlist, resolve per-entry env, spawn a
subprocess under the timeout cap, classify PASS/FAIL/TIMEOUT, accumulate, print
the summary, exit non-zero. Seven repos held that loop; the three HowTo repos
were already thin shims.

All ten are now shims. 2085 lines became **890** (3x119 + 4x77 + 3x75), and
most of that is prose: of `autolens_workspace_test`'s 77 lines, 32 are the
docstring explaining why it delegates.

(The figure 1127 appears in this task's commit message, PyAutoMind#283 and the
PyAutoHands#260 close-out comment. It is wrong — a verification loop fell back
to a cached CDN read and counted autolens_workspace at its pre-merge 356.
Confirmed against `origin/main`: that file is 119 lines. 890 is the correct
total.)

## The argument, which was not "they have drifted"

The prompt was filed on a drift finding. Re-measured 2026-08-24 from every
repo's `main`, there was **zero functional drift inside any variant** — the
three workspace copies byte-identical, the four `_test` copies differing in two
docstring lines, the three HowTo copies in `PROJECT` alone.

That is not evidence the design was safe. It is the receipt for three manual
N-repo sweeps that had been paid to restore it: the env-resolver fork (#185),
the per-script timeout and process-group kill (#226/#227), and the jupyter
guard. The HowTo tier needed **none** of the three, precisely because it holds
no logic. The case for collapsing is maintenance cost, not drift.

The prompt's blocking question — "does autolens_workspace_test's timeout/kill
get promoted, or keep a documented divergence?" — was already answered by
promotion in #226/#227. All ten copies imported `timeout_for` and `kill_group`
before this task started; `_kill_group` existed in zero.

## The real obstacle was discovery model, not behaviour

The shared runners were opt-out (recursive discovery minus `no_run.yaml`); the
seven logic-bearing copies are opt-in allowlists (`smoke_tests.txt`,
`smoke_notebooks.txt`). That mismatch is why they could not delegate. So each
phase was a PyAutoHands feature first and per-repo edits second.

## Two bugs found by measuring before writing

**1. The `no_run`-wins rule would have deleted 13 scripts from smoke coverage
(#262).** #261 shipped "an explicit exclusion is the more specific intent, so
`no_run` wins over the allowlist". Measured against the real repos, that rule
would have silently skipped 9 scripts in autogalaxy_workspace_test, 2 in
autolens_workspace_test, 1 in autofit_workspace and 1 in autolens_workspace —
every one of which runs in smoke today, since the vendored runners never opened
`no_run.yaml` at all.

The rule was wrong because it conflated two policies for two different runs:
`no_run.yaml` governs the release mega-run and notebook generation, the
allowlist governs the PR gate, and a script legitimately appears in both. The
failure mode is the dangerous kind — **CI would have stayed green**, because a
skipped script is not a failure. Corrected to allowlist-authoritative before any
workspace was touched, and confirmed in production afterwards: autogalaxy's nine
all ran and passed, as did autolens's two and autofit's `searches/mcmc` in both
its script and notebook forms.

Same PR fixed a second blocker: `autocti_workspace_test` is the only workspace
with no `config/build/no_run.yaml`, and the autohands-level fallback path does
not exist either, so both runners crashed with `FileNotFoundError` before
running anything.

**2. `regenerate_notebook` resolved the source by bare filename (#263).** It
looked up `scripts_dir / nb_path.name`, dropping the subdirectory, so
`notebooks/imaging/model_fit.ipynb` searched for `scripts/model_fit.py`. Every
workspace notebook is in a subdirectory, so the stale-notebook recovery was dead
on arrival — and a bare filename can find the *wrong* source when two topics
share a name. The existing tests missed it because their fixture was **flat**,
which is the one layout where the bug is invisible. The replacement tests use a
nested notebook plus a decoy script at the scripts root, and were negative-tested
against the old resolution.

## What was proven rather than assumed

- **Env resolution is identical.** The old runners passed a *relative* script
  path to `build_env_for_script`; the shared runners pass an *absolute* one. All
  128 listed scripts across all seven repos were resolved both ways and diffed:
  0 differences, in env and in args. Pattern matching is substring/stem based so
  path form is irrelevant, and no profile pattern collides with the absolute
  prefix.
- No profile sets per-script `args`, so the shared runners' extra-args support
  changes nothing.
- Every allowlist entry resolves to a real file, and every listed notebook's
  source script exists for the retry path.
- The two-leg exit code is the worst of both, verified in all three
  pass/fail combinations — a failing notebook cannot be masked by passing
  scripts.
- **Every merge was verified from the CI log, not the green tick**, because a
  coverage regression here is indistinguishable from a pass. Each repo's
  "Running N listed scripts/notebooks" was checked against its allowlist:
  11/11, 22/22, 35/35, 3/3, 8/8+2/2, 14/14+2/2, 35/35+2/2.

## Traps for anyone touching this again

- `--report-dir` is load-bearing. `run_python.py` only propagates failure when a
  report was built; without it the gate runs to completion and always exits 0.
- `run_notebook.py` writes executed outputs back **in place**. Correct for
  generation, where the outputs are the product; wrong for a PR gate, which must
  not dirty the tree it tests. Hence `--no-write-back`.
- `JUPYTER_MISSING_RC` did **not** need promoting. It existed because the
  workspace copies shelled out to a bare `jupyter`; the shared runner invokes
  `sys.executable run_notebook.py`, so the abort-with-no-summary mode is
  structurally absent. One planned promotion item dissolved on inspection.
- A bare `off`/`on`/`yes` entry in `no_run.yaml` parses as a YAML **boolean** and
  crashes `should_skip` with `TypeError: argument of type 'bool' is not
  iterable`. Hit while building a fixture; not fixed, no repo currently has such
  a script name.

## Still open

The merged `claude/smoke-copy-drift-ci-docs-ozntvv` branches across nine repos
were not deleted — this session's git proxy refuses delete refspecs
(`send-pack: unexpected disconnect`). They are all proven merged into `main`.

## Mind-side note: a stale draft copy survived this record (removed 2026-08-27)

The prompt was issued from a copy, not moved: `draft/maintenance/ci/run_smoke_copy_drift.md`
stayed behind when the task went to `active/` and then into this record. It was a
strict prefix of the folded copy below — identical through the re-scoped task
list, missing only the `Issued:`/`Filed:` headers and the 2026-08-24
re-measurement — so it kept rendering on the dashboard as pickable backlog for
work that had already shipped. Nothing detects this: `lifecycle.py check` reports
OK, because a `draft/` prompt with no registry entry is a valid state.

Removed under `/prm`'s reconcile leg on 2026-08-27, after verifying the merged
end state rather than trusting this record:

- `autolens_workspace` and `autogalaxy_workspace` `.github/scripts/run_smoke.py`
  are both 119-line shims on `origin/main`, and `_BUILD_DIR` — the vestigial line
  the prompt's step 4 asked about — is gone, that step being moot once the
  variant was replaced wholesale.
- The acceptance criterion that consolidation must not cost
  `autolens_workspace_test` its per-script timeout holds through the shared path:
  `build_util.execute_scripts_in_folder` → `execute_script` → `timeout_for(env)`
  with `run_capped(timeout=…)` and `TimeoutExpired` handling, so every delegating
  repo enforces the cap the one repo used to carry alone.

## Original prompt

# run_smoke.py: three runner variants across 10 repos, no sync mechanism

Type: maintenance
Target: ci
Repos:
- @PyAutoHands
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: issued
Filed: 2026-07-25 (backfilled from git)
Issued: 2026-08-24

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

---

## Re-measurement + decision (2026-08-24)

Re-measured from every repo's `main` before planning. **The 2026-08-05
correction is itself now stale**: its blocking question has been answered
in-tree, and the drift it measured is gone.

| Variant | Repos | Lines | Intra-variant drift, measured |
|---|---|---|---|
| **workspace** | autofit_workspace, autogalaxy_workspace, autolens_workspace | 356 | **none** — byte-identical |
| **workspace_test** | autofit/autogalaxy/autolens/autocti `_test` | 198 | **comment-only** (2 docstring lines); autogalaxy ≡ autolens byte-identical |
| **HowTo** | HowToLens, HowToGalaxy, HowToFit | 75 | **one constant** (`PROJECT =`) |

Ten copies, three variants, zero functional divergence inside any variant.
Every blocker the earlier correction named is closed:

- **The timeout/kill divergence was resolved by promotion, not documentation.**
  `timeout_for` and `kill_group` now live in PyAutoHands
  `autohands/build_util.py` (#226/#227 → `52408a84`); all **ten** copies read
  `BUILD_SCRIPT_TIMEOUT` and import both with guarded local fallbacks. The
  sweep branch `claude/backport-per-script-timeout-r3w1sv` is still present on
  every affected repo. `_kill_group` exists in zero copies. Task step 2's
  "answer this before writing any code" is therefore **already answered**:
  promoted to everyone.
- **Step 1 (skip-guard)** verified: `is_clean_skip_exit` appears in exactly the
  three notebook-capable copies and nowhere else — correct, since the other
  seven never shell out to `jupyter`.
- **Step 4 (`_BUILD_DIR`)** is done — autogalaxy_workspace is byte-identical to
  its two siblings.

### The decision (task step 2, per variant)

**Full delegation to a PyAutoHands-owned runner, staged.** The HowTo tier is the
target shape and already exists in-tree.

The zero-drift measured above is not evidence the copy-per-repo design is safe —
it is the *receipt* for three manual N-repo sweeps that were needed to restore
it (env-resolver fork PyAutoHands#185, per-script timeout #226/#227, the
jupyter-guard fix). The HowTo tier needed **none** of those three sweeps,
precisely because it holds no logic: `PROJECT` plus a `subprocess.run` into
`autohands/run_python.py`. That is the argument for consolidating, and it is a
maintenance-cost argument, not a drift argument.

The real blocker is **discovery model, not behaviour**: `run_python.py` is
opt-out (recursive discovery minus `config/build/no_run.yaml`) and has no
notebook leg, while both other variants are opt-in allowlists
(`smoke_tests.txt`, `smoke_notebooks.txt`). Consolidation is therefore a
PyAutoHands feature first and per-repo edits second.

**Phase 1 — `workspace_test` (4 repos, 198 → ~75 lines).**
Add an allowlist mode to `autohands/run_python.py` (`--list <file>`, taking
precedence over recursive discovery; `no_run.yaml` still applies). Then replace
each `_test` copy with a HowToLens-shaped delegator. Nothing is promoted that
isn't already in `build_util` — `run_one` is `execute_script` plus
`timeout_for`/`kill_group`, all three already there.

**Phase 2 — `workspace` (3 repos, 356 → ~75 lines).**
Promote the notebook leg into PyAutoHands: the regenerate-from-source-and-retry
recovery, the `JUPYTER_MISSING_RC = 127` non-abort path, and the ordering
invariant that a missing `jupyter` and a `TIMEOUT_RC` are both checked *before*
`is_clean_skip_exit`. `build_util.execute_notebook` already carries the
skip-guard and `execute_notebooks_in_folder` already exists, so this is a
notebook-allowlist CLI leg plus the recovery, not a rewrite. Then collapse the
three workspace copies.

**Phase 3 — HowTo (3 repos).** No work. Already the end state; the audit
confirms it.

### Also surfaced

`PyAutoHands/docs/internals.md:183` is stale on its own inventory: it says
"nine copies, five distinct revisions — they have drifted", omits HowToFit
(which gained a copy with the opt-out HowTo smoke rollout), and the drift claim
is now false. Correct it as part of Phase 1.

### Acceptance (restated against the decision)

- The timeout/kill decision is written down above: **promoted**, with the
  in-tree evidence. No repo keeps a documented divergence on that axis.
- After Phase 2, every one of the ten copies is a thin wrapper over a
  PyAutoHands-owned module; the only per-repo content is `PROJECT` and the
  allowlist paths.
- No repo loses behaviour: the per-script timeout, the process-group kill, the
  `124` timeout exit code, the notebook regenerate-and-retry recovery, and the
  jupyter-missing non-abort path all survive as `build_util`/CLI behaviour and
  are asserted by PyAutoHands' own test suite before any workspace is collapsed.
