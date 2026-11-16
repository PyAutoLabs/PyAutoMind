# Polish the homepage flow

Type: docs
Consequence: judge
Target: Jammy2211/Jammy2211.github.io

## Original request

my homepage reads slightly chaotically, lets polish it slightly

## Approval

Yes, go ahead with that polish, keeping it brief and just changing the homepage.

## Approved plan

- Keep the portrait and personal introduction together, followed by the lensing explanation and schematic.
- Move the natural-language introduction below the schematic under “Weigh a galaxy yourself”.
- Introduce the COSMOS-Web Ring before the prompt and attach the credit to its image.
- Trim repeated explanation and rename “More” to “Explore my work”.
- Edit only index.html; check desktop/mobile layout, prompt behavior and preserved links; open a review PR.

Tier: judge — merge mode: human /prm.

Branch: feature/homepage-flow-polish
Checkout: /home/jammy/Code/PyAutoLabs/scratch/website-lensing-intro
Personal static website; outside the organism library/workspace runtime release gates.

Issued: 2026-11-12
Issue: https://github.com/Jammy2211/Jammy2211.github.io/issues/3
PR: https://github.com/Jammy2211/Jammy2211.github.io/pull/4
Commit: d18e80d

Validation: Chromium at 1440, 390, 320px; images loaded, no horizontal overflow, exact clipboard prompt. All content links and prompt preserved; diff check passed.
Next: human review/merge. Only index.html changed.
