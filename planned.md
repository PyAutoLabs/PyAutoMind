## hygiene-orphan-config-files
- issue: none yet (issued when unblocked)
- planned: 2026-07-23
- classification: feature (PyAutoBrain) + config cleanup across 9 workspace/test/assistant repos
- suggested-branch: feature/hygiene-orphan-config-files
- blocked-by: env-profile-derivation step 6 (`feature/env-profile-rename`, PyAutoBrain#154 OPEN) claims PyAutoBrain + autocti_workspace_test + autofit_workspace_test + autogalaxy_workspace_test + autolens_workspace_test + euclid_strong_lens_modeling_pipeline — 6 of this task's 10 repos. NOTE: zero FILE-level overlap (that branch touches 6 docs/agent files in PyAutoBrain, none of them `_hygiene_config.py` or `tests/test_hygiene_conductor.py`), so this is a claim-level block only. Unblocks the moment #154 and its sibling rename PRs merge.
- prompt: draft/feature/pyautobrain/hygiene_orphan_config_files.md
- summary: `/hygiene config` cannot see orphan config FILES — `_hygiene_config.py:67` skips any library yaml lacking a workspace counterpart, and the loop only iterates LIBRARY yamls, so a workspace file with no library counterpart is structurally invisible. That is how dead `grids.yaml` survived ~1yr in 10 repos. The earlier prototype flagged by FILENAME orphanhood (120 instances / 30 distinct, nearly all legitimate) and was correctly not shipped; the right signal is REACHABILITY (does anything READ it), which separates the noise by OWNER: `build/*` -> PyAutoHands (~39, legit), `priors/*` -> JSONPriorConfig path resolution (~40, legit), `non_linear/{nest,mle,mcmc}.yaml` -> NOTHING (~26, DEAD). Suppression = explicit owner map in the checker, deliberately NOT a per-repo .hygieneignore (20 new files + a config surface that can itself go stale = the failure mode being fixed). ACCEPTANCE TEST: must flag grids.yaml on the pre-deletion tree, flag non_linear today, stay silent on build/* and priors/*.
- finding: `config/non_linear/{nest,mle,mcmc}.yaml` is DEAD in 9 repos — verified 2026-07-23 that no library reads `conf.instance["non_linear"]` for them (all 6 libs checked); Nautilus takes defaults from the Python signature (`search/nest/nautilus/search.py:41` `n_live: int = 3000`) while `nest.yaml` says `n_live: 200`. The 3 user-facing workspaces already dropped them. `non_linear/GridSearch.yaml` IS live — do not remove.
- affected-repos:
  - PyAutoBrain
  - autocti_assistant
  - autocti_workspace
  - autocti_workspace_test
  - autofit_workspace_developer
  - autofit_workspace_test
  - autogalaxy_workspace_test
  - autolens_assistant
  - autolens_workspace_test
  - euclid_strong_lens_modeling_pipeline


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

## brain-lifecycle-path-fixes (build-chain umbrella Phase 0b)
- issue: none yet (issued when unblocked)
- planned: 2026-07-16
- classification: library (PyAutoBrain) — bug
- suggested-branch: feature/brain-lifecycle-path-fixes
- blocked-by: workspace-agent + wake-up-skill-rename (both claim PyAutoBrain)
- summary: fix the two pre-lifecycle-split path assumptions — draft/bug/pyautobrain/intake_writes_legacy_layout.md (intake writer) + draft/bug/pyautobrain/feature_agent_path_parser_predates_lifecycle_split.md (feature-agent parser; live-confirmed misroute 2026-07-16). Parent epic: PyAutoBuild#155.
- affected-repos:
  - PyAutoBrain

## lenstool-scaling-slam (PR3 of the lenstool reference-magnitude series)
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/265 (parent; PR1 #267 + PR2 #268 merged)
- status: planned — never started; branch/worktree released 2026-07-13 when the autolens_workspace claim was freed
- filed: 2026-07-13
- classification: workspace (autolens_workspace) — docs
- summary: apply the LensTool reference-magnitude (mag0) scaling convention (fixed reference luminosity, exponent 0.5, full dPIE r_core/r_cut/b0 + ra_ref scaling) to the SLaM pipelines, mirroring what #267 (cluster) and #268 (group+imaging) did for the example scripts. See complete.md `lenstool-scaling-reference-magnitude` for the delivered pattern + the notebook-regen catalogue-drift gotcha.
- SUPERSEDED 2026-07-17: delivered inside dpie-lenstool-default (PyAutoGalaxy#506 workspace PR autolens_workspace#287) — group SLaM scaling tiers now use the reference-anchored convention. Remove on next planned.md sweep.

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
- prompt: PyAutoMind/issued/jax_point_source_point_smoke_sentinel.md
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
