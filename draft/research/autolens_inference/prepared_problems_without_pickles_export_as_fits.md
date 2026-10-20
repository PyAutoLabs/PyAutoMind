# Prepared problems without pickles: export as .fits + metadata

Type: research
Target: autolens_inference
Repos:
- PyAutoLens
- autolens_inference
Difficulty: too-large
Autonomy: supervised
Priority: normal
Memory: wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/massive-ellipticals.md; reading-queue.md
Status: formalised
Consequence: glance
Witness: a prepared problem rebuilt from .fits + json reproduces the pickled problem's log likelihood at a fixed instance (|dlogL| < 1e-8) and is <10% of the pickle's size on disk
Review-minutes: 3
Unattended: needs-slicing

# Prepared problems without pickles: export as .fits + metadata

Human request (2026-10-20, verbatim): "intake an issue to assess if we can set up prepared things not using pickles but just .fits files and other metadata, it feels like we are outputting loads more than we need."

Type: research
Target: autolens_inference
Witness: a prepared problem rebuilt from .fits + json reproduces the pickled problem's log likelihood at a fixed instance (|dlogL| < 1e-8) and is <10% of the pickle's size on disk

## Evidence (measured 2026-10-20 on the RAL output tree, search_internal/ excluded)

- Output tree total 3.69 GB. `analysis.dill` 1227 MB (20 files), `dataset.dill` 1219 MB (20 files),
  `baseline_samples.dill` 95 MB (19 files): pickles = 2.54 GB = 69% of everything, all under
  `output/autolens/prepared/<config>/seed_<n>/<variant>/`.
- numba_cpu sparse prepared problems are ~90 MB per `analysis.dill` (hpc_ral_numba_cpu_sparse_fp64:
  7 files = 658 MB) vs ~7.5 MB for jax dense — the sparse precomputation is probably pickled into the
  Analysis (unverified).
- The laptop pull runs at ~180-350 kB/s, so pulling prepared/ turned a results check into a
  2.5-4.5 h transfer; it was excluded from the 2026-10-20 pull by hand.

## Assess

1. What `--export-prepared` (scripts/misc/slam/_runner.py) writes, and what wave.py and the divergence
   repro actually need to rebuild the problem identically.
2. Whether a prepared problem can be data (.fits: image, noise map, PSF, mask; json: model, priors,
   settings, library revisions, release pin, prepared id) that is rebuilt into Dataset/Analysis at
   load, instead of pickled objects — and whether that preserves the prepared-id identity contract.
3. Why sparse analysis pickles are 12x larger; whether derived caches (w_tilde / sparse operators)
   should be recomputed at load rather than stored.
4. Recommendation + size estimate; the code change itself is a follow-up task.

<!-- formalised by the Intake (Conception) Agent on 2026-10-20 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/88d3fcba-c2d1-4816-8ba3-b341960a2cf7/scratchpad/intake_prepared_no_pickles.md -->
