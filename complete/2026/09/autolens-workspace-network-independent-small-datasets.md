# autolens_workspace validation is network-independent under PYAUTO_SMALL_DATASETS

Chat-initiated repair, recorded retroactively at close-out with no prior Mind prompt, no issue and no task worktree (same direct-repair pattern as `ci-smoke-speedup`). `autolens_workspace#576` merged 2026-09-20 as `1016ed37da91bd6af7b209c27184d452be35cc61`.

- issue: none (chat-initiated; recorded retroactively at close-out)
- completed: 2026-09-20
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/576
- merge-commit: `1016ed37da91bd6af7b209c27184d452be35cc61`
- validation: Smoke Tests #1115 green on Python 3.12 and 3.13; the previously failing joint imaging + point-source script passed in 5.3 s and 4.7 s respectively

## What shipped

- Swept `autolens_workspace` for runtime external-data/network dependencies rather than patching only the observed CDS/Aladin failure.
- `scripts/multi_dataset/features/imaging_and_point_source/modeling.py`: under `PYAUTO_SMALL_DATASETS=1`, RXJ1131 imaging is now constructed locally as a deterministic 16x16 HST-like image. Normal execution still uses the real CDS `hips2fits` cutout.
- The synthetic RXJ1131 image includes a deterministic sky gradient, so the existing border-RMS logic produces a finite positive noise map instead of accidentally creating zero noise. The downstream path remains the real one: `Array2D` → `Imaging` → noise scaling → mask / oversampling → imaging + point analyses → shared factor graph / search.
- `scripts/weak/start_here.py`, `scripts/weak/real_data/a2744.py`, and `scripts/weak/features/strong_lensing/a2744.py`: small-dataset mode now builds a deterministic 64-source tangential-shear catalogue with sensible ellipticities and uncertainties instead of fetching the pyRRG A2744 FITS catalogue. Normal tutorials retain the real catalogue.
- `scripts/cluster/start_here.py`: the visualization-only A2744 `hips2fits` image is skipped in small mode.
- `scripts/cluster/lenstool/data.py`: small mode writes tiny valid Lenstool-shaped fixtures for the Mahler files and runs the real parsers / CSV writers; the 96 MB RELICS mosaic remains a normal-mode visualization download.
- `dataset/cluster/a2744/prep.py`: small mode uses tiny deterministic VizieR-shaped rows so dataset regeneration can be exercised offline.
- Mirrored the same behavior into the executable notebooks.
- Added `tests/test_small_dataset_network_contract.py`, which AST-checks the relevant executable scripts so module-level `_download()` / `urlopen()` calls cannot execute in small-dataset mode, pins both smoke and release profiles to `PYAUTO_SMALL_DATASETS="1"`, and protects the positive-noise construction.
- Added `multi_dataset/features/imaging_and_point_source/modeling.py` to `smoke_tests.txt` so the exact pathway that broke the nightly release is now continuously exercised by PR CI.

## Runtime dependency audit

External runtime dependencies found:

- CDS/Aladin `hips2fits` — RXJ1131 HST image in the joint imaging + point-source example.
- pyRRG GitHub catalogue — A2744 weak-lensing examples.
- CDS/Aladin `hips2fits` — A2744 cluster visualization image.
- Mahler GitHub raw files — SMACS0723 Lenstool model inputs.
- STScI RELICS archive — SMACS0723 F814W visualization mosaic.
- VizieR — A2744 dataset regeneration utility.
- MAST via `astroquery.mast` — `dataset/multi_galaxy/sdssj1011+0143/prep.py`, a dedicated one-off ingestion utility for a 215 MB archival HST frame.

The MAST preparation script remains intentionally network-backed because it is a manual dataset-ingestion utility, not a smoke/release modeling entry point. No CI case was identified where network availability itself is the behavior under test.

Second-pass searches found no additional `requests.get`, `httpx`, `pooch`, `wget` or `curl` scientific-data fetch paths.

## Key traps / findings

