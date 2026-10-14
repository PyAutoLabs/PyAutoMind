# Image dropdown contrast

Issue: https://github.com/PyAutoLabs/PyAutoEyes/issues/29
PR: https://github.com/PyAutoLabs/PyAutoEyes/pull/30
Merged: 2026-10-14
Merge commit: 965397c9f9fcbdc05f5f685e2c9d1dc9e563a051

## Delivered

The image selector and options use dark charcoal (#1f2937) on white, with a light native colour scheme. Updated eyes/board.py and regenerated dashboard.html. The scope was fully delivered.

## Validation

87 tests passed; Ruff lint and formatting passed; live board check passed 265 image URLs, manifests and state. Independent committed review CLEAN at 0a642a8. All CI steps on the exact PR head passed. Browser rendering was not verified.

## Authorization

Plan approved, then launched with `go --auto`. Human replied “I authorize” to the development-only Heart RED override for this task. RED reason: `PyAutoFit: CI failure`; stale reason: `release validation incomplete: no rehearsal for current source`. The later human `$prm` authorized merge and close-out. No release performed.

## Original prompt

# Darken image dropdown text

@PyAutoEyes

Issued: 2026-10-14
Issue: https://github.com/PyAutoLabs/PyAutoEyes/issues/29
Autonomy: supervised
Difficulty: small

Plan approved; user authorized `go --auto`. Merge remains human /prm.

## Original user request

> On the drop down menu where I select an image the font is light on white and thus hard to read all the images, can we make it darker?

> This is PyAutoEyes

## Scope

Give the figure selector and its option list explicit dark text on a white background in eyes/board.py. Regenerate the dashboard through the board command. Validate existing board tests and formatting. Preserve image selection behavior.
