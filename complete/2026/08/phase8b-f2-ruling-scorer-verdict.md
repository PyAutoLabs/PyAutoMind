## phase8b-f2-ruling-scorer-verdict (Phase 8B verdict FALSIFIED 3/4 — but PRELIMINARY 24/39, and half the rows sit outside the unit disk)
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/185
- completed: 2026-08-28
- library-pr: autolens_profiling#186 (merged 9be605bb449ed91b3f871327798644eacd3ad227 -> main)
- summary: the architect's F2/F5 ruling recorded in DECISIONS.md BEFORE any scoring ran, the scorer amended to match, and a PRELIMINARY (24/39) Phase 8B bijector-A/B verdict emitted — FALSIFIED on 3 of 4 criteria, every fired criterion recorded as thin.
- epic: inference-programme, Phase 8 (regularization). Closes the two scorer questions and the one HALT that the 2026-08-27 Phase 8B record left owed.

### The ruling (results/notes/inference/DECISIONS.md, dated 2026-08-28, written before scoring)
- F2 reference = max `lane_best_log_posterior` over ALL bijector arms in a (cell, log_det_method) group, restricted to physically valid rows: not void (`diagnostics.valid=false`, wall < 2 min, no `schema_version`) AND best-point `ell_comps` magnitude < 1. Tolerance unchanged at 10 nats. The old max-over-`none` reference was defined by the control arm's own stalling and is contaminated by box-corner points — `slogdet·log_reg·seed1` reports **2.1e53** at |e| = 1.41421.
- F2 "never reached": `none` never / `log_reg` does -> `+inf` (counts as >= 2x); the reverse -> `0`; neither -> that seed is unscorable. Median over scorable seeds as before.
- F5 demoted from HALT to a reported fp-reproducibility diagnostic (`verdict.diagnostics.f5`, `halts: false`), same 1e-9 number. It compares two separate GPU runs, not the objective — the MGE control's `log_reg` map is provably EMPTY and its arms still diverge 1.7e-2 by step 3000. The sound F5 is an in-process PyAutoFit unit test, shipped the same day in PyAutoFit#1540.
- F4's `best_fom`/`max_log_likelihood` fp limb is informational only; F4 trips only on the `knn` `logit` pinned-lane-to-boundary pathology.
- The 24 landed arms ran on 2026.8.17.1 / pre-#1536 PyAutoFit; job 341978's 15 (indices 0,2,3,14,17,19,21,24,25,26,27,30,32,33,34) run on PyAutoFit f466dce1a / PyAutoGalaxy 0fbe863d / PyAutoLens b23ee53e9. The likelihood code is unchanged across the split (#1536/#713/#1538/#589 touch results-writing and an opt-in clipper no 8B arm uses), so the halves pool — recorded as **flagged**, because that rests on reading four diffs, not on a measurement.
- No 8B arm used `ClipperPriorBoxJoint`: with a bijector set it was refused at construction (`PyAutoFit multi_start_gradient/search.py:368-383`), so every arm ran the per-component `prior_box` clipper — the direct mechanism behind the non-physical best points. Filed and fixed the same day as PyAutoFit#1539 / #1540.

### Verdict: FALSIFIED — 3 of 4 criteria fired. PRELIMINARY (24/39).
- F1 NaN wall (delaunay): FALSIFIED under cholesky (slogdet UNSCORABLE) — median first-value-NaN step **0.0 under both** arms; value-NaN lane-steps *rise* 18,143 -> 139,205.
- F2 steps-to-reference (knn): NOT falsified — ref 30,559.28; 1 matched seed; `none` never within 10 nats (tops out 1,645 nats short), `log_reg` inside by step 2,882 -> ratio `+inf`.
- F3 time at lambda > 1e4: FALSIFIED on delaunay cholesky — `none` 0.0000 vs `log_reg` 0.00076. slogdet (0.0469 -> 0.0368) and knn (0.0625 -> 0.0520) both go the *other* way.
- F4 MGE control + logit: FALSIFIED on the logit limb — `knn·logit·seed1` ends with a lane holding 7 params pinned to the box bound. Informational: MGE s0 agrees (rel 0.0 / 9.8e-15), s1 disagrees at 1.73e-2.
- F5 diagnostic: 1 pair > 1e-9, does not halt — `delaunay·slogdet·s0` step-0 fom 357,347.020 vs 357,343.242, rel 1.06e-5.
- Resolved references / rows kept: delaunay·cholesky 30,609.94 (2/7) · delaunay·slogdet 30,286.10 (2/7) · knn 30,559.28 (4/6) · mge 31,787.84 (4/4).
- **The headline finding is the exclusion rate, not the verdict**: 12 of the 24 rows — exactly half — are excluded, every one because the best point is outside the unit disk (1.032–1.41421). **Zero are void.** On `delaunay_adapt_split` the rate is 10 of 14 (71%), indifferent to bijector and log-det method alike. That is what PyAutoFit#1540 exists to fix.
- Every fired criterion is recorded as thin, and so is the one that did not fire — RESULTS.md "Three reasons to hold this loosely": F1's limb sums raw counts over 2 vs 5 arms (it survives normalisation at 3x, but the scorer does not normalise); F3 fires only because `none` is *exactly* 0.0000 against a `>=` test; F4's `n_pinned_final` proxy counts all parameters on a single seed; F2 rests on one matched seed whose reference is set by the `log_reg` arm at that same seed.

