## quick-update-display-id
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1289
- completed: 2026-05-21
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1290
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/62
- notes: Phase C of z_features/fast_visualization.md. Wires IPython.display.update_display into BackgroundQuickUpdate so search runs inside Jupyter / Colab kernels show a single self-updating subplot_fit.png in the cell that ran search.fit(...), rather than just writing PNGs to disk. Script mode unchanged (IPython.get_ipython() returns None outside a kernel → no display side effects). Implementation: ~130-line additive change to PyAutoFit/autofit/non_linear/quick_update.py adding `_is_ipython_kernel` and `_push_to_ipython` helpers + `display_id="pyauto_fit_progress"` kwarg, hooked into `_process_pending` after `perform_quick_update` returns successfully. Reads the PNG from disk (not matplotlib Figure) to sidestep cross-thread Figure handling since the worker is a daemon. Failure-containment: any IPython exception is logged and swallowed so a display issue never takes the search down. `PYAUTO_DISABLE_IPYTHON_DISPLAY=1` opt-out for papermill / nbconvert pipelines. Three unit tests cover kernel-detection no-op, missing-PNG no-op, and the `display`→`update_display` sequence with a mocked IPython. Workspace docs: new __Live Quick-Update Visualization__ section in autofit_workspace/scripts/cookbooks/analysis.py (cookbook had ZERO mention of iterations_per_quick_update or background_quick_update before this; now covers both plus the in-cell live update + script-mode fallback + opt-out + commented API-shape example). Regenerated matching notebooks/cookbooks/analysis.ipynb via PyAutoBuild py_to_notebook. Gotchas: (1) The Sonnet ship_workspace subagent had a smoke-runner cwd bug — it launched scripts with cwd=/home/jammy/Code/PyAutoLabs (parent dir) instead of cwd=$WT_ROOT/autofit_workspace, so all simulators-via-subprocess auto-simulation calls failed with "No such file or directory". I re-ran smoke manually from the correct cwd and all 7 scripts passed; then created the PR myself. The skill prompt's contract didn't pin down cwd explicitly enough; worth tightening in a future skill iteration. (2) Workspace CI smoke (3.12) and (3.13) failed on the PR because the CI env lacks the optional `nss` package + `handley-lab/blackjax` fork that `searches/nest.py` imports — pre-existing CI infrastructure gap, identical shape to the previous task's point.py CI red. Merged anyway. (3) Canonical autofit_workspace had pre-existing dirty README.md (version bump v2026.5.14.2 → v2026.5.21.1) at post-merge cleanup time; stashed + ff-pulled + popped, stash pop was a no-op because remote already had the same change. Note: ship_workspace step 3 (Sonnet subagent) needs its smoke-runner contract to explicitly state "all `python` invocations must use cwd=$WT_ROOT/<workspace>", and ideally check that `scripts/simulators/simulators.py` resolves before launching, to catch the cwd bug fast.
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/14
- completed: 2026-05-21
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1288
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/435
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/15
- notes: Phase B of z_features/fast_visualization.md. Re-enables the effective_einstein_radius latent in the Euclid pipeline workspace, previously commented out because the only available API (tracer.einstein_radius_from(grid=...)) was not JAX-traceable under compute_latent_samples' vmap+jit wrap. Deep-research finding that re-scoped the task: jax_zero_contour.ZeroSolver explicitly documents incompatibility with jax.vmap (uses lax.cond / lax.while_loop early-termination). Vmap-friendly path would require either an upstream fork or a parallel JAX algorithm bypassing ZeroSolver — both out of scope. Landed jit-only architecture instead: PR PyAutoFit#1288 adds Analysis.LATENT_BATCH_MODE class attribute (default "vmap" for backwards compat, new "jit" option). PR PyAutoGalaxy#435 adds LensCalc.einstein_radius_jit_from(init_guess, ...) — ~95-line JIT-friendly helper that bypasses _init_guess_from_coarse_grid (skimage) and ZeroSolver.path_reduce (variable-length output), computes shoelace area on raw NaN-padded paths via jnp.where masking, returns scalar jax.Array; also sets AnalysisDataset.LATENT_BATCH_MODE = "jit" so all PyAutoGalaxy/PyAutoLens analyses inherit jit-per-sample automatically. PR pipeline#15 dispatches on self._use_jax: JAX → new helper with 4-seed fan at ±1 arcsec, numpy → legacy einstein_radius_from(grid=...). Verified end-to-end: max-LL latent.effective_einstein_radius = 2.1002 arcsec on dataset 102018665_NEG570040238507752998 prior-median MGE tracer. Latent step ~480 ms/sample on CPU after the ~10s ZeroSolver compile (1000 samples ≈ 80s, vs ~30s per-sample numpy via z_projects/euclid workaround — slower for Euclid scale but unlocks the JAX-end-to-end pipeline architecture and is fundamentally faster than numpy for cluster-scale geometry). Gotchas: (1) LensCalc.from_mass_obj(tracer) is the correct construction pattern — Tracer doesn't expose einstein_radius_via_zero_contour_from directly (matches the z_projects/euclid pattern). (2) Tried direct vmap path first; failed in convert.axis_ratio_and_angle_from because _init_guess_from_coarse_grid line 1107 called tangential_eigen_value_from without xp=jnp threading. Even after fixing that, find_contours (skimage) blocks JAX trace fundamentally — necessitating the new helper. (3) PR body URL cross-references had to be patched via `gh api PATCH` because gh pr edit hit a Projects-Classic GraphQL deprecation warning — same workaround as the previous task. (4) workspace PR's url_check CI failed on a pre-existing Jammy2211/autolens_workspace reference in README.md:110 (not touched by this PR); merged anyway since the failure is independent and the library PRs were green. Follow-up: a future task should consider whether to fix README.md:110 broadly or add the URL pattern to allowlist. Future work: the new helper accepts init_guess as a required argument so callers must know lens position; for unconstrained scenarios a JAX-native seed-finder (e.g. jnp.argmin on |eigen_values| coarse grid) could replace the static init_guess — but that's a separate library task.

