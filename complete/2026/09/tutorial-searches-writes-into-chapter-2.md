Shipped inside `howto-stale-self-location` (HowToLens#82, commit `e3d240c`,
merged 2026-09-14) rather than as its own task, on the human's instruction to
fold the follow-ups in.

`scripts/chapter_optional/tutorial_searches.py` defined four searches; three
wrote their results to `output/howtolens/chapter_2/` instead of
`chapter_optional/`, apparently copy-pasted from whichever chapter 2 tutorial
they were adapted from. A reader working through the optional chapter found most
of its results filed under chapter 2.

Found while fixing stale post-split paths in the same file. Deliberately not
fixed in that first pass — it is a behavioural change to where files are
written, not prose — then folded in when the human asked for the follow-ups.

The four print strings naming those paths moved in the same commit. They had been
corrected earlier on the same branch to match the code as it stood, so changing
the `path_prefix` values without them would have re-broken what the branch had
just fixed. Post-edit, zero `chapter_2` output paths remain in the file; the four
surviving mentions are prose references to chapter 2 as a chapter.

See `complete/2026/09/howto-stale-self-location.md`.
