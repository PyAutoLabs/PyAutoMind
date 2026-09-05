# Euclid DR1 preparation — 15k-lens modelling prep (10 real + 10 resimulated validation lenses)

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoLens
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
- autolens_assistant
Themes:
- euclid
- pixelization
- ci-smoke
- point-source
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: euclid-dr1-prep
Filed: 2026-08-28

Parent tracker for an 11-phase preparation programme ahead of modelling **over 15,000
strong lenses in Euclid DR1**. This file is never routed to `start_dev` directly — each
phase below is its own prompt, issued **ONE AT A TIME** as its predecessor nears
shipping (no bulk issue queues).

The programme's shape: make `euclid_strong_lens_modeling_pipeline` a first-class,
CI-covered repo that is genuinely representative of the DR1 analysis (Mind phases 0-4), then
prove it by fitting **10 real DR1 lenses** and **10 resimulations of those same lenses**
(phases 4-6), then extend the catalogue products (phase 7). The success criterion for
the whole epic is that everything delivered for the DR1 runs out of
`/mnt/c/Users/Jammy/Science/euclid` can be reproduced from the public pipeline repo.

## Original request (verbatim)

"""
I am gearing up to model over 15000 strong lens as part of Euclid DR1, and want to do a series of preparation runs
in advance. Set this up as an epic, albeit a lot of the work is doing science which then feeds into the preparation.
For the prep, the goal is to simulate 10 Euclid lenses based on results from an earlier run of DR1 lenses which
will test the lens modeling pipeline, fit the samwe 10 real datasets for comparison and validate the aspects outlined
below.

0) change default cmap to magma: lots of people compain about the cmap so make sure there is functionality to adjust 
cmap used throughout autolens and update euclid repo configs so that magma is used.

1) Firstly, we need to set up the repo "euclid_strong_lens_modeling_pipeline" to make it a first class repo which is
representative of the complete DR1 analysis. This includles:

- Compare to the code and setup in /mnt/c/Users/Jammy/Science/euclid and make sure all of the following funtctionality
can be done in this repo:

- Fit using an initial lens model (e.g. intial_lens_model.py).
- Fit which goes on to use single Sersic model (e.g. sersic_lens_model.py).
- Fit whcih then does multi wavelenght lens model for all NIR / EXT data (e.g. lens_model_waveband.py) and ensure
that this also has a way or option to follow on the single sersic fits (sersic_lens_model_waveband.py).
- Parity on util.py, making sure it has all the PSF_FWHM_WORST stuff and all latent variables.
- Look at catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/Tile102005065RA0135279431487DECNEG0701599765928e
and make sure all the files in catalogue/scripts required to make its contents (e.g. deblending.py, lens_mass.py, magnitdes.py)
are available and clean and documented in "euclid_strong_lens_modeling_pipeline", be extra careful with pairing here.

Be extra careful to ensure the lens model parameterization uses that in /mnt/c/Users/Jammy/Science/euclid, whic had
some polished upgrades and bug fixes which probabl didnt make their way into "euclid_strong_lens_modeling_pipeline" .

In general, /mnt/c/Users/Jammy/Science/euclid was used to do science without updating "euclid_strong_lens_modeling_pipeline" 
so if there is drift take /mnt/c/Users/Jammy/Science/euclid as a source of truth. full_model.py is definitely ok
and hsoul dbe kept on "euclid_strong_lens_modeling_pipeline" make sure its using Delaunay and mirrors the Delaunay SLaM on the autolens_worksapce
in terms of what it fits.

Documentation on all this stuff is pretty good, but make sure its cleaned up and high quality without stuff
missing where possible.

2) Next, for "euclid_strong_lens_modeling_pipeline", implement CI using TEST mode against all example scripts, which we will use simulated datasets (include a single simulator.py script)
which are added to the GitHub repo to test them. This differs to the normal workspace, which typically do auto-simulate,
the motivation here is that msot people use the repo to fit real data and we dont want auto simulate stuff clouding 
the setup. Also put unit tests on all Analysis latent stuff and some CI on the latent stuff. Look at the results and code 
setup in /mnt/c/Users/Jammy/Science/euclid and make sure this repo has the same latent variables and whatnot.

3) Science runs I perform for initial_lens_model.py use JAX for the MGE fit (vis_lp) and then numba with python multiprocessing for pixelization
   (vis_pix). The reason I do this is because I have loads of CPUs available and this means this is a much fastest way
to model large sampels. At the moment, I think this requires submission scripts be sumbmitted which run once for vis_lp,
then reset and run for vis_pix, as this avoids a JAX / Python multirprocessing conflict. First, make sure this functionality
is maintained, but also look to see if we can avoid the reset of the script (but its fine if thats not possible). Then,
make sure documentaiton is clear that fully JAX GPU runs are supported, they are typically much faster and recommended if you
are modeling a small subset of Euclid lenses. Retain example batch submission scripts showing these different approaches.

4) At this point, we want to begin doing sciene testing. the autolens_assistant has a euclid_mode, and I want you
to do this science testing using this. Make a new science project called /mnt/c/Users/Jammy/Science/euclid_dr1_prelim,
copy over the first alphanumerically 10 lenses in /mnt/c/Users/Jammy/Science/euclid, and fit them using the CPU approach
on RAL. The end goal should be a catalogue folder which has the same numerics apprxoimately as the run you compared to
above with all the latent variable output and other stuff. At this point, we should be confident that everything we
provided fur the DR1 runs in /mnt/c/Users/Jammy/Science/euclid we can do so here. 

5) Simulations! I now want us to be able to take a Euclid lens we have a result for and resimulate it so that we can fit
the simulated data and test if PyAutoLens recovers the correct values. This should result in a simulator.py example
script in "euclid_strong_lens_modeling_pipeline" which basically allows any user to do this, i.e. once ive fitted a
lens resimulate it. However, the resimulation of the 10 lenses we fit should be in the euclid_dr1_prelim project,
and it should make sure the magnification of these simulated lens is recorded as one of the follow up tasks is to
figure out if the magnifications recovered by PyAutoLens are accurate or not. These simulations should use Sersic lens
light profiles, Sersic sources (will be overly simple in some cases but thats fine). For the real lenses, many inferred Sersic lens models
hit the prior edge and infer sersic_index=5. In fact, I suspect this will happen itn he fits to these 10, so when you
resimulate if the lens light Sersic is at the prior edge of 5 lower is to a value between 2 and 4.

6a) Do we recover Sersic indexes accurately on simulated lenses? For the real lenses, many inferred Sersic lens models
hit the prior edge and infer sersic_index=5. Thus, we want to know for these 10 simulated lenses, do we recover
their sersic indexes accurately, and were their real lenses at the prior edge? The expectaiton is that a dodgy PSF model
or other aspects of the lens data are the cause of this issue, whcih the resimulation will not suffer from. Lets get to the
point where we have results for 10 lenses an then we can work out what chanfges we want to make to fix it.

6b) How robust are our magnification estimates? There are known systematics in magnifciation estimation in some
previous research I did. General vibe is when the lens light and source model match the simulate ddata (e.g. Sersics fitted to Sersics)
its ok, but when there is mismatch (E.g. an MGE is used) it breaks. This can be due to two reasons: if the source becomes an MGE
its because the source model is mismatched from the simualtion. If the lens light becomes an MGE its the same but the lens light
"leaks" into the source model messing up the magnification. We have also never really validated or tested the magnifcitations using
the Delaunay source model, and this could even have bugs (E.g due to pixel areas not being quite right). So, for this
Euclid epic do all of the magnification comparisons you can on the 10 lenses in this spirit, but also have a follow up issue
which checks if the soruce code itself looks like it might have a bug or issue with the Delaunay area and thus magnification calculations.

7) Extend the catalogue: Make sure the COolest results (look up recent work implemeting this) are available as a dediciated
.csv file, in the .fits files we need a mass model one which includes convergence, potential, deflections x and y, magnification
but assess whether the file size of tehse is large and thus if we should compress a bit by only doing deflections to derive them
with autolens code... one to think about. We are going to retroactively add these to the 10 lenses we fitted, and the ability
to update the catalgoue of lens models retroactively is quite valuable, but not something I want huge amount of source code
to maintain. So do some assessment on whether there are already functionality or ways to do it via catalgoue scritps,
or doing large reruns on the HPC, bt if theres no simple elegent solution then dont worry about it. It feels like
we would either need somehting whcih scraps output and adds manually or something which reruns and updates output,
 nothing is elegent.
"""

