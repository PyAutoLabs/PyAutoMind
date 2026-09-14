Closed by HowToFit#58 reaching `main` 2026-09-14.

The bug: `scripts/chapter_1_introduction/tutorial_1_models.py` told a reader who
wanted to clone **HowToFit** to download `autofit_workspace` — a leftover from
before the HowTo series was split out of the workspace repos. It was the
user-reported symptom that opened the whole `howto-stale-self-location` line of
work.

`6f335b2` on `feature/howtofit-tutorials-1-3` fixed it in `scripts/` and
`notebooks/` but not `markdown/`, because `markdown/` is built by
`generate_markdown.py` over a curated list — a different tool from the
`generate.py` that builds `notebooks/`, and one the documented regeneration step
never runs. So the published mirror kept sending readers to the wrong repo.

Regenerated as `ac0fd0d`, pushed onto that same branch rather than a branch of
its own: on `main` **both** the `.py` and the `.md` were stale, so a branch off
main would have duplicated #58's fix and conflicted with it.

`main` now reads `https://github.com/PyAutoLabs/HowToFit`.

The root cause — the two-tool split that let the mirror go stale unnoticed —
is recorded in `complete/2026/09/howto-stale-self-location.md` and
`complete/2026/09/howto-md-rerender.md`. It is still a live trap for anyone
editing a curated script in any HowTo repo.
