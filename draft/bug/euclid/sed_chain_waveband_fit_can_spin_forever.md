# SED chain waveband fit can spin forever in Nautilus exploration (343381_8 nir_y, 40k calls, plateau) — cap the search so one band cannot block a tile's whole chain

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- hpc
- catalogue
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: Tile102008532RA0683486015030DECNEG0642073552911 nir_y re-run under the capped search terminates within the cap and the tile's remaining six bands complete inside the 12 h walltime; today that band is still in Nautilus exploration at 40000 likelihood calls after 1 h 36 min and no other band starts
Review-minutes: 3
Unattended: ready
Filed: 2026-09-17

## Observed

SLURM array `343381` (`euclid_sersic_waveband`, `--array=0,2-9`) ran the CPU SED chain
(`scripts/sersic_lens_model_waveband.py`) on nine sep1 tiles of the `euclid_dr1` science project on
2026-09-17. Eight tasks COMPLETED in 6-16 min. One — `343381_8`,
`Tile102008532RA0683486015030DECNEG0642073552911` — was still RUNNING at 1 h 36 min elapsed, still on
its **first** non-VIS band `nir_y`, output dir
`output_sed/dr1_sep1/<tile>/sersic_lens_model/nir_y/337ab77d5369c13c1a92417f9b0dd61c`.

Its `.out` log is not the signal: it stops at the Nautilus start line (13:38:30) because python stdout
is block-buffered when redirected. The signal is `files/search_internal/checkpoint.hdf5` (6.3 MB,
still growing). Read directly, it says:

- Nautilus attrs: `n_dim` 2, `n_live` 75, `n_batch` 100, **`n_like` 40000**, **`explored=False`**
  (still in the exploration phase), **20 shells** built.
- `shell_n` for the last three shells: **15935, 14596, 5610** points, against ~100-370 for the
  earlier shells. `shell_log_l_min` converging on **-16037.3719** (last three -16037.38033,
  -16037.37204, -16037.37194); `shell_log_v` down to **-21.5, -26.3**. The bound volume keeps
  shrinking while the likelihood floor moves by 1e-2 then 1e-4 nats.
- Shell 19's 5610 points span a logL range of **1e-3 nats** (-16037.37288 to -16037.37194) at position
  mean (y, x) = **(0.010338, -0.008069)"** with std **(4.1e-8, 1.3e-6)"** — a region ~**1e-7 arcsec**
  wide.
- **Not an fp32 floor:** all 5610 logL values are distinct, minimum spacing 2.2e-11 — fp64.
- **Not a prior-edge case:** no point of the 40000 has |offset| > 0.19", so it is not pinned against
  the ±0.2" `dataset_model.grid_offset` prior.
- The single highest-likelihood point of all 40000 is logL **-16029.2254** at
  (y, x) = **(0.004092, -0.008149)"** — **8 nats above** the shell-19 plateau and 0.006" away in y.
  **Only one** point of 40000 lies within 0.5 nats of it.

The likelihood surface for this band is non-smooth: a lone 8-nat spike sitting on a plateau that the
sampler keeps sub-dividing into ever-thinner shells, so Nautilus never reaches its `f_live` stop
criterion and exploration does not terminate. The tiles that finished did `nir_y` in about a minute at
~1600 likelihood calls and 15 bounds.

## Mechanism

`sersic_lens_model_waveband.py` fits **every band sequentially in one python process**: `vis_lp`
(seeded) → the VIS Sersic fit → one Sersic fit per non-VIS band. So the other six bands of this tile
(`nir_j`, `nir_h`, `decam_g`, `decam_r`, `decam_i`, `decam_z`) cannot start while `nir_y` is still
sampling. The submit script's walltime is 12 h, so the task is killed at ~01:33 BST on 2026-09-18
**with no band completed** — one pathological band costs the tile's entire SED chain, and the
catalogue loses that lens from `astrometric_offsets.csv` (52 rows / 8 lenses instead of 59 / 9) and
from `magnitudes.csv` (61 instead of 68). There is no cap, no diagnostic, and no record that the band
was attempted.

## Ask

1. **Give the waveband fit's Nautilus a hard stop.** `fit_waveband` (in
   `scripts/lens_model_waveband.py`, invoked by `scripts/sersic_lens_model_waveband.py`) should
   construct its search with a bounded likelihood budget — PyAutoFit's Nautilus config /
   `n_like_max` or the equivalent — plus a sensible `f_live`, so no single band can consume the
   whole walltime. The cap should be a named constant or config value, not buried in a call site.
2. **A band that hits the cap must record itself as capped, not as absent.** The result should be
   written with a flag (or a sentinel row / log line) that the catalogue producers can see, so that
   `catalogue/scripts/astrometric_offsets.py` and `catalogue/scripts/magnitudes.py` still
   de-duplicate correctly and a QA column or a clearly-worded log line distinguishes "band hit the
   sampler cap" from "band not present in this cut-out". Today those two cases are
   indistinguishable — both are simply a missing row.
3. **Add a fast test proving the cap fires**: a synthetic non-smooth likelihood (a plateau plus a
   narrow spike) or a mocked sampler that never converges, asserting the fit returns within the cap
   and that the capped result is marked as such. It must run in the pipeline's fast test suite —
   no cluster, no real fit.

## Witness

Re-run `Tile102008532RA0683486015030DECNEG0642073552911` `nir_y` under the capped search: the band
terminates within the cap (minutes, not hours) and the remaining six bands of that tile complete, so
the tile's SED chain finishes inside its 12 h walltime. Today that same band is still in exploration
at 40000 likelihood calls after 1 h 36 min and the other six bands never start.

## Evidence

- Science journal: `/mnt/c/Users/Jammy/Science/euclid_dr1/wiki/project/2026-09-17-sed-chain-sep1.md`,
  section "`343381_8` diagnosed at 15:03 BST".
- Checkpoint on RAL:
  `/mnt/ral/jnightin/euclid_dr1/output_sed/dr1_sep1/Tile102008532RA0683486015030DECNEG0642073552911/sersic_lens_model/nir_y/337ab77d5369c13c1a92417f9b0dd61c/files/search_internal/checkpoint.hdf5`
- `ssh euclid_jump "sacct -j 343381 -X --format=JobID,State,Elapsed"` — eight COMPLETED 6-16 min,
  `343381_8` RUNNING 01:36:17.

<!-- formalised by the Intake (Conception) Agent on 2026-09-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/7bff8610-4b84-413a-a994-d72484c4c14c/scratchpad/intake_2a.md -->
