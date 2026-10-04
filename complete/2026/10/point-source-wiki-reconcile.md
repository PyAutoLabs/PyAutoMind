## point-source-wiki-reconcile
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/370
- completed: 2026-10-04
- epic: point-source-cpu-speed
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/373
- autolens_profiling#373 merged 2026-10-04T20:49Z (head 0cefdea2, merge 1e2d8832) via human /prm (Heart RED development override). It is a docs-only reconciliation of the image-plane CPU, A100 and source-plane point-source campaign pages and their `wiki/index.md` rows. Every claim was re-checked on 2026-10-04 with `gh` + `git tag --contains | sort -V`:
  - PyAutoLens#764 is merged and released in 2026.10.4.1;
  - #580/#584/#753 are in 2026.9.27.2;
  - #353 was merged 2026-09-30;
  - autolens_inference#17 and #361 were merged 2026-10-02.
- Adds "Campaign completion evidence" to `results/notes/point_source_cpu_campaign.md`, built from committed rows only. Baseline → final is 24.69 → 2.095 ms, cross-node and indicative; the final-code single-node row is still an unmeasured control. The section also gives the disposition of every candidate and an A100 check for every shared library change. The epic close is left to the human.
- Validation: all autolens_profiling lints passed, and pytest gave 1018 passed.
- **Scope merged ≠ scope filed.** Still owed, re-filed as `draft/maintenance/autolens/point_source_cpu_campaign_owed_leftovers.md` (contract: PyAutoPulse `tasks/pointsolver_cpu_speed_campaign_remainder.md`):
  - RAL leftover cleanup (mirror sync unverified);
  - the register_model grad-zero prompt;
  - the `test_static_lattice_jax.py` move;
  - CI smoke cells;
  - the `nopad` deletion;
  - quiet-node re-runs.

## Original prompt

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
