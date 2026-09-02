# Adaptive pixelization over-sampling divides the source S/N map by the noise map…

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: on the subhalo_validation pl_eff_1_outer dataset the over-sample map handed to `apply_over_sampling(over_sample_size_pixelization=...)` by every fixed call site has sub-size 4 on about 30 % of the mask (the pixels with source S/N > 3), not 90 %; a regression test in autolens_workspace_test asserts the fraction on a simulated lens.
Review-minutes: 3

Original request (user, verbatim, 2026-09-02):

"For all runs, I can also see like it looks like the adaptive over sampling of the lensed
source also is not right with most pixels still 4. This is the code and I assume it is not
doing the cap input correct and fliiping what becomes 2 and 4 [...] Do another check to work
out how much of the workspace has this incorrect code, implement the solution (the point is
the bright high S/N regions of the lensed source should have over sampling 4, the rest 2 and
make sure it is applied on source_pix[2] (and thus onwards). Four source_pix[1] retain the
default sub size as the adapt image isnt good enough yet. So intake an issue to fix this in
the workpace, and fix it here for these scripts"

What was verified (2026-09-02, workspace main, PyAutoArray main):

- Root cause is a double division, not a flipped branch.
  `al.galaxy_name_image_dict_via_result_from(result)` returns each galaxy's
  *subtracted signal-to-noise map* (`result.subtracted_signal_to_noise_map_galaxy_dict`,
  floored at `adapt_minimum_percent` of its maximum). Every call site then passes that map
  as `data=` to `al.util.over_sample.over_sample_size_via_adapt_from(data, noise_map, ...)`,
  whose first line is `signal_to_noise = data / noise_map`. The S/N map is divided by the
  noise map a second time; with HST noise of ~0.056 counts that inflates it about 18x, so
  nearly every pixel clears the cut of 3.
- Measured on the three subhalo_validation lenses (source_pix[1] S/N maps, real noise maps):
  current call gives 76 % / 89 % / 90 % of the mask at sub-size 4 (pl_sersic_0 / pl_eff_0 /
  pl_eff_1_outer); thresholding the S/N map itself at 3 gives 15 % / 27 % / 31 %.
- Every call site in the organism passes the S/N map as `data=` (none passes an image):
    scripts/imaging/features/advanced/mass_stellar_dark/slam.py
    scripts/imaging/features/advanced/subhalo/detect/start_here.py
    scripts/imaging/features/advanced/subhalo/sensitivity/slam_source_pixelized.py
    scripts/group/features/advanced/mass_stellar_dark/slam.py
    scripts/group/features/advanced/subhalo/detect/start_here.py
  plus their notebooks (10 files by grep). No HowToLens, autogalaxy_workspace or assistant
  skill page calls the function.
- `scripts/group/slam.py` `source_pix_2` (and its no_lens_light / linear_light_profiles
  copies) uses the other idiom, `np.where(snr > 3.0, 4, 2)`, which is the correct
  arithmetic, but evaluates it on the S/N map after the in-place S/N 3.0 cap on the same
  array, so the `> 3.0` test never fires there either (covered by the sibling prompt
  draft/feature/autolens_workspace/adapt_image_snr_cap.md, item 4).
- The subhalo_validation project fixed its own copy on 2026-09-02 (commit 9893b12,
  scripts/imaging.py): threshold the S/N map directly,
  `al.Array2D(values=np.where(source_snr > 3.0, 4, 2), mask=dataset.mask)`, applied from
  source_pix[2] onwards, source_pix[1] left at uniform sub-size 2. Validated on
  pl_eff_1_outer: 30.5 % at 4, `apply_over_sampling` accepts it, the pixelization grid
  carries {2, 4}.

Scope (user, 2026-09-02: "make sure the intake does it all on slam.py files not just fixing
the group stuff (Same as image_snr cap). Obv both should include docs"):

1. Every SLaM pipeline in autolens_workspace applies adaptive pixelization over-sampling
   correctly, not only the five sites that call the function today. That is
   `guides/modeling/slam_start_here.py`, `group/slam.py` and its three copies,
   `multi_galaxy/slam.py`, and every `features/**/slam*.py` under imaging, group,
   multi_galaxy, multi_dataset and (where over-sampling applies to the pixelization grid)
   interferometer, plus `subhalo/detect/start_here.py` for imaging and group. Today most of
   these apply no adaptive over-sampling at all (grep: `over_sample_size_pixelization=` is
   absent from slam_start_here.py and from every imaging/interferometer/multi_* features
   slam.py); the five that do divide twice; the three group copies use the right arithmetic
   on the wrong (capped, aliased) array.
2. The rule at every site: from `source_pix[2]` onwards the bright lensed source (S/N > 3 on
   the source's S/N map) gets sub-size 4 and everything else 2; `source_pix[1]` keeps the
   default uniform sub-size because its adapt image is not yet good enough. Either
   threshold the S/N map directly as the project did, or pass a *model image*
   (`use_model_images=True`) with the noise map so the library's data / noise arithmetic is
   honoured; pick one idiom and use it everywhere.
3. Docs at every site: the prose cell above the call says which quantity is thresholded
   (an S/N map, not divided by the noise map again), why 4 / 2, and why `source_pix[1]` is
   exempt; regenerate every touched notebook. Update the workspace docs page(s) that
   describe SLaM over-sampling and the autolens_assistant skill(s) that teach it
   (`al_adaptive_pixelization.md` and whichever SLaM skill covers `source_pix`).
4. Library follow-up to decide at start_dev, not to block this: `over_sample_size_via_adapt_from`
   is named as if it took an adapt image but its docstring and arithmetic take data; either
   add an `over_sample_size_via_snr_from(signal_to_noise_map, cut, lower, upper)` helper in
   PyAutoArray and point the workspace at it, or rename the parameter so the misuse cannot
   recur. Decision and any PyAutoArray change ride in a separate library task.
5. Regression test in autolens_workspace_test on a simulated lens: fraction of sub-size 4
   equals the fraction of source S/N > 3 pixels.

Out of scope: the S/N 3.0 cap on the adapt image itself (sibling prompt above); the
subhalo_validation project (already fixed).

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/78dd3d8b-d65e-4d83-a0db-4c41bd18f3d6/scratchpad/intake_over_sample_snr_double_division.md -->