## Original prompt

# Phase C — Live Jupyter cell rendering via `IPython.display.update_display`

Adds in-cell live updating of the quick-update visualization when a
PyAutoFit search runs inside a Jupyter / Colab kernel. The background
threading + JAX-fast figure generation already exist (Phase A′ +
`BackgroundQuickUpdate`, Phase B latents); this phase wires
`IPython.display` so the cell *displays and refreshes in place* during
the fit, instead of just writing PNG files to disk.

## What already exists (don't re-implement)

- **Background thread:** `PyAutoFit/autofit/non_linear/quick_update.py`
  ships `BackgroundQuickUpdate` — a daemon `threading.Thread` with a
  latest-only drop backpressure policy. It calls
  `analysis.perform_quick_update(paths, instance)` off the search hot
  path. Wired into the Nautilus sampler at
  `search/nest/nautilus/search.py:196,216` via the
  `background_quick_update` kwarg on `Fitness`.
- **JAX-fast visualization:** PR #1278 / PR #434 / PR #435 mean
  `analysis.perform_quick_update` runs the JIT-cached `fit_for_visualization`
  + zero_contour critical curves with warm-call latency in the ~10s of ms.
- **Output to disk:** the visualizer writes `subplot_fit.png` (and
  related) under `paths.image_path` on every quick update.

What's missing: when a notebook user runs a search, the PNGs land on
disk but the user has to open them externally. The user-facing goal from
the original tracker is:

> "Visualization … would happen … with Jupyter Notebooks update the
> quick visuals on the fly during modeling … as a cell which updates."

## What to change

### 1. Add IPython display layer to `BackgroundQuickUpdate._process_pending`

`@PyAutoFit/autofit/non_linear/quick_update.py`

After `analysis.perform_quick_update(paths, instance)` returns, the
worker should:

1. Detect whether we're running inside an IPython kernel (Jupyter / Colab).
   Use `IPython.get_ipython()` — returns a kernel instance when inside
   one, `None` otherwise.
2. If yes: locate the `subplot_fit.png` (or configured primary plot)
   that `perform_quick_update` just wrote.
3. Use `IPython.display.update_display` with a **stable `display_id`**
   so subsequent updates *replace* the previous cell output rather than
   appending. The first call uses `display(...)` with `display_id=True`
   to initialise; subsequent calls use `update_display(...)` with the
   same id.

Suggested shape:

