## source-plane-runtime-refresh

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/349
- completed: 2026-09-28
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/351 (merge `c483417`)
- epic: point-source-cpu-speed
- parent-record: complete/2026/09/point-source-source-plane-p2e.md
- campaign: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md

Runtime refresh of the source-plane point-source chi-squared cell at release 2026.9.27.2 plus the parked A100 vmap throughput row (single-source only). Merged in autolens_profiling#351. Workspace-only, no library edits.

**Shipped**
- Runtime rows on `euclid-ral-gpu-2`, both qualified on the dashboard (device provenance, reference host, under the load cap): `hpc_ral_cpu_fp64` single JIT 0.258 ms (matches phase 2b), vmap 0.097 ms (b3); `hpc_a100_fp64` vmap 5.6 µs/call at b64 (≈114× the single call).
- A100 vmap throughput: batch wall flat b64→b1024 (0.32/0.32/0.30 ms, job 366914), per call 4.9 µs → 0.29 µs (3.4 M evals/s) — launch-bound at b1024.
- Wiki release correction: PyAutoFit#1649 and PyAutoLens#752 are released in 2026.9.27.2 (campaign page header, "What shipped" table, index row).
- `source_plane_solved.py` records `device_info_dict()` and writes per-config JSON under `--config-name`; `aggregate.py` gains `hpc_ral_cpu_fp64`; new CPU + A100 submit scripts; source-plane A100 leg is the ninth release-sweep leg; optional `PYAUTO_LIB_OVERRIDE` for scratch library clones on RAL.

**Traps / notes**
- The A100 `single_jit` (0.642 ms) is warm-up-contaminated (one warm call then mean of 10); steady median on the same node is 0.267 ms. Method left unchanged for dashboard comparability; filed as `draft/bug/autolens_profiling/runtime_cell_single_jit_gpu_warmup.md`.
- Source checkouts report `autolens_version` 2026.8.17.1 even at the 2026.9.27.2 tag (build-time stamp), so source-checkout rows do not separate by release on the dashboard. Pre-existing.
- The shared RAL stack was not moved (live jobs, dirty PyAutoFit); scratch clones at the tag commits were used and removed afterwards, as were `/mnt/ral/jnightin/sp_diag` and `sp_refresh_libs`.
- blackjax forward mode stays parked: needs a point-source search leaf in `autolens_inference/scripts/point_source/searches/`.

## Original prompt

# Point-source source-plane chi-squared campaign — runtime refresh on 2026.9.27.2 + A100 vmap row

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Epic: point-source-cpu-speed
Lane: any
Filed: 2026-09-28
Issued: 2026-09-28
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/349
Parent-record: complete/2026/09/point-source-source-plane-p2e.md
Campaign: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md

Slice of the campaign prompt above (remaining candidate 2, the A100 `vmap` throughput row), plus the
post-release refresh: PyAutoFit#1649 / PyAutoLens#752 are released in 2026.9.27.2, so the wiki's
"pending release" wording is corrected and `scripts/point_source_source/likelihood_runtime/source_plane_solved.py`
is re-run on the pinned RAL reference node (`euclid-ral-gpu-2`) at the release — CPU (`hpc_ral_cpu_fp64`)
and A100 (`hpc_a100_fp64`) rows with the #342 provenance block — and the source-plane A100 leg joins
`hpc/batch_gpu/submit_release_sweep.sh`. blackjax forward mode stays parked. Full plan on
autolens_profiling#349 (approved in-session 2026-09-28).
