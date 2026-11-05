## What shipped
PyAutoBrain#591 (commit 2df373d): intake's `Memory:` line now requires *distinctive* query terms (whole-word on ≤5% of Memory pages, idf-weighted) summing to min(9.0, 0.15 × distinct terms); navigation pages (index, log, AGENTS, README, reading-queue) are never cited. Calibrated over all 276 drafts against the live 158-page digest: 67 drafts keep a line, all on methods/concepts pages. Witness tests `test_vocabulary_only_overlap_gets_no_memory_line`, `test_distinctive_terms_still_get_memory_line`, `test_navigation_pages_are_never_cited`.

## What the filed scope missed
Trade-off accepted by the human 2026-11-05: a one-line subhalo idea and the vmap/nautilus recompile bug lose arguably-right citations.

## Follow-ups
Per-domain floor tuning, if lost citations matter in practice.

## Original prompt

# Intake injects `Memory:` citations that match on vocabulary only — add…

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-11-05
Consequence: glance
Witness: a test classifies a library-targeted tooling prompt (e.g. "write compile_repeats from the jax_compile tooling") against a fixture digest whose only overlap is generic words ("model", "profile", "fit") and asserts no `Memory:` line is written, while a prompt naming a digest page's distinctive terms still gets one; `pytest PyAutoBrain/tests -q` green.
Review-minutes: 3
Unattended: ready

The organ-target gate shipped (557f8e0 / #561), but the second half of the original suggestion —
"skip PyAutoMemory citation … when the best digest score is below a floor" — never did. On
2026-11-05 intake wrote `Memory: wiki/galaxies/sources/massive-ellipticals.md; reading-queue.md;
wiki/lensing/sources/dark-matter-substructure.md` onto an autolens_profiling tooling prompt and a
similar line onto a PyAutoFit EP regression-test prompt; both were removed by hand, as earlier
sessions did on 2026-11-03. Add a score floor in `memory_citations()` / `_with_memory`
(`agents/conductors/intake/_intake.py`), calibrated on a few real prompts, and keep "no hits → no
line". `reading-queue.md` as a citation is a smell on its own (it is an index, not a source).

<!-- formalised by the Intake (Conception) Agent on 2026-11-05 from file:/tmp/claude-0/-home-user/ad8c6486-73f7-504b-b742-a7b629366ade/scratchpad/intake/f_memory_floor.md -->
