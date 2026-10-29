# Clear COSMOS-Web Ring figures for assistant newcomers

Type: feature
Target: autolens_assistant
Consequence: judge

Primary: @autolens_assistant. Assistant-specific presentation; retain existing library/workspace diagnostic defaults.

## Original request (verbatim)

Use the COSMOS-Web ring to improe the colormap and color scheme to make it so the lens and source are both visisble,
the images of this for the starting autolens assistant stuff are crap.

For the autolens assistant and times when a user is new or being introduced to lensing, the dataset image should
only have 4 panels (image, noise map, signal to noise map, PSF) and we should avoid having over sampling information
displayed. I think things like over sampling and introduced ok in workspace tutorials so its really just
having a less information dense image for new users using the AI assistant.

Basically, my feeling is that for autolens assistant users the cosmos web ring example is their entry point to PYAutoLens, and its quite under whelming how basic the cosmos web ring in built autolens visualization looks, and that its got panels that confuse a reader. So I think we should make them clear and better and perhaps include a task or feature which prompts them to customize and change visualization with a suggest for now. Do this task and then have me run and inspect the paired Colab Notebook so I can see how the assistant structure of conversation and images look.

## Proposed plan — awaiting approval

1. Build a consistent assistant introduction plot: a readable 2x2 grid with Image, Noise map, Signal-to-noise map and PSF. Preserve model over-sampling internally but omit its panels from this presentation.
2. Compare brightness stretches and perceptually ordered color maps on the actual F444W data, choosing limits that reveal both the central lens and the ring. Keep negative/noise pixels well-defined, excluded regions distinct and colorbars truthful. Carry the chosen presentation through the notebook's introductory band comparison.
3. Update greeting/data-preparation guidance to use this view for newcomers and introduce optional customization after the background question has been answered. Suggested prompt: "Can you change the colour map and contrast so I can see the lens galaxy and the ring more clearly?"
4. Regenerate and execute the paired Colab notebook, review the rendered figures, run focused plotting/notebook/context checks, and provide a review copy plus a runnable Colab link for the human.

Tier: judge — merge mode: human /prm.

## Implementation detail

- `skills/al_greeting_cosmos_web_ring.md`: replace the full diagnostic plot recipe with the introductory recipe; retain the first background question and scientific preparation gates; add the optional visualization follow-up after audience routing.
- `skills/al_prepare_imaging_data.md` and applicable introductory guidance in `skills/_style.md`: establish the four-panel newcomer recipe, reserving detailed sampling diagnostics for explicit technical discussion.
- Assistant-owned plotting recipe/helper: compose four panels using the verified functional plotting API and Matplotlib. Choose a form that the standalone Colab notebook can execute without importing an assistant checkout. Avoid changing PyAutoArray's public subplot defaults. Share the recipe through generated content or focused consistency checks as appropriate.
- `docs/colab/cosmos_web_ring_colab.py`: replace both full dataset subplots; use appropriate brightness normalization for Image and PSF and independently meaningful noise/SNR scales; improve F150W/F444W comparison; add a small editable colormap/contrast example and Ask Gemini prompt. Numerical fitting/data preparation remains unchanged.
- `docs/colab/make_colab_figures.py`, generated notebook and relevant `docs/images/` figures: update first-party renders affected by the new style. Keep externally sourced RGB/paper images and attribution intact. Preview assets must use the feature branch where required, not stale main URLs.
- `autoassistant/tests/`: verify four image panels (excluding colorbar axes), readable handling of masks/negative values, caller-selected colormap/contrast, notebook/source consistency and context size. Regenerate generated skill discovery surfaces only if needed.
- Render before/after comparisons and execute the notebook in a compatible isolated Python environment. Current shell is Python 3.10 with no Astropy; PyAuto stack requires >=3.12. `uv` is available. Do not claim hosted Colab UI validation from local notebook execution.
- Deliver local review copies under `C:\Users\Jammy\Workspace\Science\scratch\cosmos_web_ring_intro_visuals\` and a feature-branch Colab link. Human inspects the lens/ring visibility, four-panel layout, customization interaction and notebook conversation flow.

## Survey and boundaries

2026-10-29: Heart entry GREEN. `autolens_assistant` main is clean at 7e1b80f; no remaining claim after compact-colab-setup closeout. Proposed branch `feature/cosmos-web-ring-intro-visuals`; worktree inside this workspace at `.worktrees/cosmos-web-ring-intro-visuals/`.

The existing `cosmos_web_ring_guided_walkthrough_p2_greeting.md` backlog task owns the broader no-search greeting redesign and benchmark changes; this task does not absorb that scope. Preserve its future work and note the visual recipe dependency when shipping.

No implementation edits or new issue yet; explicit plan approval required by workspace AGENTS.md.
