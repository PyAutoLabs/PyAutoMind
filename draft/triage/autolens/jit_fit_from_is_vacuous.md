# `jax.jit(analysis.fit_from)` is vacuous in the jax_likelihood scripts

Type: triage
Target: autolens
Repos:
- autolens_workspace_test
- autogalaxy_workspace_test
Themes:
- testing
- jax
Difficulty: medium
Autonomy: human-required
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: no
Filed: 2026-09-10

Found independently by two agents during `/ci_speedup` (2026-09-10). Filed as
triage because it is a **possible coverage gap, not a speed-up** — and fixing it
would change what the scripts assert, which is a human's call.

## The observation

The "Path A" blocks are titled `jit-wrap analysis.fit_from` and print
`PASS: jit(fit_from) round-trip`. But `jax.jit(analysis_jit.fit_from)` traces
**only the `FitImaging`/`FitInterferometer` constructor**:

- the jitted call itself measures **0.018s** (autolens `imaging/jax_likelihood/delaunay.py`)
  and traces in **2.5ms** over ~85 scalar inputs (autogalaxy `interferometer/jax_likelihood/delaunay_mge.py`)
- `log_likelihood` is a lazy `cached_property`, so the likelihood is computed
  **eagerly, op by op, outside the jit** — 471 and 493 separate XLA dispatches
  respectively, after the jitted call has already returned

So the block currently exercises an *eager*-JAX round-trip, not a JIT one.

## Why it was not "fixed"

Making the jit real —
`jax.jit(lambda i: analysis_jit.fit_from(i).log_likelihood)` — was measured:
2.43s instead of 13.8s cold, ~11.4s saved. It was **rejected** because it
returns a different number:

```
eager (shipped) : -44.320055417402159   numpy: -44.320055417392268  (rel 2.2e-13)
real jit        : -44.320055403729270                               (rel 3.1e-10)
```

`rtol=1e-8` would still pass, but the **printed value changes**, and it
invalidates the assertion's own written rationale ("differs only by fp reduction
ordering (~1e-13 relative, measured)", which accurately describes the eager
path). It also narrows coverage: the shipped code proves a `FitImaging` pytree
survives the jit boundary.

## The question for a human

Was the intent a genuine `jit(fit_from)` round-trip? If yes, this is a real
coverage gap across the `jax_likelihood` family in both test workspaces, and
closing it happens to be worth ~11s per script. If the intent was the pytree
boundary check, the docstring and the `PASS` message should say so.
