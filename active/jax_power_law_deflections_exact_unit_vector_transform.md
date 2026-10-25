# Give the JAX PowerLaw deflections branch the same exact unit-vector transform as the numpy branch (#598)

Type: bug
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @autolens_workspace_test
Themes:
- jax
- mass-profiles
Difficulty: small
Autonomy: safe
Priority: low
Status: draft
Consequence: glance
Witness: Numpy and JAX `PowerLaw` deflections agree bit-for-bit at on-axis grid points (the JAX branch returns exactly 0.0 there), the existing deflection pins are unchanged, and `profiles_jit.py` passes on a green run with the `atol=1e-12` removed from its `mp.PowerLaw` checks.
Review-minutes: 3
Filed: 2026-09-04

## Symptom

`autogalaxy/profiles/mass/total/power_law.py` rotates the deflection vector back
to the reference frame by **two different routes**:

- **numpy** (`:213-216`) — the exact unit-vector transform added by
  PyAutoGalaxy#598 (`8aefe5a6`); on-axis grid points come back as exactly `0.0`.
- **JAX** (`:201-206`) — still `arctan2` / `cos` / `sin`; the same on-axis point
  comes back as `1.2e-16`.

Both are correct to one ulp, but the two paths are not bit-identical where the
numpy path is now exactly zero.

## Why it matters (how it surfaced)

`@autolens_workspace_test/scripts/misc/profiles_jit.py` compares the numpy and
JAX paths with `rtol`-only tolerances, so `1.2e-16` against an exact `0.0` is an
*infinite* relative error. It failed PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33847995194. That script
was patched with `atol=1e-12` on the `mp.PowerLaw` checks (mirroring
`mp.ExternalPotential`) — a tolerance, not a fix. The asymmetry itself is still
here.

## Task

Apply the same exact unit-vector transform on the JAX branch as on the numpy
branch, so on-axis deflections are exactly `0` on both paths.

## Acceptance

- Numpy and JAX PowerLaw deflections agree bit-for-bit at on-axis points.
- No measurable JAX/JIT cost regression (the transform is a couple of ops).
- Existing deflection pins unchanged (the numpy path must not move at all).
- Optional once landed: the `atol=1e-12` on the `mp.PowerLaw` calls in
  `profiles_jit.py` could be dropped again — but only with a green run to prove it.

Issued: 2026-10-25

## Execution 2026-10-25
User authorized selecting and implementing four related tasks. Scope: Align PowerLaw JAX unit-vector transform. Separate branch and PR; no merge authorization. Related group executes serially with non-overlapping source edits.

## Implementation evidence (2026-10-25)

- Library PR: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/663 at `499827fe23c5804351d936823d1b01e7917527a4`; published Git tree equals the tested local tree.
- Full library suite: `python3 -m pytest -q -n auto test_autogalaxy`, 1356 passed, 6 skipped; Python 3.12, released 2026.10.25.1 dependencies.
- Log: `/workspace/scratch/e0d55f00a4c5/evidence/power-law-jax-axis-suite.log`.
- Heart readiness GREEN, score 100, no reasons; evidence timestamp 2026-10-25T20:54:46Z.
- GitHub Tests and Docs for the exact PR head were running at the final check; no CI success or merge claimed.
- Merge mode: human `/prm`; no merge, close-out or release authorized/performed.
- Workspace regression PR: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/129 (draft). Direct script passes with JAX 0.11.2 on this branch and fails against unmodified main; smoke-list entry added. Full workspace CI pending library availability.
- JAX log: `/workspace/scratch/e0d55f00a4c5/evidence/power-law-jax-axis-jax.log`.
- Exact axial zero components restored. Nonzero components retain series rounding differences (maximum seen 1.25e-12); no claim of full bitwise identity. Focused parity uses rtol=1e-10 and atol=0. Centre jacrev is finite. Local CPU 10000-point JIT medians: old 696.8 us, new 354.1 us (single process timing, not a portable speed claim). Existing autolens workspace tolerance retained; its removal is optional in the prompt and was not validated here.

## PRM progress 2026-10-25

Library #663 merged after all Actions jobs passed and freeze gate was clear. Companion #129 was green, but merging sibling #128 caused an append conflict in smoke_tests.txt. Resolved with a two-parent merge preserving all entries; current head `cd96d90dbf305c8d8fc9ad0fe1cbe94d60388109`. Fresh CI run 40240713169 is in progress. No substantive regression-script edits. Task remains active until this companion merges; library pending-release retained.
