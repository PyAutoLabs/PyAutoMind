# Release validation: check HowTo stored fit results load before a release ships

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoNerves
- HowToFit
- HowToGalaxy
- HowToLens
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: a release rehearsal run whose candidate wheels change a stored chapter 2 fit's identifier (e.g. a deliberately edited default prior) fails Heart's release validation with the HowToLens tutorial and folder named, and an unchanged candidate passes.
Review-minutes: 3
Unattended: ready
Lane: any

Follow-up from HowToLens#130 / PR HowToLens#134 (2026-11-11).

## Why
HowToLens now ships stored fit results for Chapter 2 Tutorials 2-6 (`output/howtolens/chapter_2/`). A tutorial finds its stored result through an identifier hashed from the model and search settings, so a library release that moves a profile class, a default prior or a search default silently sends readers back to tens of minutes of sampling. Colab clones HowToLens at the tag matching the installed release, so the first release containing the stored results is what Colab readers get.

HowToLens's `.github/workflows/stored_results.yml` runs `python .github/scripts/stored_results.py check` (test mode off, refuses to sample) on PRs, `main` and daily, against PyPI. That catches a breaking release only **after** it is published. The release gate should catch it **before**.

## Scope
- Run HowToLens's `stored_results.py check` against the release-candidate wheels inside Heart's release validation (workspace-validation release mode or release-diagnostic), with `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` (jaxlib 0.11.2 deadlock, PyAutoNerves#213) and `MPLBACKEND=Agg`.
- A failure is a release blocker and names the tutorial and expected folder (`check` prints both).
- Design it to extend to HowToFit / HowToGalaxy and HowToLens Chapters 3-4 when those ship stored results (each repo provides its own `check`).
- Runtime: about 1 min locally, about 11 min on a GitHub runner.

## Notes
- Smoke tests run in test mode and never exercise stored results, so the existing workspace-validation smoke leg cannot catch this.
- If a release legitimately changes an identifier, the fix is regenerating the stored results (AGENTS.md "Stored Chapter 2 Results" in HowToLens), not skipping the check.

<!-- formalised by the Intake (Conception) Agent on 2026-11-11 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5ee98b5f-b187-4b0a-83a9-3ad898ce13b8/scratchpad/heart_stored.md -->
