# Oversampled PSF convolution — phase 4: documentation

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Phase 4 of 4 of `feature/autoarray/oversampling.md`. Depends on phases 2–3
being shipped; documents what actually landed, not the original plan.

## Scope

1. **Docstrings**: audit `Convolver.convolve_over_sample_size` and the new
   `Imaging` constructor parameters (`convolve_over_sample_size_lp`,
   `convolve_over_sample_size_pixelization`) — full parameter docs with the
   size-2-means-2×-resolution example.
2. **API reference**: update `docs/api/*.rst` autosummary entries touched by
   the new API (PyAutoArray; check downstream docs only if they enumerate
   these signatures).
3. **Workspace guides**: where the imaging/over-sampling guide prose in
   `autolens_workspace` describes PSF convolution resolution, add a short
   section on oversampled convolution pointing at the phase-3 simulator
   example. Anchor on the core imaging API surface; keep it brief.
4. Record the explicit limitations: adaptive over sampling unsupported with
   oversampled convolution; `inversion/imaging/sparse.py` deferred to future
   work.

## Acceptance

- Docs build clean (no new broken module paths / autosummary warnings).
- No behaviour changes — prose and docstrings only.

Parent: `feature/autoarray/oversampling.md`.
Previous: `oversampling_phase_3_workspace_examples.md`.