```python
class BackgroundQuickUpdate:
    def __init__(self, convert_jax: bool = False, display_id: str = "pyauto_fit_progress"):
        self._convert_jax = convert_jax
        self._display_id = display_id
        self._display_initialised = False
        # ... existing state ...

    def _is_ipython_kernel(self) -> bool:
        try:
            from IPython import get_ipython
        except ImportError:
            return False
        ipy = get_ipython()
        return ipy is not None and "IPKernelApp" in getattr(ipy, "config", {})

    def _push_to_ipython(self, paths):
        """Display or update the primary subplot in the active IPython cell."""
        png_path = Path(paths.image_path) / "subplot_fit.png"
        if not png_path.exists():
            return  # nothing to show — visualizer didn't write that frame
        try:
            from IPython.display import Image, display, update_display
        except ImportError:
            return

        img = Image(filename=str(png_path))
        if not self._display_initialised:
            display(img, display_id=self._display_id)
            self._display_initialised = True
        else:
            update_display(img, display_id=self._display_id)

    def _process_pending(self):
        # ... existing worker body that calls analysis.perform_quick_update ...
        try:
            analysis.perform_quick_update(paths, instance)
        except NotImplementedError:
            return
        except Exception:
            logger.exception("Background quick-update raised (ignored).")
            return

        # NEW: push to active IPython cell if we're in one.
        if self._is_ipython_kernel():
            try:
                self._push_to_ipython(paths)
            except Exception:
                logger.exception("IPython display update raised (ignored).")
```

**Key points:**

- **Graceful fallback** outside IPython kernels — `_is_ipython_kernel()`
  returns False, no display call fires. Script users get the existing
  PNG-on-disk behaviour, nothing changes for them.
- **`Image(filename=path)`, not `Figure`.** Reading the PNG from disk
  avoids cross-thread matplotlib figure handling — matplotlib figures
  are not thread-safe and `_process_pending` runs on the
  `BackgroundQuickUpdate` daemon worker. PNG → bytes → IPython.display
  is thread-safe.
- **Display ID stays stable across the search** so the cell output is
  one continuously updating image, not a wall of stacked frames.
- **Quiet on failure** — log and swallow; do not crash the search.

### 2. Locate the right image path

The plot file paths come from the configured `paths.image_path`. For
imaging the canonical entry is `subplot_fit.png`; for interferometer
`subplot_fit.png` (per the visualizer naming convention). Check both
exist before picking. If neither, no-op (script wrote no quick-update
plots — e.g. `PYAUTO_FAST_PLOTS=1`).

Worth supporting a small ordered list (`subplot_fit.png`, `fit.png`,
`subplot_tracer.png`) so that whichever the analysis class wrote is
displayed.

### 3. Optional: opt-out env var

For users who don't want the IPython display behaviour even in a notebook
(e.g. they're scripting via `papermill` and don't want display side
effects), add `PYAUTO_DISABLE_IPYTHON_DISPLAY=1` as an opt-out. Default
behaviour: display when in a kernel.

### 4. Unit tests

`@PyAutoFit/test_autofit/non_linear/test_quick_update.py`

Three tests:

- `_is_ipython_kernel` returns False when not inside IPython (i.e.
  during normal pytest execution). Verifies the script-mode fallback.
- `_push_to_ipython` is a no-op when no PNG exists at the expected
  path (e.g. fast-plots-disabled run).
- With a mock IPython environment + a synthetic PNG, the first call
  uses `display(... display_id="pyauto_fit_progress")` and subsequent
  calls use `update_display(...)` with the same id. Mock the IPython
  imports so the test runs without a live kernel.

### 5. Document in `autofit_workspace/scripts/cookbooks/analysis.py`

The analysis cookbook currently has zero coverage of
`iterations_per_quick_update`, `background_quick_update`, or any other
live-visualization mechanic (verified: `grep "quick_update" cookbooks/analysis.py`
returns no matches). After the library change lands, add a new section
after the existing `__Visualization__` section (line ~198) titled
`__Live Quick-Update Visualization__` covering:

1. **What `iterations_per_quick_update` does** — the search calls
   `analysis.perform_quick_update(paths, instance)` every N likelihood
   evaluations using the current best-fit `instance`, producing
   `subplot_fit.png` etc. in the output folder so users can monitor the
   fit without waiting for completion.
2. **The `background_quick_update=True` opt-in** (Nautilus today) —
   runs the render on a daemon `threading.Thread` so the search isn't
   paused while matplotlib saves PNGs. Latest-only drop policy: if a
   new best-fit arrives before the previous render finishes, the older
   request is silently replaced.
