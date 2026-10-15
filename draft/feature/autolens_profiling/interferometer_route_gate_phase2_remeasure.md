# Interferometer route gate phase 2: re-measure the Aris routing table with the default cost model

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: glance
Status: formalised
Issued: 2026-10-15

- Status: split out of `interferometer-numba-route-gate` at close-out — the library
  phase shipped in `complete/2026/10/interferometer-numba-route-gate.md`
  (https://github.com/PyAutoLabs/PyAutoArray/issues/628,
  https://github.com/PyAutoLabs/PyAutoArray/pull/632); this is the workspace record that remains.

PyAutoArray#632 replaced the fixed `interferometer_numba_nnz_per_source_max: 60` gate with a
two-constant cost model (`t_fft = c_fft·S·pocketfft-work(padded 2ny×2nx)`,
`t_dc = c_dc·nnz·ny·nx`, c_fft 7.62e-10, c_dc 1.77e-09). The packaged default is now `null`
(cost model); a positive value is a hard gate, 0 turns numba off, and a new
`interferometer_route` setting forces a route.

Re-measure both Aris masks' routing table (125x125, extent 83²; 512x512, extent 341²) with the
default cost model at the campaign's vertex counts (125: 1,405 / 2,947 / 5,526; 512: 1,459 /
2,577 / 5,746), recording for each cell the chosen route, both measured timings and the
predicted t_fft / t_dc. Record the table in the campaign results/wiki in the
autolens_profiling#226 bake-off format, and link #628 / #632 and
https://github.com/PyAutoLabs/PyAutoPulse/issues/62 (task `interferometer_large_mask_aris`).
This also supplies the campaign's owed Aris after-measurements.

Note: the three autolens_profiling scripts that set
`interferometer_numba_nnz_per_source_max` explicitly keep hard-gate meaning — leave them
unchanged unless the re-measurement is meant to exercise the default (then drop the explicit
value in the run, not in the committed script).