## Ground truth surveyed at filing (2026-08-28)

Read-only survey done while filing, so each phase prompt cites real paths:

- **Source of truth for drift:** `/mnt/c/Users/Jammy/Science/euclid` — `scripts/`
  (`util.py` lives at `scripts/util.py`, 978 lines), `catalogue/`, `hpc/`, `config/`,
  `dataset/`, `output/`, `preprocess/`, `paper/`, `inspection_results/`.
- **Target repo:** `/home/jammy/Code/PyAutoLabs/euclid_strong_lens_modeling_pipeline` —
  `scripts/` (5 scripts), root-level `util.py` (699 lines), `hpc/`, `tests/`
  (one file), `smoke_tests.txt` (6 entries), `config/`, `tools/`, `workflow/`,
  `preprocess/`, `start_here.py`.
- **Reference catalogue tile** is `…dr1_prelim_grade_ab_catalogue_csvs_20260623/Tile102005065RA0135279431487DECNEG0701599765928`
  — the trailing `e` in the request is a typo; the bundle holds 3024 tile directories.
  The reference tile contains 13 files: `lens_mass.csv`, `lens_sersic.csv`,
  `source_sersic.csv`, `magnitudes.csv`, `model.fits`, `pre_psf.fits`, and the PNGs
  `fit_sersic.png`, `fit_multi_wavelength.png`, `rgb.png`, `segmentation.png`,
  `vis_lp_fit.png`, `vis_lp_image_with_positions.png`, `vis_pix_fit.png`.

