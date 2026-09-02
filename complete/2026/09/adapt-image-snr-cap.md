Capped the source adapt image at S/N 3.0 in every adaptive pixelization pipeline of
autolens_workspace and taught the autolens_assistant skills the rule.

## What shipped

- autolens_workspace PR #522 (feature/adapt-image-snr-cap): 43 scripts + 43 regenerated notebook
  twins, 136 `AdaptImages` construction sites. Every stage that builds a source adapt image copies
  the source entry of `galaxy_name_image_dict_via_result_from`, caps it at 3.0 and writes it back
  into the dict before `AdaptImages`, so the Hilbert image mesh, the rectangular adapt meshes and
  Adapt / AdaptSplit regularization all consume the capped image. One `__Adapt Image S/N Cap__`
  prose cell per script, always in a module-level cell (the notebook generator only promotes
  column-0 strings).
- Group pipelines (`group/slam.py` and its two copies, `group/features/pixelization/slam.py`): the
  aliased in-place cap is replaced by the copy form, `source_pix_1` is now capped, the misleading
  no-op "capped" block really caps, and the adaptive over-sample map is evaluated on the raw S/N
  image again (on the capped image the `> 3.0` test never fired, so 4x over-sampling never
  activated). Three imaging scripts that feed `over_sample_size_via_adapt_from` also bind the raw
  image first.
- Interferometer pipelines (7 scripts, 24 sites) keep `use_model_images=True` and clip a copy of
  the model image at the flux where the beam-smoothed S/N crosses 3.0, with the image-plane noise
  `sqrt(0.5 * sum|noise_map|^2)` (real part of the adjoint transform; verified 13.7e3 measured vs
  13.8e3 formula). `scaling_relation/slam.py` switched to model images like its siblings; the dead
  overwritten dict build in `pixelization/delaunay.py` was removed. On the `simple` dataset the clip
  lands at 5.6% of peak (35% of masked pixels flattened); under the 15x15 smoke mask no pixel reaches
  S/N 3 and the block says so.
- autolens_assistant PR #118: `al_adaptive_pixelization.md` gains an "Adapt image S/N cap (always)"
  section (block, why, raw-image rule, interferometer form), `al_run_slam_pipeline.md` and
  `init-slam.md` point at it, `chat_pack/08_skills_fitting.md` regenerated.

## Decisions (user, 2026-09-02)

- One task, one PR per repo, staged execution (five parallel Opus sweeps + a reconcile pass).
- Interferometer: runtime S/N-derived clip. The S/N-image route was tested and rejected: the
  interferometer "S/N" image divides by `dirty_noise_map`, which is sigma x the dirty beam (55% of
  pixels <= 0). Pure peak-scaling is a no-op because every consumer is max-normalised.

## Evidence

- All 43 touched scripts run under the smoke profile after a 24-simulator pre-pass: 41 PASS;
  `interferometer/features/pixelization/delaunay.py` passes serially (parallel dataset race);
  `subhalo/sensitivity/slam_source_parametric.py` (`'Model' object has no attribute 'centre'`) and
  `slam_source_pixelized.py` (`al.MapperValued` missing) fail identically on unmodified main.
  The intermittent hang in the latter is a pre-existing PyAutoFit `Process.run` race (worker exits
  on a transiently empty job queue; control hung 2/6, edited 1/6).
