# Phase 8B: F2 reference ruling, F5 demotion, preliminary verdict on 24/39 arms

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- inference
- regularization
- jax
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Epic: inference-programme
Phase: 8
Filed: 2026-08-28
Issued: 2026-08-28

User request (verbatim): "8B verdict first and F2 reference ruling".

The W5 / Phase 8B bijector A/B (`scripts/misc/searches/bijector_ab.py`, issue #162)
is blocked on two scorer questions and one HALT. The architect's ruling, to be
recorded VERBATIM in spirit as a dated entry in
`results/notes/inference/DECISIONS.md` BEFORE any scoring is run:

1. **F2 reference** = the maximum `lane_best_log_posterior` over ALL arms (every
   bijector: none/log_reg/logit) in the (cell, log_det_method) group, restricted
   to physically valid rows: exclude rows that are void (`diagnostics.valid=false`,
   wall < 2 min, missing schema) and rows whose best point has ell_comps magnitude
   >= 1 (use `recovered_offline_verification.best_point_ell_comps_magnitude` where
   present, else compute from the best-point parameter vector /
   `diagnostics.ell_comps_pairs`; document the field used). Tolerance stays
   `REFERENCE_TOLERANCE_NATS` (10). Rationale: the old max-over-`none` reference
   was defined by the control arm's own stalling and is now contaminated by
   non-physical box-corner points (`slogdet_log_reg_seed1` reports 2.1e53).
2. **F2 "never reached"**: at a matched seed, if `none` never comes within tolerance
   in 3000 steps but `log_reg` does, that seed's reduction ratio is `+inf` (counts as
   >= 2x); if `log_reg` never reaches but `none` does, ratio 0 (counts against); both
   never -> seed unscorable. Median over scorable seeds as before.
3. **F5 demoted** from HALT to a reported diagnostic — it compares two separate GPU
   runs' step-0 min-over-lanes foms and measures fp reproducibility, not the
   objective (the mge control's identity map diverges 1.7e-2 by step 3000). Keep
   computing and reporting it with the same 1e-9 number, labelled
   "fp-reproducibility diagnostic". The sound F5 is an in-process PyAutoFit unit
   test, filed separately.
4. **F4**: the `best_fom`/`max_log_likelihood` fp-equivalence limb is informational
   only (per the 2026-08-27 entry); F4 trips only on the knn `logit`
   pinned-lane-to-boundary pathology.
5. Record that the 15 resubmitted arms (job 341978, indices 0,2,3,14,17,19,21,24,25,
   26,27,30,32,33,34) run on the post-pull stack (PyAutoFit f466dce1a, PyAutoGalaxy
   0fbe863d, PyAutoLens b23ee53e9) whereas the 24 landed arms ran on 2026.8.17.1 with
   pre-#1536 PyAutoFit; the likelihood code is unchanged between them (#1536/#713/
   #1538/#589 touch results-writing and an OPT-IN clipper only) — state this as the
   reason the A/B is not split, but flag it.
6. The verdict written now is **PRELIMINARY (24/39)**; the final verdict is re-run
   when 341978 lands. Also record that with a bijector set the joint disk clipper is
   refused at construction (`PyAutoFit multi_start_gradient/search.py:368-383`) — so
   no 8B arm used `ClipperPriorBoxJoint`; filed as a PyAutoFit follow-up.

Deliverable: scorer amendments (minimal, ruff-clean) + unit tests, the 24 harvested
JSON/PNG committed under
`results/searches/multi_start_prodigy/imaging/<cell>/hst/phase8b/`, a preliminary
verdict artifact labelled 24/39, and the human summary in
`results/notes/inference/phase_08_regularization/RESULTS.md` "8B" plus the
DECISIONS entry.
