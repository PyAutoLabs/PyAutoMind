# python_matrix smoke fails: autofit_workspace searches/mle.py needs optax not in smoke env

Type: bug
Target: autofit_workspace
Repos:
- autofit_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

The nightly `python_matrix` (PyAutoHands) smoke matrix fails on `autofit_workspace`
across **every** Python version (3.9–3.13), while `autolens_workspace` and
`autogalaxy_workspace` pass. Deterministic, single failing script.

## Evidence

Run 29721343824 → `1 smoke test(s) failed`, `FAIL: searches/mle.py`:

```
File ".../PyAutoFit/autofit/non_linear/search/mle/multi_start_gradient/search.py", line 129, in _fit
ModuleNotFoundError: No module named 'optax'
...
ImportError: MultiStartAdam requires the optional `jax` and `optax` dependencies.
Install them with `pip install autofit[jax] optax`.
```

`searches/mle.py` demonstrates `MultiStartAdam`, a JAX/optax gradient search. The
smoke matrix installs the release wheels **without** the `[jax]`/`optax` extras,
so the script raises a (correct, helpful) ImportError at runtime and the smoke
job fails.

## Fix locus — decide (do NOT degrade the user-facing script)

`MultiStartAdam`'s ImportError is correct behaviour — do not add a silent guard
or mask it. Two clean options:
1. **Exclude `searches/mle.py` from the numpy-only smoke set** — it's a JAX/optax
   demo, in the same class as other JAX-requiring scripts already kept out of the
   curated smoke subset (see the smoke-tests-are-a-small-curated-subset and
   no-JAX-in-unit-tests conventions). Preferred if the smoke matrix is meant to
   stay dependency-light.
2. **Install the extras for the autofit_workspace smoke job** — add
   `autofit[jax] optax` (or `autonerves[jax]`) to that matrix leg's install step
   in PyAutoHands `python_matrix.yml` so the demo runs as intended.

Confirm which smoke-tier `searches/mle.py` belongs to, then apply the matching
fix. Check whether other new JAX/optax search demos (`searches_minimal/*` in the
developer workspace are already excluded) have the same exposure.

## Validation

Re-run the `python_matrix` `autofit_workspace` leg (or the workspace's smoke
runner) and confirm `searches/mle.py` no longer fails the job.

<!-- filed from /wake_up overnight-failure triage on 2026-07-20 -->
