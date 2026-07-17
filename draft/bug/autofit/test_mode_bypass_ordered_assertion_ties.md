# TEST_MODE bypass crashes on ordered-parameter assertion ties

Type: bug
Target: PyAutoFit
Repos:
- @PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Found during the CTI resurrection epic (Phase 4, 2026-07-17). `PYAUTO_TEST_MODE=2/3`
bypass evaluates the model at the **prior medians**. A model whose components have
identical priors plus an ordering assertion (the standard idiom for breaking
exchange degeneracy, e.g. PyAutoCTI trap models with
`model.add_assertion(trap_0.release_timescale < trap_1.release_timescale)`)
ties exactly at the medians, so the bypass evaluation raises
`autofit.exc.FitException: GreaterThanLessThanAssertion` and the script crashes.

Real samplers resample assertion-failing points gracefully — this is purely a
bypass-path artifact, and it makes every ordered-trap CTI workspace script
un-smokeable at TEST_MODE=2 (reproduced with a bare
`model.instance_from_prior_medians()`; TEST_MODE=1 passes).

Suggested fix: at the bypass evaluation, catch `FitException` from assertions
and retry with a small deterministic perturbation of the unit-cube point (or a
seeded random draw), mirroring what a real sampler does. Keep it deterministic
so smoke runs stay reproducible.

Blocks: autocti_workspace smoke coverage of `modeling/start_here.py`-class
scripts (CTI epic Phase 5); the workspace documents the artifact in its
AGENTS.md meanwhile.
