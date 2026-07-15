# MultiStartAdam.py fails the mode=release validation shard — release profile forces PYAUTO_DISABLE_JAX=1

Type: bug
Target: autofit_workspace_test
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

Original request (verbatim): *"do the blocking env fixes first"* — the blocking item from the
`/morning` digest of 2026-07-15.

## Symptom

`nightly-release` has failed five nights running (2026-07-11 → 2026-07-15). Stage 3
(release-fidelity integration) dispatches PyAutoHeart `workspace-validation.yml` at
`mode=release`; exactly one shard fails — `run_scripts (3.12, autofit_test, searches)`:

```
scripts/searches/MultiStartAdam.py ...   FAIL (1.7s)
ValueError: MultiStartAdam is a JAX-native gradient search and requires a JAX-traceable
Analysis (e.g. `AnalysisImaging(..., use_jax=True)`). The supplied analysis is not running
on the JAX backend.
```

Latest failing runs: PyAutoBrain nightly `29390030719` → PyAutoHeart validation `29390440297`
(job `87272559383`). Every other shard in that run is green.

This is **not** the shifting perf-flake tail tracked in the release-tail epic (Heart #72) —
it is a fresh, deterministic regression introduced by the multi-start gradient search
promotion (PyAutoFit #1370 and its workspace follow-ups, merged 2026-07-14).

## Root cause

`MultiStartAdam._fit` hard-guards on the JAX backend
(`PyAutoFit/autofit/non_linear/search/mle/multi_start_gradient/search.py:120-126`):

```python
if not getattr(analysis, "_use_jax", False):
    raise ValueError(...)
```

`autofit_workspace_test/config/build/env_vars_release.yaml` (the `mode=release` profile —
**not** `env_vars.yaml`, which is the per-PR smoke profile) pins:

- `PYAUTO_TEST_MODE: "0"` — real searches, so `AbstractSearch.fit` does **not** take the
  `mode >= 2` bypass at `abstract_search.py:683-689` and `_fit` really runs.
- `PYAUTO_DISABLE_JAX: "1"` — forces `use_jax=False`, so the script's
  `af.ex.Analysis(..., use_jax=True)` is silently flipped and the guard fires.

The profile re-enables JAX for exactly two patterns — `jax_assertions/` and
`searches/BlackJAXNUTS` — via `set: { PYAUTO_DISABLE_JAX: "0" }`. `searches/MultiStartAdam`
was never added, so the new script inherits the disabling default.

## Why sibling scripts do not fail

- `autofit_workspace/scripts/searches/mle.py` also uses `af.MultiStartAdam` with
  `use_jax=True`, but that workspace's `env_vars_release.yaml` pins
  `PYAUTO_DISABLE_JAX: "0"` as its default — JAX is on, so it passes.
- `autolens_workspace` / `autogalaxy_workspace` `scripts/guides/modeling/searches.py`
  construct `af.MultiStartAdam` but never call `.fit()` — config-only, so the guard is
  never reached.

## Fix

Scope settled with the human 2026-07-15 (`/morning` → `/start_dev … --auto`). Three parts.

### 1. Release profile — unblock MultiStartAdam (the blocking fix)

Add an override to `autofit_workspace_test/config/build/env_vars_release.yaml`, mirroring
the `searches/BlackJAXNUTS` precedent directly above it:

```yaml
  - pattern: "searches/MultiStartAdam"
    set: { PYAUTO_DISABLE_JAX: "0" }
```

Note the profile's own documented convention: overrides here only ever `set:` (never
`unset:`) a var that `defaults` pins.

### 2. Release profile — close the vacuous-JAX gap on the sibling scripts

`searches/Dynesty_jax.py` and `searches/Nautilus_jax.py` also declare `use_jax=True` but are
absent from the release-profile overrides, so under `PYAUTO_DISABLE_JAX=1` they validate the
NumPy path while presenting as JAX tests — the same failure mode the profile's own
`jax_assertions/` comment describes. Unlike `MultiStartAdam` they carry no hard guard, so
they pass vacuously and nothing fails loudly. Give them the same `set:` override.

**Each must be verified to actually pass with JAX enabled.** These have (as far as we know)
never run their JAX path in CI, so a real failure may be hiding behind the vacuous pass. If
one does fail, do not paper over it: surface it as its own bug and leave that script's
override out of this PR rather than shipping a knowingly-red shard.

### 3. Smoke profile — make the per-PR gate able to catch this class of bug

Under `env_vars.yaml` (smoke), `PYAUTO_TEST_MODE: "2"` bypasses the sampler entirely, so
`MultiStartAdam.py` passes without ever executing its JAX path. That is *why* this reached
night five: the per-PR gate structurally could not catch it. Follow the `searches/BlackJAXNUTS`
precedent so the script really runs:

```yaml
  - pattern: "searches/MultiStartAdam"
    unset: [PYAUTO_TEST_MODE, PYAUTO_DISABLE_JAX]
```

Human's call, explicitly: it should not stay bypassed if running it is what ensures the bug
is caught. Scoped to `MultiStartAdam` only — the nested samplers (`Dynesty_jax`,
`Nautilus_jax`) stay bypassed under smoke on cost grounds.

## Acceptance

- `scripts/searches/MultiStartAdam.py` passes under the release profile
  (`PYAUTO_TEST_MODE=0`, `PYAUTO_DISABLE_JAX=0`) and recovers the truth basin
  (centre≈50, normalization≈25, sigma≈10).
- `Dynesty_jax.py` and `Nautilus_jax.py` each verified green with `PYAUTO_DISABLE_JAX=0`, or
  the failure surfaced as a separate bug and that override withheld.
- `MultiStartAdam.py` really executes (not bypassed) under the smoke profile.
- The `autofit_test/searches` shard goes green; `nightly-release` reaches Stage 3 clean.
