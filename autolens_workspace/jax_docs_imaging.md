# Phase 3a — `__JAX__` sections in `autolens_workspace/scripts/imaging/*.py`

The canonical per-dataset-type doc pass. Adds `__JAX__` sections to the
four user-facing imaging scripts. Sister prompts (3b interferometer, 3d
point_source) mirror this structure with dataset-specific adjustments.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md` (admin_jammy
main `f381393`). Sections 3.1 (principles), 3.3 (Analysis path), 3.4
(Simulator path), 3.4.1 (JIT-it-yourself, advanced — points to lens_calc.py)
all apply.

**Depends on Phase 2 shipped** — the `__JAX Variant__` code blocks in
`simulator.py` use `al.SimulatorImaging(..., use_jax=True)`, which only
exists once Phase 2 (`autoarray/simulator_use_jax.md`) has landed in
PyAutoArray + PyAutoLens main.

**Run in Opus** per [[feedback_tutorial_prose_opus]] — workspace tutorial
prose, science-teaching narrative.

## Scope

**In scope** (four files in `autolens_workspace/scripts/imaging/`):

1. `start_here.py` — extend the existing `__JAX__` sections at lines 33,
   240 to align with the Phase 0 contract. Today the section is
   under-documented; refresh per principle 1 (JAX is default) and reference
   Phase 1's top-level `start_here.py` `__JAX__` block as the canonical
   conceptual home.
2. `simulator.py` — add `__JAX__` section + `__JAX Variant__` code block.
   This is the file most changed by Phase 2; the variant shows
   `SimulatorImaging(use_jax=True)` + `@jax.jit` in the canonical form.
3. `fit.py` — add `__JAX__` section explaining that the
   `al.AnalysisImaging(dataset=dataset)` line is already running JAX (the
   `use_jax=True` default), and the search driver does the JIT internally.
   Code is unchanged; the addition is prose.
4. `likelihood_function.py` — add `__JAX__` section covering the hand-rolled
   `@jax.jit` pattern around a user's own `log_likelihood(instance)` function.
   Reference `fitness._vmap` as the validation pattern per
   [[feedback_jax_validation_vmap_not_jit]].

**Out of scope:**

- `features/` subdirectory under `imaging/`. Phase 3a touches the four
  top-level dataset scripts; per-feature scripts are left for follow-on
  passes (or never — they're not always tutorial scripts).
- `modeling.py`. Today it imports the analysis and runs a search; same
  framing as `fit.py`. If the prose addition is identical, link both to
  the same `__JAX__` text and don't duplicate.
- `data_preparation/`, `data_preparation.py`. Not JAX-relevant.
- The notebook regeneration. Notebooks regenerate from `.py` via the
  `/generate_and_merge` skill during the ship pass; this prompt edits
  only `.py` files.
- The pytree story (principle 2). That's Phase 5a (`data_structures.py`
  guide). Cite, don't duplicate.

## Files

### 1. `autolens_workspace/scripts/imaging/start_here.py`

Existing `__JAX__` content at lines 33+ and 240+ needs to be refreshed
against the Phase 0 contract. Specifically:

- Lead: "If you installed `autolens[jax]`, your modeling fits are already
  JAX-accelerated by default. No action needed."
- Cross-reference: link to the top-level
  `autolens_workspace/start_here.py` `__JAX__` block (Phase 1) as the
  canonical principles home.
- Link forward to `simulator.py`'s `__JAX Variant__` for the
  "I want fast simulations too" case.
- Drop any prose that contradicts the Phase 0 contract (e.g. anything
  framing JAX as opt-in, anything showing `xp=` at the user surface).

Length: 30-50 lines of prose.

### 2. `autolens_workspace/scripts/imaging/simulator.py`

Two additions:

**(a) `__JAX__` prose section near the top.** Explains the
NumPy default for simulations and points to the `__JAX Variant__`
at the bottom of the script for the fast path:

```python
"""
__JAX__

By default this script runs simulation entirely on NumPy — readable, no
JAX dependency required. For an order-of-magnitude speedup on large or
repeated simulations (parameter sweeps, mock-data studies, batch figure
generation), see the `__JAX Variant__` block at the end of this script,
which shows the canonical `@jax.jit + SimulatorImaging(use_jax=True)`
pattern.

Modeling fits are JAX-accelerated by default — see
`autolens_workspace/start_here.py` `__JAX__` section for the principles.
"""
```

**(b) `__JAX Variant__` code block at the end of the script.** Runnable;
shows the post-Phase-2 API:

```python
"""
__JAX Variant__

For fast repeated simulations, wrap `SimulatorImaging.via_tracer_from`
in `@jax.jit` and pass `use_jax=True` to the simulator constructor.
The simulator handles pytree registration internally — you write nothing
JAX-specific beyond the decorator.
"""
import jax

simulator_jax = al.SimulatorImaging(
    exposure_time=300.0, psf=psf, background_sky_level=0.1, use_jax=True
)

@jax.jit
def simulate(tracer):
    return simulator_jax.via_tracer_from(tracer=tracer, grid=grid)

