# Order the two lens-light MGE bases in vis_lp and expose a Nautilus seed

Type: feature
Target: workspaces
Repos:
- euclid_strong_lens_modeling_pipeline
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: review
Witness: two independent unseeded vis_lp runs of the ordered model on tile 102005065 (euclid_dr1_prelim, RAL) give set-A and set-B ell_comps that agree run-to-run to within 0.05 per component with no A<->B swap, log evidence within 1.0 of the unordered baseline 9492.7, and per-set ell_comps marginal widths narrower than the unordered run's (the bimodal mixture collapses); the pipeline's test_mode run and `pytest tests/` pass locally under both `--use_cpu` and the JAX path with the assertion attached.
Review-minutes: 8
Unattended: ready


Apply the recommendation of `docs/mge_label_degeneracy.md` (euclid_strong_lens_modeling_pipeline#54) now that PyAutoFit#1583 (merged 2026-09-08, on library `main`; the RAL stack tracks library mains via HPCPullPyAuto) makes `add_assertion` enforceable on the JAX path.

In `scripts/initial_lens_model.py`:
1. After the model `af.Collection` is composed (after line ~236), attach an ordering assertion between the two lens-light MGE bases so the label symmetry is broken exactly: `|e_A|^2 > |e_B|^2` on the two shared ell_comps prior pairs (set A = `profile_list[0]`, set B = `profile_list[20]`), with a descriptive assertion name. Add a short prose block explaining why (two identical 20-Gaussian bases with iid priors are exchangeable; unseeded Nautilus lands on either labelling; see the note).
2. Expose the Nautilus seed for the vis_lp search as a `seed: Optional[int] = None` argument of `fit()` and a `--seed` CLI option in `start_here.py` (and wherever `fit()`'s arguments are plumbed, e.g. the two-stage batch scripts), default `None` (unseeded, so the witness measures the ordering alone). Document that `seed` is a search identifier field.
3. Do not change the vis_pix stage: it freezes the vis_lp ML instance; the ordering makes the frozen values canonical.
4. Keep `--use_cpu` working: on the NumPy path the assertion is enforced by exception + resample; on the JAX path by the traced penalty.

Constraints: land only between phases (both changes alter the vis_lp identifier and force fresh runs); euclid_dr1_prelim phase 4 (SLURM 342301_[0-9], 342314_3) must be finished or explicitly abandoned first. The science clone at `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim` pulls this change and `hpc/sync push --no-data` carries it to RAL; the witness reruns are a Cortex task on euclid_dr1_prelim, not part of this PR.

Out of scope: the `mge_model_from` ordering option in PyAutoGalaxy (ideas.md).

<!-- filed 2026-09-08 by the mge-label-degeneracy session from the ideas.md bullet tagged "research mge-label-degeneracy · scripts/initial_lens_model.py:162"; that bullet is retired by this prompt -->
