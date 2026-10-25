# `@PyAutoFit` `test_emcee_call_path_runs_at_jitted_speed` is a wall-clock ratio assertion that flakes on shared CI runners

Issued: 2026-10-25
Type: test
Target: autofit
Repos:
- PyAutoFit
Difficulty: trivial
Autonomy: safe
Priority: normal
Status: active
Consequence: glance
Witness: the test no longer asserts a wall-clock ratio between the wrapped call path and the raw jitted function on CI; it asserts structurally that the Emcee call path dispatches to the compiled objective (e.g. the wrapper calls the jitted callable exactly once per evaluation with no Python-side re-tracing), with the timing comparison kept only under an opt-in env flag for local profiling.
Filed: 2026-10-14

`test_autofit/non_linear/search/mcmc/test_emcee_jax_timing.py::test_emcee_call_path_runs_at_jitted_speed` failed on PyAutoFit main df6d218f1 (run 38577574188, `unittest (3.12)` only: "call_wrap 0.116 ms vs jit 0.055 ms") while the same code passed on #1687's PR CI and on the previous main run 5bf057f28; `gh run rerun --failed` on the same run went green. A failure on main turns Heart RED and stops every `--auto` ship gate (it parked B4b on 2026-10-14). Sub-millisecond ratio assertions cannot be stable on shared runners; replace with a structural assertion.
