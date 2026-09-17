## colab-gate-candidate-audit
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/229 (closed completed 2026-09-17)
- completed: 2026-09-17
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/230 (head `4f7e04e`, merge `08c74aa`)
- classification: bug (organ) — PyAutoHeart only, no PyAutoNerves change. Fable session (architect) on web-github; implementation delegated to an Opus subagent, reviewed and shipped in-session; /prm run on the mcp surface.
- ci: Heart Tests run 35226926677 on `4f7e04e`, pytest 3.12 + 3.13 both success (the only PR-triggered workflow; push fires on main only). Full suite locally 1026 passed. Merged by `/prm`, mergeable_state clean.
- witness: NOT run — the red-first witness needs a desktop with python3.12 and TestPyPI reach (`bash heart/checks/verify_install.sh F --testpypi --version 2026.9.17.1.dev77201 --report-json /tmp/vi.json`); expected: released facet F WARN (6 missing), candidate facet `autonerves=2026.9.17.1.dev77201`, F PASS, `ready: true`; negative control without `--version` unchanged. The next nightly rehearsal is the live witness.

## What shipped

Heart was RED on `install verification FAILED (testpypi; checks F)` and `release
validation FAILED (stage integrate)` with one cause: in a TestPyPI rehearsal
(`TARGET_VERSION` set) check F's seed step pinned the venv to the candidate, but
the verbatim injected setup cell ran `pip install autonerves --no-deps` UNPINNED
and the released `setup_colab.setup()` reinstalled the whole stack unpinned, so
the Colab gate audited the RELEASED bootstrap (autonerves 2026.9.15.1) and never
the candidate. The bootstrap fix (PyAutoNerves #168/#169) was on main but
untagged: Heart RED -> nightly never publishes -> PyPI stays broken -> Heart RED.

Decision 2026-09-17 (human): do not release; fix the gate so no authorisation is
needed. In a rehearsal check F gates on the CANDIDATE (FAIL -> RED as before) and
reports the released bootstrap as a WARN row that is verdict-neutral — the
nightly publishes only on GREEN, so YELLOW would still have blocked the release
that is the remedy.

- `heart/checks/verify_install.sh` check F, `--version` only: released facet
  (`colab_gate.py verify` into `F_gate_verify_released_*.json`, advisory, never
  FAILs), then `/tmp/F_driver_repin.py` re-pins `autonerves autofit autoarray
  autogalaxy autolens ==VERSION` from `PIP_INDEX_ARGS` `--no-deps`, applies the
  `COLAB_GATE_AUTONERVES_SRC` overlay if set, `importlib.reload`s
  `autonerves.setup_colab` and reinstalls `_PROJECTS["autolens"]["packages"]`
  `--no-deps` exactly as `_colab_setup` does (no second `setup()`), then the
  candidate facet with today's FAIL semantics. Candidate pass + released fail ->
  `F|WARN|released Colab bootstrap (autonerves=<ver>) broken for readers:
  <detail>; candidate <version> passes` before the notebook cell and `F|PASS`.
  Continuous run (no `--version`): one audit, unchanged. `n_warn` counted;
  `n_fail` counts only FAIL so `ready` stays true on WARN. Sidecar folds the
  released report in as `colab_gate.verify_released` beside `seed`/`verify`;
  the `{check,status,detail}` shape untouched (validate.py folds only `ready`).
- `heart/readiness.py`: comment only — WARN is verdict-neutral by the
  2026-09-17 decision.
- `heart/dashboard.py`: `ready` true + any WARN row -> section WARN, `passed
  with warnings (<index>; <letters>)`, WARN details as detail lines.
- Docs: script header + usage (`Check F in a rehearsal (--version)` block),
  `skills/verify_install/verify_install.md`, `docs/release_validation.md`,
  `health_agent/capabilities.yaml`. `colab_gate.py` untouched.
- Tests: script text (re-pin driver, both facets, continuous single audit,
  `n_warn`), the lifted sidecar writer (WARN+PASS rows -> `ready` true,
  `verify_released` nested on every F row, readiness not red/yellow), readiness
  (WARN verdict-neutral; FAIL beside WARN still red), dashboard (WARN renders
  WARN with detail; FAIL still FAIL).

## Traps / findings

- An unpinned `pip install autonerves` can never pick a `.devN` pre-release,
  so switching the index alone cannot make the verbatim cell install the
  candidate; an explicit `==` pin (or `--pre`) after the cell is the only
  Heart-side fix. The cell must stay verbatim — it is the thing readers run.
- `colab_gate.py verify` "heals" by installing Colab's own pins for packages
  Colab ships; running it twice in one venv is safe for the gate because a
  Colab-shipped package is never a FAIL, so the advisory pass cannot mask a
  candidate miss.
- After the re-pin, the candidate's own `_colab_setup` package list is
  installed unpinned `--no-deps`; the already-installed dev versions satisfy
  the bare `autolens` etc. requirements, so pip leaves them alone and only the
  `_SHARED_EXTRAS` land.
- The only PR-triggered workflow in PyAutoHeart is `heart-tests.yml` (push on
  main only), so one `pull_request` run with two legs is the whole CI picture
  for a Heart feature PR.
- `/prm` on the mcp surface: the shallow single-branch clone had no
  `origin/feature/...` tracking ref after the push, which made a stop hook
  report an unpushed commit that was already on origin; `git config --add
  remote.origin.fetch` for the branch fixed the ref.

## Original prompt

# Check F audits the released Colab bootstrap in a TestPyPI rehearsal, not the candidate

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoNerves
Difficulty: moderate
Autonomy: supervised
Priority: high
Status: formalised
Consequence: block
Witness: with `TARGET_VERSION` set, the check F driver's `colab_gate verify` line reports `installed PyAuto stack - autonerves=<TARGET_VERSION>, autofit=<TARGET_VERSION>, autoarray=<TARGET_VERSION>, autogalaxy=<TARGET_VERSION>, autolens=<TARGET_VERSION>`, asserted by a test that reads the gate's verify report JSON rather than a log grep; the negative control is that with no `TARGET_VERSION` (the continuous PyPI-index tick) the audited stack is still the latest released one, unchanged. Red first: today's rehearsal log shows `autonerves=2026.9.15.1` with `TARGET_VERSION=2026.9.17.1.dev77201`.
Review-minutes: 30
Unattended: ready
Filed: 2026-09-17
Issued: 2026-09-17

## Finding

PyAutoHeart is RED with two reasons that share one root cause, `install
verification FAILED (testpypi; checks F)` and `release validation FAILED (stage
integrate)`. In run 35195111347 all 707 workspace scripts passed and only check
F, the Colab gate, failed.

In a TestPyPI rehearsal (`TARGET_VERSION` set, here `2026.9.17.1.dev77201`) the
seed step does the right thing. `verify_install.sh` line 775 onwards builds
`f_targets` pinning all five PyAuto packages to the candidate version, with a
comment explaining exactly why an unpinned resolve would produce an incoherent
dev/released mix.

The driver then undoes it. `/tmp/F_driver_setup.py`, written at
`verify_install.sh` line 824 as "the injected setup cell, verbatim", runs

    pip install autonerves --no-deps

with no version pin (line 832), which resolves to the latest final release on
PyPI, `autonerves-2026.9.15.1`. That released `autonerves.setup_colab.setup()`
(line 859) then runs its own unpinned `pip install autolens autogalaxy autofit
autoarray autonerves ... --no-deps` (`setup_colab.py` line 309), and the whole
candidate stack is downgraded underneath the gate:

    Successfully installed anesthetic-2.8.14 autoarray-2026.9.15.1 autofit-2026.9.15.1 autogalaxy-2026.9.15.1 autolens-2026.9.15.1 ... nautilus-sampler-1.0.4
    colab_gate verify: installed PyAuto stack - autonerves=2026.9.15.1 ...

So the rehearsal gate audits the RELEASED bootstrap, never the candidate.

## Why it is failing right now

Released autonerves 2026.9.15.1 (tag at 5130298) predates PyAutoNerves #168
(5b3636d, corner/optax/xxhash/blackjax) and #169 (8eca4b3, jax_zero_contour,
zeus-mcmc), both merged to main on 2026-09-15. Check F therefore fails on
blackjax (`autofit/non_linear/search/mcmc/blackjax/nuts/search.py:260`), corner
(`autofit/non_linear/plot/samples_plotters.py:95`), jax_zero_contour
(`autogalaxy/operate/lens_calc.py:1452`) and three more (optax, xxhash, zeus).
PyPI autonerves is still 2026.9.15.1 as of 2026-09-17.

