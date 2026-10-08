## search-ext-a3b-nss-preflight
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1678
- completed: 2026-10-08
- epic: search-extensibility (phase A3b)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1681
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1681

**Shipped:** PyAutoFit#1681 (merged 2026-10-08T20:05:54Z after A2 #1679 and A3 #1680, via a human `/prm`). It was launched with `--auto`, effective autonomy safe, tier judge. The work was implemented in the A2 worktree's manual second checkout `PyAutoFit_a3` and had no worktree or `active.md` row of its own; there was only a `planned.md` row.
- NSS now samples through `Fitness.objective` (built by `make_fitness`) and runs on `run(ctx)` + `raw_samples_from`, resuming from `NativeFileCheckpointer("nss_checkpoint.pkl")`. Assertions are traced, so NSS no longer raises `TracerBoolConversionError` under `jit`. The resume sanity check runs at the start of the run. `nss_log_likelihood_from` is removed, and `make_fitness` is now the only place that builds a `Fitness`.
- New `autofit/non_linear/search/preflight.py`. `trace_preflight` runs a `jax.eval_shape` per declared objective kind, after the test-mode bypass and the REQUIRED gate. A failure raises a chained `SearchException`. `PYAUTO_JAX_PREFLIGHT=0` skips it, and `PYAUTO_JAX_PREFLIGHT_PROBE=1` adds an opt-in numerical probe. `check_x64` warns once, and raises when a search sets the new `requires_fp64` capability (default False; no search sets it). `docs/design/run_ctx.md` is at Revision 2.
- Dynesty now chooses its single-core path with a private `_SingleCoreRun` sentinel. Only a `RuntimeError` from creating the pool still falls back; one raised mid-run (including `XlaRuntimeError`) now surfaces.
- **Witness PASS (run on a98312308):**
  - Leg 1: NSS fits `gaussian_x3_blend` under JAX on CPU at fp64.
    - Default settings (n_live 200, 5 MCMC steps) gave ln Z 133.98 on seed 0 (correct), the wrong mode on seed 1, and ln Z about 27 nats low on seed 2.
    - n_live 200 with 50 MCMC steps gave ln Z 135.35/137.62/135.67 on seeds 0–2, with all centres correct. That is inside the reference spread (Nautilus 137.06/137.07, Dynesty 134–139.7).
    - The harness verdict is `not_assessed` because the jax_cpu reference is still pending.
    - Pre-A3b main fails the same fit with `TracerBoolConversionError`, so A3b is what enables it.
  - Leg 2: conformance `-k NSS`, 16 passed.
  - Leg 3: a real NSS fit on an `np.asarray` JAX likelihood raises a chained `SearchException` in 0.05 s.
  - Leg 4: the D2 regression passes for all 7 required searches.
  - The x64 check warns once, and raises with `requires_fp64=True`.
  - Full suite: 3555 passed, 1 skipped, 4 xfailed.
- **Follow-ups found by the witness (not fixed; filed as drafts):**
  1. The x64 warning text in `preflight.py:65` is wrong. It claims `JAX_ENABLE_X64=0` leaves x64 off, but `autonerves/jax_wrapper.py:88-97` forces True for any value that is not `"true"`.
  2. The `autofit_inference` `local_jax_cpu_fp32` config actually runs fp64 (its rows record `device.x64` True), so no fp32 leg has ever measured fp32.
     - Filed together with (1) as `draft/bug/autonerves/jax_enable_x64_env_ignored_and_fp32_leg_runs_fp64.md`.
  3. When the NSS deferral is lifted in `autofit_inference`, its settings need at least 50 MCMC steps (about 5×ndim), not the n_live_200 default. Filed as `draft/feature/autofit_inference/nss_settings_for_wave2.md`.

## Original prompt

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
Blocked-by: none — RESOLVED 2026-10-08: A2 (PyAutoFit#1679, `complete/2026/10/search-ext-a2-objective-bridge.md`) and A3 (PyAutoFit#1680, `complete/2026/10/search-ext-a3-samples-checkpointer.md`) both merged to PyAutoFit main (was: search-ext-a2-objective-bridge, search-ext-a3-samples-checkpointer (PyAutoFit; both must be on the branch this stacks on))
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
