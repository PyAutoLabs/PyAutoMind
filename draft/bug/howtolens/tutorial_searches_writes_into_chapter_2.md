# HowToLens chapter_optional/tutorial_searches.py scatters 3 of its 4 results into chapter_2/

Type: bug
Target: howtolens
Repos:
- HowToLens
Themes:
- howto
- tutorials
Difficulty: trivial
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Witness: All four searches in `scripts/chapter_optional/tutorial_searches.py` write under `output/howtolens/chapter_optional/`, and the four `print` strings naming those paths match the code.
Review-minutes: 10
Unattended: ready
Filed: 2026-09-14

`scripts/chapter_optional/tutorial_searches.py` defines four non-linear searches.
One writes where it should; the other three write into a different chapter's
output folder:

- L135 — `path_prefix=Path("howtolens") / "chapter_optional"`  ← correct
- L168 — `path_prefix=Path("howtolens") / "chapter_2"`
- L267 — `path_prefix=Path("howtolens") / "chapter_2"`
- L288 — `path_prefix=Path("howtolens") / "chapter_2"`

A `chapter_optional` script depositing three of its four results in
`output/howtolens/chapter_2/` looks like a copy-paste slip from whichever
chapter-2 tutorial these searches were adapted from. The effect is that a reader
working through the optional chapter finds most of its results filed under
chapter 2.

## Scope

Decide whether the three `chapter_2` prefixes are the bug (most likely) or
deliberate, then make all four consistent.

**If the code is corrected, the prose must move with it.** The four `print`
strings at L146, L177, L275 and L296 name these output paths explicitly. They
were corrected on 2026-09-14 under `howto-stale-self-location`
(issue HowToGalaxy#75) to match the code *as it stands today* — so they are
currently truthful, and a code fix without a prose fix would re-break them:

- L146 → `output/howtolens/chapter_optional/tutorial_searches_slow`
- L177 → `output/howtolens/chapter_2/tutorial_searches_fast`
- L275 → `output/howtolens/chapter_2/tutorial_searches_zeus`
- L296 → `output/howtolens/chapter_2/tutorial_searches_emcee`

Remember the notebook twin: edit `scripts/` only, then regenerate with
`PYTHONPATH=../PyAutoHands/autohands python3 ../PyAutoHands/autohands/generate.py howtolens`.

## Provenance

Found while fixing stale post-split documentation paths under
`howto-stale-self-location` (2026-09-14). Deliberately not fixed there: that task
was scoped to prose, and this is a behavioural change to where files are written.
