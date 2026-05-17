# Fast Visualization — Sequenced Roadmap

End goal: when a search runs with `use_jax=True`, visualization is fast enough
that **a Jupyter / Colab cell can update in place during the fit**, with no
subprocess complexity. Plus a regression net in every `_test` workspace so the
next "default flipped, no test exercises the new path, ships broken to HPC"
class of bug (see 2026-05-16 Euclid all-zero-source-plane regression) gets
caught locally.

This z_feature **supersedes** the subprocess-visualization approach that was
investigated under issue #1279 / task `viz-subprocess-feasibility`. See
`z_features/complete/visualization_subprocess_feasibility.md` for the
banked spike findings (`FitImaging` round-trips cleanly through stdlib
`pickle` — design parked, not lost).

## Why pivoted

During #1279 we discovered the JAX-jittable critical-curve / Einstein-radius
infrastructure already exists in the codebase:

- **`jax_zero_contour`** (external package) is already installed in the venv
  and gives a `ZeroSolver` with JIT-compatible level-curve tracing.
- **PyAutoGalaxy `autogalaxy/operate/lens_calc.py:1001-1500ish`** has
  `..._via_zero_contour_from()` implementations for tangential / radial
  critical curves, caustics, and Einstein radius.
- **PyAutoGalaxy `autogalaxy/plot/plot_utils.py`** routes between
  `zero_contour` and `marching_squares` via the config switch
  `visualize.general.critical_curves_method`.
- The config default at
  **`autogalaxy/config/visualize/general.yaml:8`** is currently
  `marching_squares` (the legacy `skimage.measure.find_contours` path,
  not JAX-traceable).

So the unlock for "JAX-jit'd visualization" is mostly **enablement** of code
that already exists, plus a regression net to prevent the next default flip
from silently shipping broken on dataset types that have no end-to-end test.

## Phase A — Flip `critical_curves_method` default to `zero_contour`

**Scope:** one-line config change in PyAutoGalaxy, plus workspace-config
mirroring. Unlocks JAX-jittable critical curves / caustics for every fit by
default.

**Prompt file:** `autogalaxy/critical_curves_method_default_zero_contour.md` (to author)

Touches:
- `PyAutoGalaxy/autogalaxy/config/visualize/general.yaml:8` — flip
  `marching_squares` → `zero_contour`.
- Each workspace's `config/visualize/general.yaml` — mirror, since workspace
  configs override library defaults (see auto-memory
  `feedback_workspace_config_default_true`).
- New unit test: viz path with `use_jax=True` produces non-empty critical
  curves overlay on a synthetic SIE + circular source.

**Risk:** `jax_zero_contour` not installed on every environment (Python <3.11
gates it out). The existing `_critical_curves_method_resolved` fallback in
`plot_utils.py` already handles this — verify the fallback fires correctly on
a Python 3.10 env (or skip the test there).

## Phase B — Migrate latent-variable call sites to `_via_zero_contour`

**Scope:** swap `tracer.einstein_radius_from(grid=...)` (legacy, marching
squares) for `tracer.einstein_radius_via_zero_contour_from()` (JAX-jittable)
in every latent-variable call site. Once done, drop the `self._use_jax = False`
workaround in `compute_latent_samples` (this is what forced Euclid latents
onto numpy for the Einstein radius).

**Prompt file:** `autolens_workspace_test/einstein_radius_zero_contour_migration.md` (to author)

Known call sites to migrate:
- `z_projects/euclid/scripts/util.py:compute_latent_variables` (line ~580) —
  computes `effective_einstein_radius` via the old method; the
  `compute_latent_samples` workaround forces numpy.
- `z_projects/euclid_pre_f2f/scripts/util.py` and `z_projects/euclid_group`
  (audit — likely same pattern).
- `autolens_workspace/scripts/guides/results/latent.py` — audit.

For each migrated script, end-to-end test under `use_jax=True` and confirm
the JAX path stays on; no `_use_jax = False` flip required.

## Phase C — Live Jupyter cell rendering via `IPython.display.update_display`

**Scope:** in `perform_quick_update`, additionally call
`IPython.display.update_display(fig, display_id="fit_progress")` when running
inside a Jupyter kernel. Cell updates in place during the fit. No subprocess
needed.

**Prompt file:** `autofit/quick_update_display_id.md` (to author)

Touches:
- `PyAutoFit/autofit/non_linear/quick_update.py` — detect IPython kernel via
  `get_ipython()`, set a stable `display_id` on first call, `update_display`
  on subsequent calls.
- Falls back gracefully outside Jupyter (still writes PNG to disk).
- Smoke test: a notebook-style script that runs a tiny Nautilus fit and
  observes the display message stream.

Depends on **Phase A** landing first (so the rendered figure is JAX-jit
fast enough to be worth watching).

## Phase D — Per-dataset end-to-end JAX-jit visualization tests

**The regression net.** The 2026-05-16 all-zero-source-plane Euclid bug snuck
through because the existing `modeling_visualization_jit*.py` scripts in
`autolens_workspace_test` only assert that *a fit completes*. None of them
assert that the **rendered images are non-trivial**. Adding three asserts
per script would have caught the regression locally before HPC.

**Prompt file:** `autolens_workspace_test/end_to_end_jax_viz_assertions.md` (to author)

