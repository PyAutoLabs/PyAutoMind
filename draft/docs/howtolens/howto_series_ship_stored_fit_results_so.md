# HowTo series: ship stored fit results so notebooks run without sampling waits

Type: docs
Target: HowToLens
Repos:
- PyAutoFit
- HowToFit
- HowToGalaxy
- HowToLens
Difficulty: too-large
Autonomy: supervised
Priority: normal
Memory: wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/massive-ellipticals.md; wiki/galaxies/sources/cosmos-survey.md
Status: formalised
Consequence: glance
Witness: running every HowToLens tutorial that calls search.fit with a clean checkout logs "Fit Already Completed: skipping non-linear search" for each search (zero searches sample), and the tracked stored-results footprint is reported in MB.
Review-minutes: 3
Unattended: needs-slicing

Human idea (2026-11-01). Make HowToLens (then HowToFit, HowToGalaxy, other HowTo series) ship stored, lightweight fit results that PyAutoFit loads instantly, so readers complete notebooks uninterrupted.

## Intent
- Every tutorial that runs a non-linear search (HowToLens: 14 scripts — chapter_2_lens_modeling tutorials 1–7, chapter_4_scaling_up_lensing tutorials 1–6, chapter_optional/tutorial_searches) loads a pre-computed result when the reader runs the cell; no sampling wait.
- Tutorials say clearly that this is intentional, and show the real run time that produced each stored result (keep search.summary / timing so readers see what the fit actually cost).
- The FIRST fit (ch2 tutorial 1) may ship its full output folder, for illustration of a real output directory; later fits use the lightweight store.
- Only a few cells and comments per tutorial change.

## Survey already done (2026-11-01, read-only)
- PyAutoFit already skips the search when a fit is complete: `NonLinearSearch.fit` -> `paths.is_complete` (`.completed` file or a zip holding one) -> `result_via_completed_fit` (fit/PyAutoFit/autofit/non_linear/search/abstract_search.py ~L330, ~L513), which needs only `files/samples_summary.json` (via `paths.load_samples_summary`); full `samples.csv` is OPTIONAL (`FileNotFoundError` -> `samples=None`).
- So option (b) — PyAutoFit as-is, ship minimal `<output>/<path_prefix>/<name>/<identifier>/` folders with `.completed` + `files/samples_summary.json` (+ model.json/search.json) — looks viable without a library change.
- HowToLens `.gitignore` ignores `output/` wholesale; shipped results need a dedicated tracked location or un-ignore rule.

## Open questions / risks for the plan
1. Identifier fragility: the output folder is keyed by a hash of model + search settings (unique_tag); any prior/default-config/library change moves the hash and the stored result silently stops matching (fit reruns). Need a regeneration script + a CI/Heart staleness check (fail if a tutorial would actually sample).
2. Which tutorials use `result.samples` (corner plots, PDFs, errors from full samples — e.g. ch2 tutorial 7 results)? Those need samples.csv shipped, or rewriting to use samples_summary only. Measure on-disk size.
3. `pre_fit_output` still runs (visualize_before_fit etc.) on a completed fit — check cost; consider whether output mode should skip it.
4. Option (a) fallback: a PyAutoFit "bare-bones result from disk" API (small json -> Result) only if (b) is too fragile or too big. Prefer (b).
5. Where timing lives: samples_summary/search.summary already record time? Confirm and surface it in tutorial text.
6. Colab/notebook path: stored results must be present in the Colab bootstrap clone too.

## Suggested phasing
- P1 research: per-tutorial survey — files needed, sizes, samples.csv dependence, identifier stability across a release; decide (a) vs (b).
- P2 (only if (a)): PyAutoFit library change.
- P3 HowToLens chapter 2 rollout (generator script, stored results, tutorial prose + run-time display, staleness check).
- P4 HowToLens chapter 4 + optional.
- P5 other HowTo series (HowToFit, HowToGalaxy).

<!-- formalised by the Intake (Conception) Agent on 2026-11-01 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5ee98b5f-b187-4b0a-83a9-3ad898ce13b8/scratchpad/howto_stored_results.md -->
