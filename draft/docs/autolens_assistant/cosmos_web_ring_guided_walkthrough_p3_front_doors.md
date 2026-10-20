# COSMOS-Web Ring walkthrough — phase 3: HowToLens schematic + one opening story everywhere

**Work type:** docs · **Targets:** `lens/HowToLens`, `lens/autolens_assistant` (README,
`docs/setup/first_prompts.md`), hand-off for jamesnightingale.net (outside the workspace) ·
**Consequence:** judge
**Epic:** [`cosmos_web_ring_guided_walkthrough.md`](cosmos_web_ring_guided_walkthrough.md).
Depends on phases 1–2.

## Scope

1. **HowToLens** `scripts/chapter_1_introduction/tutorial_2_ray_tracing.py` (+ regenerated
   notebook/markdown): replace the region-blocked `https://i.imgur.com/zB6tIdI.jpg` with the
   vendored schematic (copy into HowToLens's own image folder or reference the assistant's
   raw URL — follow whatever HowToLens does for its other figures) and add the rays→ring
   bridge sentence. Check tutorial 1 for the same link.
2. **autolens_assistant README + `docs/setup/first_prompts.md`:** open with the schematic
   before the RGB/arrows image, state "no fit needed; the agent fits only if you ask" and frame the agent as an alternative to
   the notebook ("If you prefer…"), not two routes (see the epic's "Phase 1 outcome"); fix the
   `first_prompts.md` sentence that says the notebook fits on a Colab GPU; keep
   the starting prompt byte-identical (phase 1 test).
3. **Website hand-off:** write `docs/archive/website_cosmos_web_ring_section.md` with the
   section text, image order (schematic → RGB), captions/credits and the Colab link (release
   tag) for the human to paste into jamesnightingale.net; confirm the site's prompt matches.

## Done when

HowToLens tutorial 2 shows the vendored schematic; README/first_prompts open with it; website
hand-off file written; PRs open (HowToLens, autolens_assistant).