For every `modeling_visualization_jit*.py` and `visualization_jax*.py` across
both workspace_test repos, append assertions of the form:

```python
# Source plane reconstruction must be non-trivial.
src_image = result.max_log_likelihood_fit.galaxy_image_dict[
    "('galaxies', 'source')"
].array
assert float(src_image.sum()) > 0.0, "source-plane image is all-zero — viz regression"

# Critical curves overlay must produce at least one curve.
tc = result.max_log_likelihood_tracer.tangential_critical_curve_list_via_zero_contour_from()
assert len(tc) > 0, "no tangential critical curves — critical-curves regression"

# Einstein radius latent variable must be finite and positive.
er = result.max_log_likelihood_tracer.einstein_radius_via_zero_contour_from()
assert np.isfinite(er) and er > 0, "Einstein radius latent unconstrained — viz regression"
```

(Exact attribute paths depend on each Analysis type — `FitInterferometer` uses
visibilities, `FitPoint` uses image-plane positions, `FitQuantity` uses the
target field. The assertion *shape* is consistent: "the JIT viz path
produced a non-zero, finite, parametrised output for each dataset type's
characteristic plot.")

### Coverage audit (as of 2026-05-17)

| Dataset | autolens_workspace_test | autogalaxy_workspace_test | Gap |
|---|---|---|---|
| Imaging | ✓ `modeling_visualization_jit.py` + `_delaunay` + `_rectangular` + `visualization_jax.py` | ✓ `modeling_visualization_jit.py` + `visualization_jax.py` | needs assertions |
| Interferometer | ✓ `modeling_visualization_jit.py` + `visualization_jax.py` | ✓ `modeling_visualization_jit.py` + `visualization_jax.py` | needs assertions |
| Point source | ✓ `modeling_visualization_jit.py` + `visualization_jax.py` | n/a | needs assertions |
| Quantity | n/a | ✓ `visualization_jax.py` only | **needs `modeling_visualization_jit.py`** + assertions |
| Ellipse | n/a | **missing both** | **needs both scripts** + assertions |

Two real coverage gaps:
1. `autogalaxy_workspace_test/scripts/ellipse/modeling_visualization_jit.py` + `visualization_jax.py` — to author.
2. `autogalaxy_workspace_test/scripts/quantity/modeling_visualization_jit.py` — to author.

Both should land alongside the assertions sweep on existing scripts.

## Phase E (longer-term, optional) — Pytree-register `ModelInstance` cascade

**Scope:** the real fix that would re-enable `use_jax_for_visualization=True`
end-to-end. Reverted PR #1278 failed because `ModelInstance` (the input to
`fit_from`) and the `Galaxy` / `LightProfile` / `MassProfile` types it carries
aren't pytree-registered, so `jax.jit(self.fit_from)(instance)` raises
`TypeError: ModelInstance not a valid JAX type`.

**Prompt file:** `autofit/model_instance_pytree_cascade.md` (to author when prior phases ship)

Cascade:
- `ModelInstance` (PyAutoFit `autofit/mapper/model.py:385`)
- `Collection` (PyAutoFit)
- `Galaxy` (PyAutoGalaxy `autogalaxy/galaxy/galaxy.py:31`)
- All `LightProfile` subclasses (`lp.*`, `lp_linear.*`, `lp_basis.*`, `lp_operated.*`)
- All `MassProfile` subclasses (`mp.*`)
- All `Pixelization` mesh classes (`Delaunay`, `RectangularUniform`,
  `KNNBarycentric`, etc.)

Scaffolding exists: `autoarray.abstract_ndarray.register_instance_pytree(cls, no_flatten=...)` is already used for `FitImaging`, `Tracer`,
`DatasetModel`, `AdaptImages`, `FitPoint`, `FitQuantity`. Extending to the
input side is mechanical — the design decision per class is which fields are
"dynamic" (parameter values → leaves) vs "static" (class identity, prior
metadata → aux). Roughly 100-200 lines + per-class tests.

Once this lands, `use_jax_for_visualization=True` default can be re-attempted
(the original PR #1278 intent). At that point, `fit_for_visualization` is
fully fused under XLA and the visualization is potentially 10-50× faster than
the current JAX-eager path.

## Phase F (deferred) — Subprocess visualization for failure isolation

The original `viz-subprocess-feasibility` task (issue #1279, closed). Banked
the picklability finding (`FitImaging` round-trips cleanly through stdlib
`pickle` on every tested model — see closed-issue comment for the spike
table).

Reasons it's not in the critical path:

- Phase A+B+C should make in-process viz fast enough for live Jupyter cells.
- Subprocess viz would still be useful for **failure isolation** (a viz bug
  doesn't take the search down) and for the long-tail of cases where viz
  somehow remains slow despite Phases A-E. If those needs become acute,
  re-enter the design from the spike findings (`mp.Process` + `Queue` with
  drop backpressure — the picklability finding makes the simplest design
  viable).

Not currently authored as a prompt. Keep the door open; do not build until
needed.

## Background

- Predecessor roadmap: `z_features/complete/jax_visualization.md` (Phases
  0-3 shipped; Phase 4 became `viz-subprocess-feasibility`).
- The 2026-05-16 Euclid all-zero-source-plane regression that triggered this
  pivot: `complete.md::jax-viz-default-broken`.
- Closed issue #1279 carries the picklability spike findings in its closing
  comment for the archaeological record.
