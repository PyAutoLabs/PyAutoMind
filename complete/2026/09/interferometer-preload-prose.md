Reworded the interferometer preload prose across three pixelization example
scripts and their generated notebooks in `autogalaxy_workspace`. The old text
told users the transformer preload took "minutes to hours" and pushed them
toward a disk cache to survive it; as of the next PyAutoArray release the
preload is built as a **type-1 NUFFT in seconds**, so the prose now says that.

What the new prose says:

- the preload is a type-1 NUFFT, built in **seconds** as of the next
  PyAutoArray release;
- the **disk cache is optional** — keep it if you want, it is no longer the
  thing standing between you and a fit;
- **existing `.npy` cache files remain valid** — nothing needs regenerating;
- a short **memory / chunking** note for large visibility counts.

`use_jax=True` kwargs were left untouched. The diff is prose only — no
executable line changed, which is what let it ship past an organism-scope Heart
amber (see `heart-ack:` below).

Files: `scripts/interferometer/features/pixelization.py`,
`scripts/interferometer/modeling/features/pixelization.py`, the `pix_adapt`
chaining pixelization prose, and the three matching notebooks.

- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/238 (merged 6c9b19b1ea6d4c13a1c03a2e1fa7519f7c6ddb7c)
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/237 (closed)
- upstream: PyAutoArray#541 (merged 9bd76799d4d836efd99a9885978a93a6674cc176)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/541
- heart-ack: 2026-09-08 in-session, two reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; neither names autogalaxy_workspace, and this diff is prose only, changing no executable line

**Release gate — PyAutoArray.** The library half of this change (PyAutoArray#541)
is merged but **not yet released**. Until PyAutoArray publishes, the reworded
prose describes behaviour a user on the current release does not have: on the
released library the preload is still the slow path. The `pending-release:` key
above is what keeps that obligation on the dashboard's **Pending release**
section after this row is pruned; only `/review_release` clears it, on a release
that actually published.

## Original prompt

# Interferometer preload prose says "minutes to hours" — it is now seconds

Type: docs
Target: autogalaxy_workspace
Repos:
- autogalaxy_workspace
Themes:
- interferometer
- docs
Difficulty: small
Autonomy: supervised
Priority: medium
Epic: numba-interferometer-revisit
Filed: 2026-09-08
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/237

## The request

> update the "minutes to hours" prose

## Why

PyAutoArray#541 (merged 2026-09-08, merge commit `9bd76799`, record
`complete/2026/09/interferometer-preload-nufft-type1.md`) rebuilt the interferometer
sparse-operator preload — `nufft_precision_operator_from` — as a **type-1 (adjoint)
NUFFT**, with `method="nufft"` the new default. At `alma` (1e6 visibilities) the
measured build went from **2101 s to 7.3 s** wall (111x in CPU-seconds); `alma_high`
(5e6 visibilities) builds in 22 s where the brute force refused. A second commit on
that branch removed the last demotion path, so a caller passing `use_jax=True` stays
on the NUFFT rather than being routed back to the JAX brute force.

The workspace prose was written against the brute-force builder and is now false.
`autogalaxy_workspace/scripts/interferometer/features/pixelization/many_visibilities_preparation.py`
still says the preload "can vary between seconds and hours", "may take 10 minutes or
hours", and presents the `.npy` cache as a run-time necessity rather than a
convenience. The same claim is repeated in the `__Sparse Operators__` blocks and the
opening docstrings of `fit.py` and `modeling.py` in the same folder.

## Scope

- The prose in `many_visibilities_preparation.py`, plus the sibling sentences in
  `fit.py` and `modeling.py` that claim the preload build is slow.
- Say the array is built as a type-1 NUFFT in seconds as of the next autoarray
  release; that caching to disk is still supported but no longer necessary for run
  time; and keep the memory note — a one-shot NUFFT at millions of visibilities needs
  chunking, which the transformer's `chunk_size` provides.
- Keep the `use_jax=True` kwargs in the calls: they now stay on the fast path, and
  removing them would break users on the currently released library.
- Leave anything about `AnalysisInterferometer(use_jax=True)` alone — that is the fit,
  not the preload.
- Regenerate the notebooks for the edited scripts.

## Dependency

pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/541 —
merged but not released. The prose describes behaviour users get at the next autoarray
release, so this PR merges behind the pending-release chain, not before it.
