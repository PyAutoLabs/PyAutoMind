Heart check F is now a faithful Colab gate. Shipped 2026-09-15 as PyAutoHeart#228 (issue #227), two commits, merged c7659ae.

**What was wrong.** Check F emulated Colab by `pip install autolens jax` WITH dependencies, so its venv already held every package the real `--no-deps` bootstrap in `autonerves.setup_colab` would miss. `corner` (a base autofit dependency imported lazily inside `corner_cornerpy`) was absent on Colab on 2026-09-15 and HowToFit tutorial 5 died mid-workshop; workspace smoke (`PYAUTO_TEST_MODE=2`) and check F both reported green.

**What shipped.**
- `heart/checks/colab_gate.py`: `seed` builds a python3.12 venv holding only the packages Google's published Colab manifest (`googlecolab/backend-info` `pip-freeze.txt`, live → `$HEART_STATE_DIR` cache → vendored snapshot) ships that the stack's resolved closure needs, completed to a self-consistent subset; `verify` walks declared requirements, AST-scans every third-party import in the installed libraries (guarded or not), imports each for real, constructs `af.Emcee/DynestyStatic/Nautilus/LBFGS`, and FAILs on any unguarded miss. Check F FAIL → readiness RED.
- `verify_install.sh` check F: seed → verbatim setup cell → verify → notebook cell; with-deps install deleted; `COLAB_GATE_AUTONERVES_SRC` overlay; gate JSON under `checks[F].colab_gate`.
- `heart/config/colab_gate.yaml`: `accepted_missing` for `colossus`, `hmf` (autolens/lens/los.py line-of-sight tooling, test/dev extra, not notebook paths) and `mcp` (autofit/mcp/server.py, MCP server entry point), each with a reason; a test asserts exactly that set.
- 43 new tests; check F docs rewritten (skill row, release_validation.md, capabilities.yaml, CLI help).

**Scoping decision.** Rung 2 of the prompt's ladder: import probe after a faithful bootstrap (~3 min in the release-only `verify_install_release` lane, blocking). Rung 1 (static scan) is an input, not a gate; rungs 3/4 (notebooks end to end at real settings) test script correctness, a different class — filed as `draft/feature/pyautoheart/howto_real_settings_nightly.md`.

**Witness.** PyPI as-is → `F|FAIL` naming corner, blackjax + 5 more (74 s). PyAutoNerves#169 overlaid → `F|PASS` "Colab manifest live 2026-09-15; 87 Colab-provided, 11 extras, 39 imports probed" (179 s). Same PASS reproduced in PyAutoNerves CI (`colab-gate.yml`, run attempt 2 after #228 merged).

**Findings beyond the prompt.** Five library-side unguarded lazy imports of packages Colab does not ship: `jax_zero_contour` (autogalaxy BASE dep, `lens_calc.py:1452,1884`) and `zeus-mcmc` (`af.Zeus`) → added to `_SHARED_EXTRAS` in PyAutoNerves#169; `colossus`/`hmf`/`mcp` → accepted. `hmf` is declared in no pyproject at all (library follow-up). autofit's exact pins `networkx==3.1`, `psutil==6.1.0` contradict Colab (3.6.1 / 5.9.5) permanently — WARN.

**Release consequence.** Check F installs autonerves from the index, so release-integrate stays RED until the autonerves release carrying PyAutoNerves#169 is on PyPI. That is the gate working. Ordering: both PRs merged 2026-09-15; the autonerves release is the remaining human act.

## Original prompt

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
