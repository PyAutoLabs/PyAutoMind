# PowerLawMultipole with m=1 returns -inf / NaN deflections at slope exactly 2 (isothermal)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
Themes:
- mass-profiles
- jax
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: `ag.mp.PowerLawMultipole(m=1, slope=2.0, multipole_comps=(0.01, 0.0)).deflections_yx_2d_from(grid)` either returns finite deflections from the correct limiting form, or raises a clear exception at construction naming the m=1 / slope=2 degeneracy; a unit test pins whichever is chosen, for numpy and jax.
Filed: 2026-09-27
Updated: 2026-09-27

## Finding

Found building the phase-2c model ladder (autolens_profiling#331, source-plane point-source campaign):
an m=1 `PowerLawMultipole` with its slope tied to an isothermal lens (slope 2) gives `-inf` / NaN
deflections, so the ladder used a satellite shear instead. The power-law multipole deflection
appears to carry a denominator that vanishes when m = 3 − γ, which makes the m=1 term degenerate at
γ = 2 (isothermal, the most common slope). If so, this is a singular limit of the formula rather
than a numerical accident — confirm against the implementation.

## Fix direction

Decide between (a) implementing the m=1, γ=2 limiting form (finite, likely with a log term) or
(b) refusing m=1 at slope 2 with a clear error (and in the model, when slope is a free parameter,
documenting the singular point). Check the literature form used for the other m (see the
multipole docstring's reference) before choosing.

Issued: 2026-10-25

## Execution 2026-10-25
User authorized selecting and implementing four related tasks. Scope: Reject singular isothermal dipole multipoles. Separate branch and PR; no merge authorization. Related group executes serially with non-overlapping source edits.

## Implementation evidence (2026-10-25)

- Library PR: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/665 at `9be12cae62318cf27fcfce37059a9cd0b43302e2`; published Git tree equals the tested local tree.
- Full library suite: `python3 -m pytest -q -n auto test_autogalaxy`, 1363 passed, 6 skipped; Python 3.12, released 2026.10.25.1 dependencies.
- Log: `/workspace/scratch/e0d55f00a4c5/evidence/multipole-isothermal-guard-suite.log`.
- Heart readiness GREEN, score 100, no reasons; evidence timestamp 2026-10-25T20:54:46Z.
- GitHub Tests and Docs for the exact PR head were running at the final check; no CI success or merge claimed.
- Merge mode: human `/prm`; no merge, close-out or release authorized/performed.
- Workspace regression PR: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/130 (draft). Direct script passes with JAX 0.11.2 on this branch and fails against unmodified main; smoke-list entry added. Full workspace CI pending library availability.
- JAX log: `/workspace/scratch/e0d55f00a4c5/evidence/multipole-isothermal-guard-jax.log`.
- Chosen prompt option: reject concrete m=1, slope=2. Chu et al. 2013 equations 5/8/9 require a distinct logarithmic potential; not added. Literal singular construction also rejects during JIT tracing. Free/traced slopes must exclude 2; no tracer runtime assertion added, consistent with existing constructor guards.
