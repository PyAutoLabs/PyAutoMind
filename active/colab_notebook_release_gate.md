# Release-time gate that proves the Colab notebooks actually run

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoNerves
- HowToFit
- HowToGalaxy
- HowToLens
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: with `corner` deleted from `_SHARED_EXTRAS`, the new gate reports RED, where today's workspace smoke reports 18/18 green — i.e. the gate catches the 2026-09-15 tutorial-5 failure that every existing gate missed.
Review-minutes: 3
Unattended: ready

Filed: 2026-09-15
Issued: 2026-09-15

Raw request from the user, verbatim:

> can we /intake something that checks colab notebooks run during release? IU guess
> that could be slow but the intake can scope out the best way to do that and balance
> time versus robustness

## Why now

`autonerves/setup_colab.py` bootstraps Colab with `pip install *packages --no-deps`,
so every dependency Colab does not itself preinstall must be named by hand in
`_SHARED_EXTRAS` or it never lands. On 2026-09-15 HowToFit chapter 1 tutorial 5 died
on Colab with `ModuleNotFoundError: No module named 'corner'` — after a 2000-step
emcee search had already completed, in the results update that follows it. A workshop
was running that day.

The reason nothing caught it is the part that should shape the scoping:

- `corner` is imported INSIDE `corner_cornerpy`
  (`autofit/non_linear/plot/samples_plotters.py:95`), not at module scope. So
  `import autofit` succeeds, the model builds, the search runs to completion, and
  only the post-fit plot raises.
- Workspace smoke runs at `PYAUTO_TEST_MODE=2` (`config/build/profile_smoke.yaml`),
  which bypasses the sampler entirely — the searches are never constructed and the
  lazy imports never execute. Scripts pass green while being unrunnable by a reader.
- `config/build/no_run.yaml` already documents this same blind spot for
  `tutorial_5_expectation_propagation`.

Third instance of the class: `8336939` (PyAutoNerves#166) closed it for emcee and
dynesty; a HowToFit prompt had it open for blackjax; PyAutoNerves#167 closes corner,
optax, xxhash and blackjax at once. Each fix needs its own PyPI release to reach a
single user, and the list is being patched one user report at a time.

## What already exists (build on, do not duplicate)

- PyAutoHeart `verify_install` check F already simulates the Colab bootstrap. That is
  the right place; the open question is what it should execute once bootstrapped.
- PyAutoNerves#167 adds a test deriving `_SHARED_EXTRAS` specifiers from PyAutoFit's
  `pyproject.toml`. That closes the DRIFT class statically. It does not prove a
  notebook runs.
- 100 notebooks carry the Colab setup cell: HowToFit 18, HowToGalaxy 32, HowToLens 50,
  plus the three workspace repos.

## The tradeoff to scope — time versus robustness

This is explicitly what the task is for. Weigh these rungs and recommend one; do not
merely list them.

1. STATIC — AST-scan the libraries for function-level third-party imports, cross-check
   against `_SHARED_EXTRAS` and what Colab preinstalls. Seconds. Catches exactly this
   class; proves nothing about runtime.
2. IMPORT PROBE — after a real Colab bootstrap, import every lazily-imported module and
   construct every `af.<Search>` class the scripts instantiate. Minutes. Catches missing
   deps and bad pins without running a fit.
3. ONE REPRESENTATIVE NOTEBOOK per chapter, end to end at REAL settings — not
   `PYAUTO_TEST_MODE=2`, since that mode is the blindness. Tens of minutes.
4. EVERY notebook end to end. Hours; probably too slow for a release gate, but worth
   pricing so the decision is informed.

## Also in scope for the scoping

- Where it runs. A real Colab runtime is not reachable from CI, so check F's simulation
  is an approximation — and Colab's exact preinstalled package set is precisely the
  thing being approximated. Getting that wrong IS the bug. Say what the approximation
  does and does not cover.
- Whether the gate blocks a release or merely reports. A missing dependency makes
  notebooks unrunnable for every user, so blocking is arguable.
- Cadence: per-release, nightly, or only when `_SHARED_EXTRAS` or a `pyproject.toml`
  changes.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cc1b3873-4a26-47d0-bab7-0a193741ef7f/scratchpad/intake_raw.md -->
