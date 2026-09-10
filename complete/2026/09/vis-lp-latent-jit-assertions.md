## vis-lp-latent-jit-assertions
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/732
- completed: 2026-09-10
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/734 (merged)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1600 (merged)
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/734
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1600
- repos:
  - PyAutoLens
  - PyAutoFit

## Summary

The prompt's hypothesis — one latent NaN on every sample drops all twelve — was
disproved by the engine as it ran on RAL: `latent_samples_from` already drops an
all-NaN column and greedily salvages anti-correlated NaNs (latent-class-redesign,
2026-06), so "no finite latent samples remained" can only mean every latent was NaN
on every sample. Reproduced on the euclid pipeline's committed simulated dataset with
`use_jax=True`: `LatentLens.variables` / `LatentEuclid.variables` build the instance
with `model.instance_from_vector(vector=parameters)`, whose default assertion check
applies a Python `not` to a traced boolean inside the engine's per-sample `jax.jit`.
The `vis_lp` model gained an ordering assertion on its two MGE bases on 2026-09-08
(`order_bases=True`, PyAutoFit#1583), so every sample raised
`TracerBoolConversionError`; `_safe_jitted` swallowed each raise into a NaN row and
the block vanished. `vis_pix` runs on NumPy with no assertion, which is why it was fine.

- PyAutoLens#734: `latent_instance_from(model, parameters, xp)` — NumPy path
  unchanged (assertions checked, violation → `FitException` → NaN row dropped);
  under JAX `ignore_assertions=True, xp=xp`, exactly as `Fitness` does.
  `LatentLens.variables` uses it; subclasses that build their own instance are told
  to. Tests: helper on both backends (default path shown to raise under jit), and
  `LatentLens.variables` end to end under `jax.jit` with a model assertion.
- PyAutoFit#1600: the engine counts the per-sample failures and keeps the first
  traceback; warns "raised on N of M samples" with it, and names the every-sample
  case ("the latent function is broken for this model") instead of the generic
  masking line. Masking unchanged.

## Traps

- The engine's `_safe_jitted` / `_safe_compute` swallow *any* exception into a NaN
  row. Before #1600 a latent function that could not be traced left no trace at
  all; read the new warning before blaming the mask.
- A second, independent trace failure lives in the pipeline: the uniform
  source-flux grid (`al.Grid2D.from_mask(..., xp=jnp)` inside the jit,
  `jnp.nonzero` needs a static size). Both pipeline sites are the follow-up
  `draft/bug/euclid/vis_lp_latent_euclid_jit_trace.md`; with both changes
  `jax.jit(LatentEuclid.variables)` returns all 12 latents finite and equal to the
  eager values (measured in-session on `dataset/simulated/euclid_dr1_like`).
- The witness (tile 102005065 `latent_summary.json` populated) needs the pipeline
  follow-up merged and the RAL libraries refreshed before a `vis_lp` rerun; this
  record covers the library half only.

## Notes

- Shipped from a web-github session (session clones, no task worktree; issue and
  PRs driven through the GitHub MCP surface). Heart not installed there: the gate
  was the two full suites (PyAutoLens 621 passed; PyAutoFit 2539 passed on the
  branch merged with main) plus CI green on every run and leg of both PRs.
- The first Mind ledger push conflicted with concurrent ledger merges on
  `dashboard.md`/`dashboard.html`; merging main and regenerating fixed it.

## Original prompt

# MGE lens-light stage writes no latent output: one non-finite latent drops all twelve

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: the `vis_lp` search of `euclid_dr1_prelim` tile 102005065 (342398 dataset and config) writes `files/latent/latent_summary.json` with every finite latent populated, and a unit test shows a latent that is NaN on every sample no longer suppresses the other latents.
Review-minutes: 20
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-10

## Symptom

In PyAutoLens latent output, the MGE lens-light stage (`initial_lens_model` `vis_lp` in the euclid
pipeline) writes no latent output at all. All ten dr1_prelim `initial_lens_model/vis_lp` results
of RAL job 342398 have no `files/latent/latent_summary.json` and no `latent.results`; `search.log`
says

    compute_latent_samples: no finite latent samples remained after masking; skipping latent output.

`latent_samples_from` masks globally, so one latent that is non-finite on every sample drops all
twelve latents for the search; the `vis_pix` stage of the same tiles is fine (12 keys, all
populated).

## Do

1. Diagnose which latent is non-finite for the two-basis MGE model and why (aperture-flux latents
   on a `Basis` of linear Gaussians? `effective_einstein_radius` on the `vis_lp` mass?).
2. Decide whether the global NaN mask should sacrifice the offending latent and keep the rest
   instead of dropping the whole block.

## Why it matters

Any producer pointed at `vis_lp` (`lens_mass.py --search_name=vis_lp` is a supported flag) gets
silently blank latent columns for this reason, unrelated to the retired `latent.` prefix bug, and
the SED chain seeds `sersic_lens_model` from `vis_lp`, so this needs a verdict before the
`euclid_dr1_prelim` SED fits are trusted.

Related: `complete/2026/09/catalogue-latent-prefix-blank.md` (the retired `latent.` prefix
this is distinct from) and `complete/2026/09/aggregate-csv-latent-sigma3.md` (shipped 2026-09-10, PyAutoFit#1598) (the
silent-None path that hides both).
