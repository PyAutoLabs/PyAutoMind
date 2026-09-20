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
