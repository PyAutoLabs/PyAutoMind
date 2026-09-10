# af.Model(function) cannot resolve config priors

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Witness: af.Model(some_function) with no explicit priors builds a model instead of raising AttributeError: 'NoneType' object has no attribute '__module__'.
Review-minutes: 20
Unattended: ready
Filed: 2026-09-10

`af.Model` accepts a plain function — `prior_model.py:137` explicitly tests
`inspect.isfunction` — but the model then **crashes** unless every prior is
supplied explicitly.

`make_prior` passes **`cls=None`** into `path_for_class`, which immediately does
`cls.__module__` and raises `AttributeError: 'NoneType' object has no attribute
'__module__'`. So the config lookup that would supply a default prior for a
function argument can never run, and the function case only ever arrives with
explicit priors.

Either derive a usable config path for a function (module + qualified name, the
same shape a class gets) so config defaults work, or — if config priors are
genuinely not intended to be supported for functions — fail early with a clear
message at `af.Model(function)` construction time instead of an `AttributeError`
from deep inside `path_for_class`. A silent trap that only fires on the
no-explicit-priors path is the worst of the three options.

Add a test for whichever behaviour is chosen: config priors resolved, or a
clear, immediate error.

Found on 2026-09-10 by execution while auditing the PyAutoFit model API for the
model-figures design (research leg B, construct 13 and "What is missing from the
PyAutoFit model API", item 8).
