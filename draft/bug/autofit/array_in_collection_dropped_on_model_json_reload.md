# An af.Array inside a Collection is dropped when the model is reloaded from model.json

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: `from_dict(json.loads(json.dumps(to_dict(af.Collection(array=af.Array(shape=(3,), prior=af.UniformPrior(lower_limit=0.0, upper_limit=1.0)))))))` has an `array` attribute with 3 priors, the same `paths` and `identifier` as the built model
Unattended: ready
Lane: any

Found 2026-11-26 by the shift worker fixing PyAutoFit#1809 (prior order after reload). On main, `af.Collection(array=af.Array(shape=(3,), prior=af.UniformPrior(lower_limit=0.0, upper_limit=1.0)))` round-tripped through `autonerves.dictable.to_dict` / `from_dict` (the `paths.save_all` route for `model.json`) loses the array: the reloaded Collection has no `array` attribute and `prior_count` 0 (built: 3). The dict carries `"type": "array"`, but `"array"` is not in the parser types `autofit/__init__.py` registers with autonerves, so `ModelObject.from_dict`'s `type_ == "array"` branch is never reached through autonerves. `Array.from_dict` also builds its element priors with a fresh `loaded_ids`, so once it is reached, priors shared with the rest of the model would be duplicated and the #1809 prior-order restore would not see them: pass `loaded_ids` through.

Fix: register `"array"` as a parser type, forward `loaded_ids` in `Array.from_dict`, and add the case to `test_autofit/serialise/test_prior_order.py` (ordered paths, identifier, vector-mapped instances).
