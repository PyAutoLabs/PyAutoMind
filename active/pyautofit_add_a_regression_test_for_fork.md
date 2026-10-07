# PyAutoFit: add a regression test for `fork_context()` not fixing the multiprocessing start…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: high
Memory: wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/massive-ellipticals.md; wiki/galaxies/sources/cosmos-survey.md
Issued: 2026-10-07
Status: formalised
Consequence: glance
Witness: a new test under test_autofit that monkeypatches sys.platform="darwin" and reloads parallel.context asserts multiprocessing.context._default_context._actual_context is None; it fails on the pre-#1657 code (revert the context.py hunk locally) and passes on main
Review-minutes: 3
Unattended: ready

PyAutoFit: add a regression test for `fork_context()` not fixing the multiprocessing start method at import on darwin/win32.

Community PR PyAutoFit#1657 (@samlange04, discussion https://github.com/orgs/PyAutoLabs/discussions/27, merged 2026-10-07) changed `autofit/non_linear/parallel/context.py` so that on non-Linux platforms `fork_context()` returns the `multiprocessing` module instead of `multiprocessing.get_context()`, because the no-argument `get_context()` call at import time (`parallel/process.py:47` builds `class Process(fork_context().Process)`) locked the interpreter's default start method and made any later `set_start_method("spawn")` raise "context has already been set". The PR has no test and Ubuntu CI cannot reach the darwin/win32 branch, so the fix is unprotected against regression.

Fix: add a test (next to `test_fork_context.py`) that monkeypatches `sys.platform = "darwin"`, reloads `autofit.non_linear.parallel.context` and `process`, and asserts `multiprocessing.context._default_context._actual_context is None` afterwards (i.e. importing did not fix the start method), and that the returned object exposes `.Process`, `.Queue` and `.Pool`. Keep the existing Linux assertion (`get_context("fork")`) intact and restore the module state after the test so conftest's `fork` setting is unaffected.

<!-- formalised by the Intake (Conception) Agent on 2026-10-07 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b718db7a-3dd7-461b-aa15-d27db7e34ca3/scratchpad/community/intake_af.md -->
