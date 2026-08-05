# PR CI for PyAutoHands's own test suite

Shipped: PyAutoLabs/PyAutoHands#230 (squash-merged as `6d5d608`, 2026-08-05).

PyAutoHands had **28 test modules / ~300 tests and zero PR checks**. None of its
three workflows was triggered by `pull_request`: `python_matrix.yml` is a weekly
cron over the five *libraries'* suites, `navigator_check.yml` is
`workflow_call`-only, and `release.yml`'s `python3 -m pytest` runs inside
`${{ matrix.project.path }}` — a matrix of the five libraries, with PyAutoHands
checked out beside them only as a helper, so `tests/` was never collected. A
Hands PR's only gate was whatever the authoring session happened to run locally.

That matters more here than for a leaf repo: `build_util` and `env_config`
execute every workspace smoke run and every release build, so a regression
surfaces as a mysterious workspace-CI failure three repos away.

Added `.github/workflows/tests.yml` on the shape of the two existing organ
self-test gates (PyAutoBrain `tests.yml`, PyAutoHeart `heart-tests.yml`) —
`push: [main]` + `pull_request`, Python 3.12/3.13/3.14, pytest only,
`cancel-in-progress` restricted to non-`main` refs. PyAutoHands is now the third
organ with a self-test gate; Gut still has none (no workflows at all).

## Findings worth keeping

**The dependency set is not what reading the source suggests.** PyAutoHands has
no `pyproject.toml`, so there is no `.[dev]` extra to install the way
`heart-tests.yml` does, and `pytest` is not in `requirements.txt`. Derived
empirically by starting from `pytest --collect-only` in a clean venv and adding
one package at a time, the real set is `pytest PyYAML ipynb-py-convert Pillow`.
Two traps: `nbformat`/`nbconvert` look required from the imports but are **not**
(tests self-skip on their absence), while **`ipynb-py-convert` is needed as a
CLI binary** `build_util` shells out to — not as an import, so no amount of
reading import statements finds it. Naming packages explicitly beats
`-r requirements.txt`, which drags in `jupyterlab` + `ipykernel` and turns a 6s
gate into a slow one.

