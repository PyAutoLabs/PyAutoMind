## release-validation-tail-burndown
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/72 (closed)
- completed: 2026-07-14
- repos: (epic — coordinated PyAutoConf/Fit/Array/Galaxy/Lens + workspaces)
- summary: EPIC/capstone. Burned down the 18f/5t mode=release tail. All real correctness bugs fixed+merged+validated on wheels (A jax-drift, B param9 #164, D database #1367, E aggregator #274, F CSE #499, G interferometer #606, inversion #388, + jax_grad-config/timeout/shapelets-delaunay no_run). Structural perf-flake tail resolved by SLOW-no_run'ing the flaky real-search population (alwt#169, agwt#73) — lean choice over a reverted advisory tier (#74). Fresh mode=release run v2026.7.14.1.dev66001 = 542p/0f/0t/87s → release_ready true → Heart RED→YELLOW (score 65, zero RED). See project_release_2026_07_13_blocked_3bugs.

## Original prompt

# Release-validation tail burn-down — clear the 18f/5t so mode=release goes GREEN

Type: test
Target: release_validation
Repos:
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- autolens_workspace_test
- autogalaxy_workspace_test
- autofit_workspace_test
- PyAutoFit
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

## Context — where the release stands (2026-07-13)

The three release-BLOCKER bugs from the held 2026-07-13 release are **fixed, merged,
and confirmed on wheels** (see `complete/2026/07/{matern-kernel-tfp-jax-incompat,
jax-pytree-partition-vars-no-dict,verify-install-check-f-autosimulate-and-dep-pin}.md`
and memory `project_release_2026_07_13_blocked_3bugs`):
- Matern tfp×jax → PyAutoArray#386 (merged)
- pytree leaf-int registration → PyAutoFit#1366 (merged)
- verify_install Check-F → PyAutoHeart#71 (merged)

Re-validation on the wheels (TestPyPI **2026.7.13.1.dev65601**) improved the full
release-fidelity script set from **530p/26f** → **539p/18f (+5 timeout)**, with the 3
bugs cleared and **zero regressions** (confirmed no `vars()`/`_partition`/pytree crash
anywhere; the 2 "new" failures are timeout flakes). But Heart stays **RED** because
`workspace-validation.yml mode=release` runs the FULL script set and RED-blocks on ANY
integrate failure — so the **pre-existing long tail** now gates the release. This task
is to burn that tail down to GREEN (or reclassify it), so the release can proceed.

**Runs for reference (artifacts expire — the inventory below is authoritative):**
- Original (blocked): PyAutoHeart workspace-validation `run_id=29266305445` (530p/26f)
- Re-validated: `run_id=29279095224`, profile=release, wheels `2026.7.13.1.dev65601`
  (rehearsal `run_id=29278651693`) → 539p/18f/67s/5t

## The remaining failures (21 pre-existing + 2 new flakes), by cluster

Triage each cluster: reproduce on the wheels/main, decide **real bug vs release-profile
gap vs flaky timeout**, fix at the right layer (library / workspace script / env profile),
never mask a real regression. Some are almost certainly release-profile/perf, not code.

### A. JAX-likelihood numerical parity (HARD FAIL — `assert_allclose` DESIRED mismatch)
- `autolens_workspace_test scripts/jax_likelihood_functions/multi/rectangular.py` — FAIL, `DESIRED: array(-12928.700871)`
- `.../jax_likelihood_functions/multi/rectangular_mge.py` — FAIL, `DESIRED: array(-6146.592113)`
  Multi-wavelength JAX likelihood parity is off on the wheels. Most likely a real
  numerical/parity issue (or a stale expected value). Highest-signal cluster — start here.

### B. JAX grad
- `.../jax_grad/imaging_pixelization.py` — FAIL
- `.../jax_grad/interferometer.py` — FAIL

### C. `modeling_visualization_jit` (viz-under-jit, 3)
- `autogalaxy_workspace_test scripts/ellipse/modeling_visualization_jit.py`
- `.../imaging/modeling_visualization_jit.py`
- `.../interferometer/modeling_visualization_jit.py`
  Recurring viz-under-jit cluster (see prior heart-yellow viz fixes); likely one shared root.

### D. Database (6)
- `autofit_workspace scripts/database/directory/{general,multi_analysis}.py`
- `.../database/scrape/{general,grid_search,multi_analysis,sensitivity}.py`
  Suspected AssertionErrors — triage as one cluster (shared scrape/directory machinery).

### E. Aggregator (2)
- `autolens_workspace scripts/guides/results/aggregator/{galaxies_fits,samples_via_aggregator}.py`

### F. Chaining / SLaM / group (likely mixed real + timeout)
- `autolens_workspace scripts/group/features/advanced/subhalo/detect/start_here.py`
- `.../group/features/advanced/mass_stellar_dark/chaining.py`
- `.../imaging/features/advanced/double_einstein_ring/chaining.py` — **TIMEOUT(300s)** (new; flaky)
- `.../multi/features/slam/simultaneous.py`

### G. Interferometer
- `autolens_workspace scripts/interferometer/model_fit.py` — FAIL

### H. Misc
- `autofit_workspace scripts/features/minimal_output.py` — FAIL

### I. Timeouts (300s) — release-profile/perf, not crashes (5 total; 3 identified)
- `autogalaxy_workspace scripts/imaging/features/shapelets/modeling.py` — **TIMEOUT(300s)**.
  NOTE: this is the shapelet script whose pytree crash we just fixed — it now *runs* but the
  real JAX shapelet fit exceeds the 300s script cap under the release profile. Needs a
  fast-mode/TEST_MODE flag in the release env profile (`config/build/env_vars.yaml`), not a
  code fix. (Sibling `features/advanced/shapelets/modeling.py` PASSes at 97.9s.)
- `.../imaging/features/advanced/double_einstein_ring/chaining.py` — TIMEOUT (see F)
- `autolens_workspace_test scripts/jax_likelihood_functions/multi/shared_preloads.py` — TIMEOUT
- (2 more timeouts unidentified from the summary — enumerate from the per-script log on re-run.)

## Two structural follow-ups to fold in
1. **shapelets/modeling.py >300s under release profile** — give it the fast-mode/TEST_MODE
   treatment the smoke profile uses, so a working-but-slow fit isn't a release blocker.
2. **`mode=release` RED-friction (Heart policy)** — release-validation RED-blocks on the
   ENTIRE full-set tail, while the nightly correctly gates only the curated smoke subset.
   Decide whether `mode=release` should gate on a release-relevant subset (or split
   blocking-vs-advisory tiers) so a known non-blocking tail can't indefinitely hold a
   release. This is a PyAutoHeart/Brain design question, not a script fix — may spin out
   as its own prompt.

## How to work it
Cluster-by-cluster (`start_dev` per cluster or a `register_and_iterate` queue). For each:
reproduce on the wheels or on main+PYTHONPATH, classify (real bug → fix at source/script;
profile gap → env_vars.yaml; flaky timeout → perf/flag), fix, and confirm the cluster clears
on a fresh `mode=release` re-validation. Cross-check against the nightly smoke subset so
fixes don't regress it. When the integrate stage is green (or the tail is reclassified as
advisory), Heart → GREEN and the minor-version choice returns to the human.
See [[project_release_2026_07_13_blocked_3bugs]], [[feedback_verify_triage_clusters]],
[[feedback_smoke_tests_small_subset]], [[feedback_no_silent_guards]].