- **Downloading then cropping is not small-dataset mode.** The failed RXJ1131 path fetched the 200x200 remote image first and only then capped it. The correct abstraction is to avoid the remote dependency entirely and construct the small deterministic dataset at the dataset boundary.
- **`PYAUTO_TEST_MODE` is the wrong knob for data availability.** `PYAUTO_SMALL_DATASETS` already owns deterministic reduced dataset construction; test mode remains about search behavior.
- **Synthetic imaging still needs physical noise structure.** A constant image makes a border-derived RMS collapse to zero. The local image therefore includes deterministic sky structure and keeps the original noise-map code intact.
- **The release profile already defaults to small datasets.** Existing `PYAUTO_SMALL_DATASETS=0` overrides are targeted at unrelated `*/start_here`, guides, and potential-correction paths; they do not match the repaired joint/weak/Lenstool examples.
- **A green generic smoke run would not have proved this fix.** The RXJ1131 script was not previously in `smoke_tests.txt`; it was added before merge and then explicitly passed on Python 3.12 and 3.13.
- GitHub-hosted smoke runners do have internet access, so the runtime proof is paired with the static network-reachability contract: under small mode the network calls are structurally unreachable.

## Invariant

> `PYAUTO_SMALL_DATASETS=1` workspace validation must be deterministic and must not require external dataset/network availability, while normal tutorial execution continues to use scientifically meaningful real data where appropriate.

## Original prompt

> Sweep the entire "autolens_workspace" for scripts that download or otherwise fetch external datasets/resources at runtime. Look for all mechanisms, not just the current "hips2fits" example: e.g. "urlopen", "urlretrieve", "urllib", "requests", custom "_download" helpers, shell/network calls, remote FITS/images/catalogues, or similar.
>
> The motivation is today's nightly release failure in:
>
> "multi_dataset/features/imaging_and_point_source/modeling.py"
>
> where the release-fidelity run failed because the CDS/Aladin "hips2fits" service could not be reached. Release/smoke validation should not depend on external network services unless network access is specifically what the example is intended to test.
>
> For every runtime external-data dependency you find:
>
> 1. Understand what the downloaded data is actually used for and whether the scientific/tutorial version of the script should continue using the real remote data. Preserve that normal user behaviour wherever appropriate.
>
> 2. Inspect how "PYAUTO_SMALL_DATASETS" is already used throughout PyAutoLens and the workspace. Treat this as the mechanism for making dataset construction small, deterministic and network-independent in CI. Do not overload "PYAUTO_TEST_MODE" if small-dataset mode is the more appropriate abstraction.
>
> 3. When "PYAUTO_SMALL_DATASETS=1", avoid the external download entirely. Prefer constructing a minimal deterministic local/simulated dataset that exercises the same downstream PyAutoLens pathway. Do not download the full dataset and then crop it.
>
> 4. Keep the code after dataset construction as close as possible to the real-data path, so CI still exercises the meaningful functionality: dataset objects, masks/grids, analyses, model composition, likelihood evaluation, factor graphs/searches where applicable, etc. Do not turn these into trivial "imports successfully" tests.
>
> 5. Make synthetic data physically/numerically sensible. For example, imaging must have a valid non-zero noise map rather than accidentally deriving zero noise from a constant synthetic image.
>
> 6. Normal execution without "PYAUTO_SMALL_DATASETS=1" should retain the existing real-data/download behaviour and educational value.
>
> 7. Check both "profile_smoke.yaml" and "profile_release.yaml" and make sure the relevant scripts actually receive "PYAUTO_SMALL_DATASETS=1". Pay particular attention to existing overrides that deliberately disable small datasets.
>
> 8. Add/update tests where useful to pin the important contract: under small-dataset mode these scripts must not attempt network access.
>
> After the sweep, report:
>
> - every external runtime dependency found;
> - whether it can currently execute during smoke/release validation;
> - the proposed treatment for each;
> - any cases where network access genuinely should remain part of CI.
>
> Then implement the fixes across the workspace.
>
> Finally, run the relevant smoke/release-style validation locally as far as practical, and specifically verify that "multi_dataset/features/imaging_and_point_source/modeling.py" runs under "PYAUTO_SMALL_DATASETS=1" with network access unavailable.
>
> The desired invariant is:
>
> "PYAUTO_SMALL_DATASETS=1" workspace validation must be deterministic and must not require external dataset/network availability, while normal tutorial execution continues to use the scientifically meaningful real data where appropriate. @GitHub
>
> Follow-up: run the GitHub smoke validation for the branch, include the RXJ1131 script explicitly, merge the PR once green, and update PyAutoMind through the PyAutoBrain close-out conventions.
