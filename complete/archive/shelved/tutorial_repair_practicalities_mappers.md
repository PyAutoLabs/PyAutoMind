# HowToLens broken tutorials: tutorial_2_practicalities + tutorial_2_mappers (parked NEEDS_FIX)

Type: bug
Target: howtolens
Repos:
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Two HowToLens-specific tutorial breakages (2026-07-20 sweep), unrelated to the just-merged
should_simulate migration (#39):
- `chapter_2_lens_modeling/tutorial_2_practicalities` — `NameError: 'af' not defined`; the tutorial
  is missing ~80 lines of imports + setup (a truncated/incomplete script). Restore the missing head.
- `chapter_4_pixelizations/tutorial_2_mappers` — `ValueError: zero-size array reduction, empty mapper
  array` (empty mapper under test-mode small grids; may need a full-data override OR a real fix).

Remove each NEEDS_FIX from HowToLens/config/build/no_run.yaml once green. Only edit scripts/, then
regenerate notebooks. tutorial_2_practicalities is likely a quick restore; tutorial_2_mappers may
relate to the pixelization/mapper clusters.
