# Point-source wiki reconcile + CPU campaign completion evidence (docs-only)

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
Consequence: judge
Epic: point-source-cpu-speed
Issued: 2026-10-04

Contract: the PyAutoPulse task `organs/PyAutoPulse/tasks/pointsolver_cpu_speed_campaign_remainder.md`
(https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/pointsolver_cpu_speed_campaign_remainder.md),
"Campaign completion evidence" leftover. The stale lines on the sibling A100 and source-plane campaign
pages are in scope too: point_source_image_plane_gpu_breakdown and point_source_source_plane_chi_squared_speed.

## Original request (2026-10-04, in-session)

"do the proposed priority order stuff, all of it". This is task B of that order: a docs-only
autolens_profiling PR.

## Scope

1. `wiki/campaigns/point_source_image_plane_cpu.md`:
   - change "In flight: PyAutoLens#763" to say PyAutoLens#764 merged on 2026-10-02 and was released in
     2026.10.4.1 (workspace_test#338 merged);
   - add a completion-evidence section, written in the ledger and summarised on the page:
     - the baseline/final comparison;
     - the disposition of every candidate;
     - the GPU regression check for each shared library change.
   Verify each claim with `gh` and the git tags.
2. `wiki/campaigns/point_source_gpu_breakdown.md`: replace the #350 branch pointer with PR #353 (merged 2026-09-30).
   Phase 0+1 shipped; the forward-NaN bug is issued as PyAutoLens#767.
3. `wiki/campaigns/point_source_source_plane.md`: autolens_inference#17 is merged (2026-10-02), not open. The
   search leaf exists.
4. Replace the removed Mind draft paths with PyAutoPulse task URLs.
5. Note that the RAL leftover folders still exist and that the mirror sync is unverified. Cleanup stays human-gated.
6. Reconcile the `wiki/index.md` rows for the three campaigns.
