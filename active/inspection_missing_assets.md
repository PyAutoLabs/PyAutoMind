# Inspection bundle tolerates missing optional result assets

Issued: 2026-09-22
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/100
Plan-approved: 2026-09-22 (user: go)
Type: bug
Lane: local-dev
Autonomy: human-required
Target: @euclid_strong_lens_modeling_pipeline

## Original request (verbatim)

• Fix the Euclid catalogue inspection-bundle builder so one completed fit with missing optional output assets does not abort the entire sample build.

  Repository/workflow:
  - Work in `/home/jammy/Code/PyAutoLabs`.
  - Use the PyAutoLabs `bug` → `start-dev` workflow and follow all AGENTS.md plan/approval gates.
  - Canonical target is `lens/euclid_strong_lens_modeling_pipeline`.
  - The active science clone is `/mnt/c/Users/Jammy/Science/euclid_dr1`.
  - Do not disturb its existing dirty/untracked science data.

  Observed failure:
  - RAL catalogue job: `350451`
  - Invocation:
    `hpc/sync submit cpu submit_build_inspection_bundle --export=ALL,SAMPLE=dr1_sep1_rest,RUN_TAG=sersic100_20260922,OUTPUT_DIR=output_sed,SED_OUTPUT_DIR=output_sed,CREATE_ARCHIVE=0,DATASET_PREFIX=Tile`
  - SLURM status: `FAILED 1:0`
  - Log:
    `/mnt/c/Users/Jammy/Science/euclid_dr1/hpc/batch_cpu/error/error.350451.err`
  - Failure:
    `FileNotFoundError: No FITS output named 'galaxy_images'`
    from `catalogue/scripts/deblending.py` during `AggregateFITS.extract_fits`.
  - Failing dataset:
    `Tile102006997RA0602279119243DECNEG0663160559050`
  - Its Sersic run completed, but its log reports that the maximum-likelihood sample could not be reconstructed, so fit-dependent outputs such as latent variables, visualization and FITS were skipped.
  - The first two lenses successfully produced valid `pre_psf.fits` and `model.fits`, each with 17 HDUs covering VIS, DECam g/r/i/z and NIR Y/J/H.

  Required behavior:
  1. Treat missing per-result FITS, PNG, WCS or similar optional generated assets as a per-lens/per-result skip, with a clear warning.
  2. Continue processing the rest of the sample and continue to later bundle stages.
  3. Do not hide structural/programming errors unrelated to missing result assets.
  4. Print useful built/skipped/error counts and identify affected lens/band names.
  5. Preserve idempotency.
  6. Audit other bundle producers—especially `multi_wavelength.py`, `magnitudes.py`, and `astrometric_offsets.py`—for the same failure mode.
  7. Add focused regression tests using a completed-result fixture with a missing optional asset.
  8. Run relevant catalogue/unit tests and independent review.
  9. Ship the fix through the normal library/workspace workflow, sync the corrected catalogue tooling to the `euclid_dr1` RAL checkout, and rerun the catalogue job only after I approve the implementation
  plan.
  10. Verify the resulting FITS, CSV and PNG products and report row/file counts plus any skipped lenses.

  Do not reinterpret missing outputs as scientific success, and do not rerun model fits as part of this task.

## Proposed issue / implementation plan — awaiting approval

Title: fix: isolate missing assets in Euclid inspection bundles
Branch: feature/inspection-missing-assets
Workflow: start_dev → start_workspace → ship_workspace; one cohesive bug fix,
followed by deployment and catalogue-only verification. No fitting runs.

### Diagnosis and scope

RAL error.350451.err confirms AggregateFITS.extract_fits raises FileNotFoundError
for galaxy_images outside deblending.py's existing empty-aggregator handler.
multi_wavelength.py likewise extracts outside its handler. magnitudes.py and
astrometric_offsets.py index every WCS value without checking for absent output.
PyAutoFit fits_source correctly raises for absent FITS; the consumer owns the
policy that these generated assets are optional. No library API change planned.
Brain's heuristic reported high/single-repo/test-failure and suggested phases;
inspection refines this to a runtime error with one cohesive producer-policy fix,
then separate deployment/verification phases, not unrelated PRs.

### High-level plan

