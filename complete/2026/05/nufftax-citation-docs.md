## nufftax-citation-docs
- issue: N/A (ad-hoc follow-up to PyAutoGalaxy#391 — nufftax-default-transformer)
- completed: 2026-05-10
- library-prs: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/396, https://github.com/PyAutoLabs/PyAutoLens/pull/503
- repos: PyAutoGalaxy, PyAutoLens
- notes: |
    Added a `## NUFFTax` section to `docs/general/citations.md` in both
    PyAutoGalaxy and PyAutoLens so users running interferometer fits on
    the JAX path know to cite `nufftax` (the new pure-JAX NUFFT dependency
    introduced by PyAutoGalaxy#391) and the upstream FINUFFT paper its
    algorithm is based on. Followed the precedent set by the existing
    `## Jax-Zero-Contour` section — guidance lives only in
    `docs/general/citations.md`, not in the canonical
    `files/citations.{bib,tex,md}`.
