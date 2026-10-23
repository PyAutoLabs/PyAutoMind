# COSMOS-Web Ring: image-first guided walkthrough (notebook + greeting skill)

**Work type:** docs · **Target:** `lens/autolens_assistant` (plus one-line follow-ups in
`lens/HowToLens` and the website) · **Filed:** 2026-10-20 from a review session.

## Request (verbatim, from the human)

> I want us to do a review of this experience for random people doing it. I think the fact it
> asks the user their level (e.g. a curious reader) is good, but it still feels like the user
> isnt really guided through the lensing too much, only a subplot of the data is put in a claude
> temporary folder and the inference modeling kicks off on GPU without much fanfare. I think
> this agent conversation could be more guided by the format of the google colab notebook, I
> think its structure of "What is a Strong Lens", "The Picture" "Four Colours, One Ring" and so
> on is good. However, I think the Notebook should have an image after every header (so "What
> is a strong lens" has the 2D schematic of a strong lens found in HowToLens), "The Picture"
> should have the RGB in line in the matplotlib boko so its there before running code, and I
> think we should upload this notebook with run all having been run so images are already
> included. I think we should not do full inference when we go via the agent cause its too
> slow, the Notebook has the good versus not great text and I think the agent should direct
> towards that unless the user wants to do lens modeling. I also think the autolens_assistant
> image with the arrows should be used and present in "Preparing The Data" for the notebook.
> The notebook should thus not have priors covered as I dont want to do inference which is
> slow. So the goal should just be to guide the reader to an example of a "good model" (see
> Science/active/cowls_ansofi) and a "bad model". I really think the assistant in general, not
> just for this example, should be trying to get images displayed to the user more quickly.

Follow-up decisions (same session): use Mercier et al. 2024 (A&A 687, A61; arXiv:2309.15986,
CC BY-SA 4.0) lens-model figure (the four-column PyAutoLens data / model / normalised residual
/ source figure, F444W row) as the "what a publication-quality model looks like" motivation,
slotted **before "The Model"**. Two tiers only (good, bad). Good = the cowls_ansofi
`mass_total[1]` result evaluated in the notebook (no search), not its PNG; bad = the single
Sérsic source. Schematic DELIVERED 2026-10-20 (AI-generated for the human, 2000x667 RGBA,
1.6 MB): placed untracked at `lens/autolens_assistant/docs/images/strong_lens_schematic.png`
in the canonical checkout — copy it into the worktree (and downscale/optimise if it stays
above ~500 KB). It shows observer (JWST) ← two bent "Lensed Source Galaxy Light" rays around
a "Lens galaxy", with an "Extra Galaxy" below and the "Source galaxy" at right. **It does not
show the two rays becoming multiple images or a ring**, so wherever it is used the prose must
make that link explicitly before the RGB follows: the two rays are two of infinitely many
paths; every path around the lens arrives from a slightly different direction, so the observer
sees the source smeared into arcs, and when source and lens line up, a full ring — then show
the COSMOS-Web RGB as "this is that ring". Its "Extra Galaxy" label also pre-announces the
arrows image in Preparing The Data. The human also wants it (a) as the opening image on
jamesnightingale.net before the RGB (personal site, not in this workspace — hand over the
file + a caption) and (b) in HowToLens tutorial 2 in place of the region-blocked imgur link.

## Review findings (why)

- Greeting skill's first reply runs PyAutoLens to plot `subplot_imaging_dataset` into
  `scripts/scratch/`; the shipped `docs/images/cosmos_web_ring_rgb.png` and the annotated
  `docs/images/cosmos_web_ring_dataset.png` (arrows) are never shown. Every route then runs a
  48-start Prodigy fit (minutes, GPU) after one question.
- `docs/colab/cosmos_web_ring_colab.ipynb` is committed with 0/11 code-cell outputs; no image
  precedes code; "What Is A Strong Lens?" has no picture; two slow fits; priors paragraph.
- HowToLens tutorial 2 schematic is an imgur link (`i.imgur.com/zB6tIdI.jpg`) that is
  region-blocked ("Content not viewable in your region"); nothing local.
- `autoassistant/tests/test_colab_notebook.py::test_notebook_regenerates_byte_identically`
  forbids a committed notebook with outputs; Colab runs from `autolens_workspace`, so inline
  images need absolute raw-GitHub URLs (pinned to the release tag, as the website already does).
- cowls_ansofi F444W `data/noise_map/psf/mask_extra_galaxies.fits` are md5-identical to the
  assistant bundle; its `mass_total[1]` zip holds `files/tracer.json` (MGE lens light 40
  Gaussians, PowerLaw θ_E 0.768" slope 1.94, shear, Delaunay + AdaptSplit source), mask 2.1".

## Plan

1. **Vendor images** into `docs/images/`: lensing schematic (new, human-generated, with a
   `sources/README.md` row); Mercier+24 lens-model figure (F444W row crop, CC BY-SA credit
   line); keep RGB + arrows images. Fix HowToLens tutorial 2 to the vendored schematic (own PR).
2. **Notebook rewrite** (`docs/colab/cosmos_web_ring_colab.py`), image under every header,
   no inference:
   - What Is A Strong Lens? → schematic.
   - The Picture → RGB image, then F444W plot cell.
   - Four Colours, One Ring → F277W/F444W pair.
   - Preparing The Data → arrows image, then noise-scaling + mask cell (2.1" to match ansofi;
     confirm vs 1.8" in the greeting).
   - **NEW: What A Lens Model Looks Like** → Mercier+24 figure; what the columns mean; link to
     the paper and COWLS.
   - The Model → the four pieces; no priors paragraph.
   - Good Versus Not-Great → load ansofi `tracer.json` (committed to
     `scripts/cosmos_web_ring/results/ansofi/` with provenance), build `FitImaging` on the
     prepared dataset, `subplot_fit_imaging` + source reconstruction; then the Sérsic
     max-likelihood model the same way. Check: AdaptSplit needs the adapt image — commit it or
     switch the committed tracer to a constant-regularisation evaluation; `sersic_source/`
     currently stores only `summary.json`, so its instance must be re-recorded.
   - The Mass Inside The Ring → from the evaluated good tracer (LensCalc), no search.
   - Where Next → "run the fit yourself" via reference script / agent; HowToLens; papers.
   - Commit the notebook **executed**; change `to_notebook` test to compare with outputs
     stripped; add a `make colab` execute step.
3. **Greeting skill** (`skills/al_greeting_cosmos_web_ring.md`): first reply opens the RGB and
   arrows images with the platform opener (no Python), two-sentence explanation, one question.
   After the answer: walk the notebook's sections using shipped figures, ending at good vs bad
   (evaluate, don't search). Full inference only on explicit request, cost stated first.
   Update `benchmarks/prompts/conversational/easy_cosmos_web_ring.md` + the fit card if its
   truth assumes a search.
4. **Assistant-wide rule** in `skills/_style.md`: show an existing figure before writing code;
   when code must plot, open the PNG for the user. Sweep `al_*` skills for compliance.
5. **README / first_prompts / website line**: "no fit needed; fit via the agent if you want".

## Done when

Executed notebook renders every section with an image before its code; CI green with the
new output-stripped comparison; greeting benchmark passes with the no-search route; HowToLens
tutorial 2 shows the vendored schematic.

## Approval record (2026-10-20)

Human approved the plan, the three-phase split below and authorized the **Heart RED
override (development only)** for this docs work. Added scope: the opening experience must be
**the same in every spot** — jamesnightingale.net, README, `docs/setup/first_prompts.md`, the
Colab notebook header and the greeting skill all carry the identical starting prompt and the
same image sequence (schematic → RGB → …), so a visitor from any door gets one polished story.
Phases: `_p1_notebook.md`, `_p2_greeting.md`, `_p3_front_doors.md` (this file is the umbrella).

**Schematic decision 2026-10-20 (human):** the SVG `docs/images/strong_gravitational_lensing_schematic.svg`
(pushed to main that morning) is rejected ("rubbish") and is removed in phase 1. The JWST-style
PNG `strong_lens_schematic.png` is the only schematic, everywhere (notebook, greeting, README,
HowToLens, website); the rays→ring link is carried by prose.

## Phase 1 outcome (2026-10-20, PR autolens_assistant#161, awaiting /prm)

**Merged 2026-10-23** via human /prm (autolens_assistant#161; record `complete/2026/10/cosmos-web-ring-notebook.md`). Phase 1 DONE; next is `_p2_greeting.md`.

Shipped with design changes made during the maintainer's copy-edit pass — **phases 2 and 3
must follow the shipped notebook, not the original plan**:
- Bands: the live colour comparison is **F150W/F444W** (not F277W); the published-model figure
  is `docs/images/mercier2024_lens_model_f150w_f444w.png` (F150W above F444W).
- **"Good Versus Not-Great" is replaced by "Explore The Model"**: the reader edits
  `einstein_radius_offset` (arcsec) and `lens_light_scale`, sees original/changed rows of model
  image, light-subtracted image and residuals; the Sérsic "bad model" comparison is gone from
  the notebook (its tracer stays in `results/sersic_source/` as an artefact). The greeting skill
  (phase 2) should mirror this: load the good model, show its fit, then offer "change the mass /
  the lens light and look at the residuals", not a Sérsic bad fit.
- No "For the scientist" asides anywhere; "**🤖 Ask Gemini:**" lines bold with emoji; the
  notebook is "a guided tour", with the agent offered as an alternative ("If you prefer…"), not
  "two routes". Phase 3 README/first_prompts/website text should use the same framing.
- The Picture opens with `cosmos_web_ring_rgb_labelled.png` (colour ring + arrows); the
  three-panel `cosmos_web_ring_dataset.png` stays under Four Colours and Preparing The Data.
- Section images: schematic → labelled RGB → three-panel → three-panel → Mercier F150W/F444W →
  good-model panels → explore figure → Einstein-radius figure → RGB.

Deferred follow-ups (file as small prompts when convenient): regenerate
`cosmos_web_ring_dataset.png` with F150W/F444W panels (and the 2.1" mask); drop the
over-sampling panels from displayed subplots; `first_prompts.md` GPU-fit sentence (phase 3).
