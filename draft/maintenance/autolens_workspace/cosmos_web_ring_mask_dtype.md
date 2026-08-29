# cosmos_web_ring stores boolean masks as float64, wasting ~3.4 MB of the repo's largest dataset

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- hygiene
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Filed: 2026-08-04 (backfilled from git)

Found during a `/repo_cleanup` sweep on 2026-08-04, after `clean_slate.sh`
flagged `dataset/imaging/cosmos_web_ring` as a committed 11 MB dataset over its
5 MB threshold.

## First, the thing NOT to do: it should stay tracked

`autolens_workspace/.gitignore` ignores `dataset/**` wholesale and then
explicitly un-ignores six real datasets — cosmos_web_ring at line 11, alongside
`slacs1430+4105`, `rxj1131`, `a2744`, `sdp81` and the group NEG dataset. It is
real JWST/COSMOS-Web observational data with no producing simulator, and it
backs both `scripts/imaging/start_here.py` and
`scripts/multi_dataset/start_here.py` — the workspace's two front doors. The
5 MB threshold is a size heuristic blind to that allowlist. Removing it from git
would break the first thing a new user runs.

## The actual defect

Every `mask_extra_galaxies.fits` in the dataset is a boolean mask
(`numpy.unique` -> `[0., 1.]`, exactly 2 values) stored as `>f8`:

    wavebands/F115W/mask_extra_galaxies.fits   1.34 MB   >f8   (419, 419)
    wavebands/F150W/mask_extra_galaxies.fits   1.34 MB   >f8   (419, 419)
    wavebands/F277W/mask_extra_galaxies.fits   0.34 MB   >f8   (209, 209)
    wavebands/F444W/mask_extra_galaxies.fits   0.34 MB   >f8   (209, 209)
    mask_extra_galaxies.fits                   0.28 MB   >f8   (top level)

That is 8 bytes per pixel to store one bit. Re-storing as `uint8` takes the
dataset from 11.2 MB to roughly 7.8 MB with zero information loss, and puts it
below the threshold that flagged it.

## Scope decision to make

The F115W and F150W bands are ~5.4 MB of the total and are **commented out** in
`scripts/multi_dataset/start_here.py:119-120` ("Commented out to make code run
fast, but can be included to show 4 waveband modeling"). They are deliberately
shipped-but-unused so a reader can uncomment them. Decide whether that is worth
5.4 MB, or whether those two bands should be dropped and the comment changed to
point at a download. Defensible either way — but decide it explicitly rather
than letting it ride.

There is precedent for surgical exclusion at `.gitignore:16`, where
`dataset/cluster/a2744/data.fits` is re-ignored while the rest of that dataset
stays allowlisted.

## Verification

The masks are consumed by the two `start_here` scripts. After any re-encode,
confirm the loaded mask is bit-identical to the current one (compare the boolean
arrays, not the file bytes) and smoke-run both scripts — a dtype change that
silently alters mask semantics is worse than the 3.4 MB.

## Related

`complete/2026/08/committed-capped-smoke-datasets.md` (retired 2026-08-29 as obsolete) — a different
problem in the same tree (capped 15x15 smoke artifacts committed as real data in
four *other* folders). cosmos_web_ring is genuine real data and is not one of
them; do not fold these two together.

<!-- raised from a /repo_cleanup sweep, 2026-08-04 -->
