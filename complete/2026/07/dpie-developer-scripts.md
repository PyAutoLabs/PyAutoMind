## dpie-developer-scripts
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/108
- completed: 2026-07-17
- prs: autolens_workspace_developer#109 — MERGED 2026-07-17 (no CI on repo; CLEAN)
- summary: Trivial API-update follow-up to dpie-lenstool-default (#506). Three developer scripts (visualization_profiling/imaging/cluster.py, jax_profiling/simulators/cluster.py, scaling_relation_agg/error_make.py) called the removed dPIEMassSph(ra, rs, b0) signature; swapped to the renamed internal class dPIEMassB0Sph with identical values (faithful — profiling/aggregator numerics unchanged; aggregator's pre-existing b0 ∝ L^0.25 relation left untouched). Fixed a stale dPIEPotentialSph docstring ref. Isolated in its own worktree so the 23 pre-existing dirty files on the autolens_workspace_developer main checkout (searches_minimal/source_science experiments from a prior session) were never touched.
- notes: Closes the "3 developer scripts" follow-up flagged on #506. Required pulling the canonical PyAutoGalaxy checkout to merged main so dPIEMassB0Sph was importable.
