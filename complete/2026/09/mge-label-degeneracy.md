## mge-label-degeneracy
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/54
- completed: 2026-09-08
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/55
- heart-ack: 2026-09-08 in-session, two organism-scope reasons (autolens workspace validation failures; no release rehearsal) — docs-only branch
- Summary: research note `docs/mge_label_degeneracy.md` on the exact two-fold label symmetry of the vis_lp lens-light MGE (2x20 linear Gaussians, identical sigma ladders, iid ell_comps priors, shared centre). Swap invariance pinned on shipped tile 102018665 (0.0 on JAX, 1.8e-12 NumPy). Recommendation: ordering assertion `|e_A|^2 > |e_B|^2` plus explicit `af.Nautilus(seed=...)`, applied between phases (both change the run identifier); distinct sigma ladders rejected; post-hoc relabelling dropped by decision (tiles rerun from scratch instead).
- Blocker found: `add_assertion` was unusable on the pipeline's JAX path (vmapped Nautilus Fitness raised TracerBoolConversionError at trace time; non-vmapped let FitException escape). Fixed the same day in PyAutoFit#1583 (task traced-assertions-on-jax-path).
- Traps: there is no `nest.yaml` anywhere (seed is a Nautilus kwarg); log Z within 1.0 cannot distinguish one-mode from two-mode runs (ln 2 = 0.69), so the witness must also check per-set marginal widths; any model or seed change forces fresh runs.
- Next (ideas.md): pipeline edit + witness rerun on tile 102005065 once the PyAutoFit fix is released; `mge_model_from` ordering option in PyAutoGalaxy.
- Session: parallel-claim on euclid_strong_lens_modeling_pipeline with profiling-production-representative (#235), disjoint files.

## Original prompt

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