### Surprises worth carrying into the phases

1. **`PSF_FWHM_WORST` does not exist** anywhere in `Science/euclid` (or the pipeline
   repo). The real machinery is the `WORST_BAND` / `WORST_PSF_*` FITS primary-header
   metadata consumed by `Science/euclid/scripts/lens_model_waveband.py` (lines ~70-90,
   ~256, ~298-312, ~489). Phase 1 must port *that*, not a symbol of the requested name.
2. **`full_model.py` exists only in the pipeline repo**, not in `Science/euclid` — so it
   genuinely is the pipeline repo's own asset, as the request assumes. But it currently
   uses `RectangularAdaptImage` / adaptive-rectangular meshes, **not Delaunay**.
3. **The `autolens_workspace` reference SLaM is not Delaunay either** —
   `autolens_workspace/scripts/guides/modeling/slam_start_here.py` uses
   `RectangularBilinearAdaptDensity` (init) and `RectangularBilinearAdaptImage`
   (main). So "mirror the Delaunay SLaM on the autolens_workspace" has no existing
   referent; phase 1 must put this question to the user before changing meshes.
4. **`autolens_assistant` has no literal `euclid_mode`** — what exists is the euclid
   skill family `autolens_assistant/skills/euclid_prepare_data.md`,
   `euclid_setup_pipeline.md`, `euclid_model_lens.md`, `euclid_hpc_runs.md`. The 10-lens
   science run (now Cortex euclid 4)
   drives the science run through those.
5. **The cmap lever already exists.** `visualize/general.yaml` carries
   `colormap: autoarray` in all three configs (PyAutoArray, autolens_workspace,
   euclid pipeline) and `PyAutoArray/autoarray/plot/utils.py::_default_colormap()`
   reads it. So phase 0 is mostly "verify the lever reaches every plot surface and
   set magma in the euclid configs", not "build the lever".
