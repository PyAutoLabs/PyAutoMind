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
