## function-config-priors
- completed: 2026-10-17
- constraint: Human confirmed 2026-10-17 that existing model/search unique IDs and output-folder names must not change; baseline hashes and exact output paths checked across all four branches.
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1702
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1705
- head: c0fa0b6ee5500d69f3ba9d6dde598dbe1b59f157
- validation: Full serial suite: 3706 passed, 121 skipped, 1 xfailed; model subtree 204 passed. Configured/explicit function priors, frozen evaluation, missing-config errors, and class initializer behavior covered.
- identifier-evidence: Free/fixed/mixed model hashes, search IDs and output paths equal unmodified main 99d714c71; no identifier code changed.
- merge: debd95de69c0c65ed834a16eb75eb86bdbf83426
- authorization: Human /prm in this chat, 2026-10-17.
- merge-proof: Remote PR head is an ancestor of origin/main in unshallowed PyAutoFit; zero unmerged commits. GitHub confirms MERGED.
- ci: All head workflows and jobs completed successfully; Python 3.12, 3.13 and no-JAX test legs passed. Applicable docs and generated-search-docs passed. No review objections.
- freeze: pyauto-heart freeze --show returned not frozen. Readiness remains STALE; no release-readiness claim.
- release-link-repair: GitHub pending-release label verified; restored the missing Mind link during close-out.
- shadow-row: Human confirmed merged-unchanged in this chat on 2026-10-17; stage-1 glance row appended to autonomy_log.md.

## Original prompt

# af.Model(function) cannot resolve config priors

Issued: 2026-10-17
Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: af.Model(some_function) with no explicit priors builds a model instead of raising AttributeError: 'NoneType' object has no attribute '__module__'.
Review-minutes: 3
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
