- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/137
- completed: 2026-09-09
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/138
- merge-commit: dc127ab
- bundle: mge (architect session, 2 members; the sibling
  `markdown_regeneration_sigma_min` was dropped before an issue was filed and
  stays in `draft/docs/autolens_workspace/` — see "The bundle's other member")
- summary: |
    Re-pinned `EXPECTED_LOG_LIKELIHOOD_HST` in
    `jax_profiling/jit/imaging/mge.py` from 27379.38890685539 to
    27373.152646517716, and replaced PR #134's
    `expected value not re-measured` marker with one naming the re-pin date
    and the library SHAs (PyAutoLens 7d1b04d, PyAutoArray 35aa681).

    **The prompt's premise was wrong and the plan said so up front.** The
    prompt (filed 2026-05-08) asked to re-pin to 27542.080621803576. That
    number had already been refuted on 2026-05-16 by
    `jit-regression-constant-drift` (_developer#67): it came from a checkout
    with locally-modified `jax_profiling/dataset/imaging/hst/*.fits`, and
    clean `main` passed at 27379.388907. It never appeared in any run here.
    The live reason to re-measure was one day old at issue time: `9e0e351`
    (2026-09-08, PR #134) swept the lp over-sampling bins [4,2,1] -> [4,2,2]
    and left every dependent literal pin un-re-measured by its own admission.
    This cleared one of that PR's ten markers; nine remain.

    **The attribution is what makes the new number trustworthy.** A control
    run restoring the pre-sweep [4,2,1] bins reproduced the OLD constant to
    the last ULP (27379.388906855387), and `over_sampled_pixels` moved
    17980 -> 62752. 17980 matches the committed
    `mge_likelihood_summary_hst_v2026.5.1.4.json`. So the stack was faithful
    to the one the old constant was set on and the whole 2.2777e-4 move
    (2.28x outside rtol=1e-4) is the bins change, not the environment.
    Eager/JIT/vmap agreed to 3.99e-16; `rtol=1e-4` left alone.
- traps: |
    **Two container traps, both costly, both now recorded.**

    1. `mge.py` imports `jax` (line 53) before `autolens` (line 61), which is
       too late for the config layer's `jax_wrapper` to set
       `JAX_ENABLE_X64` — so a bare `python mge.py` silently runs in
       **float32**, giving JIT 27373.130859375 and agreeing with eager only
       to ~8e-7, not the ~1e-11 the file's own comment asserts. No pinned
       constant is wrong (eager is pure NumPy `xp=np`), but every JIT/vmap
       precision and timing claim these scripts print is float32 unless the
       runner presets the env var. 33 scripts in the repo share the pattern.
       Filed as `draft/bug/autolens_workspace_developer/jax_import_order_defeats_x64.md`.

    2. **XLA:CPU deadlock in the vmap leg on 4 cores** — the script hangs
       indefinitely at `block(result_vmap)` (`mge.py:673`), 0% CPU, all
       threads sleeping; reproduced three times, with and without x64 and
       XNNPACK. `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` fixes it
       (intra-op thread-pool starvation). Container-side only. PR #130 hit
       the same wall on `pixelization.py` and simply skipped its vmap leg;
       this flag is the way past it.

    Also: the run's `mge_likelihood_summary_hst_v2026.8.17.1.{json,png}`
    artifacts were deliberately NOT committed. They are timing records, and
    container timings taken under a non-default XLA flag would corrupt a
    version-keyed profiling series read as performance history.
- environment: |
    Shipped from a Claude Code web session (no task worktree, no `gh`; issue
    and PR driven through the GitHub MCP surface). The measurement needed the
    library stack built from `main` source checkouts — PyPI wheels are not a
    substitute, since the script uses `autofit.jax.register_model`,
    `aa.DatasetInterface` and `xp=jnp` kwargs. Cloned PyAutoConf/`autonerves`
    0e7163b, PyAutoArray 35aa681, PyAutoFit 66f9f8d, PyAutoGalaxy 99cf742,
    PyAutoLens 7d1b04d and editable-installed them; CPU-only JAX 0.11.1,
    NumPy 2.5.3, Python 3.12.3. The HST dataset is committed and seeded
    (`noise_seed=1`), so nothing had to be simulated. This whole class of
    work is container-feasible — PR #130 is the precedent.
- ship-gate: |
    This repo has no CI (no `.github/`) and no smoke surface (no
    `smoke_tests.txt`, no `config/build/` profile). The gate was the script
    itself: run end to end twice, by the implementing subagent and then
    independently by the architect, exit 0 both times, 3/3 regression
    assertions plus the step-by-step and vmap-vs-JIT correctness checks.
    Branch review CLEAN. The Heart leg was **STALE (score 35)** — PyAutoHeart
    was cloned and `readiness` run, but a web container holds no Heart state,
    so the gate was un-evaluable rather than passed. That was flagged
    verbatim in the PR body rather than claimed as green, the PR stopped at
    PR-open, and the merge was the human's explicit call knowing both facts.
- bundle-note: |
    **The bundle's other member.** `markdown_regeneration_sigma_min`
    (regenerate `autolens_workspace/markdown/` so seven MGE pages show
    `sigma_min`) was dropped before an issue was filed — independent of this
    task, but far larger than its `Difficulty: small` in any container:
    PyAutoHands' `generate_markdown.py` refuses `PYAUTO_TEST_MODE` by design
    (it executes each script for real to render figures), the seven pages
    carry ~20h of declared budget in `markdown_examples.yaml`, and three of
    them declare `ENV: full_datasets`. The one cheap path does not exist:
    `notebooks/` carry **0 stored outputs** across their code cells, so
    `markdown/` cannot be re-rendered without executing. It needs a machine
    with a warm `output/`.

## Original prompt

## Re-baseline the MGE imaging JIT profiling regression value

Type: test
Target: autolens_workspace_developer
Themes:
- mge
- jax-compile
- profiling
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Filed: 2026-05-08 (backfilled from git)
Issued: 2026-09-09

`@autolens_workspace_developer/jax_profiling/jit/imaging/mge.py` hardcodes a
regression assertion at the bottom:

```python
EXPECTED_LOG_LIKELIHOOD_HST = 27379.38890685539

np.testing.assert_allclose(log_likelihood_ref, EXPECTED_LOG_LIKELIHOOD_HST, rtol=1e-4, ...)
np.testing.assert_allclose(float(full_result), EXPECTED_LOG_LIKELIHOOD_HST, rtol=1e-4, ...)
np.testing.assert_allclose(np.array(result_vmap), EXPECTED_LOG_LIKELIHOOD_HST, rtol=1e-4, ...)
```

On canonical `main` the eager `log_likelihood_ref` is now `27542.080621803576`
— a 162.7-unit drift (~0.6% relative), well past `rtol=1e-4`. Confirmed during
the `fft-mixed-precision-fix` audit (`PyAutoArray#302`): the drift is *not*
caused by the FFT precision fix, since `log_likelihood_ref` comes from the
eager NumPy `FitImaging` path which the fix doesn't touch. Both pre-fix and
post-fix builds produce 27542.08 on the same dataset.

So the hardcoded value is just stale — some upstream change between when it
was last set and now (probably a simulator tweak, an over-sample default, or
a numerical-stability change in `Isothermal.deflections_yx_2d_from`) shifted
the truth-point likelihood. The script crashes at the regression assertion
on every run currently.

### What to do

1. Run the script once on a clean checkout to capture the new value. Keep
   the same dataset path / pixel scale / mask radius the script declares so
   the regression remains comparable across machines.

2. Confirm eager / full / vmap all agree to ~1e-11 (per the existing
   docstring at line 822 of `mge.py`). If they don't, that's a separate
   correctness bug, *not* a re-baseline.

3. Update `EXPECTED_LOG_LIKELIHOOD_HST` to the new measurement. Add a short
   inline comment noting which upstream commit the value was re-pinned
   against (use `git log -1 PyAutoArray/autoarray` or similar to find the
   most recent library SHA at the time of re-baselining).

4. Optionally tighten or loosen `rtol` based on the observed agreement
   between eager / JIT / vmap. The existing `rtol=1e-4` is conservative.

### Out of scope

- Investigating *why* the value drifted. The regression assertion is a smoke
  trip-wire, not a debugging tool. Whoever cared about reproducibility at the
  ~1e-4 level should have noticed the drift in CI, but `mge.py` doesn't run
  in CI today (it's a developer profiling script). If you want it in CI,
  that's a separate task.

- The other instrument variants (`euclid`, `jwst`, `ao`) — the script
  currently only sets the HST regression value. If those should also have
  hardcoded targets, that's a feature request, not a re-baseline.

### Why this didn't get bundled into PyAutoArray#302

The fft-mixed-precision-fix work scoped its plan to PyAutoArray +
autogalaxy_workspace_test + autolens_workspace_test. `autolens_workspace_developer`
was never in scope, and the mge.py drift is independent of the fix. Bundling
it in would have inflated the PR's blast radius without clear benefit.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
