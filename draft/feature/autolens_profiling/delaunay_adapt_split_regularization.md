# Re-base the Delaunay profiling cells on AdaptSplit regularization

Type: feature
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- profiling
- regularization
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: every re-based cell has a new EXPECTED_LOG_EVIDENCE_HST pin that passes on both legs, and the AdaptSplit params->H prefix on the DelaunayNN cell is within ~1 ms/call at vmap 16 of the ConstantSplit row in results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_assembly.json
Review-minutes: 20
Unattended: ready
Filed: 2026-09-08

## Original request (verbatim)

> I think this should use AdaptSplit like regular delaunay albeit its good we sped up ConstantSplit

## Why

Every autolens_profiling likelihood cell for the Delaunay family measures
`al.reg.ConstantSplit(coefficient=1.0)`:

- `scripts/imaging/likelihood_breakdown/delaunay.py`
- `scripts/imaging/likelihood_breakdown/delaunay_nn.py`
- `scripts/imaging/likelihood_runtime/delaunay.py`
- `scripts/imaging/likelihood_runtime/delaunay_nn.py`
- `scripts/imaging/likelihood_runtime/delaunay_numba.py`

Production pipelines pair Delaunay with `al.reg.AdaptSplit` — see
`euclid_strong_lens_modeling_pipeline/scripts/initial_lens_model.py` and the
SLaM pipelines. So the profiled numbers are not the regularization production
runs actually pay for.

## Task

Re-base those cells on `AdaptSplit`, taking the adapt image from the cell's
existing adapt-image path — the same one the `Hilbert` mesh already uses — so
the Delaunay and DelaunayNN cells profile what production runs.

`AdaptSplit` shares `pixel_splitted_regularization_matrix_from` with
`ConstantSplit`, so the PyAutoArray #537 compaction (assembly 10.03 -> 0.84
ms/call at vmap 16) carries over; the only extra cost is the per-pixel adapt
weights.

Expect the log-evidence pins (`EXPECTED_LOG_EVIDENCE_HST` in each script) to
change, so each cell needs a fresh pin measured on the A100 with a same-node
control (ConstantSplit) vs feature (AdaptSplit) pair, per the protocol in
`results/notes/delaunay_nn_constant_split_assembly.md`.

Keep ConstantSplit available behind a `--regularization` CLI flag or config key
if that is cheap — the historical rows are ConstantSplit and must stay
comparable. The default flips to AdaptSplit.

Record which regularization every result JSON was measured with: a
`regularization` key next to the existing `sibson` key.

## Scope note

autolens_workspace_test is in scope only if a jax_assertions pin needs the same
flip — check `scripts/imaging/jax_likelihood/delaunay.py` there, which already
uses AdaptSplit per the PyAutoArray #537 ship notes.

## Witness

- Every re-based cell has a new pin that passes on both legs.
- The AdaptSplit params->H prefix on the DelaunayNN cell is within ~1 ms/call at
  vmap 16 of the ConstantSplit row in
  `results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_assembly.json` — i.e. the
  compaction gain survives the regularization change.

## Related

- `complete/2026/09/delaunay-nn-constant-split-assembly.md`
- PyAutoArray #536, PyAutoArray #537
- `autolens_profiling/results/notes/delaunay_nn_constant_split_assembly.md`

<!-- formalised by the Intake (Conception) Agent on 2026-09-08 -->
