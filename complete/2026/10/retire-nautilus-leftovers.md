## retire-nautilus-leftovers
- issue: https://github.com/PyAutoLabs/autofit_workspace_developer/issues/31
- completed: 2026-10-14
- epic: search-extensibility (B4a follow-up)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_developer/pull/32

**Shipped:** autofit_workspace_developer#32 (merged 2026-10-14 as c08e90006; glance tier, human-approved deletion the same day; the repo has no CI). Committed deletion of `searches_minimal/nautilus_sweep.py`, `searches_minimal/nautilus_jax_mlp.py` (both imported `nautilus_profile`, deleted in #30 and re-homed to autofit_profiling) and the stale `searches_minimal/output/nautilus_profile_summary.txt`. Their recorded summaries `nautilus_sweep_summary.txt` and `nautilus_jax_mlp_summary.txt` are kept as measurements. Witness: no file under `searches_minimal/` imports `nautilus_profile`. Pre-delete SHA `009709bc6f87a2e56ef0c9e9839a1c686ab77790`; `condemned.md` entry `autofit_workspace_developer/searches-minimal-nautilus-leftovers`.

## Original prompt

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
Issued: 2026-10-14

Split out of `complete/2026/10/search-ext-b4a-breakdown-exporter.md` at close-out. autofit_workspace_developer#30 deleted `searches_minimal/nautilus_profile.py` and `nautilus_bottleneck_findings.md` (re-homed to autofit_profiling). `searches_minimal/nautilus_sweep.py` and `nautilus_jax_mlp.py` still import the deleted module, so they no longer run standalone (no CI runs them), and `output/nautilus_profile_summary.txt` is a stale artefact. Recommendation (Fable, 2026-10-14): delete all three by committed deletion with a `condemned.md` entry; if a sweep or MLP timing is still wanted it belongs in autofit_profiling as a cell. Human to confirm at start_dev.