6. **Script drift.** `Science/euclid/scripts/` has 15 scripts; the pipeline repo has 5.
   Absent from the pipeline repo: `sersic_lens_model_waveband.py`,
   `sersic_lens_model_pix.py`, `sersic_lens_model_pix_waveband.py`,
   `multi_lens_model_pix_waveband.py`, `galaxy_sersic_model.py`, `diagnose_latent.py`,
   `diagnose_latent_vis_pix.py`, `build_inspect.py`, `audit_sed_outputs.py`,
   `reorganize_normies.py`. The whole `catalogue/` tree (27 files under
   `catalogue/scripts/`) is absent from the pipeline repo.

## Phases (order is load-bearing)

0. `complete/2026/08/cmap-magma-default.md` — colormap lever audit + magma
   defaults in the Euclid configs. Independent; gated nothing.
   **SHIPPED 2026-08-28** — issue PyAutoArray#509 (closed); PyAutoArray#510 and
   euclid_strong_lens_modeling_pipeline#42 both merged.
1. `complete/2026/08/euclid-pipeline-parity.md` — port the DR1 analysis
   from `Science/euclid` into the pipeline repo (scripts, `util.py`, `catalogue/scripts`,
   parameterization, docs). Drift rule: `Science/euclid` wins. Blocked 2-4; now unblocked.
   **SHIPPED 2026-08-29** — issue euclid#43 closed, PR #44 merged.
2. `complete/2026/08/euclid-ci-test-mode.md` — committed simulated
   datasets + TEST-mode CI over every example script + latent unit tests. Gate: 1.
   **SHIPPED 2026-08-29** — issue euclid#45 closed, PR #46 merged.
3. `complete/2026/09/restore-pipeline-narrative-prose.md` (was 3a) — **restore the in-script
    narrative prose**: `start_here.py` back to a fully documented end-to-end new-user
    guide (kept as a shim over `initial_lens_model.fit`), `scripts/*.py` written to assume
    it has been read (point back for repeats, explain in full what it does not cover —
    e.g. the empty `__Source Pix__` block), `catalogue/scripts/*.py` lifted toward the
    `workflow/example/` register. Recovered prose is 4+ months stale: verify against the
    code and `autolens_workspace` before restoring. Gates: 1, 2. Inserted 2026-08-31.
    **SHIPPED 2026-09-01** — issue euclid#47 closed, PR #48 merged. Follow-up bug prompt
    filed: `draft/bug/euclid/vis_lp_batch_size_kwarg_silently_ignored.md` (the `vis_lp`
    search passes a `batch_size` kwarg `af.Nautilus` silently swallows).
4. `complete/2026/09/euclid-cpu-two-stage-route.md` (was 3b) — preserve and
   document the two-stage vis_lp (JAX) → vis_pix (numba + multiprocessing) CPU route
   and the full-JAX-GPU route. Gate: 1 (can overlap 2). Ran after phase 3 so its new
   documentation landed in a repo whose narrative register is already restored.
   **Issue euclid#49** — opened 2026-09-01 at filing, as the gate ref the Cortex science
   phase names.
   **SHIPPED 2026-09-03** — issue euclid#49 closed, PR #50 merged (`2412552`, 9 commits):
   `--stage {all,vis_lp,vis_pix}`, the `batch_cpu` two-stage submission chain, `hpc/README.md`
   as the route guide with measured RAL times (GPU 1 h 14 min, two-stage CPU 3 h 17 min), the
   `jax_fork_control` control test (no hang; process boundary kept as the conservative
   default), a `jax.default_backend()` guard on every GPU script, and the
   `apply_sparse_operator` drift removed from the JAX path. Follow-ups filed:
   `draft/bug/euclid/gpu_per_lens_time_vs_documented_10_min.md`,
   `draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md`.
   **Both gates of the Cortex 10-lens science run (`euclid#48`, `euclid#49`) are now closed.**

**→ Cortex** — the four science phases below are no longer Mind phases. They live under
`PyAutoCortex/phases/euclid/` with their own phase numbers, and the entries here are
pointers so the ordering of the programme still reads end to end. The Mind phase list
resumes at 8.

- **old 4 → Cortex phase 4** `PyAutoCortex/phases/euclid/dr1_prelim_10_lens_science_run.md`
  — **science run on RAL**; new `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim` project, first
  10 lenses alphanumerically, CPU approach, driven through the assistant's euclid skills.
  Gates: `euclid#48` (the merged Mind-phase-3 PR) and `euclid#49` (Mind phase 4).
  Human-driven, supervised.
