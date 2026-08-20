- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1489 (auto-closed by the merge's `Closes` line)
- completed: 2026-08-18
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1490 (MERGED, merge c302f51d, `pending-release`)
- notes: REGRESSION fix, shape A from the issue — strict NumPy-path bounds restored in the priors
  themselves. `UniformPrior.log_prior_from_value` and `LogUniformPrior.log_prior_from_value` now
  return `-inf` outside `[lower_limit, upper_limit]` on the NumPy path, mirroring the JAX path;
  `Fitness.log_likelihood_from` skips the prior subtraction when the prior sum is non-finite
  (`-inf - -inf = NaN` guard); dated corrections to the false "MCMC samplers reject -inf" sentence
  in `clipper.py` and in this repo's `complete/2026/08/prior-support-clipper.md`; stale BFGS
  comment updated. New `test_autofit/mapper/prior/test_prior_bounds_1489.py` (scalar/array bounds,
  -inf FoM for out-of-box vectors, NaN-free inversion, end-to-end Emcee containment) plus updates
  to `test_prior.py` and `test_clipper.py` where they pinned the broken behaviour (the LBFGS test's
  foil literally asserted the clipper-less fit escapes the box).
- archaeology (the load-bearing finding, full trail in issue #1489 comments): NOT long-standing
  behaviour as the prompt claimed — the box was enforced until release 2025.10.16.1 via
  `assert_within_limits`/`PriorLimitException(FitException)` in `instance_from_vector` (Fitness
  caught it → resample `-inf` → MCMC rejection; the 2019 docstring said so). The guard was deleted
  2025-06-20 (`5d85b80c3` + `30d470360`, JAX jit-compat cleanup — its JAX arm was a
  `jax.debug.callback` hack; its tests were deleted with it so nothing went red), landed on main
  via PyAutoFit#1155 (2025-10-06), first shipped 2025.10.16.1. `2e3540771` (2026-05-14) then
  re-added strict bounds on the JAX path only ("NumPy paths preserved exactly"), creating the
  asymmetry the prompt observed and mis-dated. Exposure window: NumPy-path Emcee/Zeus/Drawer/LBFGS
  fits on autofit >= 2025.10.16.1 with poorly-constrained parameters under a Uniform/LogUniform box.
- evidence: reproduced on main @ fe9f813 (identical finite log posterior in/out of box; Emcee
  30x600 with an unconstrained parameter under UniformPrior(-0.1, 0.1): 100% of accepted samples
  outside, runaway to |offset| ~ 1e14 — the stretch move grows exponentially in an unpenalised flat
  direction). Counter-check on autofit 2025.5.10.1 (pre-regression): PriorLimitException raised,
  objective -inf, 0/630 samples escape. Post-fix (same script/seed): 0/540 escape, contained to
  [-0.0997, 0.0999]; well-constrained 3-param reference fit posterior statistically unchanged
  (median shifts ~0.02 against sigma ~0.1-0.5). Full suite 1734 passed / 8 skipped; the 2 failures
  (test_messages::test_beta, test_nautilus::test__single_core_builds_no_pool) are
  missing-optional-dependency env failures reproducing identically on untouched main.
- merge-context: merged 2026-08-18 ~16:11 UTC on explicit human authorization ("pr ci green and
  merge") with all 3 checks green (unittest 3.12, unittest 3.13, docs-build). Web session — no
  local worktree; branch `claude/uniformprior-bounds-numpy-1n1u3s` pushed directly. The human also
  overrode the worktree-conflict guard (PyAutoFit was claimed by stored-sample-reconstruction-guard
  and version-stamp-sync-guards; change surface disjoint from both).
- follow-ups (filed/known at completion):
  1. Shape C deliberately deferred: default `LBFGS` to `ClipperPriorBox` (the
     adjacent identifier question was decided 2026-08-18 — record
     `complete/2026/08/clipper-in-search-identifier.md`). With strict priors and
     `ClipperNone`, an LBFGS step out of the box now sees an infinite objective — C gives scipy
     declarative bounds instead.
  2. Workspace smoke literal risk: `*_workspace_test` scripts that pin literal values from
     Emcee/Zeus/LBFGS chains may shift on the next nightly against the merged main — triage any
     new mismatches against this change before rebaselining.
  3. Released-results caveat for users: fits run on autofit 2025.10.16.1 → 2026.8.x with Emcee/
     Zeus/Drawer/LBFGS and poorly-constrained box-bounded parameters may have sampled outside the
     declared prior; worth a release-notes line when this ships to PyPI.
  4. `test_beta` + `test__single_core_builds_no_pool` fail on clean main without optional deps
     (sympy?/nautilus-sampler absence) — hygiene candidate: skip-if-missing markers.

## Original prompt

# UniformPrior bounds are not enforced in the objective on the NumPy path

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised

## What this is

`UniformPrior.log_prior_from_value` short-circuits to `return 0.0` whenever
`xp is np`, **without ever evaluating the bound**
(`autofit/mapper/prior/uniform.py`, in the `if xp is np:` branch). The JAX path
immediately below it does the right thing:

```python
def log_prior_from_value(self, value, xp=np):
    if xp is np:
        return 0.0
    in_bounds = (value >= self.lower_limit) & (value <= self.upper_limit)
    return xp.where(in_bounds, xp.zeros_like(value), -xp.inf)
```

So for a value outside the box:

- NumPy: `sum(log_prior) == 0.0` — **not penalised**
- JAX: `-inf` — correctly penalised

Per prior type on the NumPy path, outside support:

| prior | NumPy result outside support | penalised? |
|---|---|---|
| `UniformPrior` | `0.0` | **no** |
| `LogUniformPrior` above `upper_limit` | finite `-log(value)` | **no** |
| `LogUniformPrior` below `0` | `-inf` | yes |
| `TruncatedGaussianPrior` | `-inf` | yes |
| `GaussianPrior` | unbounded by design | n/a |

`LogUniformPrior`'s own docstring already states this outright — "The NumPy path
is otherwise unnormalised and **unbounded** … The JAX path **additionally**
returns `-inf` outside `[lower_limit, upper_limit]`" — so the asymmetry is
documented there and undocumented for `UniformPrior`.

**No other guard exists.** `instance_from_vector` accepts an out-of-box vector
without raising; Emcee and Zeus have no bounds handling of their own; and the
strict `logpdf` (which *does* return `-inf`) is used only by the messages / EP
machinery, never by the search fitness path.

## Who is exposed

For searches with `fom_is_log_likelihood=False`:

| search | UniformPrior box enforced? |
|---|---|
| Emcee, Zeus, Drawer | **no** |
| LBFGS / BFGS | only if a clipper is set — the default `ClipperNone` passes `bounds=None`, so **no** |
| BlackJAXNUTS, `MultiStartGradient` (JAX) | yes (`-inf`) |
| Nautilus, Dynesty | unaffected — they propose in the unit cube |

## This corrects the phase-1 record

`complete/2026/08/prior-support-clipper.md` claims "the MCMC samplers reject
`-inf` proposals so the walker simply stays put". **There is no `-inf` to reject
for a `UniformPrior` on the NumPy path.** That sentence is the load-bearing
justification for why the clipper was scoped to the gradient searches only, and
it is wrong for the reason above.

## Severity, honestly

Not "results are wrong" — "the sampled posterior may not be the declared model".
Walkers are *initialised* within limits and the likelihood usually falls away
outside the sensible region, so the exposure is for **poorly-constrained
parameters** — exactly the ones that diffuse to the walls. Nautilus and Dynesty
are unaffected and are the production workhorses, so the blast radius is
Emcee / Zeus / Drawer / LBFGS users.

**NOT VERIFIED:** whether any real past fit actually drifted outside a box. The
mechanism is unguarded; that it has bitten is unproven. Establishing that is the
first task, not an assumption.

## Not a regression

Git history puts the NumPy `return 0.0` **before** the May-2026 JAX
`xp`-dispatch commit that made the JAX side strict. The asymmetry was created by
tightening JAX, not by loosening NumPy. This is long-standing behaviour.

## Why this is not fixed inline

Making the NumPy path strict changes behaviour for **every existing Emcee / Zeus
/ LBFGS run**. A walker that currently wanders outside a box and comes back would
start being rejected; chains, acceptance rates and stored results all move. That
is a deliberate, measured change with its own before/after, not a drive-by.

## Orthogonal to per-parameter step scaling — keep them straight

Emcee is **immune** to the step-scaling problem (affine invariance) and **fully
exposed** to this one. A search can be immune to one and exposed to the other. Do
not let this be absorbed into `active/per_parameter_step_scaling.md`.

## Suggested shape of the work

1. **Reproduce first.** Run an Emcee fit with a deliberately unconstrained
   parameter under a narrow `UniformPrior` and show samples outside the box. If
   it cannot be reproduced, say so — the mechanism would still be worth closing,
   but the framing changes.
2. Decide the fix: strict NumPy path (behaviour change, needs a measured
   before/after) versus a `Clipper`-style opt-in for the NumPy searches versus
   making `LBFGS` default to a real clipper. These are not equivalent and the
   choice is a human one.
3. Whichever lands, correct the phase-1 record's "MCMC samplers reject `-inf`"
   sentence — it is cited elsewhere as a reason the clipper was scoped narrowly.

## Out of scope

- Per-parameter step scaling (`active/per_parameter_step_scaling.md`).
- Changing `Prior` classes in a way that alters the nested samplers, where the
  hard box currently works correctly.

## CORRECTION (2026-08-18, deep-dive on the issue): this IS a regression

The "Not a regression" section above is **wrong** — it looked only at
`log_prior_from_value`'s own history. The enforcement never lived there: from
2019 the `return 0.0` docstring said the bound "is check[ed] for when the
instance is made (in the `instance_from_vector` function)" —
`Prior.assert_within_limits` raised `PriorLimitException(FitException, ...)`,
`Fitness` caught `FitException` and returned `-inf`, and the MCMC samplers
rejected it. The phase-1 sentence was TRUE under that mechanism.

The guard was deleted on 2026-06-20's timeline as follows: commits `5d85b80c3` +
`30d470360` (2025-06-20, JAX jit-compat cleanup — the guard's JAX arm was a
`jax.debug.callback` hack; its tests were deleted with it, so nothing went red),
merged to main in PyAutoFit#1155 (2025-10-06), **first shipped in release
2025.10.16.1** (previous release 2025.5.10.1). `2e3540771` (2026-05-14) then
re-added strict bounds on the JAX path only ("NumPy paths preserved exactly"),
creating the asymmetry this prompt observed and mis-read as long-standing.

Empirical before/after (same script/seed): autofit 2025.5.10.1 →
`PriorLimitException`, objective `-inf`, 0/630 Emcee samples escape; main
@ fe9f813 → no error, finite identical objective, 450/450 samples escape to
~1e14. Exposure window: every NumPy-path Emcee/Zeus/Drawer/LBFGS(-no-clipper)
fit on autofit >= 2025.10.16.1. Full archaeology:
https://github.com/PyAutoLabs/PyAutoFit/issues/1489#issuecomment-5329318098
