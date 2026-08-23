# Three `jax_likelihood` pins are stale by ~1.24e-4 and fail the smoke gate on main

Type: bug
Target: workspaces
Repos:
- autolens_workspace_test
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-14 (backfilled from git)

Three `autolens_workspace_test` JAX-likelihood scripts fail their pinned-value
assertions on `main`, marginally over tolerance. They fail every local smoke
run, so the `autolens_test` workspace can never come back clean.

## Failing scripts

```
interferometer/jax_likelihood/rectangular.py
interferometer/jax_likelihood/mge.py
multi_dataset/jax_likelihood/mge.py
```

## The failure

```
AssertionError: Not equal to tolerance rtol=0.0001, atol=0
interferometer/rectangular: JAX vmap likelihood mismatch
 [0]: -3163.8939270532364 (ACTUAL), -3164.286252 (DESIRED)
Max absolute difference among violations: 0.39232495
Max relative difference among violations: 0.00012399
```

**1.24e-4 against an rtol of 1e-4** — 24% over the tolerance, not a
qualitatively broken computation. The likelihood has drifted slightly since the
constants were pinned (or the pin was recorded at lower precision: `-3164.286252`
is 10 significant figures while the computed value carries 17).

## Confirmed pre-existing

Reproduced with `pyauto-heart smoke autolens_test` under two roots — a feature
worktree and canonical `main` — producing **byte-identical** ACTUAL and DESIRED
values in both. Not caused by any in-flight branch.

## Scope

- Decide per script whether the pin is stale (re-pin) or the drift is a real
  regression (investigate). **Do not blanket re-pin** — the point of an absolute
  pin is to notice exactly this, and 4e-4 on an interferometer likelihood may be
  a genuine numerical change worth understanding first. Bisect the value before
  overwriting it.
- Check whether the pins were recorded at reduced precision; if so, the fix is
  to re-record at full precision rather than to widen the tolerance.
- Widening `rtol` is the tempting move and the wrong first move — it would hide
  the next drift too.
- Audit the **other** `jax_likelihood` pins in the same sweep; three failing
  together suggests a shared cause, and the rest may be sitting just inside
  tolerance.

## Provenance

Found while running the smoke gate for PyAutoFit#1473 (MultiStartGradient NaN
step diagnostics). Unrelated to that change — the failing scripts contain no
`MultiStart` reference, and the control run against `main` matched exactly.

Related but distinct: `draft/test/workspaces/restore_workspace_test_likelihood_baselines.md`
covers restoring *removed* NumPy baselines; this is about *existing* JAX pins
having drifted out of tolerance.
