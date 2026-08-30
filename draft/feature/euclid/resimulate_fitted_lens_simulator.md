# simulator.py: resimulate a fitted Euclid lens, and resimulate the 10 prelim lenses with true magnifications recorded

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoLens
Themes:
- euclid
- simulation
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Epic: euclid-dr1-prep
Phase: 5
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28

Phase 5 of 10 in the Euclid DR1 preparation epic. **Gate: phase 4** (needs the 10 real
fits as truth inputs). **Gates phases 6a and 6b.**

User request (verbatim):

"""
5) Simulations! I now want us to be able to take a Euclid lens we have a result for and resimulate it so that we can fit
the simulated data and test if PyAutoLens recovers the correct values. This should result in a simulator.py example
script in "euclid_strong_lens_modeling_pipeline" which basically allows any user to do this, i.e. once ive fitted a
lens resimulate it. However, the resimulation of the 10 lenses we fit should be in the euclid_dr1_prelim project,
and it should make sure the magnification of these simulated lens is recorded as one of the follow up tasks is to
figure out if the magnifications recovered by PyAutoLens are accurate or not. These simulations should use Sersic lens
light profiles, Sersic sources (will be overly simple in some cases but thats fine). For the real lenses, many inferred Sersic lens models
hit the prior edge and infer sersic_index=5. In fact, I suspect this will happen itn he fits to these 10, so when you
resimulate if the lens light Sersic is at the prior edge of 5 lower is to a value between 2 and 4.
"""

## Two artefacts, two homes

- **`simulator.py` in `euclid_strong_lens_modeling_pipeline`** — a general, documented
  example: *"I have fitted a lens; resimulate it."* Any user, any fit result. This is the
  **same** `simulator.py` phase 2 committed its datasets from — **it now exists**
  (`scripts/simulator.py`, shipped 2026-08-29 in
  `complete/2026/08/euclid-ci-test-mode.md`, PR #46) with a `--from-result` mode
  already in place, though its SED is flat for now. Extend that script; do not write
  a second one.
- **The 10 resimulations in `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim`** — the actual
  simulated datasets built from phase 4's results. These are science outputs and live in
  the science project, not in the public repo.

## Simulation recipe

- **Sersic lens light**, **Sersic source**. Deliberately simple — over-simple for some
  of the 10, and that is explicitly fine. The point of 6a/6b is to test recovery under a
  *matched* model first.
- **Record the true magnification** of every simulated lens, as a first-class output
  stored alongside the dataset. Phase 6b's entire question depends on having a ground
  truth here, so this is not optional and must not be reconstructible-only-by-rerunning.
  Record enough to distinguish the magnification definitions in play (point vs area) —
  phase 6c may show these disagree.
- **Prior-edge correction:** many real fits pin `sersic_index = 5` at the prior edge.
  When a lens's inferred lens-light Sersic index is at that edge, **lower it to a value
  in [2, 4]** for the simulation. Record both the inferred and the simulated value per
  lens, so 6a can ask "was the real lens genuinely at the edge, or was that an artefact?"
  Decide and document the rule for *choosing* the replacement value (a fixed 3.0? drawn?
  matched to the population median?) — 6a's interpretation depends on it.
- Match the real data's PSF, noise and exposure characteristics, since 6a's hypothesis is
  that a dodgy PSF model drives the prior-edge pile-up. If the simulation is to be free
  of that defect, be explicit about *which* aspect is idealised and which is faithful —
  otherwise the comparison cannot be interpreted.

## Deliverables

1. `scripts/simulator.py` in the pipeline repo, documented, TEST-mode-clean, in
   `smoke_tests.txt`, taking a fit result and emitting a Euclid-format simulated dataset.
2. 10 simulated datasets in `euclid_dr1_prelim`, one per phase-4 lens.
3. A truth table per lens: mass parameters, lens-light Sersic index (inferred and
   simulated), source parameters, and true magnification(s).

## Acceptance / gate

- A user with a fit result can resimulate it in one command.
- All 10 resimulations exist with recorded truths, including magnifications.
- The prior-edge rule is applied and both values recorded per lens.
- Gates 6a and 6b.
