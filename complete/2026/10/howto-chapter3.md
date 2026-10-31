# Chapter 3 reviewed pixelization lessons — merged checkpoint

- issue: https://github.com/PyAutoLabs/HowToLens/issues/111
- completed: 2026-10-31
- cleanup: user authorized removal; completed worktree and local feature branches removed; review copies preserved
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/112
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/95
- summary: Merged the reviewed Chapter3 checkpoint in both HowTos; preserved the remaining Lens adaptive work as a separate follow-up.

## Shipped — 2026-10-31

Both approved Chapter 3 PRs are merged:
- https://github.com/PyAutoLabs/HowToLens/pull/112 — merge `5249e06ae2383ba4f56004c38d7aee37a364a878`.
- https://github.com/PyAutoLabs/HowToGalaxy/pull/95 — merge `06876fe8e6fd71ee3946485ed56dd1f3a27f834e`.

Every workflow and job on both heads passed: 3 workflows / 8 jobs per PR, including Python 3.12 and 3.13 smoke. Local smoke: Lens44/44, Galaxy29/29. Notebook generation and independent review passed. Chapter2 is unchanged.

This closes the reviewed checkpoint: Lens lessons1–4 and Galaxy lessons1–3, detailed MGE introductions, mapping/inversion explanations, regularization, chained fits and Maresca Figure1. The existing Lens adaptive tail is retained; Delaunay/Hilbert/Split consolidation and the final Delaunay fit remain a separate five-block-review follow-up, recorded in Mind. Heart RED is not cleared by these merges.

## Resume checkpoint

Approved prose and code are now in main. Do not repeat review of the merged lessons or modify Chapter2. Continue the remaining Lens adaptive sequence in five-block reviews with actual Python code, using current Delaunay, Hilbert image mesh and Split regularization, with phenomenological explanations and a final Delaunay fit. See `draft/docs/howto/chapter_3_adaptive_continuation.md`.

The generated notebooks, original review drafts and checkpoint are preserved at `C:\Users\Jammy\Workspace\Science\scratch\chapter_3_implementation_2026-10-31`. Full search convergence is not claimed by sampler-bypass smoke. The separate Galaxy Chapter2 branch should integrate these changes and regenerate shared catalogues.

## Original prompt

# Chapter 3 pixelizations restructure — checkpoint

Date: 2026-10-31
Targets: @HowToLens @HowToGalaxy (Chapter 3 only)
Type: docs
Status: workspace-dev — implementing approved blocks
Issue: https://github.com/PyAutoLabs/HowToLens/issues/111
Issued: 2026-10-31
Consequence: judge — merge mode: human /prm

## Actual state

- The human requested `ok prm and checkpoint` after approving the revised chapter introductions.
- Queried open PRs in PyAutoLabs/HowToLens and PyAutoLabs/HowToGalaxy: both empty.
- Both tutorial checkouts are clean on main. No tutorial edits, task branch, task issue, tests, rendered comparisons or generated notebooks exist for this task.
- This record is a local draft checkpoint, not a completed or shipped task. Do not mark the work complete or imply that /prm merged anything.
- The approved prose and Python cells are in the originating Codex chat. Read that chat before applying exact wording; the summaries below are not replacements for the approved text.
- Earlier Heart RED authorization was specifically for read-only research and restructuring proposals. Do not treat it as a development-shipping override. Recheck current Heart before implementation.

## Review contract and approvals

- Structure approved before edits. Review prose and accompanying Python in batches of five coherent blocks; apply only approved blocks.
- User prefers the original tutorials' patient, conversational explanations. Preserve core scientific intuition and indexed demonstrations; remove likelihood derivations, not the teaching detail.
- Tutorial 2 blocks 6–10: use the ORIGINAL LONG version. The shorter revision was explicitly superseded: `ok go back to the original high amount of text, we can refine this later, and then keep going in terms of blocks`.
- Chapter 2 must remain unchanged. MGE is the baseline analytic modelling method.
- Scripts are canonical; regenerate notebooks and navigator/catalogue through the established Hands process after editing and validation.

## Final chapter scope

HowToLens:
1. Pixelized source reconstruction: merge original tutorials 1, 2 and 3. Keep indexed mappings, matching image/source coordinate groups, source mesh contributions and interpolation weights, multiple images, reconstruction vector values, pre/post-PSF image reconstruction and residuals.
2. Interpolation and Bayesian regularization: use original tutorial 4's narrative as backbone. Absorb only essential conceptual material from tutorial 5; link the workspace likelihood_function.py instead of reproducing matrix construction and evidence derivations.
3. Borders and source coverage: shorten original tutorial 6, retaining circular/annular comparison, indexed central coordinates, border tracing, relocation on/off and mask coverage experiments.
4. Lens modelling: original tutorial 7, including incorrect-mass/demagnified examples, MGE initialization, positions constraint, chained pixelized fit, and a TWO-BLOCK runnable foreground-light chain.
5. Adaptive Delaunay reconstruction: merge original 11 and 12 and the essential concepts of original 8. Introduce a concise motivation for resolution/smoothing limitations here.
6. Complete Delaunay model fit: finish with a real search, residual inspection and uncertainty interpretation.