1. Isolate development from canonical and science changes; register task and survey claims.
2. Skip products/rows missing optional assets, identifying lens, band, result and reason.
3. Preserve valid output, row alignment, ordering, deduplication and idempotency.
4. Audit all ten stages and prove unrelated errors still fail the build.
5. Run focused completed-result regressions, catalogue/unit checks and independent review.
6. Ship through workspace gates, sync only reviewed tooling, rerun the exact catalogue
   invocation, and inventory FITS/CSV/PNG products and skipped results.

### Detailed implementation and acceptance evidence

- catalogue/scripts/catalogue_util.py: small shared helpers for optional-asset
  availability and consistent built/already-present/skipped/error accounting.
  Detect absence at the actual result input boundary; never catch arbitrary
  FileNotFoundError around output writes or broad TypeError/ValueError/Exception.
  Include result identifiers as well as lens/band in warnings. Fatal errors
  retain their traceback and nonzero status; summaries must not call them success.
- deblending.py main: validate/read both FITS inputs before publishing either
  bundle. For a missing required input in a selected band, skip that lens's
  deblending pair and warn with the missing band, preserving complete existing
  pairs. Do not publish a silently reduced-band pair that existence-based
  idempotency would freeze. Stage writes safely so missing model.fits cannot
  leave a newly written pre_psf.fits masquerading as a completed pair.
- multi_wavelength.py main: check the selected subplot asset per result; skip
  the affected lens composite with explicit band diagnostics when unavailable.
  Preserve deterministic ordering and avoid publishing an unlabelled incomplete
  composite. Keep valid repeat runs idempotent.
- magnitudes.py and astrometric_offsets.py main: after existing newest-result
  selection, exclude rows missing required generated WCS/latent assets; derive
  labels and values from exactly the same survivors. No fallback to an older
  scientific result just because it has more files. Preserve existing CSV schemas
  and report unavailable measurements as skips, never fabricated values.
  Missing optional files differ from corrupt files, malformed WCS dictionaries,
  invalid HDUs and model/programming errors, which must remain visible failures.
