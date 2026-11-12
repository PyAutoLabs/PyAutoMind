# Brief strong-lensing introduction on the personal website

Merged https://github.com/Jammy2211/Jammy2211.github.io/pull/2 on 2026-11-12
at 7c04658f4fa734c15389c1a37245aae142c1ea48, following explicit human merge approval.
Issue: https://github.com/Jammy2211/Jammy2211.github.io/issues/1

Both the homepage and Natural Language & AI page now include the approved short
explanation and the existing assistant schematic before the COSMOS-Web Ring
walkthrough. The image is shared, responsive and has descriptive alternative text.
The Natural Language Markdown source and generated HTML remain synchronized.

Validation: Chromium at 1440px, 390px and 320px on both routes (image load,
aspect ratio and no horizontal overflow); reproducible Pandoc rendering;
byte-identical source image; clean git diff whitespace check. No PR CI is
configured for this personal static site; merge was explicitly authorized.

Previews: /mnt/c/Users/Jammy/Workspace/Science/scratch/website_lensing_intro_2026-11-12/

## Original prompt

# Brief strong-lensing introduction on the personal website

Type: docs
Issued: 2026-11-12
Issue: https://github.com/Jammy2211/Jammy2211.github.io/issues/1
Difficulty: small
Target: Jammy2211/Jammy2211.github.io (personal website, outside organism registry)
Consequence: judge

## Original request

The 2D schematic we made, which is used on the autolens_assistant repo, is not used o my website (front page or natural language) and I think it would be good there as a quick intro to strong lensing, keep it brief but it makes it clearer what I do to the lay person 

## Approved scope

Yes, go ahead and add it to both pages, keeping it brief as proposed.

Reuse autolens_assistant/docs/images/strong_lens_schematic.png in assets/images/.
Add the approved three-sentence introduction before the COSMOS-Web Ring example
in index.html and natural_language/draft.md; regenerate natural_language/index.html.
Use responsive image sizing and descriptive alt text; check desktop/mobile layout,
local image links and reproducible rendering. Open a feature PR; human merges.

Approved copy: A galaxy’s gravity can bend light from a more distant galaxy into
arcs or a ring. This is strong gravitational lensing. I use these distorted images
to measure the matter we cannot see, including dark matter and black holes.

Branch: feature/website-lensing-intro
Checkout: /home/jammy/Code/PyAutoLabs/scratch/website-lensing-intro

## Handoff — 2026-11-12

- Implemented approved copy and shared schematic on both pages.
- PR: https://github.com/Jammy2211/Jammy2211.github.io/pull/2
- Commit: d91cd2f on feature/website-lensing-intro.
- Changed index.html, natural_language/draft.md, generated natural_language/index.html,
  natural_language/page.css, assets/images/strong_lens_schematic.png.
- Chromium passed for both routes at 1440, 390 and 320 px: image load, aspect ratio,
  no horizontal overflow. Desktop/mobile previews visually inspected.
- Pandoc regeneration reproducible; source image byte-identical; diff whitespace clean.
- Preview folder: /mnt/c/Users/Jammy/Workspace/Science/scratch/website_lensing_intro_2026-11-12/
- Personal static website is outside library/workspace runtime release gates.
- Next action: human review and merge PR #2; site is not yet published.
