# Export VIS magnitudes for the Euclid DR1 top-1000 fits

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- catalogue
Status: draft
Issued: 2026-09-20
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/95

User request (verbatim):

"""
For the euclid_dr1 project we haev modeld the 1000 brightest galaxies, with most vis_lp results in, andI think we wee trying to build a catalogue from them and get magnitudes. How is that effort going, is a csv with most magnitudes in VIS feasible?

ok work towards that goal
"""

Goal: produce a reliable, auditable VIS-only CSV for the top-1000 DR1 sample from existing completed fits, without treating the separate multiband SED `magnitudes.csv` as already available. Record all 1,000 input IDs, measured values where defensible, and explicit missing/quality status otherwise. Preserve existing fit outputs; do not launch new modelling jobs without a separate science decision.