The standalone fit-problems tutorial proposed as new tutorial 5 was CANCELLED by the human. Its five draft blocks are NOT to be implemented. Renumber the remaining lessons accordingly. Original tutorial 9_model_fit and standalone tutorial 8_adaptive_pixelization are removed.

HowToGalaxy: shared introductory reconstruction and regularization changes; retain a galaxy-specific modelling culmination. No lens mass, source-plane or SLaM claims in its introduction. Detailed later HowToGalaxy blocks have not yet been reviewed.

## Tutorial approvals in originating chat

- Tutorial 1 original blocks 1–10 approved, then five restoration blocks approved. Integrate restorations into the tutorial, not as an unrelated appendix. Restored mapper/inversion concepts take precedence over the earlier overly compressed account.
- Tutorial 2 revised, expanded blocks 1–5 approved; original long blocks 6–10 approved. Preserve interpolation versus regularization, weak/strong coefficient experiments, evidence interpretation, scan, linear/non-linear distinction and resolution experiment.
- Tutorial 3 blocks 1–10 approved, including current elliptical border treatment and limitations.
- Tutorial 4 blocks 1–5 approved with Maresca FIGURE 1 ONLY embedded high in the notebook after opening motivation, before experiment. Attribute Maresca, Dye & Li (2021), link https://arxiv.org/abs/2012.04665. No Figure 2. Figure 1 shows under-magnified, correct and over-magnified solutions.
- Tutorial 4 blocks 6–10 approved, with one short sentence in block 8 emphasizing that PositionsLH prevents the demagnified solutions by penalizing failed source-plane consistency. Avoid claiming search chaining or .instance alone supplies this protection.
- Tutorial 4 foreground blocks 11–15 were REJECTED as excessive. Replace with the two subsequently approved blocks: actual initial foreground+analytic-source fit, then pixelized fit carrying foreground shapes via .instance and mass/shear via .model.
- All analytic lens/source fitting components throughout tutorial 4 must use MGE, superseding the displayed Sersic code. Human approved the text subject to this replacement. MGE Gaussian intensities remain linearly solved when .instance fixes Gaussian geometry.
- Current chapter introductions below approved by the final `ok prm and checkpoint`.
- Adaptive Delaunay lesson and final Delaunay fit blocks remain to be drafted/reviewed.

## Implementation grounding and unresolved validation

- Current RectangularUniform already interpolates bilinearly. There is no standalone RectangularBilinear class in the checked source. User explicitly dropped the non-interpolating progression. Do not add a new mesh class.
- Introductory mesh: RectangularUniform. Constant regularization on rectangular meshes; Split belongs to irregular meshes.
- Delaunay/Hilbert/AdaptSplit reference: autolens_workspace/scripts/imaging/features/pixelization/delaunay.py. Default SLaM entry example currently uses rectangular meshes; do not describe all SLaM as Delaunay.
- Hilbert controls image-plane mesh placement; ray tracing makes source nodes. Current example caps adapt-image S/N at 3 and uses edge points. Explain physical purpose without teaching algorithm internals.
- Split describes local smoothness using interpolated points; AdaptSplit additionally varies smoothing with source signal. They are not synonyms.
- Source plane data coords, source mesh indexes, interpolation support, image pixels, and source brightness entries must remain distinct in narrative and plots.
- mapped_reconstructed_operated_data is the blurred IMAGE reconstruction, not the source reconstruction. Use plot_mapper(solution_vector=...) for source maps.
- BorderRelocator currently estimates an ellipse from traced border coordinates; old docstrings claim nearest-border relocation. Ground in executable source.
- Source_complex simulator has no shear; lens_sersic and simple__no_lens_light have shear. Match simulator truth in controlled experiments. Older tutorial code contains mismatches.
- Draft code has NOT run. Validate live APIs, solve/plot results, source sampling, simulator accuracy, finite evidences, search convergence, MGE instance semantics and sensible automatically generated positions. Do not preserve unsupported statements about specific fit outcomes.
- Do not compare raw evidence across different datasets/masks. A coefficient scan is conditional, not a posterior or uncertainty estimate. Avoid guarantees that evidence/regularization/borders remove all bias.
- Use current al.model_util.mge_model_from, following SLaM: lens total_gaussians=20, gaussian_per_basis=2, centre_prior_is_uniform=True, sigma_min=pixel_scale/10; source total_gaussians=20, centre_prior_is_uniform=False. Inspect actual helper/current chapter 2 before implementation; do not edit chapter 2.

