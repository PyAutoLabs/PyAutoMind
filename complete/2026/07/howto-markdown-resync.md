## howto-markdown-resync
- issue: https://github.com/PyAutoLabs/HowToLens/issues/28 (closed)
- completed: 2026-07-11
- prs: HowToLens#29 (ab01aaca) + HowToFit#17 (e738b085) + HowToGalaxy#20 (442db308) — all MERGED 2026-07-11
- summary: re-synced 4 stale HowTo ch1 markdown pages after the truncation-restore work merged post-batch-2b. HowToLens tutorial_1+tutorial_2 re-rendered from restored scripts (were truncated → now full, 16+14 imgs); HowToFit tutorial_5 re-render; HowToGalaxy tutorial_4_methods dropped (stub). markdown/+1 config entry only, no scripts/CI. Calibration merged-unchanged.

- issue: https://github.com/PyAutoLabs/HowToLens/issues/26 (CLOSED)
- prs: HowToLens#27 + HowToGalaxy#19 + HowToFit#16 — all MERGED 2026-07-11 (docs-only, library-free)
- completed: 2026-07-11
- summary: /intake → --auto supervised. HowToLens ch1 tutorial_1/tutorial_2 were cut off mid-docstring — an LLM output-token cutoff during the workspace bootstrap (frozen at the truncated length since commit #1, original source gone). Restored tutorial_1 (429→672, log10+Galaxies+Units+WrapUp adapted from the complete 654-line HowToGalaxy sibling) and tutorial_2 (214→391, ray-tracing grids/images/Galaxies/Tracer/Mappings/WrapUp from guides/tracer.py). These two were the ONLY genuine truncations across all three HowTo repos. Prevention: .github/scripts/check_tutorials_complete.py + a `tutorials-complete` CI job in all 3 repos requiring every non-stub tutorial to reach a terminal __Wrap Up__/__Summary__ section (a truncation never does). Also filled HowToGalaxy's empty tutorial_4_methods (0 bytes since bootstrap → not-written stub) + normalized 12 complete-but-unmarked tutorials across the 3 repos. Smoke 6/6 + 4/4 + 10/10; all CI green incl the new check. Heart YELLOW (6 ambient reasons) acked in-session at each ship; merges human-approved. Worktree + branches cleaned. Traps in [[project_howto_truncation_restore]] (linter must live in .github/scripts not scripts/, else notebook-gen converts it; revert dataset/ before staging; single-backslash LaTeX in docstrings).

## Original prompt

# Re-sync HowTo markdown pages after tutorial truncation-restore

Type: docs
Target: workspaces
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Follow-up to the markdown-renderings rollout ([[markdown-example-renderings]])
and the HowTo truncation-restore work ([[project_howto_truncation_restore]]).
The restore landed AFTER batch-2b rendered the chapter_1 pages, so 4 generated
markdown pages are stale (rendered from truncated/empty scripts):
- HowToLens tutorial_1_grids_and_galaxies (restored 429→672) — re-render
- HowToLens tutorial_2_ray_tracing (restored 214→391) — re-render
- HowToFit tutorial_5_results_and_samples (normalized) — re-render
- HowToGalaxy tutorial_4_methods (was 0-byte → now a "not written yet" stub) —
  DROP from markdown_examples.yaml (no content/images to show; re-add when the
  real tutorial is authored)

Regenerate markdown/ only (no scripts/ edits, no CI touch). Verify 0 path
leaks, index links resolve, no embedded errors, restored tutorials execute.
Ship 1 pending-release PR per repo behind the four-leg gate.
