# jax_grad build scripts raise/zero because env_vars forces PYAUTO_DISABLE_JAX=1

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: trivial
Autonomy: supervised
Priority: normal
Status: formalised

The `jax_grad/*` family was reported as gradients that raise or come back all-zeros — assumed to be
the "needs custom_jvp" lineage ([[project_jax_gradient_audit_shipped]]). **Reproduction on clean
`main` (2026-07-21, CPU fp64) overturned that premise:** every gradient script passes standalone —
`imaging_lp`, `imaging_mge`, `imaging_pixelization` (all 7 variants), `point_source`, `weak` all
match finite differences. The custom_jvp / kernel-CDF gradient-audit work already fixed the math
months ago; the `NEEDS_FIX 2026-04-10` markers are stale.

## Actual root cause (config, not library)

`autolens_workspace_test/config/build/env_vars.yaml` **defaults** set `PYAUTO_DISABLE_JAX: "1"`. Every
`jax_grad/` script drives `jax.value_and_grad(fitness.call)`. With JAX force-disabled the library uses
the numpy `xp` path while autodiff traces it → the traced array reaches numpy → `TracerArrayConversionError`.
The `jax_grad/imaging_lp` + `imaging_mge` overrides unset `PYAUTO_SMALL_DATASETS` but **forgot
`PYAUTO_DISABLE_JAX`** — unlike the `jax_likelihood_functions/` and `jax_substructure/` folder overrides,
which unset both.

One cause, both original symptoms: `imaging_lp` passes a `positions_likelihood_list` → the positions
path raises the traceback; `imaging_mge` has no positions path → the numpy value is constant w.r.t. the
tracer → **gradient all zeros**.

## Fix (workspace-only, one repo)

1. `config/build/env_vars.yaml`: replace the two per-script `jax_grad/imaging_{lp,mge}` overrides with
   one folder-level `jax_grad/` override that unsets **both** `PYAUTO_SMALL_DATASETS` and
   `PYAUTO_DISABLE_JAX` (matching `jax_likelihood_functions/`). This also correctly wires
   `imaging_pixelization`, `point_source`, and `weak`, which are un-overridden today and silently
   broken in the build sweep under `DISABLE_JAX=1`.
2. `config/build/no_run.yaml`: remove the two stale `NEEDS_FIX 2026-04-10` lines (`jax_grad/imaging_lp`,
   `jax_grad/imaging_mge`). Leave `jax_grad/interferometer.py` (SLOW) intact.
3. No `.py` script edits — they already pass.

Note: the prompt's earlier claim that `imaging_pixelization` had a `PYAUTO_SMALL_DATASETS` override in
env_vars.yaml was incorrect — it had no override at all; the folder-level pattern supplies it.
