Three loose ends left standing by `howto-stale-self-location`
(`complete/2026/09/howto-stale-self-location.md`), cleared 2026-09-14. No issue:
each was a known, recorded piece of debt from that close-out rather than new
intent.

**Merged:** HowToLens#84, PyAutoHands#282. Also landed: HowToFit `ac0fd0d` on
another session's branch (see below).

## 1. The hand-patched page, replaced (HowToLens#84)

`markdown/chapter_1_introduction/tutorial_0_visualization.md` shipped in #82
hand-patched: a worktree render had leaked
`~/Code/PyAutoLabs/PyAutoArray/.../convolver.py:1478` and the line was corrected
by hand. Content was right; the file was not byte-identical to generator output,
so the next worktree render would have reintroduced the leak.

Regenerated rather than repaired, once PyAutoHands#281 landed. The warning block
is gone from the page entirely, so the hand-patched line no longer exists rather
than merely being correct. Zero `/home/`, `~/Code` or `PyAutoLabs-wt` hits.

## 2. A false positive that broke a real build (PyAutoHands#282)

**The guard shipped in #281 failed the markdown build for
`tutorial_0_visualization` in both HowToLens and HowToGalaxy.** It flagged

    # workspace_path = "/Users/.../<repo>"

— the commented example every `tutorial_0_visualization` shows the reader, with
prose directly above it saying it is commented out so they do not use it. The
guard could not tell authored teaching material from a leaked runtime path.

`check_no_local_paths()` now takes the script being rendered and exempts any path
present verbatim in it: **only paths the execution introduced can be leaks.** The
exemption is per-path, not per-page, so a genuine leak on a page that also carries
an authored path still fails. Two regression tests, the second asserting exactly
that. 460 pass.

**Found by rendering a real page, not by a test.** #281 shipped with 12 green
tests that exercised the redaction roots thoroughly — and every one of them fed
the guard synthetic page text. None rendered an actual tutorial, and the shape
that broke it exists only in real content. Had #281 merged and the session
stopped there, the next person to rebuild either repo's tutorial 0 would have hit
a failing build with no obvious cause.

The failure mode was the right one, though: a guard that fails loudly got caught
the first time it met real content, where the behaviour it replaced — silently
publishing a contributor's directory layout — had gone unnoticed indefinitely.

## 3. The Mind drift

`emcee-log-prob-alignment` (PyAutoFit#1628, another session's live task) was
registered in `active.md` with its prompt still in `draft/`, so the registry
implied a path that did not exist and `lifecycle check` reported DRIFT. `git mv`
+ repointed the `prompt:` line; check now OK. State only — nothing about that
task was touched.

## Also landed: HowToFit (not merged here)

`ac0fd0d` pushed to `feature/howtofit-tutorials-1-3` (HowToFit#58, another
session's open PR), regenerating `markdown/chapter_1_introduction/tutorial_1_models.md`
so the published mirror stops sending a reader who wants HowToFit to
`autofit_workspace`.

Landed on that branch rather than its own because on HowToFit `main` **both** the
`.py` and the `.md` are still stale: a branch off main would have duplicated
#58's fix and conflicted with it. #58 is that session's to merge.
`draft/docs/howtofit/markdown_mirror_missed_by_url_fix.md` therefore **stays
open** and is repointed at the commit rather than retired — the fix exists but has
not reached `main`.

## Note

HowToLens was again taken as a parallel worktree over the residual
`model-figures-rollout-lens` claim, on the same evidence as the parent task: this
branch touched one generated chapter-1 page; that branch touched chapter 2 and 4
scripts and notebooks.
