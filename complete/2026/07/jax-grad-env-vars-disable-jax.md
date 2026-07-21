# jax_grad build scripts un-broken: env_vars forced PYAUTO_DISABLE_JAX=1

**Shipped:** 2026-07-21 · **Issue:** PyAutoLabs/autolens_workspace_test#188 · **PR:** #189 (merged) · **Type:** bug (config) · **Repos:** autolens_workspace_test

## What & why

The `jax_grad/*` gradient-correctness scripts were flagged (`NEEDS_FIX`) as raising or
returning all-zero gradients, assumed to be the "needs `custom_jvp`" lineage (the Brain
sized it "too-large, split into phases"). **Reproduction on clean `main` overturned the
premise** — the gradient math already passes. The real failure was a workspace **config**
bug: `config/build/env_vars.yaml` defaults set `PYAUTO_DISABLE_JAX: "1"`, and the
`jax_grad/imaging_{lp,mge,pixelization}` overrides unset `PYAUTO_SMALL_DATASETS` but
forgot `PYAUTO_DISABLE_JAX` (unlike the `jax_likelihood_functions/` folder override). With
JAX force-disabled the library takes the numpy `xp` path while `jax.value_and_grad` traces
the likelihood, so the traced input is never differentiated:
- `imaging_lp` (positions path) → `jax.errors.TracerArrayConversionError`
- `imaging_mge` / `imaging_pixelization` (no positions path) → all-zero gradient

One cause, all three original symptoms.

## Fix (2 config files, no `.py`/library edits)

- `config/build/env_vars.yaml`: three per-script `jax_grad/imaging_{lp,mge,pixelization}`
  overrides → one folder-level `jax_grad/` override, `unset: [PYAUTO_SMALL_DATASETS,
  PYAUTO_DISABLE_JAX]` (mirrors `jax_likelihood_functions/`). Also wires `point_source` +
  `weak`, previously un-overridden and silently broken.
- `config/build/no_run.yaml`: removed three stale `NEEDS_FIX` markers (lp/mge 2026-04-10,
  pixelization 2026-07-21). `jax_grad/interferometer.py` (SLOW) left intact.

## Validation

Clean `main`, CPU fp64. Fixed env (JAX on, full data): `imaging_lp`, `imaging_mge`,
`imaging_pixelization` (7/7 variants), `point_source`, `weak` all pass AD=FD. Build-default
env (`PYAUTO_DISABLE_JAX=1`): `imaging_lp` raises `TracerArrayConversionError`;
`imaging_pixelization` fails variant A with `AssertionError: Gradient is all zeros` —
reproducing the original markers.

## Decisions / gotchas

- **Folder-level over per-script** (user-chosen): matches `jax_likelihood_functions/`;
  fixes the whole folder including two scripts the prompt didn't name.
- **Stale local checkout:** my local `main` was behind `origin/main`; PR #186 (merged the
  same day) had added the third (pixelization) marker. Re-based onto `3d8d604` (PR #186
  touched only the two YAMLs — scripts unchanged, so repro stayed valid).
- **Concurrent worktree** alongside the unrelated `viz-refactor-asserts-1280` (non-overlapping files).
- **Heart RED at ship:** all reasons pre-existing/unrelated; opened under the corrective-PR
  exception for `58 stale parked script(s)` (this PR removes 3). Merge was human.

## Follow-ups

- None required. `jax_grad/interferometer.py` stays SLOW-skipped (a timing issue, unrelated
  to this cause; its env is now also correct via the folder override).
- Broader signal: the `58 stale parked script(s)` Heart reason likely hides more
  already-fixed markers (cf. the pix-not-positive-definite cluster #140, also all-stale).

## Original prompt

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
