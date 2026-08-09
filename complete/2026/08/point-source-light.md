## point-source-light
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/561
- completed: 2026-08-09
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/562
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/208, https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/103
- summary: Added standard and linear point-source light profiles with total-flux normalization and oversampled PSF convolution. Added a documented user-facing simulator and generated notebook, plus integration coverage for flux conservation and linear-profile conversion. All library, navigator, and workspace smoke checks passed before the library-first squash merges. Accurate sub-pixel placement requires a PSF sampled on the matching finer grid; factor 1 remains the pixel-centred approximation.

## Original prompt

# We currently does not have implemented a point source of

Type: feature
Target: PyAutoGalaxy
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

We currently does not have implemented a point source of light, light profile, which would be a delta function
implemneted in a single pixel in the image. This should be easy to addd, and would be added in the light/profiles
module of autogalaxy.

First it would be added as a standard light profile, and then variants for linear would be added.

For point sources of light, 2d convolution is tricky, as it really requires 2D subsampling of the PSF and convoluiton,
which are features that will be added relatively soon. Thikn about if there are simple approaches we can use to
add this now, but its fine to defer until we have full support for over sampled PSF convolution. In that case,
add some sort of a warning when this light profile is used for modeling.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
