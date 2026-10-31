# Resume: paired HowToLens / HowToGalaxy tutorial review

Saved: 2026-10-31. The approved introductory phase is merged and closed. The broader course review is not complete.

## Next action
The human plans larger changes to HowToLens Tutorials 3, 4 and 5 before continuing this editorial review. Do not apply the old Tutorial 3 proposal: it was shown in chat but never approved or edited. Once the human's rewrite is ready, read the current source and resume at Tutorial 3 with five coherent blocks at a time.

## Shipped work
- HowToLens Tutorials 0–2: https://github.com/PyAutoLabs/HowToLens/pull/104, merged e986a4ae89c840fe2ef2f7f01c4dd07c75147247.
- HowToGalaxy Tutorials 0–1: https://github.com/PyAutoLabs/HowToGalaxy/pull/93, merged ead53e6d736dcf302b93d1d5b54486dd81f80352.
- Shipping issue https://github.com/PyAutoLabs/HowToLens/issues/103 is closed. Completion record: complete/2026/10/howto-paired-review.md.
- Canonical scripts, all five matching notebooks and both navigation catalogues are included. Tutorials 3–5 were untouched. Continue from the main checkouts, not the old task bundle.

## Review contract
Follow HowToLens order and pair HowToGalaxy material by topic, not tutorial number. Show full proposed prose and associated code for FIVE coherent blocks at a time in chat, then apply after approval. Preserve the patient teaching tone and useful explanations without overloading introductory lessons. No whole-tutorial rewrites or file-click-only proposals. Use Brain's docs workflow and TUTORIAL_WRITING_STYLE.md.

HowToGalaxy tutorial_2_data.py pairs with HowToLens tutorial_6_data.py, not ray tracing.

## Accepted science and teaching decisions
Tutorial 0 clarifies simulation/loading/plotting and preserves the Galaxy dataset when showing masks. Figure sizing uses explicit Matplotlib axes, passed to aplt.plot_array.
Tutorial 1 distinguishes pixel centres/edges and native/slim ordering; geometry copies grids and explains the clockwise inverse rotation into an anticlockwise profile frame. Elliptical radius is sqrt(x^2+(y/q)^2). The manual Sérsic calculation includes intensity and the circularised radius sqrt(q)*eta; k=2n-1/3 is approximate. Explicit major-axis coordinates avoid the radial helper's clockwise rotation. Radial axes show intensity. Galaxy components share a suitable radial grid. Units include ~3260 light-years per kpc and corrected AB calibration guidance. Library docstring issues were observed but not edited.
Tutorial 2 uses both strong_lens_schematic.png and cosmos_web_ring_rgb_labelled.png from autolens_assistant/docs/images. Extra galaxy distance is not inferred from sky position. Ray tracing maps image-plane coordinates backwards to source-plane coordinates. IsothermalSph deflection magnitude is constant away from the centre. Reduced deflections are deferred to Tutorial 3. A central source-plane zoom precedes Mappings; three groups of five fixed slim indexes use matching colours at full default extents, with optional extent zoom encouraged. These plots use autoarray.plot as aaplt because public aplt wrappers do not expose extent/indexes. An __Env__ section declares ENV: full_datasets so automated runs preserve the 101x101 teaching grid.

Terminology: model = simplified mathematical description; light-profile image = one profile; galaxy image = summed profiles; model image = observation-level prediction, including PSF where appropriate, without implying fitting or added random noise. Early lensing lessons simply say “lensed image”; do not introduce “unblurred” or PSF terminology before it is taught. Avoid unnecessary fitting disclaimers and unsolicited foreshadowing.

## Validation and evidence
Both final PR heads passed all 3 GitHub workflow runs / 8 jobs, including full smoke on Python 3.12 and 3.13. Five notebooks were structurally validated and checked for code parity with source, excluding standard setup injection. Actual PyAutoLens mapping/zoom figures were rendered and visually inspected.
The human explicitly approved the plotting corrections, Heart RED override and merges. Exact readiness reason was `release validation FAILED (stage integrate)`. No release or test bypass occurred; that approval is historical, not a standing grant for future work.
Logs and reusable isolated Python 3.12 environments: /home/jammy/Code/PyAutoLabs/scratch/ship/.
Human review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/howto_paired_review_ship_2026-10-31/.
Actual figures: /mnt/c/Users/Jammy/Workspace/Science/scratch/howtolens_mappings_2026-10-31/.

Continuing findings prompt: draft/docs/howtolens/tutorial_correctness_and_howtogalaxy_parity.md. Keep the broader review open until the student-led course pass is complete.
