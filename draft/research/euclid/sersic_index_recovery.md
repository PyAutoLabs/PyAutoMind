# Do we recover Sersic indices? 10 simulated Euclid lenses vs the real prior-edge pile-up

Type: research
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoLens
- PyAutoGalaxy
Themes:
- euclid
- priors
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: euclid-dr1-prep
Phase: 6
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28

Phase 6a of 10 in the Euclid DR1 preparation epic. **Gate: phase 5.** Runs in parallel
with 6b and 6c. Science, on RAL — human-driven, `supervised`.

User request (verbatim):

"""
6a) Do we recover Sersic indexes accurately on simulated lenses? For the real lenses, many inferred Sersic lens models
hit the prior edge and infer sersic_index=5. Thus, we want to know for these 10 simulated lenses, do we recover
their sersic indexes accurately, and were their real lenses at the prior edge? The expectaiton is that a dodgy PSF model
or other aspects of the lens data are the cause of this issue, whcih the resimulation will not suffer from. Lets get to the
point where we have results for 10 lenses an then we can work out what chanfges we want to make to fix it.
"""

## The question, sharpened

Real Euclid fits pile up at `sersic_index = 5` — the prior's upper edge. Two competing
explanations:

- **Real signal.** These lenses genuinely have high-index light profiles and the prior is
  simply too narrow.
- **Artefact.** A defective PSF model (or another data-side systematic) drives the fit to
  absorb the mismatch into a high Sersic index.

The resimulations from phase 5 are built with indices in [2, 4] and (per phase 5's
recipe) without whatever data defect is suspected. So if the fits to the *simulated* data
recover the input index, the pile-up is an artefact of the real data; if they *also* pile
up at 5, the problem is in the model or the fitting, not the data.

## Deliverables

1. Fit all 10 simulated datasets with the same Sersic lens-model stage used on the real
   data (`sersic_lens_model.py` family), on RAL.
2. Per lens: input index, recovered index, posterior width, and whether the posterior is
   railed against the prior edge. A plot of recovered vs input across the 10.
3. The paired comparison with the **real** fits from phase 4: for each of the 10, was the
   real lens at the prior edge?
   `Science/euclid/catalogue/scripts/plot_lens_sersic_index.py` already exists and plots
   this population — reuse it rather than hand-rolling a new plot.
4. A verdict on which of the two explanations the data supports, and — if artefact — a
   named next step (widen the prior? fix the PSF model? both?). Do **not** implement the
   fix in this phase; the request is explicit that we "get to the point where we have
   results for 10 lenses and then work out what changes we want to make".

## Interpretation hazards to respect

- N = 10 is small. A pile-up in 2 of 10 does not distinguish the hypotheses. Say up front
  what fraction would count as a result.
- If phase 5's replacement index rule was a fixed value, recovery is easier to assess but
  says less about the population. Note which rule was used and what it costs the
  inference.
- The prior edge is at 5 for the *real* fits; confirm the simulated fits use the **same**
  prior, or the comparison is not like-for-like.

## Acceptance / gate

- 10 simulated fits complete, recovered-vs-input table and plot produced.
- The real-lens prior-edge status of the same 10 lenses established from phase 4 output.
- A written verdict naming the likely cause and the recommended change, filed as a
  follow-up prompt if a change is warranted. No fix implemented here.