- CI: #522 7/7 checks green (smoke 3.12 + 3.13); #118 2/2 green. Heart YELLOW at ship
  ("PyAutoArray: open PR 10d old"; stale "release validation incomplete: no rehearsal for current
  source") — unrelated.

## Follow-ups (filed or to file)

- Filed: `draft/docs/autogalaxy/adapt_image_is_the_s_n_map.md` — say the adapt image is the S/N
  map in every `__Adapt Images__` cell, library docstrings, and assess the AdaptImages API naming.
- To file: library-side cap (`galaxy_name_image_dict_via_result_from(..., snr_cap=)`); the two
  pre-existing sensitivity-script failures (MapperValued drift, `centre` AttributeError); the
  PyAutoFit `Process.run` job-queue race; gentler interferometer clip variant if 5.6% of peak is too
  aggressive.
- The subhalo_validation recipes themselves are handled by the PyAutoCortex rerun ruling.

## Original prompt

# Cap the adapt image at S/N 3.0 in every adaptive pixelization pipeline

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- autolens_assistant
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: every Hilbert / rectangular-adapt / Adapt-regularization call site in autolens_workspace scripts builds its AdaptImages from a source S/N image whose maximum is exactly 3.0 (grep finds no uncapped `galaxy_name_image_dict["('galaxies', 'source')"]` handed to an image mesh or AdaptImages), and the group source_pix_2 over-sample map contains 4s again.
Review-minutes: 25
Issued: 2026-09-02
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/521

Cap the adapt image at S/N 3.0 everywhere an adaptive pixelization consumes it: the Hilbert
image-mesh, the rectangular adapt meshes and the Adapt / AdaptSplit regularization.

Original request (user, verbatim, 2026-09-02, while ruling on the subhalo_validation
pl_eff_1_outer result in PyAutoCortex):

"The problem with the pl_eff_1_outer result, for the delaunay, is that the Hilbert mesh is
not adapting to the fainter images of the outer source and thus still has too low
resolution. I think this is because the adapt_image does not have this scaling, which is
used in other scritps, applied to it, which caps the max values to 3.0, meaning fainter
sources are up weighted compared to the brightest soures."

    signal_to_noise_threshold_image_mesh = 3.0
    adapt_data_snr_max = galaxy_image_name_dict["('galaxies', 'source')"]
    adapt_data_snr_max[adapt_data_snr_max > signal_to_noise_threshold_image_mesh] = (
        signal_to_noise_threshold_image_mesh
    )

"can we check if the cap is simply not implementd on the autolens_workspace (where I assume
the scripts were built by the autolens_assistnat) and thus whether we need to intake a task
to updated the autolens_workspace SLaM pipelines accordingly?"

"intake this, and yes, the rectangular should also used the capped adapt image as even
there dont want to over weight bright galaxies, and the aapt images may also impact
regularization and thus use this capped image (check that is true on group) so intake for
all these aspects"

What was verified (2026-09-02, workspace main, PyAutoArray main):

- The library applies no cap. `Hilbert.weight_map_from` (autoarray
  inversion/mesh/image_mesh/abstract_weighted.py) is |adapt|/max, **weight_power, floored
  at weight_floor. `RectangularRTUAdaptImage.mesh_weight_map_from` clips at 1e-12 below,
  raises to weight_power, floors, normalises: no upper cap. `Mapper.pixel_signals_from`
  (the Adapt / AdaptSplit regularization weights) reads `self.adapt_data.array` raw.
  So any cap is the calling script's job.
- In the workspace the cap exists only in `scripts/group/slam.py` `source_pix_2` and its
  two copies `group/features/no_lens_light/slam.py` and
  `group/features/linear_light_profiles/slam.py`. Git history: it has only ever lived in
  group/slam.py (present at the initial commit, copied into the group features when that
  directory was created). It was never in any imaging script.
- Uncapped Hilbert call sites: `group/slam.py` `source_pix_1`,
  `imaging/features/pixelization/delaunay.py`, and the S/N-based site in
  `interferometer/features/pixelization/delaunay.py` (its second Hilbert site uses
  `use_model_images=True`, a different quantity, and needs its own treatment).
- The imaging SLaM pipelines (`guides/modeling/slam_start_here.py`,
  `imaging/features/*/slam.py`, interferometer twins) use RectangularBilinearAdaptDensity /
  RectangularBilinearAdaptImage with Adapt regularization and pass the raw S/N adapt image
  through `AdaptImages`; no cap anywhere on that path.
