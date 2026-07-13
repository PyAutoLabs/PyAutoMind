# PyAutoReduce: post-phase-3 consolidation refactor (whole project)

Type: refactor
Target: PyAutoReduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Three instrument phases (ACS, WFC3, NIRCam) landed in two days; consolidate
the accumulated structure debt across the whole repo, behaviour-preserving:

- `pipeline.reduce_target` has grown to ~200 lines with backend branches —
  decompose into per-stage functions with an explicit stage context, keeping
  the provenance record layout byte-identical.
- The three integration scripts (`reduce_slacs0008.py`, `reduce_j0252_wfc3.py`,
  `reduce_cosmos_web_ring.py`) triplicate sub-pixel registration + parity
  statistics — extract one shared validation module.
- `drizzle/combine.py` and `drizzle/jwst_combine.py` duplicate the
  chdir/resolve discipline and the provenance-fragment assembly (R, weight
  uniformity, exposure lists) — extract shared helpers.
- Known review deferral: `psf/stars.reject_crowded` is O(N²) — vectorize with
  identical selection results (same output for the same input is the
  invariant; this is structure, not optimisation).
- Import placement and small smells accumulated by the fast phases
  (function-local imports that can hoist without dependency cost, the
  `exptime` coercion in pipeline, EPSFStars import site).

Out of scope (behaviour-visible, not refactor): `_fwhm_of` diagnostic upgrade
(changes reduction.json values), any dial default changes, tier-2 PSF.

Witnesses: the 83-test unit suite (numpy/astropy-only, runs per commit);
plus offline cached re-runs of `slacs0008-0004` (ACS path) and the F444W
ring band (JWST path) as end-to-end behaviour witnesses — provenance records
and products must be identical up to timestamps/software-version stamps.