## Approved HowToLens introduction

Look at a resolved lensed arc. Its broad shape may be smooth, but the light along it can contain bright knots, faint extensions and irregular structure. A model might reproduce the overall arc while leaving compact, coherent features in the residual image.

In Chapter 2, we introduced linear light profiles and multi-Gaussian expansions (MGEs). By combining Gaussians of different widths, an MGE can describe a much more flexible radial brightness distribution than a single Sérsic profile. Gaussian groups with different ellipticities and orientations can also describe changes in flattening and isophotal twists. Fixed widths and linearly solved intensities keep the number of non-linear parameters manageable.

That flexibility makes MGE a useful modelling tool, but consider the geometry of our worked example. Within each galaxy’s Gaussian group, the components shared a common centre and elliptical shape. Adding more Gaussians gives us finer control over how brightness changes around that centre. It does not give us separate centres for star-forming knots, off-centre clumps or several distinct source components.

We could add offset Gaussian groups. MGEs are not fundamentally restricted to one centre. The practical difficulty is deciding how many groups to use, where to place them and how to fit their geometry as the source becomes more complicated.

This is where the image residuals become useful. If an MGE captures the broad light distribution but leaves compact structure along the arcs, its source description may need more spatial freedom. Those residuals are not proof of source clumpiness: errors in the mass model, foreground light subtraction, telescope blurring or other aspects of the data treatment can also produce structure. We need to investigate their origin.

In this chapter, we introduce pixelized source reconstruction. Instead of prescribing a light-profile centre and shape for every feature, we describe the source brightness on a mesh. Different regions of that mesh can take different brightness values, allowing the reconstruction to represent more complicated source structure.

The connection to Chapter 2 is direct. There, we solved for Gaussian intensities linearly. Here, for a specified mass model and mesh, we solve for source brightness values using the same underlying advantage: they enter the predicted image linearly.

This additional freedom also allows the reconstruction to fit noise. We therefore introduce regularization—a prior that controls how freely neighbouring source brightnesses can vary. Pixelization is not assumption-free: the mass model, mesh geometry, resolution and regularization all affect the inferred source.

MGE remains valuable, especially for foreground lens light and initial source fits. Pixelization is the next tool when the source requires more spatial freedom. We will learn how to use these tools together, inspect their reconstructions and recognise when their assumptions need revisiting.

## Approved HowToGalaxy introduction

Look at a resolved galaxy image. Its broad light distribution may follow a smooth bulge and disc, while smaller regions contain bright star-forming knots, off-centre clumps or irregular extensions. A model can capture the overall galaxy yet leave these features clearly visible in the residual image.

In Chapter 2, we introduced linear light profiles and multi-Gaussian expansions (MGEs). Combining Gaussians of different widths gives us a more flexible radial brightness distribution than a single Sérsic profile. Gaussian groups with different ellipticities and orientations can also describe changes in flattening and isophotal twists. Fixed widths and linearly solved intensities provide this flexibility without introducing a large number of non-linear parameters.

Our worked example nevertheless imposed a particular geometry: the Gaussians within each galaxy’s group shared a common centre and elliptical shape. Adding more Gaussians improves our control over the brightness distribution around that centre, but does not create independently positioned knots or several components with distinct centres.

We could introduce offset Gaussian groups. The limitation is not that MGEs cannot represent multiple centres, but that increasingly complicated galaxies require us to choose and fit an increasingly elaborate arrangement of components.

Suppose the MGE reproduces the smooth galaxy light but leaves compact, structured residuals. These may indicate that the model needs more freedom to describe local features. They are not automatically evidence for additional galaxy components: an inaccurate PSF, background estimate, contaminating object or other data-treatment error can also leave structured residuals.

In this chapter, we introduce pixelized reconstruction as another way to describe the galaxy’s light. We infer brightness values across a mesh without assigning a separate analytic centre and shape to every feature. The predicted image includes telescope blurring, so the reconstruction is an inferred description of the galaxy rather than simply a copy of the observed pixels.

This builds on the linear profiles of Chapter 2. Instead of solving for Gaussian intensities, we solve for the mesh brightness values. Their extra freedom can describe irregular structure, but can also fit noise. Regularization supplies a prior that controls variations between neighbouring brightness values.

The reconstruction still depends on modelling choices, including the mesh, its resolution, regularization and the treatment of the data. We will learn to inspect how those choices affect both the reconstructed galaxy and the image residuals.

