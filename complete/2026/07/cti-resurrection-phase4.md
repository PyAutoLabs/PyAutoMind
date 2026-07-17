- issue: https://github.com/PyAutoLabs/autocti_workspace/issues/1 (closed)
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/90 (merged first)
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/2 (merged 87da42b)
- summary: CTI resurrection Phase 4 — autocti_workspace (118 scripts) onto the current stack. Plot function API replaces the removed Plotter/MatPlot object stack everywhere (scripts/plot/ rewritten as function-API tutorials mirroring autolens guides/plot); analysis summing → af.AnalysisFactor/af.FactorGraphModel across all multi-dataset fits; simulator kwarg + fitsable I/O + priors limits: config sync; new visualize config schema (stale mat_wrap/include deleted); AGENTS.md/CLAUDE.md added; .gitignore modernized (previously ignored almost nothing — the mechanical ship agent's binary-leak pre-flight caught 5000+ output files, root cause fixed). Database tutorials were genuinely broken beyond drift and repaired: hard-coded output/ scrape paths → with_test_mode_segment(conf.instance.output_path), per-type scrape scoping (1D loader was ingesting 2D-format fits), Aggregator.from_directory (ctor lost directory=), 1D region names driven at 2D data, FPA diagnostics grid 6x6 → the simulator's 2x2. Validation: EVERY script run (overview 6/6, plot tree 20/20, modeling/chaining/results/database all pass; TM2 ordered-assertion artifact documented, TM1 counterparts pass).
- library-companions (PyAutoCTI#90, from validation): visualize_combined quick_update kwarg + per-factor instance zip + region_list_from(instance[0]); Result.analysis_unwrapped (factor child results carry AnalysisFactor whose __getattr__ forwards to the PRIOR MODEL, not the wrapped analysis); fpr_mask_from None-region guards + ArrayException guard for trimmed datasets; *_list empty-input ValueError; ImagingCI check_noise_map threading + loader check_noise_map=False. Suite 271/271.
- traps: PYAUTOFIT_TEST_MODE is a NO-OP — the knob is PYAUTO_TEST_MODE (my cookbook propagated the wrong var; sub-agents self-corrected; one false-pass hid overview_6's stale sum(analysis_list) until an honest rerun). A factor-graph global instance carries the FactorGraphModel itself as a trailing child. TM2 bypass ties ordered-trap assertions at prior medians (autofit bug prompt filed: draft/bug/autofit/test_mode_bypass_ordered_assertion_ties.md). The workspace-side API gate resolves aplt.* against autolens — bypass for autocti scripts. Sub-agents spawning their own children stall silently — resume them with "finish yourself".
- heart: shipped + merged through the same pre-existing CTI-unrelated RED reasons on human ack 2026-07-17 ("Ship + merge + Phase 5").
- epic-next: Phase 5 (final) — autocti_workspace_test rebuild (preserve Euclid tvac/temporal heritage), smoke wiring, Build/Heart registration, notebook regeneration, first modern autocti release.

## Original prompt

# CTI resurrection — Phase 4: autocti_workspace update

Type: feature
Target: autocti_workspace
Repos:
- @autocti_workspace
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Phase 4 of the CTI resurrection epic (Phases 0-3 merged: PyAutoCTI #83/#85/#87/#89
+ Heart#87 + Brain#135). Bring autocti_workspace (118 scripts / 79 notebooks;
last updated 2024-11) onto the current library APIs.

## Scope

1. **Plot API migration** (70 scripts reference the old API): the deleted
   `aplt.*Plotter` / `MatPlot*` / `Output` / `Title` object stack → the Phase-1
   matplotlib function API (`aplt.subplot_*`, `figure_*`, `output_path=` /
   `output_format=` kwargs). The `scripts/plot/` tutorials are rewritten as
   function-API tutorials; other sections' plotting calls converted in place.
2. **Library API drift**: `add_poisson_noise` → `add_poisson_noise_to_data`,
   instance `.output_to_fits` → `autoconf.fitsable`, prior-config
   `gaussian_limits` → `limits`, multi-dataset `analysis + analysis` →
   `af.AnalysisFactor`/`af.FactorGraphModel`, dataset output format notes.
3. **Configs**: sync `config/visualize.yaml` plots schema (new keys), priors
   yaml `limits:` rename, general.yaml version keys; mirror new library
   defaults per workspace-config convention.
4. **Validation**: run a representative subset per section under
   `PYAUTOFIT_TEST_MODE=1` (arcticpy installed); fix fallout.
5. **Notebooks**: regenerated from scripts by the PyAutoBuild pipeline at
   release (Phase 5) — not hand-edited here beyond deleting stale ones if the
   generator requires it.

## Conventions

Tutorial narrative prose is preserved; only code cells and prose that names
the old API change. Judgment-tier session edits the prose-bearing overview +
plot tutorials; mechanical per-directory conversions may be delegated with a
strict cookbook.
