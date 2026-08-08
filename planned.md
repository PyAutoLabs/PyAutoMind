## rhayes-audit-validation-phases-2-4
- epic: https://github.com/PyAutoLabs/PyAutoArray/issues/415 (OPEN — the public watch point promised to @rhayes777 in all five replies)
- status: planned — phase 1 MERGED and closed 2026-07-29 (PyAutoArray#417 `9411904d`, PyAutoLens#662 `2a3f1a63`, tracker #416 closed, PyAutoLens#531 closed); worktree released, no repo claims held
- filed: 2026-07-28 · phase-1 shipped 2026-07-28
- classification: library (PyAutoArray + PyAutoGalaxy + PyAutoLens) — bug, user-facing
- prompt: draft/bug/autoarray/rhayes_audit_validation_and_crashes.md (carries the phase-1 completion record + the phase 2-4 table)
- suggested-branch: feature/api-validation-guards
- open-issues: PyAutoArray#332, PyAutoArray#333, PyAutoGalaxy#440, PyAutoLens#532 — all stay open until phases 2-3 land
- phase-2 (9 constructor guards; #333 B5-B8/B13 + PyAutoGalaxy#440 B9/B11/B12): needs the shared `_validate_*` home decision — PyAutoArray is the natural floor. Constructors are JAX-traced: no Python `if` on a possible tracer. The negative-redshift half of #532 rides here, NOT with phase 4.
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
- prompt: PyAutoMind/bug/health_fixes/samples_parameter_paths.md
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

## heart-ci-linkage
- prompt: PyAutoMind/feature/pyautoheart/ci_linkage.md
- status: planned
- filed: 2026-06-30
- classification: organism (PyAutoHeart CI signal + registry)
- suggested-branch: feature/heart-ci-linkage
- milestone: M0 (foundational — release-validation gate builds on a trustworthy CI signal)
- summary: |
    Final-review finding: Heart's CI signal is too coarse/narrow to gate a
    release. ci_status reads `gh run list --limit 1` (newest run, any workflow,
    any branch) but workspaces gate on 3 workflows × 2 Pythons; readiness gates
    only the 5 libraries' CI (workspace CI observed but never gated); and the
    signal should come from the Actions server (mobile-reachable via MCP) with
    report.json as enrichment, not a hard dependency. Plus repos.yaml is stale
    (PyAutoPrompt→Mind, PyAutoPaper→Memory; organism repos unpolled). Rework
    ci_status to per-required-workflow-on-main, gate workspace CI, make the run
    conclusion the primary test_run signal, refresh the registry.
- affected-repos:
  - PyAutoHeart

## heart-release-validation
- prompt: PyAutoMind/feature/pyautoheart/release_validation.md
- status: planned
- filed: 2026-06-30
- classification: organism (PyAutoHeart deep validation + report + readiness gate)
- suggested-branch: feature/heart-release-validation
- milestone: M2 (depends on M1 = build-testpypi-rehearsal-mode)
- boundary: |
    Heart never mutates a repo and never triggers a build. The Brain Release
    Agent dispatches the rehearsal + validation workflows and awaits them; Heart's
    `validate` is ingest-and-judge only; the Health Agent (read-only) reports the
    verdict. Heart and Build never call each other.

## heart-release-profile-wheel-integration
- prompt: PyAutoMind/feature/pyautoheart/release_profile_and_wheel_integration.md
- status: planned
- filed: 2026-06-30
- classification: organism (validation fidelity — wheels + release env profile)
- suggested-branch: feature/heart-release-profile-wheel-integration
- milestone: M3 (depends on M1 + M2; closes Gaps A & B)
- summary: |
    Make the validation run install the TestPyPI wheels (no source on PYTHONPATH,
    scripts run from inside the workspace checkout so autoconf resolves workspace
    config/) and run at release fidelity via a named `release` env profile
    (user workspaces TEST_MODE=1+small+fast; *_test TEST_MODE=0, full-res),
    mirroring release.yml's tier split. Env-var profile only — does not touch
    config/general.yaml test:/version: toggles.
- affected-repos:
  - PyAutoHeart
  - PyAutoBuild
  - autolens_workspace_test / autogalaxy_workspace_test / autofit_workspace_test
  - autolens_workspace / autogalaxy_workspace / autofit_workspace
- summary: |
    New third Heart tier: a release-grade `pyauto-heart validate` that composes
    a TestPyPI build rehearsal + unit tests + the full workspace/workspace_test
    integration surface, ingests the run reports into a tracked
    `validation_report.json`, and hard-gates `readiness` GREEN on a fresh pass
    for the current source SHAs. Driven from mobile via the Brain health agent
    (GitHub dispatch/poll via MCP; Heart stays credential-free). Bakes in two
    verified gaps the current `workspace-validation.yml` has: it tests source
    not wheels (PYTHONPATH-shadow), and it runs the smoke profile
    (PYAUTO_TEST_MODE=2 + PYAUTO_SMALL_DATASETS=1) not a release-fidelity profile.
- affected-repos:
  - PyAutoHeart
  - PyAutoBrain
  - PyAutoBuild

## build-testpypi-rehearsal-mode
- prompt: PyAutoMind/feature/pyautobuild/release_yml_testpypi_rehearsal_mode.md
- status: planned
- filed: 2026-06-30
- classification: organism (PyAutoBuild executor capability)
- suggested-branch: feature/build-testpypi-rehearsal-mode
- milestone: M1 (prerequisite for M2 = heart-release-validation)
- summary: |
    Add a TestPyPI-only "rehearsal" dispatch mode to release.yml: build current
    source, publish to TestPyPI, emit the version string, and STOP before
    PyPI/tag/notebook steps — so Heart can install and validate the actual wheels
    before any release. Small, isolated, highest-value first piece.
- affected-repos:
  - PyAutoBuild

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
- prompt: PyAutoMind/bug/autogalaxy/nfw_truncated_potential_accuracy.md
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
- prompt: PyAutoMind/feature/autogalaxy/piemass_potential.md
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

## notebook-kernel-cwd-auto-simulate
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/204
- prompt: draft/bug/workspaces/notebook_kernel_cwd_breaks_auto_simulate.md
- status: planned
- filed: 2026-07-27
- classification: library+workspace (PyAutoHands runner vs per-script path resolution — fix option is a HUMAN CALL, see prompt)
- suggested-branch: feature/notebook-kernel-cwd-auto-simulate
- summary: |
    jupyter nbconvert runs the kernel in the NOTEBOOK'S OWN directory, but the
    auto-simulate guard shells out to a workspace-root-relative simulator path.
    So every notebook that auto-simulates dies with exit status 2 ("can't open
    file"). Proven empirically: launcher cwd .../cwdtest, kernel cwd
    .../cwdtest/notebooks/sub. Accounts for ~20 of the 29 failing jobs in
    workspace-validation run 30242158468. Scripts are unaffected (they do run
    from the root), which is why run_scripts mostly passes and run_notebooks
    mostly fails.

## auto-simulate-guard-wrong-simulator-target
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/359
- prompt: draft/bug/autolens_workspace/auto_simulate_guard_wrong_simulator_target.md
- status: planned
- filed: 2026-07-27
- classification: workspace
- suggested-branch: feature/auto-simulate-guard-wrong-simulator-target
- summary: |
    likelihood_function.py scripts load dataset/imaging/simple but their
    auto-simulate guard runs no_lens_light/simulator.py, which writes
    simple__no_lens_light — so the guard fires and the load still fails. Guard
    target dates to 1f39244f; surfaced now because #354 swapped the raw
    path-exists check for should_simulate. FIRST establish whether the target
    was always wrong or should_simulate changed the predicate (the latter would
    be a much wider bug), THEN sweep all 116 migrated guards for the same
    mismatch.
