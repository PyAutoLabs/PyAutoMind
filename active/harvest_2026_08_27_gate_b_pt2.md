# `@autolens_profiling` Harvest 2026-08-27: Gate B pt 2, recovered 8B rows, scorer + ledger repairs

Type: feature
Target: autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-08-27

Original request (verbatim): "Look at the JAX profiling gradinet epic, download results
overnight from A100, and do a major assessment of the results so far are, maybe double
checking some conclusiojns." → audit → "yep do all that" (ranked actions 2–7).
Audit: https://claude.ai/code/artifact/d9f4b0f3-52a1-4830-a9ad-11a225b77507

Harvest is staged (not committed) in the Claude session scratchpad
`/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/22944545-bd52-466e-bb08-4236d7b478a6/scratchpad/`:
`ral_harvest/` (RAL mirror of results/ + hpc logs), `recovery/results/...` (six
`recovered_offline: true` Phase 8B JSONs + `recover_phase8b.py`), `recovery_table.json`.

## Scope

1. **Target-id honesty first** — `@autolens_profiling/scripts/misc/searches/_targets.py:306-330`
   `_positions_block` uses module defaults; make it read the resolved positions setup
   (threshold_mode/value, factor) so the three Phase-4 arms get distinct `target_id`s.
   Add a `penalty_at_best` readout to schema v2 for MultiStart rows if it is cheap
   (one likelihood call at the best point with/without the penalty); otherwise record it
   as owed.
2. **Harvest rows** into `results/searches/`: 10 Phase-4 diagnostic rows
   (`multi_start_prodigy_autoconv/imaging/mge/hst/*_pos_t0.3_f1e5.json`,
   `*_pos_tauto0.2_f1e8.json`; mark seed0 tauto as INVALID — silent resume, 68 s),
   2 refs rows (`nautilus/imaging/{knn,delaunay_matern}/hst/hpc_hpc_a100_fp64_ref.json`),
   6 recovered 8B rows (`recovery/results/.../phase8b/*.json`, keep the
   `recovered_offline` markers), 3 knn 8B rows + 4 mge 8B controls from `ral_harvest`.
   Do NOT copy the four rewritten nbatch JSONs (341894/5 short-circuit overwrote walls).
3. **Scorer repair** `scripts/misc/searches/bijector_ab.py`: `score_f1`/`score_f2`
   must return UNSCORABLE (not PASS/FAIL) on missing data; F4 → "best_fom and max
   log-likelihood equivalent within fp64 on the winning lane" (F5 already proves the
   objective is inert); record the F2 reference deviation as a DECISIONS entry needing
   human ratification. Do not emit a Phase 8B verdict yet (delaunay arms still running).
4. **Ledger** (`results/notes/inference/`): DECISIONS.md entries (append-only, dated) for
   W6 n_batch, W2 Stage 2, W4 harvest, 8B 340576 loss + 341874/5 crash+recovery, and
   **Gate B pt 2 CALLED** (human-approved 2026-08-27): "PositionsLH is not intrinsically
   hostile to gradient MAP on MGE; factor 1e8 was mis-scaled for a fixed-step searcher.
   At factor 1e5 Prodigy(n=256, prior_box, autoconv) is 5/5 positions-on at parity with
   positions-off. Gate B pt 1 extends to positions-on at factor ≤ 1e5; 1e8 rejected."
   Caveats: idealised truth positions; one cell/5 seeds (Wilson-95 lower 0.57, does not
   re-establish ≥99%); 1e5 shown safe not calibrated (nothing between 1e5 and 1e8; SLaM
   factor 3 untested); Nautilus unaffected; no penalty_at_best field.
   PROGRAMME.md state table rows for 8B / Phase 4 / W4 / Gates; §9b; `:970` Sibson →
   target-config error. phase_04 RESULTS.md: diagnostic section (table: off 5/5; t0.3
   f1e5 5/5; t0.3 f1e8 2/5 under Phase 3's coded rule; tauto0.2 f1e8 0/4 + 1 invalid;
   constrained-lane-step rate 15–18 → 38–43 → 44–53 → 41–56 %; median step scale
   0.14–0.16 vs 0.21–0.22; transit-damage mechanism; out-of-disk best points 17 % → 29 %).
   phase_08 RESULTS.md 8B: submit ids, crash root cause, recovery, per-arm table, signal,
   scorer note. REFS_V1_HARVEST.md: 9/13 certified; 341908 slam_source_pix_nn thrashed
   (0 calls in 6 h); flag knn ref 480 nats below same-target Prodigy log_reg arm.
5. **Wording corrections** from the re-check: W6 "1.78×" is per-eval (wall 1.46×,
   ESS/min 1.59×; nb1000 logZ −0.10 nat ≈ 9σ of seed sd 0.011; ESS/eval −10 %);
   W2 Nautilus: maxL lower with positions in 5/5 seeds (mean −0.126, t=−3.45, p≈0.026),
   wall −3…+7 %, not "±3 %/no-op"; Prodigy positions 2/5 under the coded rule (declare
   the stricter band if kept); phase_03 RESULTS.md:21 "0.251" → 0.028 nats below the cut,
   :22 swing → 0.0609 (50 %); phase_08 :289 duplicate of the coefficient_min correction;
   DECISIONS:449 CPU max|Δ| 1.62 is a change from 2.27, not "unchanged";
   methods/nautilus.md:76-81 831 s/12.1 ms → 707 s/10.56 ms; methods/multi_start_prodigy.md
   and methods/nss.md: add a dated banner that they pre-date Gate B pt 1 / Gate A.
   Add "Resuming .* previous samples found" to the PROGRAMME trap-check rule.
   Add the non-physical-ellipticity finding (1,252/6,240 lane best points |e|≥1, 0/246
   hits; re-based p̂ = 61/1064 = 0.057) as a second lower-bound reason in phase_03.
6. `scripts/misc/wall/rates.py`: record measured delaunay_adapt_split / knn Prodigy walls
   from this harvest if the format supports it.
7. File a Mind draft prompt (feature/autofit or autogalaxy) for the joint ell_comps disk
   constraint / reparameterisation follow-up; do not implement it here.
8. `ruff check .`, `ruff format --check .`, `scripts/misc/wall/check_submits.py --check`,
   `scripts/misc/tooling/build_readme.py` (README regen is a lint gate).

Out of scope: PR#181 (MIG preflight cap) is a separate open PR; PyAutoFit/PyAutoLens
fix is `bug/autofit/result_instance_fallback_samples_persist.md`.
