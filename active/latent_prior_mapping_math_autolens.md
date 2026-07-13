# Investigate prior → latent transform math (uniform → log10, etc.)

## Context

Parent epic: [`PyAutoPrompt/z_features/latent_refactor.md`](../z_features/latent_refactor.md).
**Research stub — small-scope by design.** This is a deliberately scoped investigation, not a committed implementation.

The parent prompt closes with:

> "Finally, is there some fancy or complicated math we should do when the priors or distributions of parameters to latent variables gets a bit complicated? e.g. mapping a uniform thing to a log10 thing?"

Concrete instance: a model parameter has a `UniformPrior` over linear units (say, `intensity ∈ [0, 10]`), but the scientific latent of interest is `log10(intensity)`. A naive `compute_latent_variables` just emits `log10(intensity)` per sample — but the **error bars** on the latent in `latent_summary.json` are then computed from the per-sample log10 values, which is fine for the median but can subtly misrepresent the Bayesian credible interval if the original prior was uniform and the user expected log-space prior behaviour. There may be other cases too (uniform → 1/x, Gaussian → exp, etc.).

This task is to **investigate whether anything actually needs doing** beyond the per-sample transform that's already implicit in `compute_latent_variables`, and to write up findings.

## Task

1. **Survey the issue.** Specifically:
   - Walk through `PyAutoFit/autofit/non_linear/analysis/analysis.py:170-305` (`compute_latent_samples`) and verify what mode produces error bars: per-sample transform (full posterior of the latent), vs delta-method propagation from the prior, vs something else.
   - List 3-5 concrete prior → latent transforms that arise naturally in PyAutoLens / PyAutoGalaxy fits (`log10(M*)`, `magnification = f(ellip, gamma)`, etc.).
   - For each, is the current "compute per sample then summarise" approach scientifically correct? In what edge case would it not be?

2. **Decide if a library change is warranted.**
   - If the per-sample approach is always correct (most likely outcome): write a short note in the autolens/autogalaxy latent module docstring explaining why, and close this task with no code change.
   - If there's a real gap: propose (don't implement) an API extension — e.g. a `transform: str` field per latent in `config/latent.yaml`, with `log10` / `exp` / `delta_method` options. Sketch what the user would write.

3. **Output** a short markdown summary as a follow-up issue comment + (optionally) a new sub-prompt in `PyAutoPrompt/autolens/` if a follow-up implementation is genuinely warranted.

## Where to look

- `PyAutoFit/autofit/non_linear/analysis/analysis.py:170-305` — `compute_latent_samples` machinery.
- `PyAutoFit/autofit/non_linear/samples/` — how samples are summarised into median + 1σ/3σ.
- `PyAutoFit/autofit/example/analysis.py:37` — toy `LATENT_KEYS = ["gaussian.fwhm"]` for a concrete instance of "transform of a parameter".
- Once shipped: `autolens/config/latent.yaml` and `autogalaxy/config/latent.yaml` — the natural place to attach transform metadata if needed.

## Verification

This is an investigation, so verification is qualitative:
- The summary clearly answers "is anything broken?" with yes/no + a reason.
- If "no": one paragraph added to the latent module docstring suffices.
- If "yes": a new sub-prompt is filed in `PyAutoPrompt/` with a clear, scoped follow-up task.

## Affected repos

- PyAutoLens (potentially — if a config-level change is needed)
- PyAutoGalaxy (potentially)
- PyAutoFit (very unlikely)
- None at all (most likely — investigation lands as docstring only)

## Suggested branch

`feature/latent-prior-mapping-investigation`

## Notes

- **Do not implement a transform mechanism speculatively.** The whole point of this stub is to find out whether it's needed. If a future user reports the bias, that's the moment to act.
- Single conversation, no multi-step plan. Expected effort: a few hours of reading + a couple of paragraphs of writing.
- Per CLAUDE.md model split: investigation + light prose → **Opus** is fine; if it collapses to "no change needed", the touch is trivial enough either way.
