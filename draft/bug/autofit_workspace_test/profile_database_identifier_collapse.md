# `@autofit_workspace_test` profiling mocks collapse to one database row after PyAutoFit#1686

Type: bug
Target: autofit_workspace_test
Autonomy: safe
Epic: search-extensibility
Consequence: judge

## Request (verbatim)

> I authorize, so do it and then prm then give me the release prompt

(the human's reply to the finding below, authorizing the Heart RED development override, the ship and the `/prm`)

## Finding

`Release Integrate` run 38698294068 (PyAutoHeart, 2026-10-15 07:22 UTC) fails on one
script: `scripts/profiling/aggregator/profile_database.py` —
"Database ingested 1 fits, expected 5". Reproduced locally against the installed stack
(expected 10 on the first grid cell).

Cause: PyAutoFit#1686 (search-ext A4 seed, merged 2026-10-14) made `SearchOutput.id`
prefer the identifier persisted in the output's `.identifier` file over a recompute, so
historical outputs keep their identity. The profiling mocks in
`scripts/profiling/aggregator/mock_results.py` are `copytree` copies of one template leaf
with only `search.json`'s `unique_tag` rewritten; every copy carries the template's
`.identifier`, so the database keys all of them to the same row.

## Fix

One line in `stamp_results`: unlink `.identifier` in each copy so the identifier is
recomputed from the rewritten `unique_tag`. Verified locally with fresh mocks: the whole
profiling grid passes. Note the generator's manifest cache: a stale mock set is reused
unless removed, so the verification deleted `output/profiling_aggregator/mock` first.

## Gate

Heart RED (release validation FAILED at stage integrate — this very failure). Development
override granted by the live human (session 6ffb59e9, fourth grant): commit, push, PR-open;
merge by human `/prm`, also authorized in the same message.