MGE and other analytic profiles remain useful for describing and measuring smooth galaxy components. Pixelizations complement them when more complicated structure needs to be represented, including in models that combine analytic components with a pixelized reconstruction.

## Next action

Resume start_dev with this checkpoint and the originating chat. Do not repeat approval of accepted structure/prose. Recheck Heart and repo claims, register the task through the standard Mind issue workflow, create workspace worktrees, and apply the approved chapter introductions and reviewed lesson blocks. Draft/review remaining adaptive and final-fit content in batches of five. Validate actual figures/searches, required smoke and links, regenerate notebooks/catalogues, then open the reviewable PRs. Only then can /prm judge CI and merge; no merge was possible at this checkpoint.

## Implementation resumed — 2026-10-31

User authorized: "Yes go ahead and implement the approved changes in both HowToLens and HowToGalaxy, run the checks and get both PRs up." Explicit Heart development permission: "Proceed with implementation and validation despite Heart RED". Concurrent Galaxy claim exception: "Allow separate Chapter 3 worktree". Current chat ID: 01a19297-ff24-7bb0-87ce-437076a9d0a9. Exact approved assistant drafts recovered to `.worktrees/howto-chapter3/review/draft_*.md`.

Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/howto-chapter3`; both tutorial repos on `feature/howto-chapter3`. Only approved/reviewed material being implemented; adaptive Delaunay tail remains pending separate review. Python3.12 validation environment in worktree review/venv; activation imports local libraries. No merge authorized by current implementation request.

## Implementation checkpoint — source and notebooks ready

Approved HowToLens lessons 1–4 and HowToGalaxy lessons 1–3 are implemented on `feature/howto-chapter3` in the task worktrees. Both exact MGE introductions now appear in the first lesson and chapter README as well as the extensionless introduction file. Chapter 2 scripts and notebooks are unchanged. Lens adaptive lessons 8/11/12 are retained with necessary reference updates; their consolidation and final Delaunay fit remain pending five-block review. Only Maresca Figure 1 is included.

Validation completed: seven revised lessons pass targeted capped smoke, including chained-fit likelihood evaluation with samplers bypassed; Hands generated 45 Lens and 30 Galaxy notebooks successfully; notebook schema, tutorial completeness, navigation, search-memory lint, catalogue reproducibility and whitespace checks pass. Independent review findings (missing visible intros, terminal headings, typo) are resolved. Full repository smoke is running through Heart isolated environments; HowToGalaxy uses Heart's API with an explicit workspace specification because the CLI registry lacks that key. No full search-convergence claim is made.

Exact-head working changes are staged, not committed or pushed yet. PR body drafts and validation logs are under `.worktrees/howto-chapter3/review/`. Human-readable notebooks/checkpoint: `C:\Users\Jammy\Workspace\Science\scratch\chapter_3_implementation_2026-10-31`. Heart currently reports RED: `release validation FAILED (stage integrate)`. User's RED override covers implementation and validation; finish all branch checks before the ship gate.

## PR-open checkpoint — 2026-10-31

- HowToLens PR: https://github.com/PyAutoLabs/HowToLens/pull/112 — `cc6b8277df021c052e57f6d9d7887f866fd9774f`.
- HowToGalaxy PR: https://github.com/PyAutoLabs/HowToGalaxy/pull/95 — `a4f27b7354a6595b8df30533c14a8477502daf5a`.
- Full Heart-prepared isolated repository smoke: Lens **44 passed / 0 failed**, Galaxy **29 passed / 0 failed** (Python 3.12). Exact reports in each task worktree's `test-results/`.
- Extra full-size Galaxy regularization lesson: **39 reconstructions pass** across three meshes. Smoke search chains evaluate likelihoods with sampling bypassed; no convergence claim.
- Notebook generation **45 Lens / 30 Galaxy pass**, retaining only in-scope Chapter 3 changes. Schema/code parsing, tutorial completeness, navigation, catalogue reproducibility, search-memory lint, whitespace and independent review pass.
- Live ship override: **“Open both PRs despite Heart RED”**. Exact current RED reasons: **“PyAutoFit: 2 commit(s) behind origin”**; **“release validation FAILED (stage integrate)”**. Recorded on issue #111, both PR bodies, active.md and autonomy_log.md. No merge/release authorized.
- Both source worktrees clean after commits/pushes. Chapter 2 source/notebooks untouched. Separate Galaxy Chapter 3 worktree exception remains valid; regenerate shared catalogues after integrating the Chapter 2 branch.

Next: human `/prm` judges required GitHub CI and merges this approved checkpoint. Continue the remaining Lens adaptive/Delaunay/Hilbert/Split material and final fit through five-block review; existing adaptive lessons retain their numbering until then. No scheduled CI watcher.
