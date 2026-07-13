## psf-oversample-simulator
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/482 (closed)
- completed: 2026-07-08
- prs: PyAutoArray#359, PyAutoGalaxy#483, PyAutoLens#575, autolens_workspace#233, autolens_workspace_test#150 (all merged, chain order, mains verified green each step)
- notes: |
    Oversampled-PSF simulator support (series option a). OperateImage.
    convolved_padded_image_2d_from (uniform-s padded frame; Galaxies+Tracer
    shared), via_image_from image_is_convolved flag, from_gaussian kwarg,
    simulator.py example section + navigator catalogue regen. Simulate-and-
    fit round trips in ALL 3 projects (user req) — the PyAutoGalaxy one
    caught a silently-unapplied CRLF patch. CI reds were pending-release
    chain artifacts (against-main runs) + catalogue staleness; both resolved.
    Series remaining: phase 4 docs + refactor follow-up (test_autoarray/
    output gitignore gap noted for refactor).
