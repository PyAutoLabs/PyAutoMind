# `@autofit_workspace_developer` retire the `searches_minimal/` Nautilus leftovers orphaned by B4a

Type: maintenance
Target: autofit_workspace_developer
Repos:
- autofit_workspace_developer
Difficulty: trivial
Autonomy: safe
Priority: low
Status: formalised
Consequence: glance
Epic: search-extensibility
Witness: `searches_minimal/` contains no file that imports `nautilus_profile`, `output/nautilus_profile_summary.txt` is gone, and the deletion is recorded with its pre-delete SHA in `condemned.md`.
Unattended: ready
Filed: 2026-10-14

Split out of `complete/2026/10/search-ext-b4a-breakdown-exporter.md` at close-out. autofit_workspace_developer#30 deleted `searches_minimal/nautilus_profile.py` and `nautilus_bottleneck_findings.md` (re-homed to autofit_profiling). `searches_minimal/nautilus_sweep.py` and `nautilus_jax_mlp.py` still import the deleted module, so they no longer run standalone (no CI runs them), and `output/nautilus_profile_summary.txt` is a stale artefact. Recommendation (Fable, 2026-10-14): delete all three by committed deletion with a `condemned.md` entry; if a sweep or MLP timing is still wanted it belongs in autofit_profiling as a cell. Human to confirm at start_dev.
