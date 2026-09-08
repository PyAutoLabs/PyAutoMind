# Remove the two-fold label degeneracy in the Euclid lens-light MGE model

Type: research
Target: workspaces
Repos:
- euclid_strong_lens_modeling_pipeline
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Issued: 2026-09-08
Consequence: glance
Witness: after the recommended change, two independent unseeded vis_lp runs on tile 102005065 give set-A and set-B ell_comps that agree run-to-run to within 0.05 per component (no A<->B swap), with log evidence within 1.0 of the current baseline (9492.7).
Review-minutes: 3
Unattended: ready


Investigate removing the two-fold label degeneracy in the Euclid lens-light MGE model.

In `scripts/initial_lens_model.py` the lens light is composed with `mge_model_from(gaussian_per_basis=2)`: a Basis of 40 linear Gaussians built as two sets of 20 with identical sigma ladders, identical TruncatedGaussian(0, 0.3, ±0.5) priors on ell_comps, and a shared centre. Swapping the two sets' ellipticities gives a bit-identical model image, so the posterior has an exact two-fold label symmetry; Nautilus runs unseeded (seed: null), so which set lands in which mode is a coin flip per run.

Confirmed 2026-09-08 by comparing the May (euclid project, job 306843) and September (euclid_dr1_prelim, job 342301) vis_lp results for the same ten DR1 tiles: 6 of 8 well-determined tiles swapped set A<->B (e.g. tile 102005065 set A PA 0 -> 90 deg, set B 90 -> 0 deg), the unordered pair of ellipticities is conserved in every tile, mass/source ell_comps, centres, Einstein radii and log evidence are unchanged, and the dataset is byte-identical. It reads as a sign flip when one set is inspected alone.

Investigate the options for removing the degeneracy and recommend one:
(a) break the symmetry at the model level, e.g. a monotone ordering constraint between the two sets' ellipticity magnitudes or angles, or asymmetric priors;
(b) give the two sets different sigma ladders (e.g. interleaved or offset) so they are no longer exchangeable;
(c) an explicit Nautilus seed in config/non_linear/nest.yaml for reproducibility only (does not remove the degeneracy);
(d) a post-hoc canonical relabelling in the results/aggregator layer.

Assess for each whether it changes the fit quality, the run time, the downstream vis_pix identifiers (the MGE ell_comps propagate as fixed instances), and whether it belongs in the pipeline or upstream in the library's `mge_model_from` helper (in which case the library repo that owns it becomes the target of the follow-up).

<!-- formalised by the Intake (Conception) Agent on 2026-09-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/57e6c543-0042-4147-9573-df3686a157da/scratchpad/intake-mge-degeneracy.md -->
