# euclid pipeline: `LatentEuclid.variables` cannot be traced under the latent engine's `jax.jit`, so the JAX `vis_lp` stage writes no latents

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: the `vis_lp` search of `euclid_dr1_prelim` tile 102005065 rerun on the 342398 config writes `files/latent/latent_summary.json` with all twelve latents populated, and a JAX unit test evaluates `LatentEuclid.variables` under `jax.jit` on the `vis_lp_model_from` model with every value finite.
Review-minutes: 15
Unattended: ready
Filed: 2026-09-10

euclid pipeline: LatentEuclid.variables cannot be traced under the per-sample jax.jit the PyAutoFit latent engine uses, so the JAX (GPU) vis_lp stage writes no latent output (RAL job 342398, all ten euclid_dr1_prelim tiles; PyAutoLens#732 has the full diagnosis). Two independent trace failures in util.py: (1) line 516 'instance = model.instance_from_vector(vector=parameters)' checks the vis_lp ordered-MGE-bases assertion (order_bases=True, added 2026-09-08) with a Python 'not' on a traced boolean -> jax.errors.TracerBoolConversionError; replace with autolens.analysis.latent.latent_instance_from(model=model, parameters=parameters, xp=xp) (PyAutoLens#732 adds it; it skips assertions and threads xp under JAX, as Fitness does). (2) _source_flux_latents_on_uniform_grid line 621 builds al.Grid2D.from_mask(mask=fit.dataset.grids.lp.mask, over_sample_size=4, xp=xp) inside the jit -> jnp.nonzero needs a static size -> ConcretizationTypeError; the mask is static, so build the grid with xp=np (drop the xp kwarg) and keep xp for image_2d_from. Verified on dataset/simulated/euclid_dr1_like with use_jax=True: with both changes jax.jit(LatentEuclid.variables) returns all 12 latents finite and equal to the eager values. Also add a JAX test: tests/test_compute_latent_variable.py is deliberately JAX-free, so add one test that evaluates LatentEuclid.variables under jax.jit on the vis_lp_model_from model (satisfying the ordering assertion) and asserts every value finite. Witness: the vis_lp search of euclid_dr1_prelim tile 102005065 rerun on the 342398 config writes files/latent/latent_summary.json with all twelve latents populated. Gated on PyAutoLens#732 merging and the RAL libs refreshed.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->
