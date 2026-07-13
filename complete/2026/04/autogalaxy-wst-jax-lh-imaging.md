## autogalaxy-wst-jax-lh-imaging
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/8
- completed: 2026-04-22
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/364
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/9
- umbrella: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/5 (task 3/9)
- notes: Added `_register_fit_imaging_pytrees` staticmethod on `ag.AnalysisImaging` (mirrors autolens) + custom `Galaxies` list-subclass pytree flatten. Workspace side: simulator.py + 4 JAX-likelihood imaging scripts (lp, mge, mge_group, rectangular-non-adapt). Deferred 3 adapt-image variants (rectangular_mge, delaunay, delaunay_mge) to a follow-up library task tracked at `admin_jammy/prompt/autogalaxy/adapt_images_pytree_fix.md` — post-unflatten `self.galaxies` has fresh `Galaxy.id`s that don't match `adapt_images.galaxy_image_dict` (aux) keys. Autolens's rectangular.py passes today despite having the apparent same setup — root-cause diff deferred to that follow-up. Gotchas: `ag.lp_linear.Sersic` on a single-galaxy model returns empty `blurred_image` (inversion required); `raise_inversion_positions_likelihood_exception` is autolens-only.
