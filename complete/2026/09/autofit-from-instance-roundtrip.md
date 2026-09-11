## autofit-from-instance-roundtrip
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1607 (closed)
- completed: 2026-09-11
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1609
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1609
- session: claude --resume session_01CWGZiKQo2PhvsymabkUJJm (web-github; PyAutoFit attached mid-session, no task worktree)
- summary: |
    `AbstractPriorModel.from_instance` copied every entry of `instance.__dict__`
    onto the model, so attributes an `__init__` derives from its arguments
    (ExternalShear's `centre`, Isothermal's `slope`) became model arguments.
    `dict()` types a prior-free model as `instance`, `from_dict` calls
    `cls(**arguments)`, and the constructor rejected the derived key — so a
    `model.json` written from a `from_instance` model could not be loaded by
    `Aggregator.from_directory`. The generic-object branch now filters
    `__dict__` to the constructor's parameters (`inspect.getfullargspec` args +
    kwonlyargs), keeping every key when the constructor takes `**kwargs` or is
    uninspectable. Derived attributes are recomputed by `__init__` on rebuild.
    Tests: 5 round-trips in `test_autofit/mapper/model/test_from_instance_roundtrip.py`
    (derived attr, tuple arg, `**kwargs`, nested) and an
    `Aggregator.from_directory` regression in `test_from_directory.py`; 5 of the
    6 fail without the fix. Full suite 2575 passed / 43 skipped; CI green on
    3.12, 3.13, nojax and docs. No public API change, no workspace impact.
- traps: |
    - `pytest -n auto` cannot run the PyAutoFit suite at all: the parametrize
      ids in `test_autofit/mapper/prior/test_prior_properties.py` embed object
      addresses, so xdist workers collect different ids. Reproduced on clean
      main; filed as its own bug prompt. Run the suite serially until it lands.
    - `from_dict` round-trip classes must be module-level in the test file, or
      the `class_path` written into the dict does not resolve on read.
    - Two Mind sessions filing rows at the top of `active.md` in the same hour
      conflict in the ledger auto-merge; the fix is an ordinary merge of
      `origin/main` into the session branch (keep both rows), never a rebase.

## Original prompt

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