3. **What this PR adds** — when running inside a Jupyter or Colab
   kernel, the cell that ran `search.fit(...)` **auto-updates in
   place** during the fit. A single image element refreshes every
   `iterations_per_quick_update` likelihood evaluations rather than a
   wall of stacked frames. No code change needed by the user; the
   `BackgroundQuickUpdate` worker detects the kernel and pushes the
   freshly-written `subplot_fit.png` via `IPython.display.update_display`
   with a stable `display_id`.
4. **Script mode unchanged** — when running outside a kernel
   (`python my_fit.py`), the PNGs still land on disk and nothing is
   displayed inline. No new dependency at search time; `IPython` is
   only imported when actually running inside a kernel.
5. **Opt-out** — `PYAUTO_DISABLE_IPYTHON_DISPLAY=1` skips the display
   step even when running inside a kernel, for papermill / automated
   nbconvert pipelines that don't want display side effects.
6. **A small worked example** at the bottom of the section: a 5-line
   snippet showing `af.Nautilus(iterations_per_quick_update=50,
   number_of_cores=1, ...)` with `background_quick_update=True`, plus
   a brief note about how to view the output (cell shows the live
   image; PNG also on disk at `paths.image_path / "subplot_fit.png"`).

Style: match the surrounding cookbook prose (`"""..."""` blocks with
`__Section__` headers, prose explaining the concept then a code
example). Don't include a runnable Nautilus fit in the cookbook itself
— the existing convention is to comment out non-trivial searches and
just show the API shape.

After the script is updated, regenerate the corresponding notebook via
PyAutoBuild's `py_to_notebook` (or it'll regenerate automatically on
the next `/pre_build`). The workspace PR should include the regenerated
`.ipynb`.

## Smoke validation

After implementation, create a tiny notebook-style script (Python `.py`
that imitates a notebook kernel by importing `IPython.display`) and
verify it produces `display_data` / `update_display_data` messages on
the kernel side. Alternatively, run an actual `jupyter nbconvert --execute`
on a notebook that fits a small Nautilus search and inspect the cell
output for the updating image.

## Out of scope

- Subprocess visualization. `BackgroundQuickUpdate` (threading) is the
  shipped approach; this phase doesn't revisit the deferred Phase F
  subprocess design.
- Matplotlib figure capture / cross-thread figure handling. We avoid
  this entirely by reading the PNG from disk after `perform_quick_update`
  writes it.
- Colab-specific tweaks. The IPython kernel detection should cover
  Colab automatically (it runs an IPython kernel). If Colab-specific
  display quirks emerge, follow up in a separate prompt.
- Multi-figure layouts (residual / source plane shown side-by-side in
  the cell). For now, a single primary subplot per cell is sufficient.

## Verification

1. **Unit tests:** `pytest test_autofit/non_linear/test_quick_update.py` —
   all three new tests pass; existing tests unchanged.
2. **Script mode:** run any existing PyAutoFit search from a plain
   Python script. Confirm no behaviour change (PNG still lands on disk;
   no IPython side effects; no warnings about missing IPython).
3. **Notebook smoke:** create a minimal notebook that runs a small
   `n_live=25, n_like_max=200` Nautilus fit on the `autofit_workspace`
   Gaussian example with `iterations_per_quick_update=50` and
   `background_quick_update=True`. After execution, the cell should
   show a single image (not multiple stacked frames) reflecting the
   final iteration's `subplot_fit.png`.
4. **End-to-end:** rerun the Euclid pipeline's
   `start_here.py` (no `PYAUTO_DISABLE_JAX`, `PYAUTO_TEST_MODE=1`)
   *inside* a jupyter kernel (e.g. `jupyter nbconvert --execute` on a
   wrapper notebook) and confirm the cell shows a live-updating
   `subplot_fit` image during the fit.

## References

- `z_features/fast_visualization.md` — parent tracker, Phase C section.
- PyAutoFit commit `1fee93174` — added `BackgroundQuickUpdate`. The
  worker hook for the IPython display layer goes inside
  `_process_pending`.
- PyAutoFit `autofit/non_linear/fitness.py` — call sites that drive
  `BackgroundQuickUpdate.submit(...)`. No changes needed there; the
  display layer is entirely inside the worker.
- `IPython.display.update_display` docs:
  https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html
