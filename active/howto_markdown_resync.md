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
