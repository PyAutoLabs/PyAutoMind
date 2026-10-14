# `@PyAutoFit` A5 (consumers): generate rosters, tiers and anchors from the pinned search manifest

Type: refactor
Target: autofit
Repos:
- PyAutoHands
- PyAutoBrain
- PyAutoNerves
- autofit_assistant
- autolens_assistant
- autogalaxy_assistant
- autofit_workspace
- autolens_workspace
- autogalaxy_workspace
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: A5-consumers
Blocked-by: search-ext-a5-library (PyAutoFit, `search_ext_a5_library_run_ctx_migrations.md`) merged and released
Witness: `python -m autofit search-manifest --json` pinned to the installed `autofit.__version__` regenerates every roster block byte-identically (`--check` mode in each consumer); the Hands navigator `--roster` mode writes the fenced roster block in the curated `llms.txt`; the af/al/ag assistants' roster blocks regenerate from the same manifest; Brain's SamplerSurface keys tiers by registry class; workspace CI checks the registry `example`/`integration_test` anchors against the pinned version, not `main`; al/ag `guides/modeling` search guidance collapses onto domain advice plus a matrix link; the capability matrix links each row to its B3 catalogue card.
Review-minutes: 30
Unattended: needs-slicing
Filed: 2026-10-14

Authority: epic report "#### A5" consumer bullets (D18: consumers generate from the versioned manifest pinned to the installed version), `search_extensibility_epic_surveys/03_search_docs.md` "Phase 3 — consumers generate". Library half: `search_ext_a5_library_run_ctx_migrations.md`. Survey the actual consumer file names first (the report's `guides/modeling/searches.py` path does not exist in the current workspaces; find the live equivalents and the Brain samplers faculty surface) and record them in the plan. One PR per repo; Hands and Brain first (generators), then the assistants and workspaces.
