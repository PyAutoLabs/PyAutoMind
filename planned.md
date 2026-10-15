<!-- toc:start -->

**Contents**

- [isothermal-ell-sph-oversampling-at-the-cusp](#isothermal-ell-sph-oversampling-at-the-cusp)
- [remote-mcp-deployment-tiers](#remote-mcp-deployment-tiers)
- [samples-parameter-paths](#samples-parameter-paths)
- [piemass-potential](#piemass-potential)
- [latent-nan-guard-honest-run](#latent-nan-guard-honest-run)
- [knn-partial-point-block](#knn-partial-point-block)
- [sibson-internal-edge-continuity](#sibson-internal-edge-continuity)
- [adaptsplit-logdet-backend-parity](#adaptsplit-logdet-backend-parity)
- [interferometer-numba-route-gate](#interferometer-numba-route-gate)
- [delaunaynn-wide-row-overhead](#delaunaynn-wide-row-overhead)
- [pulse-interferometer-large-mask](#pulse-interferometer-large-mask)
- [search-ext-b5c-family](#search-ext-b5c-family)

<!-- toc:end -->

## isothermal-ell-sph-oversampling-at-the-cusp
- status: planned — NOT yet a prompt file; file one via `/intake` before starting
- found: 2026-08-09, while pinning B10 of the @rhayes777 audit (`complete/2026/08/autogalaxy-profile-validation-guards.md`)
- classification: library (PyAutoGalaxy) — accuracy / numerical, NOT part of the audit
- summary: `mp.Isothermal(ell_comps=(0,0))` and `mp.IsothermalSph` are the same profile analytically. Under the DEFAULT `over_sample_size=4` their **potential** disagrees by up to **7% at the central pixel** (`0.0707` vs `0.0761`). With `over_sample_size=1` the disagreement collapses to `3.2e-06` — the same order as the deflections (`2.4e-06`). So this is an **over-sampling artefact at the profile's singular centre**, not a broken potential: over-sampling averages sub-pixel values across the `r -> 0` cusp and the two forms diverge there.
- benign baseline (explained, no action): the elliptical form clips `axis_ratio` to `0.99999` for numerical stability while `IsothermalSph` hardcodes `1.0`; that propagates into `einstein_radius_rescaled` (`0.5000025` vs `0.5`) and accounts for the ~1e-6 floor. This is what @rhayes777 reported as B10 and it is correctly pinned.
- why it still matters: the `1e-2` tolerance pinned in `test_autogalaxy/profiles/test_validate.py::test__b10__potential_agrees_between_elliptical_and_spherical_isothermal` papers over that 7% local disagreement, and the same over-sampling-at-a-singularity behaviour may affect other singular profiles.
- CORRECTION on the record: PyAutoGalaxy#566's PR body and the comment on PyAutoGalaxy#440 describe this as the potential agreeing "three orders of magnitude worse" at `1.9e-03` relative, framed as an accuracy defect. That normalised by the GLOBAL MAX potential and mis-attributed the cause. Superseded by the analysis above.
- RETRACTED: the guess that this shares a root cause with `draft/bug/autogalaxy/nfw_truncated_potential_accuracy.md` (MGE decomposition). It does not — MGE is not involved.
- affected-repos:
  - PyAutoGalaxy

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

## knn-partial-point-block
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/609
- filed: 2026-10-02
- prompt: draft/bug/autoarray/fix_knn_neighbor_search_for_a_partial.md
- classification: both
- suggested-branch: feature/knn-partial-point-block
- prior-blocker-cleared: Audit PRs Array611/workspace342 merged 2026-10-02; see complete/2026/10/mesh-interpolator-numerics-audit.md. Survey current claims at start-dev.
- affected-repos:
  - PyAutoArray
  - autolens_workspace_test
- resume: Audit#603 discovered deterministic partial-final-block neighbor corruption; filed separately per explicit user request. No implementation begun or worktree created. Audit retains strict expected-failure witness citing609. Schedule repair independently and promote regression after fix.

## sibson-internal-edge-continuity
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/610
- filed: 2026-10-02
- prompt: draft/bug/autoarray/fix_sibson_interpolation_at_internal_edges.md
- classification: both
- suggested-branch: feature/sibson-internal-edge-continuity
- prior-blocker-cleared: Audit PRs Array611/workspace342 merged 2026-10-02; see complete/2026/10/mesh-interpolator-numerics-audit.md. Survey current claims at start-dev.
- affected-repos:
  - PyAutoArray
  - autolens_workspace_test
- resume: Audit#603 found incorrect internal-edge Sibson weights and near-edge partition failure. Filed separately per explicit user request; strict expected-failure regressions retained in audit. No repair begun or worktree created. Plan algorithmic repair independently.

## adaptsplit-logdet-backend-parity
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/627
- filed: 2026-10-15
- prompt: draft/bug/autoarray/adaptsplit_regularization_log_det_differs_betwee.md
- classification: library
- suggested-branch: feature/adaptsplit-logdet-backend-parity
- blocked-by: interferometer-sparse-data-vector (using PyAutoArray)
- affected-repos:
  - PyAutoArray
- resume: PATCH READY 2026-10-15 (verified in a scratchpad copy: 3 new tests fail-before/pass-after, inversion suite green; session 3e3dea38 scratchpad patch_627.patch — temporary, the diff is also on the issue). ROOT CAUSE (amended plan on #627): backends build different H because mapper_util.adaptive_pixel_signals_from counts zero-weight entries; fix there + two tests, leave log-det code alone. Launched --auto (effective supervised) with the Heart RED development override on the issue (session 3e3dea38). /start_library once the PyAutoArray claim frees.

## interferometer-numba-route-gate
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/628
- filed: 2026-10-15
- prompt: draft/feature/autoarray/interferometer_numba_route_gate_should_scale_wit.md
- classification: both
- suggested-branch: feature/interferometer-numba-route-gate
- blocked-by: interferometer-sparse-data-vector (using PyAutoArray); runs after adaptsplit-logdet-backend-parity by the human's ordering
- affected-repos:
  - PyAutoArray
  - autolens_profiling
- resume: plan on #628; launched --auto (effective supervised) with the Heart RED development override recorded on the issue (session 3e3dea38, 2026-10-15). DelaunayNN #624/#625 merged 2026-10-15 so no factory.py conflict. Library phase first, autolens_profiling re-measurement record second.

## delaunaynn-wide-row-overhead
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/629
- planned: 2026-10-15
- prompt: draft/feature/autoarray/delaunaynn_wide_row_imaging_overhead.md
- classification: library (+ PyAutoPulse campaign ledger)
- suggested-branch: feature/delaunaynn-wide-row-overhead
- blocked-by: interferometer-sparse-data-vector (using PyAutoArray)
- plan: approved by the human 2026-10-15 (session 0b91c774) — full two-level plan on #629; target ≈2× Delaunay at imaging sub 4; Sibson failed rows keep size ≥ 1 (NaN propagates)
- pulse: human asked to log + monitor under a PyAutoPulse speed-up campaign — create `delaunay-nn-cpu` in campaigns.yaml with tasks for #623 (complete, PyAutoArray#624/#625, complete/2026/10/delaunay-nn-numba.md) and #629 once PyAutoPulse is free (Library may start first if PyAutoArray frees earlier)
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 0b91c774, AskUserQuestion "Yes, override for this task"
  - reasons: verbatim on #629
  - permitted: commit, push, PR-open; merge separate
- affected-repos:
  - PyAutoArray
  - PyAutoPulse

## search-ext-b5c-family
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/14
- filed: 2026-10-15
- prompt: draft/research/autofit_inference/search_ext_b5c_second_model_family.md
- status: queued (issued #14 under --auto with the Heart RED development override, not started); blocked-by: ral-category-paths-phase2 (autofit_inference, PyAutoCortex) — launch when that claim is released
- classification: research (autofit_inference primary, PyAutoInsight; PyAutoCortex ledger lines by the architect), Consequence judge, Autonomy supervised; Feature Agent: split-into-phases — #14 scopes stage 1 (protocol, references, pilot manifest + submit), scoring/freeze/scored wave = B5c-2
- suggested-branch: feature/search-ext-b5c-family
- epic: search-extensibility
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 6ffb59e9, AskUserQuestion answer 'Both, override for development (Recommended)' (third grant, night launch)
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready"; "[red] Worktree drift"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
- next: worktree_create search-ext-b5c-family autofit_inference PyAutoInsight; implement per #14; end at PR-open

