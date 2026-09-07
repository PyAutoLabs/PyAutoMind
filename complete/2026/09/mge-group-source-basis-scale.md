# mge_group's model anchored on the simulator truth so the positive-only solver no longer zeroes the source

autolens_workspace_test#303 → `98dadac1`, closing autolens_workspace_test#299, merged 2026-09-07. One of six corrective PRs shipped 2026-09-07 under the human-authorised Heart RED corrective-PR exception (reasons: `release validation FAILED (stage integrate)` and `workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)`). Fable session planned; Opus subagents implemented per task; merged via /prm the same day. Validation of the RED clearing is the next scheduled Workspace Smoke and Release Integrate runs on fresh wheels.

- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/299
- completed: 2026-09-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/303
- corrective-red: authorization https://github.com/PyAutoLabs/autolens_workspace_test/issues/299#issuecomment-5573411919

## What shipped
- `scripts/imaging/jax_likelihood/mge_group.py`: lens MGE `ell_comps` anchored on the simulated bulge/disk, source centre prior (0.0, 0.2) and `ell_comps` on truth, satellite `einstein_radius` `UniformPrior(0.0, 0.02)` (`simulator/simple.py` simulates no group members). Pin `-1358.450245` → `1185.535713`; the 9.0 floor unchanged with a note not to raise it. chi2 5650 → 562 on 556 px; source block non-zero (8 of 30); response 29.2.

## Key traps / findings
- Not a PyAutoArray defect. At prior medians the five satellites (theta_E 0.25 each, all at x>=0) displaced the source-plane centroid to (0, +0.57") while the source centre prior was (-0.1, 0.1): the source basis sat where no arc landed and NNLS correctly returned zero, so the +5% mass perturbation had no path to the likelihood (bit-identical values).
- Both planned levers (lens ladder ceiling, source ladder floor) and two more (extra-galaxy ladder ceiling, lens `gaussian_per_basis`) left the source at zero; the controls "remove extra light" (no effect) vs "remove extra mass" (source restored, +228) isolated the mechanism. Shrinking satellite mass alone is a knife edge (response 295 → -10.5 across ceilings 0.01–0.06); truth-anchoring the whole model is monotone (19–115).
- Coverage given up: satellites carry negligible mass. Follow-up filed: `draft/test/autolens_workspace_test/mge_group_dataset_with_real_group_members.md`.
- The prompt was wrong on two facts (floor is 9.0 not 0.02; main has 60/30/10 Gaussians, not 40/20/8) — verified before planning.

## Original prompt

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
Issued: 2026-09-07

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

<!-- was a member of the ci-timing-fast-tests epic (retired COMPLETE 2026-09-06, ledger complete/archive/epics/ci_timing_fast_tests_epic.md); now ordinary backlog -->
