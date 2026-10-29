# Clear COSMOS-Web Ring figures for assistant newcomers

Type: feature
Target: autolens_assistant
Consequence: judge
Issued: 2026-10-29
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/168

Primary: @autolens_assistant. Assistant-specific presentation; retain existing library/workspace diagnostic defaults.

## Original request (verbatim)

Use the COSMOS-Web ring to improe the colormap and color scheme to make it so the lens and source are both visisble,
the images of this for the starting autolens assistant stuff are crap.

For the autolens assistant and times when a user is new or being introduced to lensing, the dataset image should
only have 4 panels (image, noise map, signal to noise map, PSF) and we should avoid having over sampling information
displayed. I think things like over sampling and introduced ok in workspace tutorials so its really just
having a less information dense image for new users using the AI assistant.

Basically, my feeling is that for autolens assistant users the cosmos web ring example is their entry point to PYAutoLens, and its quite under whelming how basic the cosmos web ring in built autolens visualization looks, and that its got panels that confuse a reader. So I think we should make them clear and better and perhaps include a task or feature which prompts them to customize and change visualization with a suggest for now. Do this task and then have me run and inspect the paired Colab Notebook so I can see how the assistant structure of conversation and images look.

## Approved plan

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

User explicitly approved this plan on 2026-10-29. Single assistant presentation task; no public library API change. Brain keyword sizing overestimated scope by treating references to existing library APIs as proposed changes.

## Implementation checkpoint — 2026-10-29

- Approved scope implemented in `.worktrees/cosmos-web-ring-intro-visuals/autolens_assistant`, branch `feature/cosmos-web-ring-intro-visuals`, based on 7e1b80f; source changes not yet committed.
- Assistant-owned `autoassistant/intro_plots.py` supplies four panels, asinh brightness stretch (0.01), truthful colorbars and explicit excluded-pixel display. The converter embeds this helper into standalone Colab and folds its setup cell.
- Greeting, preparation and style guidance updated; notebook adds editable colormap/contrast and a Gemini prompt. Generated figures/notebook rebuilt and executed with Python 3.12 + packaged PyAutoLens 2026.10.26.1. Existing numerical preparation preserved.
- Validation: 24 focused tests passed, 1 existing expected failure; all notebook cells executed; API gate passes; Gemini contexts 70 + default pass cap check. Fit score 3717.19 matches recorded reference. Logs: task root `validation.log`, `notebook-build.log`, `api-check.log`, `readiness.json`.
- Build uses a snapshot of merged PyAutoHands 16dec73 because the canonical checkout predates the compact-Colab generator. No Hands source modified.
- Human review bundle: `/mnt/c/Users/Jammy/Workspace/Science/scratch/cosmos_web_ring_intro_visuals/` (`comparison.html`, `walkthrough.html`, portable `cosmos_web_ring_colab.ipynb` with embedded illustrations). Hosted Colab/Gemini remains untested.
- Ship gate RED: PyAutoArray: 4 uncommitted source change(s); PyAutoGalaxy: 9 commit(s) behind origin; PyAutoLens: 7 commit(s) behind origin. Additional stale reasons: release validation incomplete: no rehearsal for current source; release push credential check stale (pyautolabs-bot, 49h old).
- Asked the human for a development-only override for issue #168 after surfacing exact reasons and passing evidence. Await response before commit/push/PR. No merge or release authorized. If authorized, record the override in all four sinks; publish branch and create/attach PR; provide the hosted Colab link (make new static illustration URLs accessible at the branch/immutable commit).

## Published checkpoint — 2026-10-29

- Human authorized development-only shipping: "Authorize development-only shipping for #168". Recorded on issue, PR, active registry and autonomy log. No merge/release authorization.
- PR: https://github.com/PyAutoLabs/autolens_assistant/pull/169; head ad6dce151e52f20e094f3a5846e132bd49580a91. Worktree clean; branch pushed.
- New static images are pinned to immutable commit 96e49bac7edd75670067d0e077184c2480a56637 so pre-merge Colab can show them. The notebook was regenerated and executed after pinning; validation again 24 passed, 1 existing expected failure (`publish-validation.log`, `publish-notebook-build.log`).
- Run/review: https://colab.research.google.com/github/PyAutoLabs/autolens_assistant/blob/ad6dce151e52f20e094f3a5846e132bd49580a91/docs/colab/cosmos_web_ring_colab.ipynb
- Next: human inspects hosted Colab and Gemini flow, then requests any refinements or /prm.
