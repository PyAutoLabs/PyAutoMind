# Witt–Wynne SIEP projection as a catalogue output of the Euclid pipeline

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- catalogue
- point-source
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Review-minutes: 25
Unattended: never
Filed: 2026-09-17
Issued: 2026-09-17

## Original request (verbatim)

> We recently implemented the Witt-Wynne thing (although I now cant find its guide
> in the autolens_workspace). So find all that, do a review that it is definitely
> numerically sound and implement correctly, then make it an output of the
> euclid_strong_lens_modeling_pipeline repo with clear docs and whatnot, and
> prepare me an email to point a colleague to it with one of the example q1 lens
> models in that repo ready to run. Make sure its part of what is built when we
> make the catalogue, and then ensure this all works in the euclid_dr1 project

## Context

- The guide shipped 2026-08-28 as `autolens_workspace/scripts/guides/misc/witt_wynne.py`
  (complete/2026/08/witt-wynne-projection.md, autolens_workspace#511). It ports
  `isit4or2or1` v1.0 (Schechter, Lu & Hernández 2026; Zenodo 10.5281/zenodo.20086659,
  CC-BY-4.0): SIEP quartic solver (positions, magnifications, time lags, 4/2/1
  verdict), `.in` writer, and two projections of a PyAutoLens tracer onto SIEP space
  (caustic-matching and Schechter's literal ellipticity+shear vector sum).
- Independent numerical review 2026-09-17 (session scratch `review/report.md`, to be
  attached to the issue): solver exact to 1e-13 away from the axes; PA map, e
  conversion, shear sign, b-from-profile, `.in` field order and h handling all SOUND;
  time-lag constant 0.12 % low from the C++'s own rounded literals. Findings that
  gate catalogue use: (SEVERE) `_mass_and_shear_from` picks the MGE light `Basis`
  as the mass profile on the exact pipeline model (84° PA error); (high) wrong-branch
  quartic roots are kept so the 1-image verdict never fires; (high) on-axis sources
  return finite wrong positions; (high) vector-sum e collapses to 0 when e_pot = γ
  aligned; unguarded IndexError on a sub-critical lens. Outside the caustic the
  verdict agreement is 51/68 (caustic-matched) vs 22/68 (vector-sum) on a 136-case
  grid, so caustic-matching is the projection to ship.
- The sibling task `draft/feature/autolens_workspace/witt_wynne_guide_fixes.md`
  applies the same fixes to the guide; the solver/projection code is duplicated
  into the pipeline on purpose (the pipeline must not import the workspace, and the
  numerics are not yet stable enough to freeze into PyAutoLens — that is a later
  refactor once both copies agree).
- Pipeline facts (survey 2026-09-17): producers live in `catalogue/scripts/`, chained
  by `scripts/build_inspection_bundle.sh` (8 stages; new producer becomes stage 7 of
  9, before the SED pair); producers are excluded from smoke tests via
  `config/build/no_run.yaml` with a reason; `lens_mass.py` projects
  `initial_lens_model/vis_pix`; no per-lens redshifts exist (placeholders
  z_l=0.5, z_s=1.0); `wcs.json` carries the source centre (`vis_lp`) or
  `source_clumps[0]` peak (`vis_pix`); `catalogue/README.md` states "No producer
  publishes the image positions yet".

## Deliverables

1. `catalogue/scripts/witt_wynne_util.py` — pure-numpy SIEP solver + projection,
   copied from the guide with the review fixes: exclude light `Basis` from the mass
   pick (take `Isothermal`/`PowerLaw` + `ExternalShear` by class), filter quartic roots
   by lens-equation residual, NaN row + `n_images=-1` sentinel for degeneracies
   (min(|p|,|q|)<1e-6, e∉(0,1), empty caustic, None mass), documented (y,x)/(x,y)
   argument conventions. CC-BY-4.0 attribution + citations in the module docstring.
2. `catalogue/scripts/witt_wynne.py` producer (modelled on `lens_mass_maps.py`):
   `--sample/--output_path/--inspect_dir/--unique_tag/--search_name` (default
   `vis_pix`), `--z_lens/--z_source` (defaults 0.5/1.0, recorded in a provenance
   column), `--projection` (default `caustic`, option `vector_sum`). Per lens: max
   log-likelihood tracer via `al.agg.TracerAgg`, source centre from `wcs.json`
   (rule recorded), caustic-matched SIEP → `inspect/<sample>/<lens>/witt_wynne.in`
   (zero-centred, no sky coordinates) and a row in `inspect/<sample>/witt_wynne.csv`
   (b, e, PA_E_of_N, source offset, n_images verdict, predicted image positions,
   magnifications, lags, D_ol, D_ls, z provenance). Skip-and-continue on a lens
   with no usable fit; never abort the bundle.
3. Wire-up: `scripts/build_inspection_bundle.sh` stage + renumbered echoes;
   `config/build/no_run.yaml` entry with reason; `catalogue/README.md` (file table,
   run order, the "No producer publishes the image positions yet" sentence),
   root `README.md` and `scripts/README.md` producer tables (fix the stale
   seven/eight-stage counts), `docs/drift_report.md` producer↔file map, and a new
   `docs/witt_wynne.md` explaining the projection, conventions, the verdict
   agreement numbers from the review, and how a colleague feeds the `.in` to
   `isit4or2or1`.
4. Tests (fast suite, JAX-free): `tests/test_witt_wynne.py` — solver regression
   against the guide's hard-coded `2025wny` rows, degeneracy sentinels, the Basis
   exclusion on an MGE+SIE+shear model, `.in` line order / CSV field order from a
   hand-built model; repo invariants stay green.
5. End-to-end check on the committed Q1 example (`q1_walsmley/102018665_…`): real
   `initial_lens_model.py` fit locally, then `witt_wynne.py --sample=q1_walsmley`
   and the full bundle; the produced `.in` is the attachment for the colleague email.
6. euclid_dr1_prelim: merge pipeline main into the science clone
   (`/mnt/c/Users/Jammy/Science/euclid_dr1_prelim`), run the producer against the
   ten pulled DR1 tiles in `output/dr1_prelim_grade_ab`, report the ten verdicts,
   and note the result in the Cortex ledger (`scripts/cortex.py log`, human's words).
7. Email draft for the colleague (path to the repo, install, the one-lens run, the
   producer command, what the `.in` contains and its conventions, caveats:
   placeholder redshifts, SIEP-without-shear projection, outside-caustic accuracy).
