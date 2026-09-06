# imaging/jax_likelihood/mge_group.py: positive-only solver zeroes the source MGE on the rebuilt data

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-09-06
Epic: ci-timing-fast-tests

Left over from phase 6 (autolens_workspace_test#293 / #294). After the shared
imaging dataset moved to 100x100 @ 0.3" with fainter lens light,
`scripts/imaging/jax_likelihood/mge_group.py` (weekly `workspace-smoke.yml` and
`release-integrate`; not on the PR gate) fails its own +5% mass-sensitivity
assertion with a *bit-identical* likelihood under the perturbation:

```
AssertionError: imaging/mge_group: likelihood insensitive to a +5% lens-mass perturbation
(median=-1358.4502451974756, perturbed=-1358.4502451974756)
```

A probe of the inversion shows why: the positive-only solver returns all 20
source-basis reconstruction components as exactly 0.0 while the lens MGE basis
(40 Gaussians, abs sum 70.5) and the extra-galaxy bases absorb the arcs. The
mass model is at the truth, so this is not the bad-prior case the script's own
comment documents; it is the broad lens basis reaching arc scale on the coarser
data. Two levers were tried in phase 6 and backed off (lens/source Gaussian
budgets 30 -> 20 / 10 -> 8; lens sigma ladder capped at 2.0" instead of the 3.0"
mask radius): both still bit-identical. The file differs from `main` by one line,
its regenerated pin.

Ask: give the source basis a scale the lens basis cannot absorb (e.g. a source
MGE sigma ladder starting well below the lens ladder, or a lens ladder that stops
below the Einstein radius), or establish whether the positive-only solver's
behaviour on a ~560-pixel mask is the real cause (a PyAutoArray question). The
assertion and its 0.02 floor stay as they are; the fix is in the model.
