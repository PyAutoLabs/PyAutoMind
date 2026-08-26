<!-- toc:start -->

**Contents**

- [isothermal-ell-sph-oversampling-at-the-cusp](#isothermal-ell-sph-oversampling-at-the-cusp)
- [remote-mcp-deployment-tiers](#remote-mcp-deployment-tiers)
- [samples-parameter-paths](#samples-parameter-paths)
- [piemass-potential](#piemass-potential)
- [latent-nan-guard-honest-run](#latent-nan-guard-honest-run)
- [submit-wall-per-cell-throughput](#submit-wall-per-cell-throughput)

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
- note: latent/latent_nan_robustness.py PASSES but VACUOUSLY under the smoke profile — TEST_MODE=2 yields only 4 bypass samples, and DISABLE_JAX=1 silently flips its deliberate AnalysisImaging(use_jax=True) to False (PyAutoLens analysis/analysis/dataset.py:89), so the JAX column-masking branch the guard exists to catch is never taken. MultiStartAdam/BlackJAXNUTS precedent. Work = (1) config/build/env_vars.yaml override for `latent/latent_nan_robustness` with unset: [PYAUTO_TEST_MODE, PYAUTO_DISABLE_JAX]; (2) trim the script under the 300s cap. MEASURED: honest run = 412s; PYAUTO_TEST_MODE=1 does NOT help (455s) — Nautilus is NOT the bottleneck (~136s post-fit results update + ~56s latent compute on 100 samples), so the lever is sample count. Script is in the curated smoke_tests.txt, which DOES read env_vars.yaml, so this lands in the per-PR gate. Adjacent to the blocker's own follow-up ("re-time the SLOW siblings"). NOT bugs, verified passing from clean output, no change needed: imaging/model_fit.py and latent/latent_variables_smoke.py.

## submit-wall-per-cell-throughput
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/176
- filed: 2026-08-26
- prompt: draft/bug/autolens_profiling/submit_wall_estimates_per_cell_throughput.md
- classification: workspace (autolens_profiling only) — plan APPROVED, issue filed with the
  full two-level plan; blocked only on the worktree claim, not on any open design question.
- suggested-branch: feature/submit-wall-per-cell-throughput
- blocked-by: log-det-multistart-tag (using autolens_profiling) — claimed mid-session by
  session_01MdmS2jfUPi8BNjtDVBjBYX at PyAutoMind d9bfff9d, after this task's branch survey
  read a clean `worktree_list_claimed`. NO FILE OVERLAP: #175 edits
  `scripts/misc/searches/_samplers.py`; this task adds `scripts/misc/wall/` and edits
  `hpc/batch_gpu/submit_search_*` + `.github/workflows/lint.yml`. The block is the
  one-worktree-per-repo rule, not a real collision — a human may fold this into #175's
  worktree instead of waiting.
- summary: |
    RAL job 340576 lost 35 of 39 arms (an overnight A100 block) because
    `submit_phase8b_bijector_a100` justified `--time=0:30:00` with an MGE step rate for an
    array whose arms are mostly knn and delaunay_adapt_split. Measured 2026-08-25:
    mge 0.117 s/step, knn 2.23 (19x), delaunay_adapt_split 4.83 (41x) -- so "6x headroom"
    was ~8x short for knn, ~16x short for delaunay. Those rates are recorded NOWHERE in the
    repo, and only 11 of 82 submits state any wall basis. Fix: `scripts/misc/wall/rates.py`
    (curated per-cell table mirroring `vram/config.py`, lookup RAISES on an unmeasured cell
    rather than falling back to a neighbour), a `# WALL-BASIS:` header required on
    `submit_search_*`/`submit_phase8b_*`, `check_submits.py` gating every cell a submit runs
    against its own row + its `--time`, wired into `lint.yml`; phase8b `--time` -> 6:00:00
    from its SLOWEST cell. Sibling of #175 -- both came out of the same 340576 post-mortem
    and both gate the Phase 8B rerun.
- affected-repos:
  - autolens_profiling
