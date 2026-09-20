## wide-sersic-default
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/96
- completed: 2026-09-20
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/97
- summary: Set the lens-light Sersic index prior in `scripts/sersic_lens_model.py` to `UniformPrior(0.5, 10.0)`, matching the experiments' `wide_n` variant. The source-light prior, global Sersic configuration, and output tag remain unchanged. PR #97 merged as `5c5c0b0`. The matching `euclid_dr1` science-clone script was committed locally as `c7ac145`; its unrelated science ledger and run data were preserved.
- validation: Both scripts compile and the installed-model probe confirms lens 0.5–10.0 and source 0.8–5.0. Repository invariants 12/12 and Euclid smoke 9/9 passed; formal branch review was CLEAN. Both GitHub Actions workflows passed, including unit, slow, and smoke jobs on Python 3.12 and 3.13.
- release: PR carried the `pending-release` label. Heart release validation remained RED (`stage integrate`) with YELLOW manifest drift; the user explicitly authorized the task-specific development override, then invoked `/prm` after CI passed to authorize merge and closeout. This is not a release of the pipeline or libraries.

## Original prompt

# Wider lens Sersic index prior as the default for DR1

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Status: active
Issued: 2026-09-20

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