- **old 5 → Cortex phase 5** `PyAutoCortex/phases/euclid/resimulate_fitted_lens_simulator.md`
  — `simulator.py` in the pipeline repo + the 10 resimulations in `euclid_dr1_prelim`, with
  true magnifications recorded and `sersic_index` pulled off the prior edge. Ready when
  Cortex euclid 4 is accepted. It also carries a real `simulator.py` PR, filed as a Mind dev
  prompt when the phase opens.
- **old 6a → Cortex phase 6** `PyAutoCortex/phases/euclid/sersic_index_recovery.md` — do we
  recover Sersic indices on the simulated lenses, and were the real ones at the prior edge?
  Ready when Cortex euclid 5 is accepted.
- **old 6b → Cortex phase 7** `PyAutoCortex/phases/euclid/magnification_robustness.md` —
  magnification systematics under model match/mismatch (Sersic-vs-Sersic, MGE source, MGE
  lens light, Delaunay source) across the 10 lenses. Ready when Cortex euclid 5 is accepted.

8. `complete/2026/09/delaunay-area-magnification-audit.md` (was 6c) — source-code audit of
   Delaunay pixel-area and magnification calculations. **May run alongside the Cortex
   magnification-robustness phase**; does not gate on it. May spawn a separate bug prompt
   if a real defect is found.
   **SHIPPED 2026-09-04** — issue PyAutoArray#522 closed, PR PyAutoArray#523 merged (`8c2e0d18`, merge `548ff1e`; tests +
   docstring only, no behaviour change; audit posted in full on #522). Verdict: **two real
   defects, neither fixed here by design**, filed as follow-ups:
   `complete/2026/09/delaunay-dual-area-magnification.md` — **SHIPPED 2026-09-05**, PyAutoArray#524
   closed, PR #525 merged (`46aaac67`, merge `de92d09c`), pending-release — (the Delaunay
   `areas_for_magnification` returns Voronoi cell areas, but the mapper is barycentric-linear
   so the exact quadrature weight is the barycentric dual area; identity-lens μ is 1.0 to
   2e-5 with dual areas, −13..−53 % on adaptive-style meshes and −95..−99 % when the source
   fills the hull with Voronoi areas; `zeroed_pixels` cannot rescue it — the pathology is one
   ring inside the convex hull) and
   `draft/bug/autolens/magnification_latent_zero_for_pixelized_source.md` (the pipeline's
   `magnification` latent is a hard 0/0 for any pixelization-only source because
   `Galaxy.image_2d_from` returns zeros; 9/9 archived `vis_pix` results record `0.0`; the
   Sersic control reproduces `truth.json` bit-for-bit). The rectangular-mesh lead (+6 %/+28 %
   guard-ring signature, not established) went to the cluster epic's
   `draft/test/workspaces/mesh_magnification_correctness.md`.
   **Statement to Cortex phase 7:** Delaunay magnification numbers from `source_science.py`
   are NOT trustworthy until the autoarray follow-up ships; the Sersic rungs 1-4 are sound.
   **Statement to Cortex phase 4 / Mind phase 9:** the `vis_pix` catalogue `magnification`
   column is a `0.0` sentinel today, so phase 4's numerics witness must exclude it (or
   the autolens follow-up must ship first) and phase 9's magnification layer depends on it.
   Record: `complete/2026/09/delaunay-area-magnification-audit.md`. The two follow-up bug
   prompts are the epic's next steps (autoarray fix first, then the autolens fix with its
   euclid workspace leg behind the library-first gate).
9. `draft/feature/euclid/catalogue_extension_coolest_mass_fits.md` (was 7) — COOLEST CSV,
   mass-model FITS products with a file-size assessment, and a feasibility verdict on
   retroactive catalogue updates. Gates: the Cortex 10-lens science run
   `PyAutoCortex/phases/euclid/dr1_prelim_10_lens_science_run.md` (needs a catalogue to
   extend); the Cortex magnification-robustness phase informs the magnification layer.

