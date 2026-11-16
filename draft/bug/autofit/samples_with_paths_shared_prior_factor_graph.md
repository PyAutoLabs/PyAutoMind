# autofit: Samples.with_paths / without_paths break on factor-graph fits with shared priors

Type: bug
Target: autofit
Repos:
- @PyAutoFit
- @autocti_workspace
Themes:
- samples
- factor-graph
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: on a FactorGraphModel fit whose model is shared across factors (e.g. autocti_workspace `scripts/dataset_1d/advanced/database/start_here.py` output), `samples.with_paths(["0.cti.trap_list"])` and `samples.without_paths(["3.cti.ccd"])` both return the filtered parameters, for every factor prefix, matching `with_paths(["3.cti.trap_list"])`; the commented-out example in `scripts/dataset_1d/advanced/database/examples/samples.py` is switched back on.
Review-minutes: 10
Unattended: never
Lane: any
Filed: 2026-11-05

Found 2026-11-05 while fixing the autocti database examples (PyAutoCTI#121).

## What happens

A FactorGraphModel with the model shared across 4 factors has
`samples.model.paths` listing every shared prior under all 4 aliases:
`('0','cti','trap_list','0','density')`, `('1',…)`, `('2',…)` and `('3',…)`.
`all_paths` groups them. The stored sample kwargs, however, use only the
**last** alias (`3.cti.trap_list.0.density`). As a result:

- `samples.with_paths(["0.cti.trap_list"])` (and `"1."`, `"2."`, and the tuple form) raises
  `KeyError: Could not find any of the following keys in kwargs ('0.cti.trap_list.0.density',)`
  from `samples.py` `parameter_lists` (line ~262). Only `"3.cti.trap_list"` works.
- `samples.without_paths(["3.cti.ccd"])` raises a KeyError on `('0','cti','ccd','well_fill_power')`,
  while `without_paths(["0.cti.ccd"])` works.

Filtering is therefore asymmetric and only works through one alias. The kwarg
lookup should accept any alias of a shared prior, using `model.all_paths`.

## Reproduce

```bash
cd autocti_workspace   # with PyAutoLabs activate.sh
PYAUTO_TEST_MODE=2 python scripts/dataset_1d/advanced/database/start_here.py
python -c "import autofit as af; s=list(af.Aggregator.from_database('database.sqlite').values('samples'))[0]; s.with_paths(['0.cti.trap_list'])"
```