**The gate immediately paid for itself.** The suite was not green: 9 failures.
Seven were the missing dependencies. Two were real —
`tests/test_python_matrix_workflow.py` still asserted that Python 3.14 lives in
an isolated `experimental_python_314` job with `continue-on-error: true`, but
`b038fdc` ("promote Python 3.14 to required matrix legs", following the
PyAutoFit#1439 forkserver fix) had deliberately promoted 3.14 into the required
unit + smoke matrices and retired that job, updating `summary.needs` and the
banner text to match — but not the test guarding the contract. It had been
failing unnoticed for five days because nothing ran it. **A deliberate CI-policy
change orphaned its own guard test and nothing reported it** — which is the
argument for the gate, discovered by building the gate.

The workflow was correct and the test stale, so the test was updated to the
promoted shape rather than the workflow reverted (human-confirmed: 3.14 required
is the intent). Worth noting the general shape of that judgment — "never edit a
test to mask a regression" is the right default, and the evidence that overrode
it here was that the commit message stated the promotion as intent, referenced
the upstream fix that unblocked it, and left `python_matrix.yml` internally
consistent (`summary.needs` and banner both updated). Only the test lagged.

**Python 3.14 was declared but never exercised on Hands's own code.** Verified
clean before adding it to the matrix — CI ran real 3.14.6 (301 passed, 4
skipped, ~6s, identical profile to 3.12/3.13). Added
`test_self_test_gate_tracks_the_supported_python_set`, asserting `tests.yml`'s
matrix equals `python_matrix.yml`'s required `unit_tests` matrix, so promoting
or dropping a version has to touch both files. Checked the assertion is not
vacuous — both sides parse to non-empty lists.

**A green tick hid a coverage hole, and CI/local disagreement is how it
surfaced.** CI reported 301 passed / 4 skipped against a local 302 / 3. Same
total, so nothing was missing, but one test that passes locally *skips* in CI:
`test_workspace_config_precedence.test_actual_workspace_files_exist` walks
`repo_root.parent / <workspace>` asserting each of the six workspaces owns its
`config/build/{no_run,profile_smoke,visualise_notebooks}.yaml`, and skips at the
first one absent. In a full local workspace it asserts all six; in CI's bare
checkout it asserts nothing. Left open deliberately — closing it means six extra
checkouts for a repo-layout invariant, coupling a 6s gate to six other repos —
but stated in the workflow header rather than hidden. **Generalisable habit:
compare CI's pass/skip counts against the local baseline rather than accepting
the green.**

## Trap for next time

`lifecycle.py record --prompt` only folds prompts from `active/`. This task
never went through `/create_issue` → `active/` (the work was done in the same
session that filed the prompt), so the draft was folded into this record by hand
and `draft/test/pyautohands/pr_ci_for_own_test_suite.md` removed explicitly.

## Original prompt

# PyAutoHands PRs run zero checks — gate its own test suite on `pull_request`

Type: test
Target: pyautohands
Repos:
- PyAutoHands
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

`@PyAutoHands/tests/` holds **28 unit-test modules** covering the executor's
core logic — `build_util` (script/notebook execution, per-script timeouts,
clean-skip exit codes), `env_config` (profile discovery, per-script env
building, JAX marking, workspace config precedence), `result_collector`,
`check_navigator`, `clone_seed.substitute`, `generate_release_notes` /
`slack_release_notes`, `bump_colab_urls`, `repro_command`, and the
`python_matrix` workflow parser.

**None of it runs in CI.** PyAutoHands has exactly three workflows and not one
of them is triggered by `pull_request`:

| Workflow | Trigger | What it actually tests |
|---|---|---|
| `python_matrix.yml` | `workflow_dispatch` + weekly cron (Mon 03:00 UTC) | the **five libraries'** suites (`test_autonerves`, `test_autoarray`, …) on 3.12/3.13/3.14 — never `tests/` |
| `navigator_check.yml` | `workflow_call` only | reusable catalogue check invoked by the *workspaces* |
| `release.yml` | `workflow_dispatch` (driven by Brain's nightly-release) | the `release_test_pypi` job's `python3 -m pytest` runs inside `${{ matrix.project.path }}`, whose matrix is PyAutoNerves/PyAutoFit/PyAutoArray/PyAutoGalaxy/PyAutoLens. PyAutoHands is checked out beside them as a *helper*, so its own `tests/` are never collected. |

`grep -rn "pull_request" .github/workflows/` returns nothing. So a PyAutoHands
PR carries **zero check runs**, and its only gate is whatever the authoring
session happened to run locally — the same hole PyAutoBrain had before
`tests.yml` and PyAutoHeart had before `heart-tests.yml`.

This matters more here than for a leaf repo: PyAutoHands is the **Hands** —
`build_util` and `env_config` are what execute every workspace smoke run and
every release build. A regression in `timeout_for` or `build_env_for_script`
surfaces as a mysterious workspace-CI failure three repos away.

## What to do

Add `@PyAutoHands/.github/workflows/tests.yml`, mirroring
`@PyAutoBrain/.github/workflows/tests.yml` and
`@PyAutoHeart/.github/workflows/heart-tests.yml` — they are the two
established organ-self-test gates and this should be the third of the same
shape, not a new pattern:

- `on: { push: { branches: [main] }, pull_request: }` — one run per commit.
- `concurrency: { group: hands-tests-${{ github.ref }}, cancel-in-progress: ${{ github.ref != 'refs/heads/main' }} }`.
  **Keep the `!= main` condition**: a cancelled run on `main` reads as red CI,
  because `cancelled` is in Heart's `FAILURE_CONCLUSIONS`.
- Matrix `python-version: ["3.12", "3.13"]`, `fail-fast: false`.
- Run `pytest tests/ -q` from the repo root.

**Deliberately pytest only.** It must not invoke `autohands generate` /
`run_all` / `pre_build`, and must not reach the network or check out a
workspace — those need live sibling checkouts and belong to the release and
scheduled drivers, not to a PR gate. Both sibling workflows carry that
constraint as a header comment; write the equivalent here, naming what this
gate does *not* cover.

### The dependency set is the one real unknown

PyAutoHands has **no `pyproject.toml`** — it runs from its checkout, so there
is no `.[dev]` extra to install the way `heart-tests.yml` does. `pytest` is not
in `requirements.txt` either. The modules under test pull third-party imports
at import time: `yaml` (`env_config`), `nbformat` and
`nbconvert.preprocessors.ExecutePreprocessor` (`build_util`). So the install
step needs roughly `pip install pytest PyYAML nbformat nbconvert` — but derive
the real set empirically rather than trusting that list:

1. Create a clean venv, install nothing but `pytest`, and run
   `pytest tests/ --collect-only`. Add packages one at a time until collection
   succeeds, then until the suite runs.
2. Prefer naming the packages explicitly in the workflow (PyAutoBrain's
   approach: `pip install pytest PyYAML`) over `-r requirements.txt`, which
   drags in `jupyterlab` and `ipykernel` and would make a ~30s gate slow.
3. If a test turns out to need something genuinely heavy, that is a signal the
   test should be isolated or marked — say so rather than bloating the gate.

### Establish the green baseline first

The suite has never been run by CI, so **do not assume it is green**. Run it
locally on 3.12 and 3.13 before writing the workflow. If entries fail:

- A **real** failure (stale API, drifted expectation) → fix it in the same PR
  if it is small and obvious; otherwise split it out and say so.
- Never weaken an assertion or delete a test to reach green. If something is
  genuinely broken in `autohands`, that is a `bug/pyautohands/` prompt, and
  this task lands the gate around whatever is passing plus a filed follow-up.

Report the baseline in the PR: how many tests, how long, on both versions.

## Out of scope

- **Coverage gates / thresholds.** No sibling organ gate enforces one; do not
  introduce the pattern here.
- **Running the ecosystem-facing entrypoints in CI** (`generate`, `run_all`,
  the navigator regeneration). Those are release-path concerns.
- **Adding a `pyproject.toml`** to PyAutoHands. Packaging PyAutoHands is a
  separate decision with its own blast radius; this task installs deps
  explicitly in the workflow and leaves the repo un-packaged.
- **Touching `python_matrix.yml`.** Its weekly library sweep is a different
  job with a different purpose; leave it alone.

## Done when

- A PyAutoHands PR shows a passing `pytest (3.12)` / `pytest (3.13)` check pair.
- `main` pushes build the same workflow (so Heart's `ws_ci` rollup, which reads
  main-HEAD conclusions, has something to read for this repo).
- The workflow header states what the gate deliberately does not run.
