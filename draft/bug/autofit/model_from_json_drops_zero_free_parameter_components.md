# af.Model.from_json writes zero-free-parameter components back as instances

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- serialization
- visualization
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Filed: 2026-09-11

Found by the model figure while adding it to `autolens_workspace/scripts/guides/modeling/cookbook.py`
(model-figures epic phase 3, PyAutoLens#736). The cookbook's `__JSon Outputs__` stage dumps a model
with `model.output_to_json` and reloads it with `af.Model.from_json`. `model.info` looks unchanged,
but the reloaded model is not the same model: every component with **zero free parameters** comes
back as a plain instance instead of an `af.Model` — in the Solved Parameters model the `Delaunay`
mesh (all-fixed `pixels`/`zeroed_pixels`/`areas_factor`) and the whole `point_source` galaxy
(`PointSolved` has no parameters) collapse to single fixed pills. `af.ModelPlotter` shows it
directly: fixed leaf slots drop 6 → 4 and solved rows 3 → 2 across the round trip, and
`GraphSpec.from_model(...).to_dict()` differs. The galaxy cookbook's model (every component has a
free parameter) round-trips byte-identically, so the trigger is the zero-free-parameter case.

## Ask
- Reproduce with `test_autofit/graph_spec` style: dump/reload a `Collection` holding an all-fixed
  `Model` and a parameter-less `Model`; assert `GraphSpec.from_model(reloaded).to_dict()` equals the
  original's.
- Decide whether `from_json` should preserve `Model`-ness for such components (likely: the JSON
  already records `type: model`? check `autofit/mapper/prior_model/abstract.py` `from_dict`) and fix.
- Until fixed the lens cookbook says the reloaded figure differs; revert that sentence when it no
  longer does.