## Consequence

Chicken and egg. The nightly rehearsals on 2026-09-16 and 2026-09-17
(PyAutoHands runs 35068075515 and 35193720454) were rehearsal-only with the
`release` job skipped because Heart is RED. Heart is RED because the bootstrap
fix is unreleased. The rehearsal gate cannot observe the fix even when the
candidate carries it. Any future bootstrap regression will pin Heart RED the
same way until a human overrides the gate, which is exactly the outcome the
gate exists to avoid.

## Design intent

Keep the two modes distinct. The continuous PyPI-index tick (no
`TARGET_VERSION`) SHOULD keep auditing what a reader gets today, the released
bootstrap. That verdict is truthful and must not change. The release-integrate
rehearsal (`TARGET_VERSION` set) must instead audit the CANDIDATE: after the
verbatim setup cell has run, re-pin autonerves and autofit, autoarray,
autogalaxy, autolens to `==$TARGET_VERSION` from the rehearsal index
(`PIP_INDEX_ARGS`) with `--no-deps`, reload `autonerves.setup_colab`, and re-run
its package install so that the `_SHARED_EXTRAS` of the candidate is what gets
audited.

Note that an unpinned `pip install autonerves` can never pick a `.devN`
pre-release, so switching the index alone is not enough; an explicit `==` pin
(or `--pre`) is required.

## Fix options (implementer's choice, both named)

1. A small PyAutoNerves seam: an environment variable honoured by
   `setup_colab.setup()` supplying index arguments and a version pin, so the
   bootstrap installs the candidate when a rehearsal asks it to. Cleaner, but
   the seam itself only takes effect once released.
2. Heart-only: generalise the existing `COLAB_GATE_AUTONERVES_SRC` overlay
   (`verify_install.sh` lines 729 and 842, currently dev/witness only and
   documented "Never set in CI", and currently re-pinning autonerves alone) into
   a rehearsal-mode re-pin that covers all five packages and re-runs the
   package install. Lands entirely inside Heart, so it works on the next run.

The overlay mechanism is proven to work; what is missing is that it only re-pins
autonerves, not the four libraries the setup cell downgrades, and that nothing
sets it in rehearsal mode.

Out of scope: the IMMEDIATE unblock is a human-authorised release carrying
PyAutoNerves main (the #168 and #169 bootstrap fixes). That is a release
decision, not this prompt's work, which is about the rehearsal gate being
unable to see a fix the candidate already carries.

Related: PyAutoHeart#228, PyAutoNerves#168, PyAutoNerves#169,
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/35195111347
