After the latent refactor series shipped ([z_features/complete/latent_refactor.md](../z_features/complete/latent_refactor.md)),
the autolens SLaM smoke test timed out at the 5-minute mark while still inside
the first SLaM stage's post-fit latent processing.

__Root cause__

`PyAutoFit:autofit/non_linear/search/updater.py:226` (`_compute_latent_samples`)
ignores `PYAUTO_TEST_MODE`. It always draws `output.latent_draw_via_pdf_size`
samples (default 100) and runs `analysis.compute_latent_samples(...)` on each.

Per `PyAutoGalaxy:autogalaxy/analysis/analysis/dataset.py:28`,
`AnalysisDataset.LATENT_BATCH_MODE = "jit"` (override from the default `"vmap"`)
because the einstein-radius latent routes through `jax_zero_contour.ZeroSolver`,
whose `lax.cond` / `lax.while_loop` early-termination is vmap-incompatible.
In `"jit"` mode `_compute_latent_samples` runs a literal Python loop
(`for p in parameters_batch: jitted_compute_latent(p)`) — JIT cache is reused
after sample 1, but Python dispatch + JAX kernel launch is paid per sample.

On WSL CPU this measures > 1.5 s/sample. 100 samples × 5 SLaM stages = 500
latent dispatches per fit ≈ 12+ min of pure post-processing per SLaM script,
fatal for smoke. Real-mode SLaM runs pay the same tax but it's amortised
against minutes of sampling so wasn't visible.

`PYAUTO_TEST_MODE` already short-circuits the sampler (50 mock calls) but the
post-fit latent path is unaffected — the smoke runs do all 100 latent draws
even though the fit results are mocked and the latent values are never asserted on.

__The fix__

Short-circuit `_compute_latent_samples` in test mode. Latent values are not
needed when the fit itself is mocked.

1. **`PyAutoConf:autoconf/test_mode.py`** — add a new helper alongside
   `skip_visualization()`, `skip_checks()` etc:

   ```python
   def skip_latents():
       """Return True if latent variable computation should be skipped."""
       return is_test_mode() or os.environ.get("PYAUTO_SKIP_LATENTS", "0") == "1"
   ```

   This composes two triggers (matches the pattern already used by
   `skip_fit_output`, which is part of the fast-smoke env set in
   `autolens_workspace/CLAUDE.md`). `is_test_mode()` auto-enables it inside
   `PYAUTO_TEST_MODE` runs; `PYAUTO_SKIP_LATENTS=1` allows manual control
   without enabling test mode (useful for real fits where the user just
   wants to skip latent post-processing).

2. **`PyAutoFit:autofit/non_linear/search/updater.py`** — in
   `_compute_latent_samples` (line 226), short-circuit early:

   ```python
   def _compute_latent_samples(self, ...):
       """Compute and persist latent variable samples if configured."""
       from autoconf.test_mode import skip_latents
       if skip_latents():
           return None
       if not ((during_analysis and conf.instance["output"]["latent_during_fit"])
               or (not during_analysis and conf.instance["output"]["latent_after_fit"])):
           ...
   ```

   Return type is `Optional[Samples]`. Downstream (`_profile_and_summarize`
   at line 117) already accepts `latent_samples=None` — no further changes
   needed inside updater.

3. **Unit test** in `test_autofit/non_linear/search/test_updater.py` (or
   equivalent — confirm test layout) covering:
   - `is_test_mode_run()` path → `_compute_latent_samples` returns `None`
   - `PYAUTO_SKIP_LATENTS=1` path → same
   - default path (test mode off, flag unset) → unchanged behaviour

   No JAX in unit tests per [[feedback_no_jax_in_unit_tests]] — mock the
   `analysis.compute_latent_samples` call.

__Validation__

Run the SLaM smoke test that previously timed out:

```bash
PYAUTO_TEST_MODE=2 PYAUTO_SKIP_FIT_OUTPUT=1 PYAUTO_SKIP_VISUALIZATION=1 \
PYAUTO_SKIP_CHECKS=1 PYAUTO_SMALL_DATASETS=1 PYAUTO_FAST_PLOTS=1 \
python scripts/imaging/features/advanced/slam/start_here.py
```

Should complete in seconds, not minutes. Confirm via a no-PYAUTO_TEST_MODE run
that real-mode latent computation is unchanged (latent.csv produced as before).

__Out of scope__

- The deeper architectural fix — splitting `LATENT_BATCH_MODE` per-latent so
  fast latents vmap while einstein-radius stays jit-per-sample — is a separate
  follow-up at `autogalaxy/latent_batch_mode_per_latent.md` (TBA). That fix
  matters for real-mode SLaM runs where the 500-dispatch tax is real even
  with `PYAUTO_TEST_MODE` skip; this prompt only unblocks smoke testing.
- No new env var documentation in workspace CLAUDE.md files (the canonical
  fast-smoke command set already covers the test-mode case; `PYAUTO_SKIP_LATENTS=1`
  is for power users who can read autoconf/test_mode.py).
