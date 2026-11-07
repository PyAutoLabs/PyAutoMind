# Looks shipped — dismissed

<!-- The close-out guard (PyAutoBrain `intake looks-shipped`, run daily by
     .github/workflows/looks_shipped.yml) flags open drafts with strong evidence
     their work already shipped. It never retires anything: a human answers each
     flag on the dashboard's "Looks shipped — confirm" section.

     Confirm  = close the draft: `python3 scripts/lifecycle.py close <slug>
                --date <YYYY-MM-DD> --from-file <record-body.md>
                --prompt <draft path> --apply`.
     Dismiss  = add one bullet below — the draft path first, then the date and
                why it is NOT shipped. A dismissed draft is no longer flagged and
                the batch planner may propose it again. Delete the bullet to let
                the guard look at it afresh.

     Format: `- draft/<work-type>/<target>/<name>.md — YYYY-MM-DD — <why>` -->

- draft/bug/autofit/ep_moments_loggaussian_transformed_scatter.md — 2026-11-07 — PyAutoFit main 0a557d7fa: `_OuterAxis.to_physical` (autofit/graphical/laplace/moments.py:243-249) still returns `-log_du_dx`, the double-counted Jacobian the draft fixes, and `split_variables` still promotes every bounded variable; the witness commit fdba47e49 is the parent module (#1654), not this fix.
- draft/feature/autofit/model_figures_ep_overlays.md — 2026-11-07 — No `overlays=` keyword or mean±std/precision/KL overlay exists in PyAutoFit main 0a557d7fa; autofit/model_figure/ep/state.py:45 still says posterior values and KL sparklines "are a separate" follow-up. Witness commit 73008021a is a docs pointer.
- draft/feature/autofit/prior_exit_sampler_coverage.md — 2026-11-07 — The witness `ClipperPriorBox` is the prerequisite (#1537), not this audit; no complete record covers Adam/Lion/ADABelief clip-rate coverage (clipper-validation-campaign measured MultiStartProdigy only).
- draft/feature/autofit/skip_the_likelihood_for_assertion_violating_samp.md — 2026-11-07 — PyAutoFit main 0a557d7fa `Fitness.call` still builds the instance with `ignore_assertions=True` and calls `log_likelihood_function` unconditionally (fitness.py:531-535), applying the assertion mask only at the end (:608); witness commit 323f6d5cd is the unrelated per-fit status record in interpolator/covariance.py.
- draft/bug/autoarray/adaptive_mesh_degenerate_pixel_pair.md — 2026-11-07 — Witness commit e52782ff fixes adaptive *rectangular* node centres (#667), not Delaunay near-duplicates; PyAutoArray main e2b05f00 has no de-duplication or minimum-separation step in `inversion/mesh/image_mesh/` and no delta-spike weight-map test.
- draft/bug/autoarray/interferometer_log_evidence_large_regularization_coefficient_cholesky.md — 2026-11-07 — PyAutoArray main e2b05f00 `_log_det_symmetric_from` (inversion/abstract.py:1037) still documents and keeps the default Cholesky raising on NumPy and NaN on JAX; no NaN→rejection guard or coefficient-1e6 regression test. Witness commits are the unrelated streaming P4 data_term override.
- draft/bug/autoarray/mapping_overlay_follow_ups_forward_regions_throu.md — 2026-11-07 — PyAutoGalaxy main `util/plot_utils.py:183` `plot_array` still takes no `regions=` (item 1), and PyAutoArray `plot_mapper` still swallows exceptions into `logger.info` (mapper_plots.py, item 4). Witness commit 499e087a is the small-datasets cap work.
- draft/bug/autoarray/sibson_serial_kernel_loses_allocation_hoisting.md — 2026-11-07 — The witness test is the existing #676 bit-identity test the draft names as its regression guard; `_sibson_from_tables_serial` (_sibson_numba.py:377) is still a plain `function_copy` of the prange body with no manual hoisting, and the file is unchanged since #676.
- draft/bug/autoarray/simulator_imaging_poisson_drawn_before_flag_check.md — 2026-11-07 — PyAutoArray main e2b05f00 `SimulatorImaging.via_image_from` (dataset/imaging/simulator.py:246-254) still draws Poisson noise unconditionally before checking `add_poisson_noise_to_data`; the euclid pipeline commit that names the draft is a downstream workaround, not the library fix.
- draft/bug/autoarray/sparse_terms_nufft_origin_and_mask_compatibility.md — 2026-11-07 — PyAutoArray main e2b05f00 `TransformerNUFFT._shift` (operators/transformer.py:443-446) still applies only the even-size half-pixel offset, never `real_space_mask.origin`; no mask fingerprint in `SparseTerms` provenance. Witness commit 8c73a9fb is the primary-beam tests.
