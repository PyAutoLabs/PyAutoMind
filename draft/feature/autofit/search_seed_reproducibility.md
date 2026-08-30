# Give PyAutoFit searches a `seed` — today no search can be made reproducible

Type: feature
Target: autofit
Repos:
- PyAutoFit
Themes:
- samplers
Difficulty: medium
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Issue: (none yet)
Filed: 2026-08-05 (backfilled from git)

## The gap

There is no supported way to make a PyAutoFit search reproducible. A search's
randomness comes from three places, and the caller can reach none of them:

1. **The sampler's own generator.** `DynestyStatic.search_internal_from` builds
   `dynesty.NestedSampler(...)` and splats `**self.search_kwargs`
   (`autofit/non_linear/search/nest/dynesty/search/abstract.py:157`). That
   property is a **closed dict** of eleven fixed keys — `bound`, `sample`,
   `walks`, … — so an extra kwarg cannot be threaded through it. `dynesty`
   itself *does* accept `rstate`, and defaults it to
   `np.random.Generator(PCG64(None))` — OS entropy
   (`dynesty/dynesty.py:607-608`, `814`). So the one knob that would fix this
   exists in the dependency and is unreachable from PyAutoFit.
2. **The initializer.** `autofit/non_linear/initializer.py:301` draws initial
   unit values with the stdlib `random.uniform`, i.e. off the process-global
   `random` module rather than a search-owned generator.
3. **`numpy.random`**, wherever callers or model code touch the legacy global.

Seeding any one of these leaves the other two free.

## Why it matters

This is the *root* cause behind
`complete/…/covariance_interpolator_test_unseeded_rng.md`
(PyAutoFit#1450) — the flake that killed the **2026.8.2.1 live release**. That
fix had to seed all three sources from a test fixture, and to reach (1) at all
it **monkeypatches `dynesty.dynesty.get_random_generator`** — reaching into a
third-party module's namespace from a test, which is exactly the kind of thing
that breaks silently on a dependency upgrade.

Two consequences beyond that one test:

- **Any** test that runs a real search is unseedable by construction, so the
  same flake class can reappear anywhere in the suite. `test_single_variable`
  in that same file was already flaking at 3.6% on source (1) alone, with no
  random call of its own.
- **Users cannot reproduce a fit.** Re-running the same model on the same data
  gives a different chain. For a scientific inference library that is a real
  gap, not only a test-hygiene one.

## Proposed work

1. Add a `seed` parameter to the search classes (`AbstractSearch`, honoured by
   the dynesty searches first), defaulting to `None` = today's behaviour, so
   this is additive and no existing fit changes.
2. When `seed` is set, derive and pass `rstate` into the dynesty sampler —
   either by adding `rstate` to `search_kwargs` or by giving subclasses a hook
   to extend it. Check `DynamicNestedSampler` takes the same route.
3. Give the initializer a generator seeded from the same `seed`, instead of the
   global `random` module.
4. **Check the identifier and serialization surface before committing to the
   shape.** PyAutoFit hashes search configuration into run identifiers
   (`__identifier_fields__`) and writes search config to JSON/the database. A
   `np.random.Generator` is not JSON-serializable, so store the integer seed,
   not a generator object, and decide deliberately whether `seed` belongs in
   `__identifier_fields__` — including it changes identifiers for existing
   runs, which is the trap PyAutoGalaxy#549 was careful about.
5. Once it exists, simplify the `seed_search_randomness` fixture in
   `test_autofit/interpolator/test_covariance.py` to use it and drop the
   `dynesty.dynesty` monkeypatch.
6. Consider extending to the other samplers (emcee/zeus already take a seed
   concept; nautilus and the MLE searches need checking) — but land dynesty
   first rather than blocking on full coverage.

## Exit criteria

A search constructed with a fixed `seed` produces a bit-identical result across
repeated runs and across processes; no existing search's identifier or output
changes when `seed` is left unset; the interpolator test fixture no longer
monkeypatches a third-party module.
