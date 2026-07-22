# group/slam PriorException: upper limit must be greater than lower limit (parked NEEDS_FIX)

Type: bug
Target: autolens
Repos:
- autolens_workspace
- HowToLens
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Parked since 2026-04-10; still parked after the 2026-07-21 census. Same failure in two repos (one
root cause): `PriorException: upper limit must be greater than lower limit` in the group SLaM pipeline.

Affected: `autolens_workspace/scripts/group/slam` and `HowToLens/.../group/slam`.

Likely a prior-limit passed/chained in the group SLaM setup that collapses (lower >= upper) — e.g. a
`GaussianPrior` limit derived from a previous search's value, or a hard-coded limit pair that inverted
after an API/default change. Reproduce on clean main, fix the prior construction, remove the NEEDS_FIX
marker from BOTH repos' config/build/no_run.yaml.
