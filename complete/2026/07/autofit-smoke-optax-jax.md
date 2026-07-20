# autofit-smoke-optax-jax — smoke matrix optax/jax fix

**Shipped 2026-07-20.** Issue [PyAutoHands#170](https://github.com/PyAutoLabs/PyAutoHands/issues/170), PR [#171](https://github.com/PyAutoLabs/PyAutoHands/pull/171) (merged `4fdc385`).

## Problem
Nightly `python_matrix` smoke failed on `autofit_workspace` across every Python version (`FAIL: searches/mle.py`, `ModuleNotFoundError: No module named 'optax'`). `searches/mle.py` gained a `MultiStartAdam` demo needing `PyAutoFit[jax]` (= `autonerves[jax]` + `optax`); the smoke job installed plain `./PyAutoFit` while Array/Lens got `[optional]`.

## Fix (PyAutoHands `.github/workflows/python_matrix.yml`, smoke_tests job only)
- Smoke install `-e ./PyAutoFit` → `-e "./PyAutoFit[optional]"` (brings optax+jax).
- Smoke matrix `3.9–3.13` → `3.11–3.13` (`autonerves[jax]` gated to ≥3.11 by design), with an explanatory comment.
- unit_tests job untouched (3.9–3.13, plain PyAutoFit — no JAX in unit tests).

## Traps / notes
- Part of the [[project_autoconf_autonerves_rename_cascade]] fallout.
- `PyAutoFit[jax]` = `['autonerves[jax]', 'optax']`; `[optional]` includes `autofit[jax]` transitively.
- Validation is deferred: `python_matrix` runs on schedule (Mon 03:00 UTC) / dispatch, so no PR check — verify on next run.
