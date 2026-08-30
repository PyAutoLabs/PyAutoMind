# Extend the catalogue: COOLEST CSV, mass-model FITS products, and a retroactive-update feasibility verdict

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoLens
- PyAutoGalaxy
Themes:
- euclid
- catalogue
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: euclid-dr1-prep
Phase: 7
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28

Phase 7 of 10 in the Euclid DR1 preparation epic. **Gate: phase 4** (needs a catalogue to
extend). Phase 6b informs the magnification layer.

User request (verbatim):

"""
7) Extend the catalogue: Make sure the COolest results (look up recent work implemeting this) are available as a dediciated
.csv file, in the .fits files we need a mass model one which includes convergence, potential, deflections x and y, magnification
but assess whether the file size of tehse is large and thus if we should compress a bit by only doing deflections to derive them
with autolens code... one to think about. We are going to retroactively add these to the 10 lenses we fitted, and the ability
to update the catalgoue of lens models retroactively is quite valuable, but not something I want huge amount of source code
to maintain. So do some assessment on whether there are already functionality or ways to do it via catalgoue scritps,
or doing large reruns on the HPC, bt if theres no simple elegent solution then dont worry about it. It feels like
we would either need somehting whcih scraps output and adds manually or something which reruns and updates output,
 nothing is elegent.
"""

## COOLEST — the recent work to build on (surveyed 2026-08-28)

COOLEST interop is already implemented; do not reinvent it. The existing surface:

- `PyAutoGalaxy/autogalaxy/interop/coolest/` — `mass.py`, `light.py`, `conventions.py`
- `PyAutoLens/autolens/interop/coolest.py`
- Tests: `PyAutoGalaxy/test_autogalaxy/interop/test_coolest_mass.py`,
  `test_coolest_light.py`, `test_coolest_conventions.py`;
  `PyAutoLens/test_autolens/interop/test_coolest.py`
- Worked example: `autolens_workspace/scripts/guides/coolest_interop.py`
  (notebook sibling under `notebooks/guides/`)

Task: emit COOLEST results as a **dedicated `.csv` per lens** in the catalogue tile
directory, alongside the existing `lens_mass.csv` / `lens_sersic.csv` /
`source_sersic.csv` / `magnitudes.csv`.

## Mass-model FITS — with a size assessment, not a foregone conclusion

The request wants a mass-model FITS carrying **convergence, potential, deflections x,
deflections y, magnification**. It also flags the obvious tension: five 2D maps per lens
× 15,000 lenses is a lot of bytes.

So this is an assessment, and it must produce numbers before a decision:

- Measure the actual per-lens size of the full five-plane product at the catalogue's grid
  resolution, and extrapolate to 15,000 lenses.
- Measure the **deflections-only** alternative (2 planes), from which convergence,
  potential and magnification are derivable with autolens code. Quantify what deriving
  costs at read time, and whether all four derived quantities really are recoverable from
  deflections alone at acceptable accuracy (potential in particular — check before
  asserting it).
- Consider FITS compression and dtype (float32 vs float64) as a middle path; a
  half-precision decision is cheaper than an architecture decision.
- Then recommend. "Store all five" is a legitimate answer if the numbers say so.

Note that the reference tile already ships a `model.fits` — check what it contains before
adding a second FITS product, and prefer extending it over creating a parallel file.

## Retroactive update — explicitly allowed to conclude "don't build it"

The 10 lenses from phase 4 need these products added *after* the fact. The user's own
framing is that neither available route is elegant: scrape existing output and add
manually, or rerun on the HPC and update output.

The deliverable is an **assessment**, in this order:

1. Does existing functionality already do this? Check the catalogue scripts
   (`Science/euclid/catalogue/scripts/` has `build_inspect.py`,
   `collect_*_fits.py` collectors, `deduplicate_deblending_fits.py` — the collector
   pattern is the closest existing thing) and the PyAutoFit aggregator/database, which is
   built precisely for deriving new quantities from stored samples without refitting.
2. If not, is there a small, low-maintenance addition that does?
3. If neither: **say so and stop.** The request is explicit — "if theres no simple
   elegent solution then dont worry about it". A written verdict with the options priced
   is a complete, shippable deliverable. Do not build a large maintenance burden here.

Whatever the verdict, the 10 phase-4 lenses still get their COOLEST CSV and mass-model
FITS, even if by a one-off script that is not promoted to permanent infrastructure.

## Deliverables

1. COOLEST `.csv` emitted per lens by the catalogue scripts, using the existing interop.
2. Mass-model FITS product (full or deflections-only per the assessment), with the size
   numbers written down and the choice justified.
3. The 10 phase-4 lenses retroactively carry both.
4. A written feasibility verdict on retroactive catalogue updates at DR1 scale, with
   "no elegant solution — not built" as an acceptable outcome.

## Acceptance / gate

- COOLEST CSV and mass-model FITS present for all 10 prelim lenses.
- The size assessment has real measured numbers and an extrapolation to 15,000 lenses.
- The retroactive-update question has an explicit recommendation, whichever way it falls.
- Magnification maps in the FITS product should carry phase 6b's trust caveat if that
  phase found the estimates unreliable.
