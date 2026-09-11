# `af.Model.from_instance` serialises derived attributes the class `__init__` rejects, so the aggregator cannot deserialise `model.json`

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Witness: `af.Model.from_dict(af.Model.from_instance(al.mp.ExternalShear(gamma_1=0.02, gamma_2=0.02)).dict())` and the same for `al.mp.Isothermal(...)` round-trip without error, a regression test in `test_autofit/mapper` pins it on a class whose `__init__` rejects a derived attribute, and an `Aggregator.from_directory` over a search whose model was composed with `from_instance` loads the result.
Review-minutes: 15
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-11

## Symptom

Found 2026-09-10 while writing the autolens_workspace_test latent integration smoke
(autolens_workspace_test#315 / PR #316). Composing a model with
`af.Model.from_instance(<profile instance>)` copies *derived* attributes onto the model
that the class constructor does not accept, and the `model.json` the search then writes
cannot be deserialised, so `Aggregator.from_directory` raises before reading any result:

```
af.Model.from_dict(af.Model.from_instance(al.mp.ExternalShear(gamma_1=.02, gamma_2=.02)).dict())
  -> TypeError: ExternalShear.__init__() got an unexpected keyword argument 'centre'
af.Model.from_instance(al.mp.Isothermal(...))
  -> TypeError: ... unexpected keyword argument 'slope'
```

The serialised dict carries `centre` / `ell_comps` (ExternalShear) and `slope`
(Isothermal) as `Constant` / tuple arguments. `af.Model(cls, ...)` round-trips fine, and
`al.lp.Sersic` via `from_instance` also round-trips (no derived attribute clashes).

## Blast radius

- `euclid_strong_lens_modeling_pipeline/tests/test_latent_run_level.py` composes its
  model with `from_instance`; any output written that way is unreadable by the
  aggregator (the test never aggregates, so it passes).
- Any workspace example that anchors a search on a truth instance via `from_instance`
  produces results the aggregator / `AggregateCSV` cannot open.

## Do

1. `from_instance` should only carry attributes that are constructor parameters
   (inspect the class signature, as `Model.__init__` already does for priors) — or
   `from_dict` should drop non-constructor keys with a warning. Prefer the former: the
   written `model.json` should be loadable as-is.
2. Regression test on a small class with a derived attribute (`@property` or an
   attribute set in `__init__` from other arguments) plus an aggregator round-trip.

The smoke composes its models with `af.Model(cls, **fixed_values)` as a workaround; the
script docstring records why.

<!-- formalised by the Fable architect session 2026-09-10 from the A3 subagent's finding -->