- Audit lens_mass_maps.py, lens_mass.py, lens_sersic.py, source_sersic.py,
  witt_wynne.py and scripts/tools/build_inspect.py. Tighten relevant broad guards
  (notably has_grid_offset's catch-all) and handle confirmed optional-output gaps
  using the same policy; do not introduce general exception suppression.
- scripts/build_inspection_bundle.sh: retain set -euo pipefail; producer-level
  optional skips return normally so later stages execute. Any edit here is limited
  to useful summary reporting if producer summaries alone prove insufficient.
- tests/test_catalogue_missing_assets.py plus existing catalogue/offset/mass-map
  tests: on-disk completed-result fixture, incomplete result between valid results,
  absent FITS/PNG/WCS/latents, no eligible results, healthy 17-HDU ordering, CSV
  row alignment, pair publication, repeat build and recovery once assets arrive.
  Include corruption/programming/output-write error propagation and later-stage
  execution. Test actual aggregator reads, not only mocks that raise the symptom.
- Update catalogue/README.md with skip/completeness/count semantics. Run focused
  regressions and the fast unit suite; no slow fitting tests or model reruns.
  Independently review the full diff and evidence; resolve findings before ship.
- After approval and validation: compare every changed tooling file with local
  science and RAL versions, preserve local edits and remote configuration, deploy
  only the approved file manifest with checksums (no broad push/reset/clean or
  data transfers), and use existing submit_build_inspection_bundle with the exact
  original exports. Track the submitted catalogue job in this session; no
  persistent polling/automation. If still running when reporting, state that
  verification is pending rather than claiming completion.
- Validate actual output: FITS readability/HDUs/band names, healthy reference pairs,
  CSV row and per-lens counts/duplicates, PNG decoding and dimensions, stage
  completion, and all skipped lenses/bands. Confirm result archives are untouched.

### Survey and current gates

- Canonical pipeline root: /home/jammy/Code/PyAutoLabs/lens/euclid_strong_lens_modeling_pipeline;
  clean main at 5c5c0b0; origin/main at 1c67027 (#99 merged).
- Proposed development branch feature/inspection-missing-assets from origin/main;
  worktree to be created by start_workspace after approval and claim reconciliation.
- Local main Mind registry has no pipeline claim; origin/main retains stale
  euclid-single-rgb-vis-lp awaiting-merge claim. GitHub confirms #99 MERGED at
  2026-09-21T09:21:08Z, merge 1c67027. Reconcile through lifecycle workflow before
  claiming; do not overwrite unrelated dirty main Mind registry changes.
- Science clone main is ahead 21; tracked dirt in .gitignore, util.py and
  wiki/project/state.md plus untracked science data and submit scripts. Read only
  so far. No source/tests/science files edited and no jobs submitted.
- Mind draft is isolated in .task-ledger/inspection-missing-assets on
  codex/inspection-missing-assets; original main checkout dirt preserved.
- Vitals refreshed 2026-09-22T06:19:02Z: RED, exact blocker
  `release validation FAILED (stage integrate)`. Also reports workspace validation
  4 failures and manifest drift 7 mismatches. No prior task override transfers.
  Refresh at ship; if RED persists, present reviewed patch and validation before
  requesting the required development-only override.

Next action: obtain explicit user plan approval, then create_issue and worktree
setup. This record is a proposal, not approval or an implementation claim.


## Paused at user request — 2026-09-22

Plan approved ("go"); user then asked to pause at a good checkpoint while offline.

- Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/inspection-missing-assets/euclid_strong_lens_modeling_pipeline`
- Branch: `feature/inspection-missing-assets`, base `1c67027`; implementation remains local and uncommitted pending the Heart shipping gate.
- Implemented optional-asset checks, product/row skip diagnostics and counts, staged FITS/CSV/PNG writes, stale CSV cleanup, and explicit structural-error propagation across the catalogue producers. Completed-result regressions added in `tests/test_catalogue_missing_assets.py`.
- Validation: 241 passed, 10 fitting tests deselected (`.scratch/unit.log`); 18 new regressions passed (`.scratch/regression.log`), including the real ten-stage shell bundle with missing FITS/PNG/WCS and healthy eight-band 17-HDU output. Ruff and diff checks passed. No model fits rerun.
- Independent Sol review was requested; its final disposition is recorded separately below when available. Brain review surface CLI requires a committed diff and currently returns no reviewable diff; reviewer directly inspects the local diff and test source.
- Code snapshot: `.scratch/implementation.patch`, `.scratch/checkpoint_hashes.json`; new test file is present in worktree but untracked and is NOT included in the ordinary git diff patch.
- Deployment is prepared ONLY in `.scratch/deploy`, with `.scratch/deployment_manifest.json`. Science astrometry predates prior-edge columns, so its staged version ports this fix while preserving the existing schema; verified on the real regression fixture (5 aligned rows). No files copied into science or RAL.
- RAL SSH works. `/mnt/ral/jnightin/euclid_dr1` has no `.git`; deployment must verify preimage file hashes. Existing SED and VIS fits are running; only catalogue tooling may be transferred, never broad sync or config/fitting scripts. No new jobs submitted.
- Heart remains RED: `release validation FAILED (stage integrate)`. Plan approval did not grant a development shipping override. Before commit/push/PR, finish independent review, refresh Heart, present passing tests/review and request a task-specific development override if still RED. Follow four-sink recording. Merge needs separate authorization.
- Resume: resolve review findings, revalidate changed scope, obtain the required shipping gate approval, ship workspace PR, checksum-guard the staged file-only deployment, rerun the exact job exports in the approved plan, verify actual FITS/CSV/PNG products and report counts/skipped lenses. Science dirty/untracked data and existing model results remain untouched.

### Independent review — FINDINGS; resolve before shipping

Reviewer: independent `gpt-5.6-sol`, task `/root/review_missing_assets`, read-only.

1. **HIGH — collector accepts corrupt copied assets.** `scripts/tools/build_inspect.py` copies PNG/JSON bytes and checks existence. Reviewer reproduced `process_dataset` returning `built` after copying `b'not a png'` and `b'not json'`. Validate assets before reporting built; add corruption regression. The documentation's universal corruption-propagation claim is currently false here.
2. **HIGH — stale multi-wavelength PNG on incomplete refresh.** After a valid two-band build, adding a completed `nir_y` result without `fit.png` causes a skip while retaining the old `fit_multi_wavelength.png`. Invalidate/quarantine the stale generated composite when current inputs are incomplete; test that transition.
3. **HIGH — stale Witt-Wynne products.** Empty/skip paths retain old master and per-lens `witt_wynne.csv` and potentially `witt_wynne.in`. Reviewer reproduced stale master/split surviving `built=0 skipped=3`. Clear stale master/splits on empty refresh and skipped-lens `.in`; add regression.

Reviewer verified the staged science deployment's older astrometric schema is preserved and its missing-WCS handling matches the fix. Compilation, lint, manifest hashes passed. Claim dispositions: continuation and row alignment supported by regression evidence; universal corruption propagation and stale-output claims have the findings above. Review is **not CLEAN**. No fixes to these findings were started after the user's pause request. Resume at finding 1, then re-review the corrected patch and deployment overlay.


## Implementation and independent review complete — 2026-09-22

Resolved all three review findings: PNG/JSON collector corruption now fails before publication (including reused output); an incomplete multi-wavelength refresh invalidates its old composite; skipped Witt–Wynne projections clear stale CSV rows/splits and solver inputs.

- Validation: **249 passed, 10 fitting tests deselected** (`.scratch/unit-final.log`); independent reviewer reran all **26** missing-asset regressions. The real ten-stage catalogue shell smoke reaches stage 10 with missing FITS/PNG/WCS in an intermediate lens. Ruff check/format and diff check pass. No model fits rerun.
- Independent Sol re-review: **CLEAN**. Claim dispositions cite collector corruption tests, added-band invalidation, parametrized Witt cleanup, real shell continuation and CSV row alignment. Full record: `.scratch/review-clean.md`.
- Worktree remains `/home/jammy/Code/PyAutoLabs/.worktrees/inspection-missing-assets/euclid_strong_lens_modeling_pipeline`, branch `feature/inspection-missing-assets`, base `1c67027`. Source changes are not committed/pushed yet.
- Ship body prepared at `.scratch/pr-body.md`. Heart refreshed 2026-09-22T07:04:11Z: RED reason **`release validation FAILED (stage integrate)`**. Task-specific development override requested after passing tests/review; pending user response. No override inferred from plan approval or resume.
- Deployment preflight: all **11** scoped files on RAL match recorded local science preimages. `.scratch/deploy` preserves existing science astrometry schema; manifest `.scratch/deployment_manifest.json`. No fitting/config/data files included. No deployment performed.
- Read-only RAL baseline verified: **4 FITS files, each 17 HDUs; 0 CSV, 0 PNG; no validation errors**, in `inspect/dr1_sep1_rest_sersic100_20260922`. Hashes and extensions saved in `.scratch/ral-before-products.json` for post-rerun comparison. Inventory tool: `.scratch/verify_bundle.py`.
- Next: receive issue #100 development override, record it in four required sinks, commit/push/open pending-release PR, checksum-guard file-only deployment, rerun the exact original catalogue job, then verify actual FITS/CSV/PNG counts and skips. Merge requires separate human authorization. No RAL jobs submitted so far.


## Heart development override — issue #100

User authorization (verbatim): "Authorize issue #100 development override".

Current Heart RED reason: `release validation FAILED (stage integrate)`.
Passed branch evidence: 249 fast tests; 10 fitting tests deselected; 26 missing-asset regressions independently rerun; real ten-stage catalogue smoke; Ruff/format/diff checks; independent Sol review CLEAN.

Scope: commit, push, and pending-release PR for issue #100. The user also already approved the file-scoped RAL tooling deployment and catalogue-only rerun. No merge, release, fitting reruns, CI bypass or claim to fix Heart.


## PR opened and catalogue rerun submitted — 2026-09-22

- PR: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/101 (`pending-release`), commit `3e5357da48d5d7e9194cc3c3af29f3d239426ec8`. No merge/release performed.
- User override: "Authorize issue #100 development override", exact Heart RED `release validation FAILED (stage integrate)`; recorded on issue, PR, active registry and autonomy log.
- Deployed 11 reviewed tooling files to science clone and RAL, checking all preimage and replacement SHA-256 hashes. Preserved science astrometry's older schema. `.gitignore`, `util.py`, `wiki/project/state.md` hashes and all unrelated dirty/untracked entries unchanged.
- Rollback preimages: local worktree `.scratch/science-preimages-3e5357d`; RAL `/mnt/ral/jnightin/euclid_dr1/.catalogue-tooling-backups/issue100-3e5357d`. Full deployment manifest in `.scratch/deployment_manifest.json`.
- Submitted **RAL catalogue job 350452**, exact original invocation:
  `hpc/sync submit cpu submit_build_inspection_bundle --export=ALL,SAMPLE=dr1_sep1_rest,RUN_TAG=sersic100_20260922,OUTPUT_DIR=output_sed,SED_OUTPUT_DIR=output_sed,CREATE_ARCHIVE=0,DATASET_PREFIX=Tile`
- Verification pending job completion. No model fits submitted or rerun. No persistent monitor armed.


# Euclid inspection bundle — verified run 350452

PR: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/101  
Commit: `3e5357da48d5d7e9194cc3c3af29f3d239426ec8`  
RAL job: **350452 COMPLETED, exit 0:0, elapsed 00:07:18**  
Bundle: `/mnt/ral/jnightin/euclid_dr1/inspect/dr1_sep1_rest_sersic100_20260922`

## Verified products

| Product | Count / rows | Per-lens files |
|---|---:|---:|
| Deblended FITS | 194 files | 97 pairs |
| Multi-wavelength PNG | 97 files | 97 |
| astrometric_offsets.csv | 601 rows | 93 |
| lens_sersic.csv | 99 rows | 99 |
| magnitudes.csv | 698 rows | 99 |
| source_sersic.csv | 99 rows | 99 |

CSV total: **394 files** (4 masters + 390 per-lens tables). All FITS data/HDUs
readable and structurally valid, all PNGs verified and fully decoded, all CSVs
have consistent row shapes, no duplicate lens/band rows, and per-lens row totals
match their master. FITS-pair and PNG lens sets match exactly (97 lenses).
The four existing 17-HDU FITS files are byte-identical to their pre-rerun checksums.

Band coverage follows completed selected results, not a claim of eight-band
completion for every lens: 82 lenses have eight bands (17 HDUs/file); 1 has six,
1 has four, 3 have three, 4 have two, and 6 have one. No fits were rerun.

## Incomplete products / skips

- `Tile102006997RA0602279119243DECNEG0663160559050`: missing assets; lens=Tile102006997RA0602279119243DECNEG0663160559050 band=vis result=a8ffb46501480d922a5e322a0bdf7cff: galaxy_images.fits, model_galaxy_images.fits
- `Tile102007287RA0559861410321DECNEG0659978613159`: no matching completed results
- `Tile102007544RA0046967284897DECNEG0653123592991`: missing assets; lens=Tile102007544RA0046967284897DECNEG0653123592991 band=vis result=fe2ce737c6035fb236d35abea516cc10: galaxy_images.fits, model_galaxy_images.fits

The same three lenses lack FITS/PNG bundle products. The two completed VIS
results lack generated image/FITS assets and latent summaries; magnitudes drops
those two VIS rows. Their model-parameter summaries remain in the Sersic tables,
which does not establish scientific fit success. The third lens has no matching
completed result.

Stages depending on `initial_lens_model/vis_lp` or `vis_pix` have no inputs in the
requested `output_sed` tree: inspection-image collection, mass maps and Witt–Wynne
skip all 100 lenses; lens-mass has zero matching rows. These are explicit skips,
not successful scientific products. All stages report zero errors.

## Evidence and preservation

- 249 fast tests passed; 10 fitting tests deselected. 26 missing-asset regressions;
  real ten-stage shell smoke, Ruff/format/diff checks, independent Sol review CLEAN.
- All 9 PR checks were SUCCESS on the reviewed commit; PR remains open, unmerged.
- Eleven tooling files deployed with verified preimages/replacements and backups;
  science astrometry schema preserved. Existing science dirty/untracked state and
  `.gitignore`, `util.py`, `wiki/project/state.md` unchanged outside those files.
- No data/config/fitting-script sync, no model-fit submission, no archive generated.
- Local evidence: `ral-products.json`, `ral-before-products.json`,
  `skipped-lenses.csv` (308 stage-specific warnings), `ral-run/output.350452.out`,
  `ral-run/error.350452.err`, and `deployment_manifest.json` beside this report.
- RAL rollback: `.catalogue-tooling-backups/issue100-3e5357d` inside the project.
- Heart RED `release validation FAILED (stage integrate)` remains; user authorized
  issue #100 development override. No release or merge performed.
