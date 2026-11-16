## website-lensing-intro
- issue: https://github.com/Jammy2211/Jammy2211.github.io/issues/1 (CLOSED)
- pr: https://github.com/Jammy2211/Jammy2211.github.io/pull/2 (MERGED 2026-11-12, merge 7c04658, head d91cd2f)
- completed: 2026-11-12
- closed-out: 2026-11-15 by a health-review session — the human merged PR #2 and the issue closed, but the active.md entry stayed, failing PyAutoMind Registry Reconcile daily (2026-11-13 → 2026-11-15).
- scope: personal static website, outside the organism registry; no release involvement.
- summary:
  - Added the approved three-sentence strong-lensing introduction with the autolens_assistant 2D schematic before the COSMOS-Web Ring example in `index.html` and `natural_language/draft.md` (main contains the copy in both).
- left over: the dev-box checkout `/home/jammy/Code/PyAutoLabs/scratch/website-lensing-intro` and the remote branch `feature/website-lensing-intro` (already merged) remain — repo-cleanup, not deleted here.

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
