# NSS onto Fitness, trace preflight and x64 check (epic search-extensibility, phase A3b)

Type: refactor
Target: autofit
Repos:
- PyAutoFit
Themes:
- searches
- jax
Difficulty: medium
Autonomy: safe
Consequence: judge
Witness: NSS fits `gaussian_x3_blend` with its ordered-centre assertions under JAX (the autofit_inference harness's blend model, 10 parameters) and the A0a conformance layers pass for NSS through `Fitness.objective`; the preflight raises on an `np.asarray` likelihood with the original tracer error chained; the D2 regression (REQUIRED + `PYAUTO_DISABLE_JAX=1` + `PYAUTO_TEST_MODE=2` completes) still passes
Unattended: ready
Priority: high
Epic: search-extensibility
Blocked-by: search-ext-a2-objective-bridge, search-ext-a3-samples-checkpointer (PyAutoFit; both must be on the branch this stacks on)
Status: planned
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1678
Filed: 2026-10-08

Human launch 2026-10-08: `--auto` for A2, A3, A3b and B3. Plan `draft/research/autofit/search_extensibility_epic_report.md` §4 (phase text quoted verbatim below), architecture §3.3–§3.5, decisions in §8. A0, A0c, A1 and B2 are merged (A1: capability attributes, `Analysis.is_jax`, REQUIRED gate, registry/manifest, `docs/design/run_ctx.md` frozen). Golden identifiers (A0a(i)) are frozen by human ruling: any identifier change stops the item and is flagged. The nine A0 strict xfails are witnesses: flip only the ones a phase names, never add silent ones. Depends on A2 (objective factory) and A3 (adapter/checkpointer); implemented stacked on a branch that carries both.

## Original request (verbatim from the epic plan)

"A3b — NSS onto Fitness, trace preflight, x64 (depends on A2 and A3; surveys/02 P3; D2, D8). Repo: PyAutoFit. Scope: NSS onto `Fitness` via the factory (traced assertions; the sanity check moves to the start of the run); the `eval_shape` trace preflight per declared kind, after the test-mode bypass, chained tracebacks, plus the optional numerical probe; the x64 check; Dynesty's `RuntimeError` single-core control flow becomes an explicit sentinel that no longer catches `XlaRuntimeError`. Risk: low-medium. Verify: NSS with assertions under jit; the preflight raises on an `np.asarray` likelihood with the original error chained; an fp32 warning test; the D2 smoke-profile regression test. Witness: NSS fits `gaussian_x3_blend` with its ordered-centre assertions under JAX."

## Pins

Survey 02 §5.3: preflight = `jax.eval_shape(objective, prior-median vector)` (+ `eval_shape(grad)` when `gradient == uses`), one trace, no compile; raise naming the tracer error and the search, `raise ... from e`; it is a trace preflight, not a validity certificate; the optional numerical probe is separate. x64: warn once when `analysis.is_jax and not jax.config.jax_enable_x64` (raise only if a search declares `requires_fp64`; none do today). Placement: after the test-mode bypass and after A1's REQUIRED gate. Dynesty: survey 01 §8 "Single-core control flow" (`dynesty/abstract.py` `raise RuntimeError` inside a `try`) → explicit sentinel exception class; `except RuntimeError` must no longer swallow `XlaRuntimeError`. NSS sanity check: moves to the start of `run`.

## Verification

Full `pytest test_autofit`; nojax emulation; afT `searches/NSS.py`, `Dynesty_jax.py`, `Nautilus_jax.py` under test mode; the autofit_inference blend NSS fit (run `_runner.run_search` from the canonical `fit/autofit_inference` checkout with `sampler=NSS`, `local_jax_cpu_fp64`, test-mode budget) completing with assertions.

## Shape

One PyAutoFit PR (`pending-release`) based on the A2+A3 integration branch; merges after both. Tier judge.