## Renumbering and the Cortex split (2026-09-01)

Phase 4 of the `cortex-birth` epic (PyAutoMind#383) moved the **science half** of this
epic into `PyAutoCortex`. The Mind keeps the software phases; the Cortex holds the runs
and the rulings. The 3a/3b letters died with the split — the Mind's phases are plain
integers again, and no two Mind phases share a number.

| Old | Where it lives now | New phase | Gate |
|---|---|---|---|
| 0 | Mind (shipped) | 0 | — |
| 1 | Mind (shipped) | 1 | — |
| 2 | Mind (shipped) | 2 | 1 |
| 3a | Mind (shipped) | **3** | Gates: 1, 2 |
| 3b | Mind (shipped) `complete/2026/09/euclid-cpu-two-stage-route.md` | **4** | Gate: 1 (can overlap 2); ran after 3 |
| 4 | → Cortex `phases/euclid/` `dr1_prelim_10_lens_science_run` | **4 (Cortex)** | `euclid#48`, `euclid#49` |
| 5 | → Cortex `phases/euclid/` `resimulate_fitted_lens_simulator` | **5 (Cortex)** | Ready when Cortex euclid 4 accepted |
| 6a | → Cortex `phases/euclid/` `sersic_index_recovery` | **6 (Cortex)** | Ready when Cortex euclid 5 accepted |
| 6b | → Cortex `phases/euclid/` `magnification_robustness` | **7 (Cortex)** | Ready when Cortex euclid 5 accepted |
| 6c | Mind (shipped) `complete/2026/09/delaunay-area-magnification-audit.md` | **8** | none; ran alongside Cortex 7 |
| 7 | Mind `draft/feature/euclid/catalogue_extension_coolest_mass_fits.md` | **9** | Cortex euclid 4 |

Mind phase numbers and Cortex phase numbers are separate sequences that happen to
collide at 4 — the Mind's 4 is the CPU-route software phase, the Cortex's 4 is the
10-lens science run, and the first **gates** the second (`euclid#49`). Always say which
organ you mean.

`euclid#49` exists because a Cortex phase's `Gates:` line can only name a GitHub ref:
per decision 55, a Cortex-spawned dev follow-up gets its issue **at filing** while its
prompt stays in `draft/`, and the prompt carries the `Issue:` line so `create_issue` /
`start_dev` reuse it rather than opening a second.

## Notes for whoever resumes this

- **The old phases 4, 5, 6a, 6b are science, not software — and since 2026-09-01 they are
  Cortex phases 4, 5, 6, 7.** They run on RAL (HPC) with the human in the loop, on
  wall-clock timescales of days. They are `supervised` and must never be handed to an
  autonomous ship gate. The deliverable of each is a result and a written verdict, not a
  merged PR — though Cortex 5 does carry a real `simulator.py` PR, filed as a Mind dev
  prompt when the phase opens.
- **Mind phase 8 (was 6c) is a library audit** in PyAutoArray/PyAutoLens and is the only
  phase that can plausibly land as a fast standalone fix. It may spawn a follow-up bug prompt.
- **Mind phase 9 (was 7) is explicitly allowed to conclude "no elegant solution → don't
  build it"** for the retroactive-update leg. That is a valid, shippable outcome.
- **Phase 3 (then numbered 3a) was inserted on 2026-08-31 and shipped on 2026-09-01**, after an audit found the repo's in-script
  narrative prose had been largely lost — not by the phase-1 port (which was net prose
  *positive*) but by `355b309` (2026-04-02, −812 prose lines) which deleted the
  `pipelines/` tree, and by `fc43be0` which deleted `groups.py` / `point_source.py`
  outright. The old prose was recoverable from `git show 355b309~1:pipelines/<f>.py` but
  4+ months stale — every workspace cross-reference in it had drifted, so every restored
  claim was drift-verified against the code and `autolens_workspace`. The record
  `complete/2026/09/restore-pipeline-narrative-prose.md` carries the folded prompt with
  the verified drift list.
- Issue **one** phase at a time. Do not queue GitHub issues for later phases.
