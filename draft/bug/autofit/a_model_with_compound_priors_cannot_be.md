# A model with compound priors cannot be written to model.json, so search.fit…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: a model with a compound prior shared by two components writes model.json, reloads to an equal model, and `search.fit` starts without a TypeError
Review-minutes: 3
Unattended: ready
Lane: any

Found 2026-11-16 in the science project stars_dm_slope. A model in which one parameter is an arithmetic combination of priors (e.g. `stars.mass = (1 - f) * m` and `halo.mass = f * m`, giving a `DivisionPrior` / compound prior shared by two profiles) evaluates correctly, including inside the jitted and vmapped JAX likelihood and with model identifiers, but `search.fit` dies before sampling: `paths.save_all` writing `model.json` raises `TypeError: Object of type UniformPrior is not JSON serializable`. Traceback: `/home/jammy/Science/Science/development/stars_dm_slope/results/mocks_v1/phase1/pilot/logs/A_P1_n200_s1_failed_json.log`. The model that triggers it is `model_from("P1", ...)` in `/home/jammy/Science/Science/development/stars_dm_slope/scripts/parameterisations.py`; the workaround (two subclasses sharing the same prior objects) is in `/home/jammy/Science/Science/development/stars_dm_slope/scripts/pilot_fit.py`.
Fix: make the model-to-dict / JSON serialisation of compound (arithmetic) priors round-trip (serialise the operands and the operator), with a unit test that builds a compound-prior model, writes model.json, reloads it and compares instances; check model.info and the aggregator load path too.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Science/4543c7f0-9e90-432b-a76f-76d0789fa7b1/scratchpad/intake/1_compound_prior_model_json.md -->
