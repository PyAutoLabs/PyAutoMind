# log_likelihood_ceiling: ship the guard OFF by default — the ceiling is not unit-safe

Target: PyAutoFit
Type: bug
Autonomy: safe
Issued: 2026-08-29

## Original request (verbatim)

sounds good let me know if you think we need it in actual autolsns analysis once we have more results

## The problem

PR #1545 (merged `b70cf7fc3`) added a magnitude ceiling to `Fitness.call` and to
`nss_log_likelihood_from`: a *finite* log likelihood whose `|value|` exceeds
`general.test.log_likelihood_ceiling` is mapped to the resample figure of merit.
It shipped enabled, at `1.0e+20`.

That threshold is **not unit-safe**. A log likelihood is
`-0.5 * chi_squared - 0.5 * noise_normalization`, and both terms scale with the
noise-map units:

- `chi_squared = sum(((data - model) / noise)**2)` grows as `noise**-2`;
- `noise_normalization = sum(log(2 * pi * noise**2))` grows linearly in the pixel
  count and logarithmically in the noise scale.

So a dataset whose noise map is expressed in a badly-scaled unit (a very small
noise value, e.g. counts vs electrons vs Jy) can produce a legitimate log
likelihood above `1e20` and have every model silently rejected as numerical
garbage — the search then sees only the resample sentinel and cannot fit at all.
The guard has no way to distinguish that from the Cholesky-garbage case it was
built for, because the only signal it reads is a magnitude in unspecified units.

## The decision (human, 2026-08-29)

Keep the code path; **flip the packaged default OFF**. The guard is opt-in for
the surface where it was actually needed — `autolens_profiling`, where run
341908_5 was diagnosed as a likelihood-overflow flood. Whether real PyAutoLens
analyses should have it on is deferred until the Wave-B harvest produces more
results.

## Scope

**PyAutoFit**

1. `autofit/config/general.yaml` and `test_autofit/config/general.yaml`:
   `log_likelihood_ceiling: null` (disabled), comment explaining the unit
   argument and that profiling opts in.
2. `get_log_likelihood_ceiling`: a **missing** key now means disabled (`inf`),
   not `1.0e20` — a workspace whose `general.yaml` pre-dates the key must inherit
   the new default, not the old one.
3. Warn the **first** time the guard fires in a process (numpy path only —
   inside `jax.jit` / `vmap` a Python `logger` call cannot run on a traced value,
   so those paths stay silent by construction; document that).
4. Update the docstrings and the existing tests: "default 1e20" expectations
   become "default disabled"; the enabled-path tests keep their coverage by
   setting the ceiling explicitly.

**autolens_profiling**

5. `config/general.yaml`: set `test.log_likelihood_ceiling: 1.0e+20` with a
   comment citing 341908_5.
6. `results/notes/inference/DECISIONS.md`: a short dated entry recording that
   the ceiling is profiling-only by human decision, and that a reassessment for
   real PyAutoLens analyses is owed after the Wave-B harvest.

## Not in scope

Changing the guard's *shape* (e.g. making it relative to the data, or deriving a
unit-aware threshold). If the reassessment says real analyses want it, that is
the design question to open then.
