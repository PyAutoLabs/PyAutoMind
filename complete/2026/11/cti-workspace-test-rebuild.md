## cti-workspace-test-rebuild
- issue: https://github.com/PyAutoLabs/autocti_workspace_test/issues/26
- completed: 2026-11-06
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace_test/pull/27

Merged 2026-11-06 (4160e321) by the human's `/prm` (judge tier). Heart STALE at ship time ("release validation incomplete: no rehearsal for current source"), human-acknowledged. Issue #26 closed. cti-upkeep phase 3b.

- Retired via Gut (R3, plus a human plan-time ruling for `imaging_ci/`): `legacy/` (139 files) + top-level `imaging_ci/` (43). PyAutoGut ref `refs/heads/archive/condemned/autocti-workspace-test-legacy` @ 72970e78 (= the pre-purge main); `condemned.md` entry `autocti-workspace-test-legacy`, sweep-after 2026-12-06.
- New checks (all assert; self-consistent with one arctic, so no new arcticpy-dependent literals; only the 0b pins move at the 2b bump):
  `{dataset_1d,imaging_ci}/recover_input.py` (chi² = 0 at the truth, offsets worse, a density likelihood scan peaks at the truth; 2D covers parallel/serial/both),
  `{dataset_1d,imaging_ci}/remove_cti.py` (round trip within 0.1% of the trail per direction; more iterations reduce the residual),
  `imaging_ci/cosmic_ray_flagging.py` (all > 40σ cosmic-ray pixels flagged, under 1% false flags, the buffered mask covers every pixel contaminated above the read noise, measured by clocking with and without the cosmic rays),
  `model_fit.py` x2 (the aggregator CTI equals the search result; imaging_ci had no round trip before).
- Harness: run_all_scripts.sh, config/build/no_run.yaml (empty), config/build/profile_release.yaml (+ a real-plotting override for plot/subplots.py, which asserts its PNGs exist); smoke 5 → 10.
- Plan deviation: a short real search can't reliably recover the density under profile_release (TEST_MODE=1 caps the sampler), so recover_input uses a deterministic likelihood scan instead.

Evidence: fresh clone, profile_smoke 10/10 (142 s); profile_release 10/10 after the subplots override; run_all_scripts.sh with no failures; CI smoke 3.12/3.13 green. Every new assertion was shown to fail when its premise is broken (wrong sim model, wrong correction model, threshold ×100, missing serial buffer, missing parallel+diagonal buffers). Two of the first-draft cosmic checks were circular (a "bright" cut tied to the threshold; trail coverage tied to the mask's own settings) and were rewritten to be independent.

Findings: (1) parallel+serial remove_cti plateaus at ~0.2 e- at pixel (0, 29), the first row's serial-overscan corner; each direction alone converges to ~1e-6 (the bound margin is 0.34 vs 0.49 e-, so watch it at the 2.7 bump). (2) The default 10-row cosmic-ray parallel buffer under-masks at density 10 / τ 5 (trails above the read noise for 11–17 rows, 61 px), but is fine at Euclid-like densities (the check uses the workspace example's traps).

## Original prompt

# autocti_workspace_test rebuild: integration checks to the autolens_workspace_test shape, legacy/ retired via Gut

Type: maintenance
Target: autocti_workspace_test
Repos:
- autocti_workspace_test
- PyAutoMind
- PyAutoGut
Themes:
- cti
- smoke
- hygiene
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: autocti_workspace_test has no `legacy/` or top-level `imaging_ci/` tree on main; both are recoverable from the PyAutoGut ref `archive/condemned/autocti-workspace-test-legacy` and listed in `PyAutoMind/condemned.md` with a `sweep-after` date; `scripts/` carries recover-the-input, remove_cti round-trip, aggregator round-trip and cosmic-ray-flagging checks for both Dataset1D and ImagingCI that ASSERT (not print); `run_all_scripts.sh`, `config/build/no_run.yaml` and `config/build/profile_release.yaml` exist; `smoke_tests.txt` runs every new script and CI smoke is green on 3.12 and 3.13.
Review-minutes: 15
Unattended: needs-human
Epic: cti-upkeep
Phase: 3
Filed: 2026-11-06
Issued: 2026-11-06

Human request (2026-11-06): "then start_dev the workspace_test rebuild (3b)".

cti-upkeep phase 3b, from the epic ledger: "autocti_workspace_test rebuilt to the
autolens_workspace_test shape (`run_all_scripts.sh`, `no_run.yaml`, recover-the-input-traps
scripts for 1D and 2D fits, aggregator round trip, `remove_cti`, cosmic-ray flagging);
`legacy/` triaged per R3". R3 (human, 2026-11-04): retire `legacy/` via Gut. The 139 Euclid VIS
heritage files leave the tree as a recoverable Gut ref through the transit window, never a
plain delete.

State found 2026-11-06 (autocti_workspace_test main 72970e7):

- `scripts/` is already modern and small: `dataset_1d/model_fit.py` and `imaging_ci/model_fit.py`
  (simulate, FactorGraphModel fit, aggregator round trip, but they print rather than assert),
  `dataset_1d|imaging_ci/likelihood/pins.py` (the 0b log-likelihood pins, rtol 1e-8; these move
  with the 2b arcticpy bump and are re-pinned there, not here), `plot/subplots.py`. smoke_tests.txt runs these 5.
- `legacy/` holds 139 files, 3.5 MB (tvac, temporal, euclid, validation, overview_output, config_2023 + README),
  written against the pre-2025 API and not runnable.
- A second untriaged tree, top-level `imaging_ci/` (43 files: cosmics, temporal, profiling,
  simulators), sits outside `scripts/` and is pre-resurrection material too. R3 named only
  `legacy/`. Human ruling 2026-11-06 at plan time: retire `imaging_ci/` via Gut in the same move. Its
  `cosmics/cosmic_ray_flagging.py` + simulators are the reference for the new flagging check.
- `config/build/` has only `profile_smoke.yaml`; no `no_run.yaml`, no `profile_release.yaml`, no
  `run_all_scripts.sh`. Release smoke (Hands release.yml) covers only the main workspaces, so
  `profile_release.yaml` here is for parity with autolens_workspace_test, not a release requirement.
- autolens_workspace_test pattern: deterministic numeric checks that `assert` (chi-squared ≈ 0 when
  fitting the truth, likelihood differences under a tolerance), `no_run.yaml` with SLOW / NEEDS_FIX
  conventions, `run_all_scripts.sh` mega-run.

Design constraint (arcticpy 2b): checks must hold whatever the arctic version. Simulate with arctic
and fit/correct with the SAME arctic, then assert self-consistency (truth fits to chi² ≈ 0 on
noise-free data; truth beats an offset model; remove_cti(add_cti(x)) ≈ x within a tolerance set
by the iteration count; flagged mask ⊇ injected cosmic rays). No absolute literals beyond the
existing 0b pins, so the 2b bump re-pins nothing new.

Gut mechanics (precedent: condemned.md release-datasets entries): commit the deletion on the
feature branch; push the pre-deletion main commit to PyAutoGut as
`refs/heads/archive/condemned/autocti-workspace-test-legacy`; add a `condemned.md` entry
(schema in that file) with the source repo + pre-purge SHA and a `sweep-after` date (transit
window per the ledger's convention).
