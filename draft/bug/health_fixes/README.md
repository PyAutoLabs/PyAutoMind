# Release-fidelity health fixes

This folder tracks the script regressions exposed by the first real release-profile
validation in [PyAutoHeart issue #27](https://github.com/PyAutoLabs/PyAutoHeart/issues/27),
GitHub Actions run `28784914443`.

The run installed and verified all five TestPyPI wheels successfully, then reported
37 script failures and 5 timeouts across 42 scripts. Local reproduction used the
shared PyAuto development environment, current `main` library checkouts, each
workspace's `config/build/env_vars_release.yaml`, and the same 300-second cap.

Each failing script is assigned to exactly one prompt:

| Prompt | Scripts | Primary concern |
|---|---:|---|
| [samples_parameter_paths.md](samples_parameter_paths.md) — ⚠️ parked, does not reproduce on current `main` ([PyAutoFit#1327](https://github.com/PyAutoLabs/PyAutoFit/issues/1327), blocked on clean-CI re-validation) | 9 | PyAutoFit result/sample path resolution |
| ~~autofit_sampler_database.md~~ — ✅ **CLOSED 2026-08-21**, record `complete/2026/08/autofit-sampler-database.md` ([PyAutoFit#1508](https://github.com/PyAutoLabs/PyAutoFit/issues/1508); **0/9 reproduce** on current `main` — no defect, no code changed in any repo; re-validation is automatic, all nine run in every `mode=release` pass) | 9 | Emcee NaNs and database output discovery |
| ~~aggregator_output_contracts.md~~ — ✅ **SHIPPED 2026-07-07**, record `complete/2026/07/aggregator-output-contracts.md` (PyAutoFit#1324; autogalaxy_workspace#122, autolens_workspace#229, autolens_workspace_test#146 all merged) | 7 | Result/aggregator prerequisites and generated paths |
| ~~jax_runtime_and_parity.md~~ — ✅ **CLOSED 2026-09-17**, record `complete/2026/09/jax-runtime-and-parity.md` ([autolens_workspace_test#317](https://github.com/PyAutoLabs/autolens_workspace_test/issues/317); **6/6 pass 2026-08-21 and again 2026-09-15** on jax 0.10.2 — defect refuted, no library code changed; the four parkings had already been lifted by PyAutoFit#1528 on 2026-08-27, so re-validation is automatic in every `mode=release` pass. One residue fixed: `imaging/jax_likelihood/delaunay_mge.py` re-enabled on both smoke gates, autolens_workspace_test#320 + autogalaxy_workspace_test#122 merged) | 6 | JAX/TFP compatibility and likelihood parity |
| ~~jit_visualization_outputs.md~~ — ✅ **CLOSED 2026-09-17**, record `complete/2026/09/jit-visualization-outputs.md` ([autolens_workspace_test#318](https://github.com/PyAutoLabs/autolens_workspace_test/issues/318); **4/4 pass 2026-08-21 and again 2026-09-15** — no defect, no library code changed; the one residual, the `point_source/visualization/modeling_visualization_jit` SLOW parking, refuted by CI retime run 35245806121 (10/10 under the 300 s cap, slowest 98.6 s) and deleted in [autolens_workspace_test#321](https://github.com/PyAutoLabs/autolens_workspace_test/pull/321); all four scripts now re-execute in every `mode=release` pass, so re-validation is automatic) | 4 | Quick-update visualizations not producing images |
| ~~numerical_inversion_failures.md~~ — ✅ **CLOSED 2026-08-22**, record `complete/2026/08/numerical-inversion-failures.md` ([PyAutoArray#467](https://github.com/PyAutoLabs/PyAutoArray/issues/467); **0/2 reproduce** on current `main` — no defect, no code changed in any repo; neither script is parked, so re-validation is automatic in every `mode=release` pass). Incidental PyAutoArray sqrt-NaN filed as `draft/bug/autoarray/reconstruction_noise_map_covariance_sqrt.md` | 2 | Non-positive-definite inversion matrices |
| [release_timeout_policy.md](release_timeout_policy.md) — ⚠️ **4/4 measured pass far under cap 2026-08-21**; start_here not measured | 5 | 300-second release-surface decisions |

Total: **42 scripts**. Scripts that pass on current `main` remain listed because they
still require a clean-worktree, directory-order reproduction before being declared
fixed. Do not rebaseline assertions or edit tutorials to conceal a library regression.

## 2026-08-09 sweep — three things to know before working this folder

1. **One of the seven has shipped** (aggregator_output_contracts, struck through above);
   its file is gone from this folder and lives in `complete/2026/07/`. The table said
   nothing about that for a month.

2. **Script paths in `jit_visualization_outputs.md` and `jax_runtime_and_parity.md` are
   all stale** — every one 404s, and every one still exists under a renamed layout
   (`scripts/jax_likelihood_functions/<dataset>/` → `scripts/<dataset>/jax_likelihood/`;
   `<dataset>/modeling_visualization_jit.py` → `<dataset>/visualization/…`; `multi/` →
   `multi_dataset/`). Corrected tables are in each prompt. A 404 in this cluster means
   drift, not deletion.

3. **Many of the named scripts are now parked** in their workspace's
   `config/build/no_run.yaml`, mostly `SLOW` for cap timeouts, with dates *after* these
   prompts were filed. A parked script cannot fail release validation, so a green
   release run is not evidence of a fix — the 2026-08-07 Stage 3 integrate reports
   `657p/0f/101s/0t`, and those **101 skips** are where this cluster's scripts went. The
   parkings also cite a **different failure** (timeout) from the defects these prompts
   describe, so unparking is a precondition for reproducing any of them.

None of the five remaining prompts was graded shipped. What this sweep could establish
offline is recorded in each file; the reproduction legs all need real runs.

## 2026-08-21 sweep — the whole cluster has now been re-run

A reproduction gate (clean `output/`, each workspace's `profile_release.yaml`, env via
`autohands.env_config.build_env_for_script`, 1800s cap) was run over **all 17 scripts** in the four
remaining prompts, plus the nine in `autofit_sampler_database`. Result: **25 of 26 measured scripts
pass on current `main`**; the 26th was operator-stopped, not failed.

That is now **three independent findings** that this cluster aged out — `samples_parameter_paths`
(#1327, parked), `autofit_sampler_database` (PyAutoFit#1508, **closed**), and these four. The
consistent explanation across all of them is the one #1327 reached: stale cached `output/` in the
2026-07 release run, against libraries that have since absorbed dozens of fixes.

**What this sweep does NOT establish**, and nobody should read into it:

1. **The parkings are not cleared.** Four `jax_likelihood/delaunay_mge` scripts are parked for an
   *intermittent* cap flake; one green run each is consistent with that note, not contrary to it.
   Only `point_source/visualization` (deterministic "exceeds 300s", ran 168s) is a genuine unpark
   candidate.
2. **These were source-tree runs**, not the TestPyPI wheels the release run installed. A
   wheel-only defect would not show here.

## 2026-08-22 — `numerical_inversion_failures` closed (the "four" above are now three)

Struck through in the table. The 2026-08-21 sweep left four prompts in `draft/`; one of them has
now closed, on the same ground that closed `autofit_sampler_database` rather than on its green run
alone:

**Neither of its two scripts is parked.** Verified against `main`:
`autogalaxy_workspace/config/build/no_run.yaml` has no
`interferometer/features/pixelization/galaxy_reconstruction` entry, and
`autolens_workspace_test/config/build/no_run.yaml` has no `interferometer/model_fit` entry — it
appears only as a *consumer*, where its simulator is marked `BOOTSTRAP-TARGET` for producing
`model_fit`'s dataset. Both scripts therefore re-execute in **every** `mode=release` pass, so
re-validation is automatic and there is no human reminder to lose.

That is the distinction that decides this whole folder: caveat 1 of the 2026-08-21 sweep blocks the
*parked* prompts from closing, and it simply does not apply here. The one that remains
(`release_timeout_policy`) still carries SLOW/NEEDS_FIX parkings describing *intermittent*
failures a single green run cannot clear. `jit_visualization_outputs` left this group on
2026-09-17 too: its single parking claimed a *deterministic* >300 s timeout, which CI retime run
35245806121 refuted 10/10 (slowest 98.6 s), so the entry was deleted and the prompt closed
(record `complete/2026/09/jit-visualization-outputs.md`). `jax_runtime_and_parity` left
this group on 2026-09-17: PyAutoFit#1528 had lifted its four parkings on 2026-08-27, which put it
on the same automatic-re-validation ground as the closed siblings (record
`complete/2026/09/jax-runtime-and-parity.md`).

It also makes **four** independent refutations of this cluster, not three — the fourth predates the
release run: `complete/2026/07/pix-inversion-not-positive-definite.md` (2026-07-21) tested the same
non-positive-definite hypothesis across six markers, found all six stale, and changed **no code**.
The `LinAlgError` had been cured on 2026-04-10 by PyAutoArray's `GaussianKernel` PD-guarantee
`f1817af0`, confirmed by a 40-draw inversion A/B across the full prior range (0 raises, 0 non-finite).

One real defect came out of the gate and is filed separately:
`draft/bug/autoarray/reconstruction_noise_map_covariance_sqrt.md`. **It looks exactly like evidence
for the non-positive-definite hypothesis and is not** — `abstract.py:859` applies `np.sqrt`
elementwise to a whole covariance matrix, so negative off-diagonals are NaN unconditionally, for any
matrix, however well-conditioned. It has been mistaken for a conditioning symptom once already.
