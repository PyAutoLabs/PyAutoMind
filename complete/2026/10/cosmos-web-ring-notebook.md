## What shipped (merged 2026-10-23)

autolens_assistant#161 (issue #160): phase 1 of the COSMOS-Web Ring guided walkthrough. `docs/colab/cosmos_web_ring_colab.{py,ipynb}` is an image-first, executed Colab notebook with no inference: the JWST F150W/F444W imaging, the vendored lensing schematic and Mercier et al. 2024 figures, the good lens model with "Explore The Model" controls, and "Ask Gemini" questions per section. Seven commits including a maintainer copy-edit; the Sérsic bad-fit comparison and the SVG schematic were rejected during review. Shipped 2026-10-20 under the Heart RED development override recorded on the task row; merged on an explicit human /prm.

## Epic state

Phase 1 of `cosmos_web_ring_guided_walkthrough.md` is done. Remaining: phase 2 (greeting mirrors the notebook) and phase 3 (HowToLens / website).

## Note

The autolens_assistant claim this task held blocked the autolens leg of PyAutoScientist#87 (AI options page); that leg is re-filed as `draft/docs/autolens_assistant/ai_options_page_autolens_leg.md` and can start now.

## Original prompt

# COSMOS-Web Ring walkthrough — phase 1: image-first Colab notebook, no inference

**Work type:** docs · **Target:** `lens/autolens_assistant` · **Consequence:** judge
Issued: 2026-10-20 · Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/160
**Epic:** [`cosmos_web_ring_guided_walkthrough.md`](cosmos_web_ring_guided_walkthrough.md)
(read it first: verbatim request, review findings, schematic usage rule, approval + Heart RED
override recorded 2026-10-20).

## Scope

1. **Vendor images** into `docs/images/` with rows in `docs/images/sources/README.md`:
   - `strong_lens_schematic.png` (already placed untracked in the canonical checkout; AI-generated
     for the human; downscale to ≤ ~1000 px wide / < 500 KB for the repo, keep the 2000 px
     original as `sources/strong_lens_schematic_2000.png` only if it fits the size budget,
     else note where the full-size file lives).
   - Mercier et al. 2024 (A&A 687, A61; arXiv:2309.15986; CC BY-SA 4.0) PyAutoLens
     lens-model figure, F444W row (observed / model / normalised residual / source); credit line.
2. **Rewrite `docs/colab/cosmos_web_ring_colab.py`** keeping the section skeleton and the
   general-reader + "For the scientist" + "Ask Gemini" pattern, with an image **before the
   code** under every header, via absolute raw-GitHub URLs (Colab runs in
   `autolens_workspace`, not this repo; pin to `main` now, note the tag switch):
   - What Is A Strong Lens? → schematic. Prose MUST bridge rays → multiple images → ring
     (epic "schematic usage rule") and the "Extra Galaxy" label.
   - The Picture → RGB `cosmos_web_ring_rgb.png` ("this is that ring"), then F444W plot cell.
   - Four Colours, One Ring → F277W/F444W pair (rendered output).
   - Preparing The Data → arrows image `cosmos_web_ring_dataset.png`, then noise-scaling +
     mask cell. Mask radius: use 2.1" to match the ansofi tracer's evaluation, or verify the
     tracer evaluates cleanly at 1.8"; say which and why.
   - **What A Lens Model Looks Like** (new, before The Model) → Mercier+24 figure; columns
     explained; links to the discovery paper and COWLS.
   - The Model → the four pieces, **no priors paragraph, no search**.
   - Good Versus Not-Great → load the committed ansofi `tracer.json`
     (`scripts/cosmos_web_ring/results/ansofi/`, from
     `/mnt/c/Users/Jammy/Science/active/cowls_ansofi/output/M25/COSJ100024+015334/F444W/slam/mass_total[1]/`
     zip `files/tracer.json`; dataset md5-identical to the bundle), build `al.FitImaging` on
     the prepared dataset, `aplt.subplot_fit_imaging` + source reconstruction. **Check:**
     AdaptSplit regularisation needs an adapt image — commit it alongside or evaluate with a
     constant regularisation and say so. Then the Sérsic "bad" model the same way: re-record
     its max-likelihood instance (`sersic_source/` has only `summary.json`) by re-running
     `scripts/cosmos_web_ring/fit_cosmos_web_ring.py`'s Sérsic variant once and saving
     `tracer.json`. Keep the good-vs-bad prose (clumpy source, residual knots, headline θ_E
     still looks fine).
   - The Mass Inside The Ring → from the evaluated good tracer (`al.LensCalc`), no search.
   - Where Next → "run the fit yourself": reference script + agent route; HowToLens; papers;
     the no-error-bars caveat moves here.
3. **Commit the notebook executed** (every code cell with outputs). Change
   `autoassistant/to_notebook.py` / `tests/test_colab_notebook.py` so the regeneration test
   compares with outputs and execution counts stripped; add a `make colab` (or script)
   target that converts and executes (`jupyter nbconvert --execute`), documented in the
   source header. Keep `test_first_code_cell_is_the_colab_setup…` and the starting-prompt
   assertions green.
4. **One prompt, everywhere (notebook side):** the starting prompt quoted in the notebook
   header must be byte-identical to README / `docs/setup/first_prompts.md` / the greeting
   skill; add a test that greps all four for the same text.
5. **Mind/benchmark:** if `benchmarks/truth/cosmos-web-ring-fit` or the fit card assume the
   notebook runs a search, update the card text only (benchmark behaviour is phase 2).

## Done when

Executed notebook renders with an image before the code in every section, both model fits
evaluate in seconds with no `search.fit`, tests green (`pytest autoassistant/tests`), README
figure-sources table updated, PR open against `autolens_assistant` main.