### What shipped
- `scripts/misc/searches/bijector_ab.py` (+371/-76): `_resolve_reference` returns `(reference, detail)` rather than a bare float; `score_f5` returns a diagnostic block instead of `falsified`/`halts`; `score_rows` carries F5 under `diagnostics.f5` rather than `f5_physical_point_equality`. The arm table, readouts, and pre-registered "any two -> falsified" threshold are untouched.
- `--stage verdict` accepted as a documented synonym for `--stage score` (the campaign notes have always named the step that way).
- The verdict artifact carries `preliminary` / `n_rows_expected`, the full per-group reference resolution, and every exclusion reason. `+inf` ratios are serialized JSON-safely (`json.dumps` would emit a bare `Infinity`); the value stays exact in the scored dict. `hardware_note` added: `<hardware>` in the filename is the SCORING host, not the machine that ran the arms (all A100).
- Data: 24 result JSON + 12 PNG under `results/searches/multi_start_prodigy/imaging/{delaunay_adapt_split,knn,mge}/hst/phase8b/` (11 JSON + 5 PNG new; the 13 already tracked are byte-identical). The 6.5 MB `rows_*.npz` dump is gitignored — nothing reads it, it re-derives from the committed JSONs on demand, and every other tracked `.npz` in this tree is <= 160 KB.
- `results/notes/inference/DECISIONS.md` (new, +159) and the RESULTS.md "8B" section (+114).
- validation: `ruff check .` / `ruff format --check` clean · `build_readme.py --check` clean (searches dashboard regenerated in the same commit for the 11 new artifacts) · `check_submits.py --check` 50 submits 0 failing · `pytest scripts/misc/test/test_searches_bijector.py` 38 passed · `pytest scripts/misc/test/` 235 passed.
- heart-ack: shipped + merged under the human-authorised RED override, sole red reason verbatim "release validation FAILED (stage integrate)". The two YELLOW reasons (workspace validation, manifest drift) are unrelated to this repo.

### One out-of-scope repair, and the trap behind it
`main`'s `lint` job had been red since PR#181 merged, on `test_hazards_prior_exit.py::test__records_the_clipper_as_what_blocks_it` — not a regression here (it failed identically on this branch's first CI run and on `main` before it). **Root cause**: PyAutoFit's `main` now also defines `class ClipperPriorBoxJoint(ClipperPriorBox)` in the same module, so the hazard's bare prefix pattern `"class ClipperPriorBox"` matched **two** lines; `anchor_from_pattern` demands exactly one and raises, `maybe_anchor_from_pattern` swallowed it to `None`, and the hazard then reported an empty `blocked_by`. The hazard's own measurement was never affected — only the mitigation anchor was lost, **silently**, which is precisely what that anchor exists to prevent. Fixed in `6443700` by anchoring on `"class ClipperPriorBox("`. The lesson generalises: a bare `class Foo` prefix pattern is falsified by the birth of any `class FooBar` in the same module.

### Owed after this (not this task's scope, no prompt filed)
- The FINAL verdict when job 341978's 15 arms land — this one is 24/39 and labelled `preliminary` in the artifact.
- An F1 limb that normalises per arm rather than summing raw counts.
- Now discharged by PyAutoFit#1540, shipped the same day: the in-process F5 unit test, and the bijector x `ClipperPriorBoxJoint` composition.

## Original prompt

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
