# Wider lens Sersic index prior as the default for DR1

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Status: draft

User request (verbatim, 2026-09-20):

"""
For euclid_dr1, can you make sure that the sersic_lens_model.py script uses the wider Sersic priors from these experiments, and this will be our default setup from now on, so do the same for euclid_strong_lens_modeling_pipeline with a quick PR or whatever.
"""

The experiment's `wide_n` variant sets only the lens-light Sersic index to
`UniformPrior(0.5, 10.0)`; the source-light Sersic keeps its configured prior.
Apply that default in the DR1 science clone and the shared pipeline script.
Keep the existing output naming unless explicitly changed in the approved plan.

## Proposed plan

1. In the `euclid_dr1` science clone, set only the lens-light
   `lens_bulge.sersic_index` in `scripts/sersic_lens_model.py` to
   `af.UniformPrior(lower_limit=0.5, upper_limit=10.0)`, matching `wide_n`.
   Commit only this script on its current `main`; preserve its existing science
   ledger changes, run data, and untracked files.
2. Make the same script edit in a dedicated
   `euclid_strong_lens_modeling_pipeline` worktree on
   `feature/wide-sersic-default`. Keep the source-light prior and global
   Sersic YAML unchanged. Keep `unique_tag="sersic_lens_model"` so catalogue
   consumers retain their path; PyAutoFit's search identifier includes the
   model, so the changed prior gets a distinct result hash.
3. Verify both scripts compile and inspect the constructed lens prior bounds;
   run the pipeline's relevant fast invariants. Review the exact diff, then
   open a focused pipeline PR. The science clone has no separate PyAutoLabs
   remote, so its local commit is reported separately.

Branch survey (2026-09-20): pipeline canonical checkout is clean on `main`;
its Sersic task worktrees and Mind claims are retired. `euclid_dr1` is on
`main`, 20 commits ahead of pipeline `origin/main`, with an existing modified
science ledger and untracked run data. This plan touches only its clean script.
