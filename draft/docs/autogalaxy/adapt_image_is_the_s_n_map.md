# Adapt image is the S/N map: fix the prose and assess…

Type: docs
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- autogalaxy_assistant
- autogalaxy_workspace
- PyAutoLens
- autolens_assistant
- autolens_workspace
- HowToGalaxy
- HowToLens
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: no `__Adapt Images__` cell in any workspace still calls the adapt image an "estimate of the
Review-minutes: 3
Unattended: needs-slicing

Adapt image is the S/N map: fix the prose and assess the AdaptImages API Say that the adapt image is the source S/N map — workspaces, library docstrings and the AdaptImages API

Type: docs
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
- autogalaxy_workspace
- HowToLens
- HowToGalaxy
- autolens_assistant
- autogalaxy_assistant
Difficulty: large
Autonomy: supervised
Priority: medium

Rewrite every `__Adapt Images__` prose cell (and the equivalent cells in the SLaM, Delaunay and
adaptive-pixelization examples) so it says what the adapt image actually is, and assess whether the
library's AdaptImages API and docstrings are honest about it.

Original request (user, verbatim, 2026-09-02, reviewing autolens_workspace PR #522):

"Is it not true that for imaging the Adapt Image IS the S/N map now, which does docstring does not
imply? Dont change code yet just answer question: __Adapt Images__

An adapt image is computed from the SOURCE LP result and passed to the analysis. This provides an
initial estimate of the source morphology for the `Adapt` regularization scheme, even though the MGE
source model may not fully capture the source structure. Search 2 improves upon this using a
pixelized adapt image."

"Ok do an intake which would do this across the workspaces (autoglaxy might matter too) "If you
want, the fix is a rewrite of that cell to say: the adapt image is the source's signal-to-noise map
(data with the lens light model subtracted, over the noise map) computed from the previous result,
it is what the adaptive mesh and regularization adapt to, and the cap below acts on it. I will not
touch anything until you say so.". However, this intake also needs to include assessing the
AdaptImages parts of the source code and being honest about whether their API reflects that fact we
are using S/N maps. For example, galaxy_name_image_dict_via_result_from implies an image but its
actually returning a signal_to_noise_map. Can you also intake that the docs here should expalin that
we use the S/N map by default because it is a standard quantity across all images, where images
depend on brightness units. Docstring and example looks good other thantht"

What is established (2026-09-02):

- `galaxy_name_image_dict_via_result_from(result)` (PyAutoGalaxy
  autogalaxy/analysis/adapt_images/adapt_images.py:138, default `use_model_images=False`) returns
  `result.subtracted_signal_to_noise_map_galaxy_dict`: for imaging, the dataset with every other
  galaxy's model image subtracted, divided by the noise map, cached as `galaxy_images_snr.fits`.
  The source entry is therefore the observed source light (lens light subtracted) in S/N units, not
  a model image; the SOURCE LP model enters only through what gets subtracted. Only
  `use_model_images=True` returns model images in flux units (what the interferometer scripts use,
  because the interferometer "S/N" path divides by the dirty noise map, which is a dirty beam).
- The `__Adapt Images__` cell quoted above (autolens_workspace scripts/guides/modeling/
  slam_start_here.py and the cells it was copied into across imaging / group / multi_galaxy /
  interferometer SLaM pipelines, the Delaunay and adaptive examples, and the autogalaxy_workspace
  twins) describes the adapt image as "an initial estimate of the source morphology" from the MGE
  fit and says "Search 2 improves upon this using a pixelized adapt image". Both mislead: the
  structure comes from the data, and source_pix_2 builds its adapt image by the same S/N route from
  the source_pix_1 result (a better lens-light subtraction, not a different quantity).
- autolens_workspace PR #522 (adapt-image-snr-cap) adds a cap at S/N 3.0 whose prose presupposes
  S/N units; the surrounding cell should say the adapt image is in those units.
- The function name `galaxy_name_image_dict_via_result_from` and the `AdaptImages`
  `galaxy_name_image_dict` attribute say "image"; the returned quantity is a signal-to-noise map.
  Whether to rename (e.g. `galaxy_name_snr_map_dict_via_result_from`, with a deprecation alias) or
  only to document is a human decision — the assessment must lay out every AdaptImages symbol,
  what each actually holds, and the blast radius of a rename across the workspaces and assistants.

Scope:

1. Workspace prose: rewrite the `__Adapt Images__` cell everywhere it appears (autolens_workspace
   and autogalaxy_workspace SLaM / pixelization / adaptive examples; HowToLens / HowToGalaxy
   adaptive-pixelization tutorials if they carry the same text) to say: the adapt image is the
   source's signal-to-noise map (data with the lens light model subtracted, over the noise map),
   computed from the previous result; it is what the adaptive mesh and the adaptive regularization
   adapt to; and, where PR #522's cap follows, that the cap below acts on it. Say once per script
   why S/N is the default: it is a standard, unit-free quantity across every dataset, whereas an
   image depends on the brightness units of the data. Keep it to one paragraph; notebooks
   regenerated per each workspace's convention.
2. Library docstrings (PyAutoGalaxy AdaptImages module, `galaxy_name_image_dict_via_result_from`,
   the result properties `subtracted_signal_to_noise_map_galaxy_dict` /
   `galaxy_signal_to_noise_map_dict`, the `AdaptImages` class and `adapt_minimum_percent` floor):
   state plainly that the default quantity is a signal-to-noise map and why (unit-free, standard
   across datasets), and that `use_model_images=True` is the flux-units alternative. Same for the
   PyAutoLens interferometer result override.
3. API honesty assessment (report, not a rename): list every AdaptImages-related public symbol
   whose name says "image" but holds an S/N map, propose the rename + deprecation-alias path and its
   cost (every workspace call site, assistants' skills, wiki/core/api pages), and end with a
   recommendation for the human to decide. If a rename is approved it is filed as its own
   refactor prompt, not done here.
4. Assistant skills and wiki/core/api pages that describe adapt images (autolens_assistant
   al_adaptive_pixelization.md, al_run_slam_pipeline.md, wiki/core/api/analysis_objects.md;
   autogalaxy_assistant equivalents): same one-paragraph correction; re-stamp provenance where the
   page carries it.

Phases (one issue, three PR waves, library first): (1) PyAutoGalaxy + PyAutoLens docstrings and the
API-honesty assessment report; (2) autolens_workspace + autogalaxy_workspace + HowToLens + HowToGalaxy
prose and notebook regen; (3) autolens_assistant + autogalaxy_assistant skills and wiki pages.

Out of scope: any rename or behaviour change (separate prompt after the assessment); the cap
itself (PR #522).

Witness: no `__Adapt Images__` cell in any workspace still calls the adapt image an "estimate of the
source morphology" from the light-profile fit; every rewritten cell names the signal-to-noise map
and the unit-free reason; the AdaptImages module docstring says "signal-to-noise map" in its first
paragraph; the assessment report is attached to the issue with a recommendation.

Where it came from: autolens_workspace#521 / PR #522 review, 2026-09-02.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/16f51d23-06be-4ec5-8b46-e9540276c31e/scratchpad/intake_adapt_image_is_snr_map.md -->
