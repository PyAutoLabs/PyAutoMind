## rhayes-audit-validation-phases-2-4
- epic: https://github.com/PyAutoLabs/PyAutoArray/issues/415 (OPEN — the public watch point promised to @rhayes777 in all five replies)
- status: **PHASES 1-3 ALL SHIPPED; ONLY PHASE 4 REMAINS (held on the reporter).** phase 1 MERGED and closed 2026-07-29 (PyAutoArray#417 `9411904d`, PyAutoLens#662 `2a3f1a63`, tracker #416 closed, PyAutoLens#531 closed); worktree released, no repo claims held
- filed: 2026-07-28 · phase-1 shipped 2026-07-28
- classification: library (PyAutoArray + PyAutoGalaxy + PyAutoLens) — bug, user-facing
- prompt: draft/bug/autoarray/rhayes_audit_validation_and_crashes.md — CAMPAIGN RECORD ONLY as of 2026-08-09 (phase-1 completion record + the phase 2-4 table); do NOT $start-dev it, start one of the four per-issue prompts below
- split-2026-08-09: phases 2-3 spanned 3 repos / 4 issues — more than one PR — so they were split one-prompt-per-issue:
  - ~~rhayes_333_input_validation_guards.md~~ — PyAutoArray#333, phase 2. **SHIPPED 2026-08-09**: PyAutoArray#440 squash-merged `f2f7a4f`, #333 closed, tracker #439 closed. Record: `complete/2026/08/autoarray-input-validation-guards.md`.
  - ~~rhayes_440_profile_validation_guards.md~~ — PyAutoGalaxy#440, phase 2 + B10. **SHIPPED 2026-08-09**: PyAutoGalaxy#566 squash-merged `a366f77`, #440 closed. Record: `complete/2026/08/autogalaxy-profile-validation-guards.md`. Also carried the negative-redshift half of #532 (see the ownership note below).
  - ~~rhayes_532_tracer_validation_guards.md~~ — PyAutoLens#532, phase 2 (B4). **SHIPPED 2026-08-09**: PyAutoLens#696 squash-merged `65183d1`, #532 closed. Record: `complete/2026/08/autolens-tracer-validation-guards.md`.
  - ~~rhayes_332_adapt_images_precondition_error.md~~ — PyAutoArray#332, phase 3. **SHIPPED 2026-08-09**: PyAutoArray#442 squash-merged `5dedb5e`, #332 closed. Record: `complete/2026/08/autoarray-adapt-images-precondition.md`.
- suggested-branch: feature/api-validation-guards (per-prompt branches now; one PR each)
- open-issues: **ALL FOUR CLOSED 2026-08-09** — PyAutoArray#333, PyAutoArray#332, PyAutoGalaxy#440, PyAutoLens#532. Only the epic PyAutoArray#415 stays open, for phase 4.
- phase-2: **COMPLETE 2026-08-09.** All three PRs merged — PyAutoArray#440 (`f2f7a4f`), PyAutoGalaxy#566 (`a366f77`), PyAutoLens#696 (`65183d1`). Issues #333, #440, #532 all closed.
- **#532 ownership note (worth remembering):** the negative-redshift half of PyAutoLens#532 was implemented in **PyAutoGalaxy**, not PyAutoLens. `al.Galaxy` IS `ag.Galaxy`, so the class and its `redshift` assignment live at `autogalaxy/galaxy/galaxy.py:52`; a Tracer-level check would have missed a bare `al.Galaxy(redshift=-0.5)`, which is the reported reproduction. **The repo an issue is filed on is where the user hit it, not necessarily where the attribute is set — check the assignment site before scoping.**
- **phase-4 guard-rails ARE NOW IN PLACE.** Control tests pin today's permissive `z_lens > z_source` behaviour at both `Galaxy` (PyAutoGalaxy#566) and `Tracer` (PyAutoLens#696) level. Phase 4 cannot turn it into an error without those tests failing — which is the intended tripwire, not an obstacle.
- shared-helper CONTRACT (established by #333, used by #440/#532 — reuse for any future guard):
  - `from autoarray import validate`; do NOT write a repo-local `_validate_*`. PyAutoGalaxy adds only per-parameter explanations in `autogalaxy/profiles/validate.py`.
  - Message shape: `"<name> must be <rule>; got <value!r>"` + an optional sentence of guidance. Name the parameter, state the rule, show the value.
  - Tracer-safe form: gate every value guard on `is_concrete_scalar`; pass non-concrete values through untouched. Shape/container checks need no gate. VERIFIED against real JAX 0.11.0.
  - Zero is permitted where it is a meaningful degenerate request (regularization coefficient, redshift); only negatives and non-finites are rejected.
- phase-3: **COMPLETE 2026-08-09.** B10 shipped with PyAutoGalaxy#566 (tolerance pins); #332 shipped as PyAutoArray#442 (`5dedb5e`). #332 decision recorded: fail-fast naming `adapt_images` rather than having the mesh self-wire the image-plane grid (the reporter's own suggestion) — building that grid needs a weighting policy, which is what `adapt_images` carries, so self-wiring would silently make a science choice for the user. Diagnosis correction: the `None` is `mesh_grid` (`border_relocator.py:450`), NOT `grid` (line 446) as recorded here previously.
- **NEW finding, not from the audit — needs its own prompt:** while pinning B10, the Ell/Sph **potential** was measured as well as the deflections the report covered. `Isothermal(ell_comps=(0,0))` vs `IsothermalSph` agree to 1.9e-03 RELATIVE on the potential, versus 2.4e-06 on deflections and 1.5e-06 on convergence — three orders of magnitude worse, for two forms that are analytically identical. NOT fixed; the tolerance is pinned at the observed level as a ratchet with a docstring saying so. Possibly the same class as `draft/bug/autogalaxy/nfw_truncated_potential_accuracy.md` (MGE potential accuracy) — worth investigating together.
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
