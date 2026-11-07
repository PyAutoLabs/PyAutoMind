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
