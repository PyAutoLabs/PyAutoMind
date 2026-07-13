# Expand autofit_workspace latent-variables tutorial coverage

## Context

Parent epic: [`PyAutoPrompt/z_features/latent_refactor.md`](../z_features/latent_refactor.md).

The autolens and autogalaxy workspace tutorials (sub-prompts #5, #6) want to lean on autofit-level foundational explanation of what latent variables are. Audit what `autofit_workspace` already has and fill gaps so those tutorials can link out for foundational context rather than re-explaining from scratch.

## Task

1. **Audit existing autofit_workspace latent docs.** Find every script/notebook that touches latent variables — the toy example at `PyAutoFit/autofit/example/analysis.py:37` (`LATENT_KEYS`) plus any workspace counterpart. Report which of the following are well-explained and which are gaps:
   - What is a latent variable in the Bayesian sense?
   - How does PyAutoFit compute latents (`compute_latent_samples` — every-sample mode vs N-draws-from-posterior mode)?
   - What does `latent/samples.csv` contain? `latent/latent_summary.json`?
   - How does the user load latent results from a completed search and use them downstream?
   - What does "error on a latent" mean — i.e. how is the 1σ/3σ propagation done?
   - How do posterior draws of latents work (sampling vs analytic transform)?

2. **Fill the gaps** by either expanding an existing tutorial (preferred) or adding one new dedicated tutorial in `autofit_workspace/scripts/searches/results/` (or wherever the latent results loading examples live).

3. **Cross-reference target:** the new tutorial in sub-prompt #5 (autogalaxy_workspace) and sub-prompt #6 (autolens_workspace) will link to whatever this task produces, so the URL/path should be stable.

## Where to look

- `PyAutoFit/autofit/example/analysis.py` — the canonical `LATENT_KEYS` + `compute_latent_variables` example.
- `PyAutoFit/autofit/non_linear/analysis/analysis.py:170-305` — the actual `compute_latent_samples` machinery (every-sample vs N-draws, JAX vmap path).
- `PyAutoFit/autofit/non_linear/paths/directory.py:262-340` — `save_latent_samples` / `load_latent_samples`.
- `PyAutoFit/autofit/non_linear/paths/abstract.py:442-485` — `_latent_variables_file` path.
- `autofit_workspace/scripts/` — existing tutorial structure to match.

## Verification

```bash
source ~/Code/PyAutoLabs-wt/<task-name>/activate.sh
cd autofit_workspace
# Run the new/expanded tutorial scripts to confirm they execute clean
python scripts/<path-to-tutorial>.py

# Smoke test
/smoke_test
```

Manual review: the tutorial reads coherently as a foundational explanation. A reader who knows Bayesian fitting but has never seen PyAutoFit's latent API should be able to follow it cold.

## Affected repos

- autofit_workspace (primary)
- PyAutoFit (only if the audit finds the source docstrings on `compute_latent_samples` are themselves the gap — in which case a small library doc edit may be in-scope; the new yaml-driven on/off lives downstream in autolens/autogalaxy, not here)

## Suggested branch

`feature/latent-tutorial-autofit`

## Notes

- Per CLAUDE.md model split: tutorial prose → **Opus**. Per memory `feedback_tutorial_prose_opus`, do not delegate the prose drafting to Sonnet.
- The audit step might reveal the docs are already complete and this task collapses to a tiny linking exercise. That's fine — file the audit findings in the issue comments and ship a minimal change.
- This sub-prompt does **not** touch latent calculations themselves — those are PyAutoLens/PyAutoGalaxy work in #1 and #2. This is pure documentation/tutorial.
