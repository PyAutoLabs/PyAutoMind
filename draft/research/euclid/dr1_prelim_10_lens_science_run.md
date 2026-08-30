# DR1 prelim science run: fit 10 real Euclid lenses in a new euclid_dr1_prelim project on RAL

Type: research
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- autolens_assistant
- PyAutoLens
Themes:
- euclid
- hpc
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Epic: euclid-dr1-prep
Phase: 4
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28

Phase 4 of 10 in the Euclid DR1 preparation epic. **Gates: phase 1 and phase 3**
(phase 2 strongly preferred — **SATISFIED 2026-08-29**: phase 2 shipped,
`complete/2026/08/euclid-ci-test-mode.md`, euclid#45 closed, PR #46 merged).
**Gates phase 5, and phase 7 needs its catalogue.**

**This is a science run on RAL, not a software task.** It is human-driven and
`supervised`; it runs on wall-clock timescales of days and must never be handed to an
autonomous ship gate. Its deliverable is a result and a written verdict.

User request (verbatim):

"""
4) At this point, we want to begin doing sciene testing. the autolens_assistant has a euclid_mode, and I want you
to do this science testing using this. Make a new science project called /mnt/c/Users/Jammy/Science/euclid_dr1_prelim,
copy over the first alphanumerically 10 lenses in /mnt/c/Users/Jammy/Science/euclid, and fit them using the CPU approach
on RAL. The end goal should be a catalogue folder which has the same numerics apprxoimately as the run you compared to
above with all the latent variable output and other stuff. At this point, we should be confident that everything we
provided fur the DR1 runs in /mnt/c/Users/Jammy/Science/euclid we can do so here. 
"""

## Correction on "euclid_mode"

There is no literal `euclid_mode` in `autolens_assistant`. What exists is the euclid
skill family, and the run goes through those:

- `autolens_assistant/skills/euclid_prepare_data.md` — validate/assemble the
  `dataset/<sample>/<dataset>/` folders.
- `autolens_assistant/skills/euclid_setup_pipeline.md` — set the project up.
- `autolens_assistant/skills/euclid_model_lens.md` — choose and run the staged pipelines.
- `autolens_assistant/skills/euclid_hpc_runs.md` — drive the RAL submissions.

## Deliverables

1. **A new science project** at `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim`, set up
   through `euclid_setup_pipeline` and driven by the **pipeline repo** (that is the
   whole point — this run is the proof that the public repo can do what the private
   science tree did).
2. **The first 10 lenses alphanumerically** from `/mnt/c/Users/Jammy/Science/euclid`
   copied over. State the sort key explicitly and list the 10 chosen datasets by name in
   the issue before running, so the selection is reproducible and auditable.
3. **Fits via the CPU approach on RAL** — the two-stage `vis_lp` (JAX) → reset →
   `vis_pix` (numba + multiprocessing) route from phase 3, submitted with the pipeline
   repo's own `hpc/batch_cpu` scripts.
4. **A catalogue folder** for these 10 lenses, produced by the pipeline repo's
   `catalogue/scripts` (ported in phase 1), containing the same product set as the
   reference tile: `lens_mass.csv`, `lens_sersic.csv`, `source_sersic.csv`,
   `magnitudes.csv`, `model.fits`, `pre_psf.fits`, and the PNG set (`fit_sersic.png`,
   `fit_multi_wavelength.png`, `rgb.png`, `segmentation.png`, `vis_lp_fit.png`,
   `vis_lp_image_with_positions.png`, `vis_pix_fit.png`) — **with the full latent
   variable output**.
5. **A numerical comparison** against the corresponding entries in
   `/mnt/c/Users/Jammy/Science/euclid/catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/`
   for those same 10 lenses. Approximate agreement is the bar — these are stochastic
   samplers, not bit-identical pipelines — but "approximate" must be quantified: state
   a per-parameter tolerance up front and report where it is exceeded.

## Acceptance / gate

- 10 lenses fitted end to end on RAL from the pipeline repo alone.
- Catalogue folder complete, latents present, numerics approximately matching the
  20260623 reference within a stated tolerance.
- A written verdict: **can everything delivered for the DR1 runs out of
  `Science/euclid` now be delivered from `euclid_strong_lens_modeling_pipeline`?**
  Any "no" is itself a finding and should feed back into phase 1.
- Gates phase 5 (the resimulations need these results as their truth inputs).
