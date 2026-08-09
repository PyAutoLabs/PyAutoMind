## rhayes-audit-validation-phases-2-4
- epic: https://github.com/PyAutoLabs/PyAutoArray/issues/415 (OPEN — the public watch point promised to @rhayes777 in all five replies)
- status: planned — phase 1 MERGED and closed 2026-07-29 (PyAutoArray#417 `9411904d`, PyAutoLens#662 `2a3f1a63`, tracker #416 closed, PyAutoLens#531 closed); worktree released, no repo claims held
- filed: 2026-07-28 · phase-1 shipped 2026-07-28
- classification: library (PyAutoArray + PyAutoGalaxy + PyAutoLens) — bug, user-facing
- prompt: draft/bug/autoarray/rhayes_audit_validation_and_crashes.md — CAMPAIGN RECORD ONLY as of 2026-08-09 (phase-1 completion record + the phase 2-4 table); do NOT $start-dev it, start one of the four per-issue prompts below
- split-2026-08-09: phases 2-3 spanned 3 repos / 4 issues — more than one PR — so they were split one-prompt-per-issue:
  - ~~rhayes_333_input_validation_guards.md~~ — PyAutoArray#333, phase 2. **SHIPPED 2026-08-09**: PyAutoArray#440 squash-merged `f2f7a4f`, #333 closed, tracker #439 closed. Record: `complete/2026/08/autoarray-input-validation-guards.md`.
  - draft/bug/autogalaxy/rhayes_440_profile_validation_guards.md — PyAutoGalaxy#440, phase 2 + B10. **UNBLOCKED 2026-08-09.** This prompt is PyAutoGalaxy's claim.
  - draft/bug/autolens/rhayes_532_tracer_validation_guards.md — PyAutoLens#532, phase 2 (B4 + negative redshift). **UNBLOCKED 2026-08-09.** Phase 4 explicitly excluded.
  - draft/bug/autoarray/rhayes_332_adapt_images_precondition_error.md — PyAutoArray#332, phase 3; NO blocker, can start immediately or in parallel.
- suggested-branch: feature/api-validation-guards (per-prompt branches now; one PR each)
- open-issues: PyAutoArray#332, PyAutoGalaxy#440, PyAutoLens#532 stay open until phases 2-3 land. **PyAutoArray#333 CLOSED 2026-08-09.**
- phase-2 (9 constructor guards; #333 B5-B8/B13 + PyAutoGalaxy#440 B9/B11/B12): **HALF SHIPPED 2026-08-09.** PyAutoArray#333 done — PyAutoArray#440 merged `f2f7a4f`. **The blocker is CLEARED:** the shared helper is `autoarray/validate.py` (public), exposing `is_concrete_scalar`, `validate_positive_finite`, `validate_non_negative_finite`, `validate_pixel_scales`, `validate_shape_native`, `validate_radii_ordered`. **Remaining here:** PyAutoGalaxy#440 (B9, B11, B12) + the negative-redshift half of #532 — both now UNBLOCKED and may run in parallel with each other.
- phase-2 CONTRACT for the two remaining prompts (do not reinvent these — import them):
  - `from autoarray import validate`, then call the helper; do NOT write a repo-local `_validate_*`.
  - Message shape: `"<name> must be <rule>; got <value!r}"` + an optional sentence of guidance. Name the parameter, state the rule, show the value.
  - Tracer-safe form: every value guard is gated on `is_concrete_scalar` and passes non-concrete values through untouched. Shape checks need no gate — shapes are static under tracing. VERIFIED against real JAX 0.11.0 in the #333 work, not merely assumed.
  - Zero is permitted where it is a meaningful degenerate request (e.g. a regularization coefficient of 0.0); only negatives and non-finites are rejected.
- phase-3 (#332 + B10): make the missing-`adapt_images` precondition legible — today it surfaces as `AttributeError: 'NoneType' object has no attribute 'array'` from `border_relocator.py:446`, naming nothing the caller controls. The regression test asserts a CLEAR FAILURE, not a successful fit. B10 is a tolerance test only (Ell/Sph 2.357e-06) — do NOT chase bit-identity.
- phase-4 HELD: `z_lens > z_source` warning — question put to @rhayes777 on PyAutoLens#532 2026-07-28, no reply yet. Multi-plane lens-behind-source is legitimate, so warning at most, never an error.
- affected-repos:
  - PyAutoArray
  - PyAutoGalaxy
  - PyAutoLens

## remote-mcp-deployment-tiers
- issue: https://github.com/PyAutoLabs/autofit_assistant/issues/20 (design/scope shipped 2026-07-21; build gated)
- status: DESIGN-COMPLETE, build BLOCKED-ON-DEMAND — issue #20 holds the full auth/transport/hosting design + Richard/PyAutoMCP coordination. No code, no network surface built. Per prompt "if it earns it": build tiers 2/3 only once demonstrated demand for REMOTE access exists.
- filed: 2026-07-21
- prompt: draft/feature/autofit_assistant/remote_mcp_deployment_tiers.md
- classification: feature (autofit_assistant + autolens_assistant) — transport/deployment/auth, NOT new tools
- suggested-branch: feature/remote-mcp-deployment-tiers
- blocked-by: (1) demonstrated demand for remote access; (2) MANDATORY security-review skill pass before any PR — never auto-ship (network-facing arbitrary-file-read surface; intake mis-sized it small/safe)
- summary: tier2 = opt-in `mcp.run(streamable-http)` + bearer-token ASGI middleware + `PYAUTO_MCP_ALLOWED_ROOTS` path confinement behind cloudflared/ngrok (default stays stdio); tier3 = hosted OAuth/OIDC + per-user scoping (Euclid sample triage; rhayes777/aggregator-agent consumer). Coordinate with Richard FIRST (rhayes777/PyAutoMCP = broader compute/optimise MCP, no transport/auth layer yet) — converge on profiles sharing one auth/transport layer, or share only the tunnel recipe.
- affected-repos:
  - autofit_assistant
  - autolens_assistant

## samples-parameter-paths
- prompt: draft/bug/health_fixes/samples_parameter_paths.md
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1327 (open, parked)
- status: parked
- filed: 2026-07-08
- classification: library (PyAutoFit) — bug, health_fixes cluster
- suggested-branch: feature/samples-parameter-paths
- blocked-by: clean-output CI re-validation (does NOT reproduce on current main)
- summary: |
    Investigated the PyAutoHeart #27 release KeyError in
    parameter_lists_for_paths. Does NOT reproduce on current main: two legs
    (shapelets 125-prior Basis; multi-analysis 22-prior) pass in-memory AND via
    true from-disk reload (model.json + samples.csv), plus all synthetic
    round-trips. The 745117bd7 fix (May 2026) was already in main at the
    2026-07-06 run; failure most consistent with STALE cached output/ in the
    release run. No library fix warranted — parked pending a clean-output CI
    re-run. Sibling health_fixes/ prompts from the same run are suspect too.
    Full trail: PyAutoFit#1327 comments.
- affected-repos:

## jax-point-source-point-smoke-sentinel
- prompt: draft/bug/autolens/jax_point_source_point_smoke_sentinel.md
- status: planned
- filed: 2026-05-21
- classification: library (triage; routing TBD by bisect)
- suggested-branch: feature/jax-point-source-point-smoke-sentinel
- summary: |
    Pre-existing regression surfaced during fast-viz-zero-contour-perf smoke.
    `autolens_workspace_test/scripts/jax_likelihood_functions/point_source/point.py`
    fails its hardcoded `-83.38049778` literal — `fitness._vmap` returns the
    `-1e99` non-finite-likelihood sentinel from `FitPositionsImagePairAll` on
    canonical main of all three libraries. Last known good: 2026-05-08
    (autolens_workspace_test@362cfa8 rebaseline). Sibling JAX point-source
    profiling drift already tracked as PyAutoLens#514; this is a more severe
    symptom on a different file — held as two hypotheses (same root cause /
    independent regression) for triage.

    Affected repos (when resumed):
      - PyAutoLens (likely primary — PointSolver / FitPositionsImagePairAll)
      - PyAutoGalaxy or PyAutoArray (possible — bisect will say)
      - autolens_workspace_test (literal rebaseline OR no change, depending on outcome)

    Sibling smoke scripts to check while triaging: image_plane.py,
    source_plane.py in the same dir — they share the seed dataset.

## nfw-truncated-potential-accuracy
- prompt: draft/bug/autogalaxy/nfw_truncated_potential_accuracy.md
- status: planned
- filed: 2026-06-05
- classification: library (accuracy bug)
- suggested-branch: feature/nfw-truncated-potential-accuracy
- summary: |
    Pre-existing accuracy bug surfaced while shipping dark-matter-potentials.
    NFWTruncatedSph.potential_2d_from (MGE) fails grad(psi)=alpha self-
    consistency in autolens_workspace_test/scripts/mass/dark.py (med 7.1e-2 vs
    ~8e-4 for every other NFW/gNFW/cNFW variant). Deflections pass, only the
    potential is off — likely the MGE sigma range (radii_max = truncation_radius
    * 5) is too narrow. Reproduce on clean main first.
- affected-repos:
  - PyAutoGalaxy


## piemass-potential
- prompt: draft/feature/autogalaxy/piemass_potential.md
- status: planned
- filed: 2026-06-05
- classification: library (missing feature)
- suggested-branch: feature/piemass-potential
- summary: |
    PIEMass (Lenstool-ported PIE) has no potential_2d_from, so it now raises a
    clean NotImplementedError (post dark-matter-potentials) and crashes tracer
    visualization (potential FITS extension) — same class as the original NFW
    bug, different profile. No MGE/CSE decomposition hook exists; needs an
    analytic port (Kassiola & Kovner 1993, or the dPIEMass r_s->inf limit) or a
    new convergence-MGE hook. Validate via grad(psi)=alpha self-consistency.
- affected-repos:
  - PyAutoGalaxy

## latent-nan-guard-honest-run
- issue: NEEDS A FRESH ISSUE — #1413 was auto-closed when PyAutoFit#1415 merged (its `Closes` line). Library half is DONE+MERGED; file a new issue for this workspace half at /start_dev time.
- planned: 2026-07-22
- classification: workspace
- suggested-branch: feature/latent-nan-guard-honest-run
- blocked-by: slow-skip-timeout-cap-doc (using autolens_workspace_test; PR #194 OPEN/MERGEABLE)
- affected-repos:
  - autolens_workspace_test
- note: latent/latent_nan_robustness.py PASSES but VACUOUSLY under the smoke profile — TEST_MODE=2 yields only 4 bypass samples, and DISABLE_JAX=1 silently flips its deliberate AnalysisImaging(use_jax=True) to False (PyAutoLens analysis/analysis/dataset.py:89), so the JAX column-masking branch the guard exists to catch is never taken. MultiStartAdam/BlackJAXNUTS precedent. Work = (1) config/build/env_vars.yaml override for `latent/latent_nan_robustness` with unset: [PYAUTO_TEST_MODE, PYAUTO_DISABLE_JAX]; (2) trim the script under the 300s cap. MEASURED: honest run = 412s; PYAUTO_TEST_MODE=1 does NOT help (455s) — Nautilus is NOT the bottleneck (~136s post-fit results update + ~56s latent compute on 100 samples), so the lever is sample count. Script is in the curated smoke_tests.txt, which DOES read env_vars.yaml, so this lands in the per-PR gate. Adjacent to the blocker's own follow-up ("re-time the SLOW siblings"). NOT bugs, verified passing from clean output, no change needed: imaging/model_fit.py and latent/latent_variables_smoke.py.
