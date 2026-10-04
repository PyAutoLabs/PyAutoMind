# Point-source CPU campaign: the still-owed leftovers after the wiki reconcile

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
- PyAutoFit
Themes:
- point-source
- profiling
Difficulty: small
Autonomy: supervised
Priority: low
Epic: point-source-cpu-speed
Status: draft
Filed: 2026-10-04

Remainder of `complete/2026/10/point-source-wiki-reconcile.md` (autolens_profiling#373, merged
2026-10-04). That PR reconciled the wiki and added the campaign completion evidence. It did not do the
leftovers. The full list, with paths, is in the PyAutoPulse contract
`tasks/pointsolver_cpu_speed_campaign_remainder.md`
(https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/pointsolver_cpu_speed_campaign_remainder.md)
under "Carried leftovers" and the phase 4b/4c leftovers.

## Still owed

1. **RAL leftover cleanup.** The `autolens_profiling_wt/` p2/p3/p4, step0-gather and mcs-headroom
   clones and worktrees are still present. The mirror sync is unverified. This is human-gated: verify the
   sync, then delete.
2. **register_model grad-zero prompt.** `jax.grad` of an AnalysisPoint likelihood is silently all-zero
   without `autofit.jax.register_model(model)`. File a PyAutoFit bug prompt to raise or warn on it.
3. **Test move:** `test_static_lattice_jax.py` placement.
4. **CI smoke cells** for the breakdown scripts (`vertex_dedup_ab.py`, `static_lattice_ab.py`, …).
5. **`nopad` deletion** in PyAutoArray `_STEP0_CONTAINMENT`. `structured` is the default. This is a
   library cleanup.
6. **Quiet-node re-runs**, for example the 8490H row (job 357321, load ~200). Do these only if absolute ms
   against phase 4a are wanted. The final-code single-node row is the still-unmeasured control.

Each item is small. Split them into separate tasks when issuing; never bulk-issue.