dataset_jax = simulate(tracer)
aplt.fits_imaging(
    dataset=dataset_jax, data_path=..., overwrite=True
)
```

Verify the variant runs end-to-end once Phase 2 has shipped — the prompt
author should run the script and confirm both the NumPy path (existing
code) and the new JAX variant produce equivalent datasets.

### 3. `autolens_workspace/scripts/imaging/fit.py`

Single `__JAX__` prose section near the top:

```python
"""
__JAX__

The `al.AnalysisImaging(dataset=dataset)` constructed in this script
defaults to `use_jax=True` — your fit is JAX-accelerated automatically if
you installed `autolens[jax]`. The non-linear search driver wraps the
likelihood function in `jax.vmap(jax.jit(...))` internally, so batches of
parameter vectors evaluate in parallel.

Watch the log output: `JAX: Applying vmap and jit to likelihood function`
indicates the JIT compile started; subsequent likelihood calls reuse the
compiled trace.

If JAX is not installed (older Python, or `[jax]` extra not picked up),
the analysis warns once and falls back to NumPy. Force NumPy explicitly
with `al.AnalysisImaging(dataset=dataset, use_jax=False)` or
`PYAUTO_DISABLE_JAX=1` — useful when debugging, since NumPy stack traces
are easier to read than JAX traces.

See `autolens_workspace/start_here.py` `__JAX__` section for the broader
principles.
"""
```

No code changes — prose only. The same block applies to `modeling.py`
verbatim (or near-verbatim); if so, just copy.

### 4. `autolens_workspace/scripts/imaging/likelihood_function.py`

`__JAX__` section near the end of the file (after the chi-squared walkthrough
is complete and the validated `fit.log_likelihood` is shown):

```python
"""
__JAX__

The hand-rolled `log_likelihood` you've assembled in this script can be
JAX-accelerated by wrapping it in `@jax.jit`. The pattern:

```python
import jax
import jax.numpy as jnp

# One-time setup: trigger pytree registration for Tracer / Galaxy /
# light-and-mass-profile classes. The AnalysisImaging path does this
# automatically, but a hand-rolled likelihood doesn't go through Analysis.
# An al.AnalysisImaging(dataset=dataset, use_jax=True) instantiation at the
# top of the script is the simplest trigger today; a dedicated
# al.jax.enable_for_modeling() helper is planned (Phase 2 open question).

@jax.jit
def my_log_likelihood(instance):
    tracer = al.Tracer(galaxies=instance.galaxies)
    fit = al.FitImaging(dataset=dataset, tracer=tracer)
    return fit.log_likelihood

# Validate the JAX path matches your NumPy chi-squared:
from autofit.non_linear.fitness import Fitness
fitness = Fitness(model=model, analysis=al.AnalysisImaging(dataset=dataset),
                  fom_is_log_likelihood=True)
log_l_jax = fitness._vmap(jnp.array([instance_parameters]))[0]
```

`fitness._vmap` is the production validation pattern — it traces through
the full vmap(jit(call)) path that the non-linear search uses, exposing
any un-threaded `xp` sites that a single `jax.jit(fn)(concrete)` call
would hide.

For JIT-ing library methods directly (not via FitImaging), see
`scripts/guides/lens_calc.py` `__JAX__` section.
"""
```

The closing reference is to Phase 5d's `lens_calc.py` guide.

## Validation

After all four files have their `__JAX__` sections:

1. **All four scripts run on NumPy** end-to-end:
   ```bash
   NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
   python autolens_workspace/scripts/imaging/start_here.py
   # repeat for simulator.py, fit.py, likelihood_function.py
   ```
2. **The `simulator.py` `__JAX Variant__` block runs** end-to-end on JAX
   (requires Phase 2 shipped). Add a `PYAUTO_DISABLE_JAX=1` guard if the
   user might run the script without JAX installed.
3. **`scripts/check_sizes.sh`** in `autolens_workspace` passes — each
   script grew, didn't shrink.
4. **`/smoke_test`** against the workspace passes — the imaging start_here
   and fit are in the curated smoke set; adding prose shouldn't break them.

## References

- Phase 0 design doc: `admin_jammy/notes/jax_interface.md`, especially
  §3.3 (Analysis path), §3.4 (Simulator path), §3.4.1 (JIT-it-yourself —
  cited in `likelihood_function.py` `__JAX__` section).
- Phase 1 (already-shipped sibling): `PyAutoPrompt/workspaces/jax_start_here_intros.md`
  — top-level `autolens_workspace/start_here.py` `__JAX__` block.
- Phase 2 (library dependency): `PyAutoPrompt/autoarray/simulator_use_jax.md`
  — must ship before this phase's `simulator.py` `__JAX Variant__` works.
- Phase 5d (downstream cross-reference): Phase 5d's `lens_calc.py` guide
  is the canonical home for the `@jax.jit + xp=jnp` JIT-it-yourself pattern;
  this phase's `likelihood_function.py` `__JAX__` section links to it.

## Out-of-band notes

- Bulk-edit safety per `autolens_workspace/CLAUDE.md` — these are
  per-file Edit calls, not Write rewrites. The `scripts/check_sizes.sh`
  guard catches accidental shrinkage.
- Notebooks regenerate via `/generate_and_merge` during the workspace ship
  pass; this phase ends at `.py` edits + smoke test pass.
