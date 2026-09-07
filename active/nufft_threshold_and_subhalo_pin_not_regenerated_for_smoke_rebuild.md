# nufft.py round-trip threshold and subhalo.py expected_vmap pin not regenerated for the 2026-09-06 smoke-dataset rebuild

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Filed: 2026-09-07
Witness: `scripts/interferometer/nufft.py` and `scripts/imaging/substructure/subhalo.py` both exit 0 on the current `main` stack under the weekly Workspace Smoke profile, and the next scheduled PyAutoHeart Workspace Smoke run carries neither in its FAIL list.
Unattended: ready
Issued: 2026-09-07

Two off-gate scripts in `autolens_workspace_test` fail on the weekly Workspace Smoke
(PyAutoHeart run 34099198772) and the Release Integrate rehearsal (run 34094964905),
bit-identically in both. Both were green on the 2026-08-31 scheduled smoke.

Cause: the 2026-09-06 smoke-gate dataset rebuild (`fb6e709` + `311fde4`) coarsened the
shared datasets (imaging 180²@0.2" -> 100²@0.3"; interferometer real-space 256²@0.1"
-> 128²@0.2") and regenerated pins "27/27 green" — but these two scripts run only on
the weekly/release channels, not the PR gate, so they were never in the 27.

1. `scripts/interferometer/nufft.py:539`
```
AssertionError: Round-trip dirty-image peak too far from original peak: 15.81 px
```
The diff rewrote the geometry to 128²/0.2" and reworded the adjacent comment
(`# 256x256-only number.` -> `# resolution-specific number.`) but left the pixel-space
threshold `assert distance < 6.0` untouched. Rescale (or recompute) the threshold for the
new geometry rather than loosening it blindly — confirm the 15.81 px is a geometry
artefact and not a real NUFFT regression by checking the round-trip on the old 256² data.

2. `scripts/imaging/substructure/subhalo.py:249`
```
ACTUAL -705876406.28 vs DESIRED -706228700.0   (rel 4.99e-4 > rtol 1e-4)
```
The only change to the script was `pixel_scales=0.2 -> 0.3`; the pinned `expected_vmap`
literal was not regenerated. Regenerate the pin from the current stack.

Also sweep every other script that runs only off the PR gate (weekly/release channel
lists in PyAutoHeart's workspace smoke config) for absolute pins or resolution-specific
thresholds the `fb6e709` regeneration missed, and fix any in the same PR.

Sibling prompts already filed for the other two rebuild residues:
`draft/bug/autolens_workspace_test/jax_grad_delaunay_eager_jit_guard_float64_scatter.md`
and `draft/bug/autolens_workspace_test/mge_group_source_basis_zeroed_on_coarse_data.md`.
