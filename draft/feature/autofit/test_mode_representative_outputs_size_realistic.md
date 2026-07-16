# Test-mode representative outputs: size-realistic samples for instant pipeline runs

Type: feature
Target: autofit
Repos:
- PyAutoFit
- PyAutoConf
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Split (2026-07-16, Feature Agent: too-large, score 14): this file is the **umbrella** —
issue the phase files, not this one. Phases (same folder):
`..._phase_1_design.md` → `..._phase_2_core_api.md` → `..._phase_3_workspace_examples.md`
→ `..._phase_4_docs.md`. Issue each phase only as its predecessor nears shipping.

Original request (verbatim):

ok, as a side project could we scope out if there would be a way to extend PYAUTO_TEST_MODE to do these runs
instantly, e.g. replace the sampling with soemthing fast but with enough samples in samples.csv that it is
representative of the resume run times. This prbbaly a standalone feature -- a test mode which produces more
realistic outputs in terms of size, but we can scope it out, /intake it and then do the work in another prompt.

## Scoping notes (pre-intake, verified against source 2026-07-16)

Context: born from the `slam-resume-profiling` task (autolens_profiling#70) — a full 5-stage SLaM cold run
takes hours on CPU, so profiling resume overhead is slow to iterate on. A test mode whose completed outputs
are size-representative would make cold runs instant while keeping resume timings honest.

What exists today (@PyAutoFit `autofit/non_linear/search/abstract_search.py`, @PyAutoConf `autoconf/test_mode.py`):

- `PYAUTO_TEST_MODE` levels: 0 off / 1 minimal iterations / 2 bypass sampler + one likelihood call /
  3 full bypass. Levels 2-3 route `fit()` into `_fit_bypass_test_mode`.
- `_fit_bypass_test_mode` -> `_build_fake_samples` writes exactly **4 fake samples** (prior-median best +
  3 perturbed), then `save_samples_summary` / `save_samples`, real `analysis.make_result`,
  real `save_results` and the normal `.completed` + zip cycle.
- A real Nautilus SLaM stage writes tens of thousands of samples.csv rows, so a bypass-completed output dir
  is orders of magnitude smaller than production — resume costs measured against it (samples CSV parse,
  zip/unzip restore, weight arithmetic) are unrepresentative.

Proposed feature (scope for planning, adjust as needed):

1. A sample-count knob for the bypass path, e.g. `PYAUTO_TEST_MODE_SAMPLES=N` (default = current 4 so
   nothing changes for existing users/tests). `_build_fake_samples` synthesizes N samples: parameters
   scattered around the prior median (deterministic seed), monotone plausible log-likelihoods, valid
   normalized weights — so samples.csv row count and byte size match a production stage (N ~ 10k-100k).
2. Everything downstream must keep working on the synthetic set: `samples.summary()` quantiles,
   search chaining (`result.model` / `result.instance`), aggregator scrape, database load. The existing
   4-sample structural guarantees ("multi-batch sample handling") must hold at large N.
3. Speed: generation must be vectorized (numpy, not per-Sample python loops) or N=50k defeats the purpose.
4. Document the profiling recipe this enables (in the pipeline_resume tier of @autolens_profiling):
   cold run with `PYAUTO_TEST_MODE=2 PYAUTO_TEST_MODE_SAMPLES=<N>` completes in seconds-to-minutes;
   the resume invocation must keep `PYAUTO_TEST_MODE` set (output is namespaced under `output/test_mode/`,
   so unsetting it on resume looks at a different output tree) — note test mode also auto-skips latents,
   a small known delta from a production resume.
5. Known representativeness limits to record, not solve: the one bypass likelihood call means the cold run
   does not leave a realistically-sized search-internal state, and adapt-image FITS content comes from the
   prior-median model rather than a converged fit (size is right; values are not). Fine for timing, not for
   science validation.

Primary repo: @PyAutoFit (bypass path + samples builder). @PyAutoConf only if a new env accessor is added
next to `test_mode_level()`. Downstream doc touch: @autolens_profiling pipeline_resume README recipe.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ce78c7e9-3f34-4983-bb53-8840527c1fb6/scratchpad/intake_testmode_samples.md -->
