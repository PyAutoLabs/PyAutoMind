# `@PyAutoFit` `inv_beta_suffstats` negative-clamp branch is a no-op

Type: bug
Target: priors
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding A2).

## Problem

`@PyAutoFit/autofit/messages/beta.py:51-111` solves for `(α, β)` of a
Beta distribution given log-sufficient-statistics, by Newton-Raphson.
The post-NR guard for negative parameters is broken:

```python
# beta.py:96-110
if np.any(ab < 0):
    warnings.warn(
        "invalid negative parameters found for inv_beta_suffstats, "
        "clampling value to 0.5",
        RuntimeWarning
    )
    b = np.clip(ab, 0.5, None)   # ← writes to LOCAL `b`, not to `ab`

shape = np.shape(lnX)
if shape:
    a = ab[:, 0].reshape(shape)   # ← unpacks from `ab`, which was never updated
    b = ab[:, 1].reshape(shape)   # ← overwrites the clamp's local `b`
else:
    a, b = ab[0, :]               # ← same: ignores the clamp

return a, b
```

The `np.clip` result is bound to local `b` and immediately overwritten
two lines later when `a` and `b` are unpacked from the unmodified `ab`.
Net effect: when the warning fires, the returned `(a, b)` are still
negative.

## Wider context — how this function is called

`inv_beta_suffstats` is called from
`@PyAutoFit/autofit/messages/beta.py:241-258` —
`BetaMessage.invert_sufficient_statistics`, which is the projection
step that turns sample moments back into Beta parameters during EP /
variational updates.

Returning a negative `α` or `β` to that pipeline means:

- The reconstructed `BetaMessage(alpha=neg, beta=neg)` has an
  ill-defined PDF (Beta requires α, β > 0).
- Downstream sampling (`np.random.beta(neg, neg, ...)`) raises.
- `logpdf` evaluates to nonsense.

Whether this is reachable in practice depends on whether the NR loop
ever fails to converge. The test suite never exercises this branch
(see audit doc). The warning would fire if it ever happens, but the
intended clamp would not actually rescue the values — the next
operation downstream would still see negative parameters and crash or
silently produce garbage.

## Python reproducer

This is a Python source bug rather than a numerical one — the clearest
demonstration is reading the source and showing the local variable
mismatch. The cleanest reproducer monkey-patches `np.linalg.solve` to
force the NR loop into the negative region:

```python
# Reproducer: inv_beta_suffstats_clamp_noop.py
import inspect
import warnings

import numpy as np

from autofit.messages import beta as beta_mod

# 1) Source inspection — see the bug directly
print("=== Source of inv_beta_suffstats ===")
src = inspect.getsource(beta_mod.inv_beta_suffstats)
print(src)
print()
print("Observe: `b = np.clip(ab, 0.5, None)` writes to LOCAL `b`,")
print("then a/b are re-unpacked from `ab` (never updated) below the clamp.")
print()

# 2) Numerical demonstration: force NR off the rails so ab goes negative
print("=== Numerical demo ===")
real_solve = np.linalg.solve

def bad_solve(A, rhs):
    """Force a giant negative step so ab becomes negative."""
    return -np.ones_like(rhs) * 100.0

np.linalg.solve = bad_solve
try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        a, b = beta_mod.inv_beta_suffstats(-1.0, -1.0)

    print(f"Warning fired? {any('clampling' in str(x.message) for x in w)}")
    print(f"Returned a = {a}")
    print(f"Returned b = {b}")
    print(f"Both >= 0.5 (would be true if clamp worked)? {a >= 0.5 and b >= 0.5}")
    print(f"Both >= 0 (Beta requires positive params)? {a >= 0 and b >= 0}")
finally:
    np.linalg.solve = real_solve
```

Expected (buggy) output: the warning fires (so the branch is taken),
but the returned `a` and `b` are deeply negative — the clamp had no
effect.

## Proposed fix

Assign the clamp back to `ab`:

```python
if np.any(ab < 0):
    warnings.warn(
        "invalid negative parameters found for inv_beta_suffstats, "
        "clamping value to 0.5",   # also: typo "clampling" → "clamping"
        RuntimeWarning,
    )
    ab = np.clip(ab, 0.5, None)
```

The reviewer should consider whether silently clamping is actually the
right behaviour or whether this should raise — a Beta projection that
needed clamping to escape negative territory probably indicates a
failed fit, and silently substituting `0.5` could mask a real problem.

## What the agent picking this up should do

1. Read `@PyAutoFit/autofit/messages/beta.py` end-to-end.
2. Grep for callers of `inv_beta_suffstats` and
   `BetaMessage.invert_sufficient_statistics` across `@PyAutoFit` and
   the workspaces — list every site so the reviewer can judge whether
   "clamp" or "raise" is the right behaviour for downstream code.
3. Run the reproducer. Confirm the warning fires and the returned
   values are negative.
4. Sketch the fix above (assign `ab =`) in a scratch checkout. Re-run.
   Confirm clamp now works.
5. File the GitHub issue via `/create_issue priors/05_inv_beta_suffstats_clamp_noop.md`.
6. **In the issue body, ask the reviewer to choose between
   (a) silently clamping (preserves current intent) and (b) raising
   (more honest about a failed projection).** Either is a one-line
   change; the reviewer's preference matters.
7. **Stop. Do not implement until the clamp-vs-raise question is
   resolved.**


## Fable verdict (2026-07-08, PyAutoFit main @ 0f26ff2d8; PyAutoFit#1330)

**Verdict: CONFIRMED — fix now (severity: medium).**
Forcing NR off the rails: warning fires, returned a = b = -498.8 — the clamp
is a no-op (local `b` overwritten two lines later). One-line fix. On
clamp-vs-raise: lean **raise** — a projection that went negative is a failed
fit and silently substituting 0.5 masks it (house rule: no silent guards;
fix/expose the producer).

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
