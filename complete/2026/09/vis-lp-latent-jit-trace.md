## vis-lp-latent-jit-trace
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/66
- completed: 2026-09-10
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/67
  (merge commit `2a8b4db52ea066c2e7df679624bd4bc03401b997`)
- summary: The JAX (GPU) `vis_lp` stage wrote **no** latents at all — RAL job
  342398, all ten `euclid_dr1_prelim` tiles. PyAutoFit's latent engine evaluates
  the latents inside a per-sample `jax.jit` (`LatentLens.BATCH_MODE = "jit"`) and
  turns any raise inside the trace into a NaN row for every sample, so two
  independent trace-time failures in `util.py` silenced the whole file:
  (1) `LatentEuclid.variables` built its instance with
  `model.instance_from_vector`, which checks the `vis_lp` ordered-MGE-bases
  assertion (`order_bases=True`, added 2026-09-08) by applying a Python `not` to a
  traced boolean → `jax.errors.TracerBoolConversionError`; it now goes through
  `autolens.analysis.latent.latent_instance_from`, which skips the assertions
  under JAX and threads `xp`, exactly as `Fitness` does. `LatentEuclid` overrides
  `LatentLens.variables` (it must, for the four Euclid aperture latents), so it
  could not inherit the library-side fix.
  (2) `_source_flux_latents_on_uniform_grid` built the uniform reference grid with
  `al.Grid2D.from_mask(..., xp=xp)`, reaching `jnp.nonzero` with a size unknown at
  trace time → `jax.errors.ConcretizationTypeError`; the mask is static, so the
  grid is now built on NumPy and `xp` stays on the `image_2d_from` that is the
  traced quantity.
  A third, unrelated drift fix rode along: the `_EmptyRow` stub in
  `tests/test_catalogue_parity.py` gained `known_paths: frozenset = frozenset()`.
  PyAutoFit#1598 made `Column._check_argument` consult that keyspace and the stub
  predates it, so all four parametrized header cases were already failing on
  `main` at 22abf6a with `AttributeError`.
- trap: both failures are **trace-time only**, so the module's eager
  known-answer tests pass on the broken code and the engine reports nothing — a
  NaN latent row, not an exception. Only jitting the *whole* `variables` call
  reproduces either; an eager call sees neither.
- trap: CI proved nothing here. PyAutoHeart's reusable `smoke-tests.yml` skips
  its matrix on `pull_request` when no path under `scripts/`, `config/` or
  `.github/` changed, so this `util.py` + `tests/` diff left `unit / smoke`,
  `slow / smoke` and `smoke / smoke` all reporting `skipping` — no pytest ran on
  the PR at all. Merged on the local serial run, the same basis pipeline PR #65
  was merged on the same day. Gap filed as
  `draft/bug/pyautoheart/smoke_gate_skips_pytest_runners_on_pr.md`.
- test: `tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit`
  jits the whole `variables` call on the `vis_lp` model — the model that actually
  carries the ordering assertion, built via `scripts/initial_lens_model.py:vis_lp_model_from`
  at the simulated dataset's own mask radius and centre — with a median-prior
  vector whose two lens-basis `ell_comps_1` entries are separated so the
  assertion is satisfied. It asserts all twelve `LatentEuclid.keys` present and
  finite and equal to the eager NumPy evaluation (`rel=1e-3`);
  `effective_einstein_radius` is asserted finite but not compared, since the two
  backends use different solvers and the median-prior mass model's tangential
  critical curve is multi-valued (a pre-existing library property).
  Local serial `pytest -q -m "not slow" tests` → **94 passed, 3 deselected, 0
  failed**, with each `util.py` hunk revert-checked one at a time: hunk 1
  reverted → `TracerBoolConversionError`; hunk 2 reverted →
  `ConcretizationTypeError`; both in place → 1 passed.
- library half: PyAutoLens#734 (`latent_instance_from`) merged to `main` at
  `0da06de6` before this PR; diagnosis in PyAutoLens#732. Library-first gate
  satisfied at merge.
- witness outstanding: the prompt's witness — the `vis_lp` search of
  `euclid_dr1_prelim` tile 102005065 rerun on the 342398 config writing
  `files/latent/latent_summary.json` with all twelve latents populated — is
  produced by the **science rerun phase**, after the RAL libraries are refreshed
  to the merged PyAutoLens `main`. This PR carries the unit-test half of the
  witness (`variables` under `jax.jit`, every value finite); the RAL half is not
  claimed here.
- siblings: task A2 of a three-task session. A1 is PyAutoFit#1601 and A3 is the
  `autolens_workspace_test` latent smoke; both were worked in the same session
  against the same latent path.
- session: `claude --resume session_01CybZmqjyQRDpfK3Cs1JaW2`; worktree
  `~/Code/PyAutoLabs-wt/vis-lp-latent-jit-trace`, removed at close-out.

## Original prompt

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
Issued: 2026-09-10

euclid pipeline: LatentEuclid.variables cannot be traced under the per-sample jax.jit the PyAutoFit latent engine uses, so the JAX (GPU) vis_lp stage writes no latent output (RAL job 342398, all ten euclid_dr1_prelim tiles; PyAutoLens#732 has the full diagnosis). Two independent trace failures in util.py: (1) line 516 'instance = model.instance_from_vector(vector=parameters)' checks the vis_lp ordered-MGE-bases assertion (order_bases=True, added 2026-09-08) with a Python 'not' on a traced boolean -> jax.errors.TracerBoolConversionError; replace with autolens.analysis.latent.latent_instance_from(model=model, parameters=parameters, xp=xp) (PyAutoLens#732 adds it; it skips assertions and threads xp under JAX, as Fitness does). (2) _source_flux_latents_on_uniform_grid line 621 builds al.Grid2D.from_mask(mask=fit.dataset.grids.lp.mask, over_sample_size=4, xp=xp) inside the jit -> jnp.nonzero needs a static size -> ConcretizationTypeError; the mask is static, so build the grid with xp=np (drop the xp kwarg) and keep xp for image_2d_from. Verified on dataset/simulated/euclid_dr1_like with use_jax=True: with both changes jax.jit(LatentEuclid.variables) returns all 12 latents finite and equal to the eager values. Also add a JAX test: tests/test_compute_latent_variable.py is deliberately JAX-free, so add one test that evaluates LatentEuclid.variables under jax.jit on the vis_lp_model_from model (satisfying the ordering assertion) and asserts every value finite. Witness: the vis_lp search of euclid_dr1_prelim tile 102005065 rerun on the 342398 config writes files/latent/latent_summary.json with all twelve latents populated. Gated on PyAutoLens#732 merging and the RAL libs refreshed.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->
