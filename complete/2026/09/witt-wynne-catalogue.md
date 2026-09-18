## witt-wynne-catalogue
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/84 (closed 2026-09-17)
- completed: 2026-09-17
- workspace-pr: euclid_strong_lens_modeling_pipeline#86 (merged cf66194 -> main; branch head e86f34d, 7 commits)
- sibling: witt-wynne-guide-fixes (autolens_workspace#552 / PR #553, merged 59051af1 — same review, guide ported from this module)
- heart-ack: 2026-09-17 — human "I authorize,"; reasons verbatim "install verification FAILED (testpypi; checks F)"; "release validation FAILED (stage integrate)" — unrelated to this branch; merged on the human's `/prm` with 9/9 CI legs green (Tests unit+slow ×2 pythons, Smoke Tests ×2, changes gates).
- origin: Paul Schechter's request to project Euclid PyAutoLens models onto Witt–Wynne space for `isit4or2or1` (Schechter, Lu & Hernández 2026; Zenodo 10.5281/zenodo.20086659, CC-BY-4.0); the guide shipped 2026-08-28 (complete/2026/08/witt-wynne-projection.md), an independent numerical review on 2026-09-17 (#84 first comment) found it sound in conventions but unsafe for catalogue use.
- what shipped: `catalogue/scripts/witt_wynne_util.py` (canonical pure-numpy SIEP quartic solver + caustic-matched and vector-sum projections + `.in`/CSV writers, with the review fixes: root filter by lens-equation residual so the 1-image verdict fires — 450/450 vs a brute-force oracle out to 4× the caustic; NaN row + `n_images=-1` sentinel for on-axis/centre/e∉(0,1)/sub-critical/vector-sum-cancellation; mass profile picked by class, lens plane only, so an MGE light `Basis` is never the mass; `z_lens < z_source` validated); `catalogue/scripts/witt_wynne.py` producer (`--sample/--output_path/--inspect_dir/--unique_tag/--search_name/--z_lens/--z_source/--projection/--caustic_pixel_scale`; per lens max-logL `initial_lens_model/vis_pix` tracer via `al.agg.TracerAgg`, source centre from `wcs.json` or recomputed via `util.pixelized_source_clumps_from` when the keys predate 2026-09-12, zero-centred `inspect/<sample>/<lens>/witt_wynne.in` + `inspect/<sample>/witt_wynne.csv` row: b, e, PA E of N, source offset, source_rule, 4/3/2/1 verdict, positions, magnifications, lags, D_ol/D_ls/h, placeholder-redshift provenance; skip-and-continue incl. the `StopIteration` from an empty aggregator query that would have aborted the bundle); bundle stage 7 of 10 in `scripts/build_inspection_bundle.sh`; `config/build/no_run.yaml` entries; `docs/witt_wynne.md`; README / `scripts/README.md` / `catalogue/README.md` / `docs/drift_report.md` wiring (10 stages, 21 bundle files); tests `tests/test_witt_wynne_util.py` (25) + `tests/test_witt_wynne.py` (18); 196 fast tests green at merge.
- merge of #85 (astrometric_offsets, landed after the branch was cut): `git merge-tree` reported 0 conflicts but the real merge had 4 (bundle script + three READMEs, all the stage-numbering collision); resolved as unions then renumbered — witt_wynne stays 7, astrometric_offsets is 10; stale pre-mass-maps stage numbers in five other producer docstrings corrected in the same PR.
- validation: ten real DR1-prelim tiles — 10/10 rows, 0 aborts, 3.45 s/lens, PointSolver verdict agreement 9/10 (the miss says 2 where the full model gives 4), positions 10–40 % of b, vector-sum differs from caustic-matching by 15–84° in PA on 6/10 (Euclid shear ≈ mass ellipticity) so caustic-matching is the default. Q1 end-to-end (deliverable 5): the committed `q1_walsmley/102018665` lens fitted on RAL A100 job 343391 (46 min: vis_lp 14m50s + vis_pix 30m08s, JAX GPU), producer + full 10-stage bundle exit 0, b 0.848″ e 0.063 PA 56.2° verdict 2 = PointSolver 2, positions median 0.26″ (0.31 b), source outside the caustic (#84 comment 5716899052). Q1 fit + inspect products preserved in the canonical checkout's gitignored `output/q1_walsmley` and `inspect/q1_walsmley`.
- deliverable 6 (science clone): pipeline main (cf66194) merged into `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim` (merge c96bdfb, clean; the clone carries 12 unpushed science commits by ruling), `witt_wynne.py --sample=dr1_prelim_grade_ab` → `inspect/dr1_prelim_grade_ab/witt_wynne.csv` 10/10 rows byte-identical to the scratch run (md5 471b5fb1…), 9 two-image + 1 four-image (Tile102007299); PointSolver miss = Tile102007903 (SIEP 2 vs full model 4). Cortex ledger `result` line written to `PyAutoCortex/projects/euclid_dr1_prelim.md` (agent-worded, flagged "human to confirm wording"); note `cortex.py log` writes `<root>/projects/<key>.md`, not the `ledger:` path in projects.yaml.
- email (deliverable 7): draft + the Q1 `witt_wynne.in`, CSV row and report staged at `PyAutoLabs/tmp/witt_wynne_q1_email/` for the human to send (install line `pip install "autolens[coolest]"`, accuracy figures match `docs/witt_wynne.md`).
- traps: the auto-mode classifier denies a bundled push+PR delegation and any Bash chaining a file write with a `gh` write — one write per call; RAL submit needs `--export=ALL,PROJECT_PATH=…,PYAUTO_HPC_BASE=/mnt/ral/jnightin/PyAuto` (first attempt with `/mnt/ral/jnightin` died in 2 s with a misleading "JAX cannot see a GPU"); `hpc/sync.conf` is gitignored so task worktrees lack it; a local JAX-CPU `vis_pix` (no pool) ran >3 h with no Nautilus checkpoint and died with the session — use the GPU submit for one-off real fits.
- follow-ups: `draft/refactor/autolens/witt_wynne_solver_library_home.md` (solver into PyAutoLens once both copies settle); compiled Zenodo C++ round-trip never re-run since the fixes; per-lens redshifts (placeholders 0.5/1.0 make lags fiducial); the shipped Q1 bundle prints three "empty aggregator" skips (stages 2/5/6 need `sersic_lens_model`); several producers on main incl. #85's `astrometric_offsets.py` are not black-clean (nothing gates on it).

## Original prompt

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