- Regularization in group: the cap DOES reach the AdaptSplit regularization in
  group/slam.py source_pix_2, but only by aliasing. `adapt_data_snr_max` is the same
  Array2D object as the dict entry, and `AbstractNDArray.__setitem__` writes in place, so
  the `galaxy_name_image_dict` handed to `AdaptImages` is the capped image. Nothing in the
  script says so.
- Side effect of that aliasing (latent bug): the very next lines compute
  `over_sample_size_pixelization = np.where(image > signal_to_noise_threshold, 4, 2)` on
  the now-capped image, whose maximum is exactly 3.0, so the `> 3.0` test is never true and
  the adaptive over-sampling of 4 never activates in group source_pix_2 (all pixels get 2).
- `autolens_assistant/skills/al_adaptive_pixelization.md` does not mention the cap, which
  is why assistant-built pipelines (the subhalo_validation recipes, built from
  imaging/features/pixelization/delaunay.py) inherited the omission.
- Measured impact on subhalo_validation pl_eff_1_outer source_pix[2]: adapt image max S/N
  41.2; the outer images have S/N 14.8 and 11.6; with weight_power 3.5 their Hilbert weight
  is 1-3% of the core's (capped: equal). 79 mesh points within 0.3" of the brightest clump
  vs 4 at each outer image; median point spacing 0.032" at the core vs 0.181" (3.6 pixels)
  at the east outer image.

Scope (all of these):

1. Add the S/N 3.0 cap, as an explicit copy (not an alias) of the source adapt image, to
   every Hilbert image-mesh call site: imaging and interferometer
   `features/pixelization/delaunay.py`, and group `source_pix_1`. One sentence of prose per
   site saying why (prevents over-concentration of source pixels on the brightest peak so
   fainter multiply-imaged features keep resolution).
2. Use the same capped image for the rectangular adapt meshes
   (RectangularBilinearAdaptImage / AdaptDensity paths) in slam_start_here.py and every
   imaging / interferometer / multi_dataset / multi_galaxy SLaM pipeline: the user's
   decision is that bright galaxies must not be over-weighted there either.
3. Put the capped image into the `AdaptImages` `galaxy_name_image_dict` deliberately, so
   Adapt / AdaptSplit regularization adapts to the capped image on every pipeline (group
   today only gets this by aliasing). Keep the raw S/N image for anything that needs it.
4. Fix the group source_pix_2 over-sampling bug: evaluate the `> signal_to_noise_threshold`
   over-sample map on the raw (uncapped) S/N image before capping, or on a copy.
5. Docs at every site (user, 2026-09-02: "Obv both should include docs"): the prose cell
   above each cap says what is capped, at what, and why (fainter multiply-imaged features
   keep mesh resolution and regularization weight); update the workspace docs page(s) on
   adaptive pixelizations / SLaM and the autolens_assistant skill(s)
   (`al_adaptive_pixelization.md` and the SLaM `source_pix` skill) so generated pipelines
   carry it.
6. Regenerate notebooks for every touched script; smoke the touched pipelines. Scope is
   every SLaM pipeline file (slam_start_here.py, group/slam.py and copies, multi_galaxy/slam.py,
   every features/**/slam*.py across imaging, group, interferometer, multi_galaxy,
   multi_dataset) plus the Delaunay feature examples, not only the group scripts.

Out of scope: the subhalo_validation recipes themselves (project-side, handled with the
rerun ruling in PyAutoCortex); any library change to bake the cap into autoarray (a
follow-up question, not this task).

Where it came from: PyAutoCortex phase
phases/subhalo_validation/delaunay_adapt_split_pl_eff_1_outer.md (awaiting a rerun ruling);
figure of the uncapped adapt image with the Hilbert points sent to the human 2026-09-02.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/78dd3d8b-d65e-4d83-a0db-4c41bd18f3d6/scratchpad/intake_adapt_image_cap.md -->
