# Add `over_sample_size_via_snr_from` so a signal-to-noise map can steer over-sampling without a second division

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Issued: 2026-09-03
Consequence: judge
Witness: `al.util.over_sample.over_sample_size_via_snr_from(signal_to_noise_map, signal_to_noise_cut=3.0, sub_size_lower=2, sub_size_upper=4)` exists, thresholds its input once with no auto-lowering of the cut, and a unit test pins that its {2, 4} map equals `np.where(snr > cut, 4, 2)` exactly; the docstring of `galaxy_name_image_dict_via_result_from` says it returns a signal-to-noise map.
Review-minutes: 3
Unattended: ready

Split out of `over-sample-snr-double-division` at close-out (autolens_workspace#523, record
`complete/2026/09/over-sample-snr-double-division.md`, scope item 4). The workspace side shipped
without any library change: every SLaM pipeline now thresholds the source S/N map directly with
`np.where(source_image_raw > 3.0, 4, 2)`.

What is wrong in the library today:

- `over_sample_size_via_adapt_from(data, noise_map, signal_to_noise_cut=5.0, ...)` is named as if it
  took an adapt image but its first line is `signal_to_noise = data / noise_map`. Every caller in the
  organism handed it the per-galaxy map from `galaxy_name_image_dict_via_result_from`, which is already
  `subtracted_image / noise_map`, so the S/N was divided by the noise twice (~18x inflation on HST-depth
  data; ~90 % of the mask at sub-size 4 instead of ~30 %).
- It defaults the cut to 5.0 and silently lowers it when `max(S/N) < 2 * cut`, so it cannot express
  "S/N > 3 → 4" even with the right inputs.
- `galaxy_name_image_dict_via_result_from` (PyAutoGalaxy) has a docstring saying "model image"; it
  returns `subtracted_signal_to_noise_maps_of_galaxies_dict`.

Decide and implement one of:

1. Add `over_sample_size_via_snr_from(signal_to_noise_map, signal_to_noise_cut, sub_size_lower,
   sub_size_upper)` in `autoarray/operators/over_sample/over_sample_util.py` beside the existing
   helper, no auto-lowering, and point the workspace idiom at it in a follow-up workspace sweep; or
2. Rename the existing helper's `data` parameter (e.g. `image`) and make its docstring state that it
   divides by the noise map itself, so passing an S/N map reads as the misuse it is.

Either way fix the PyAutoGalaxy docstring. Keep the workspace's direct `np.where` idiom working; the
assistant skill `al_adaptive_pixelization.md` documents that idiom and the never-do-this.
