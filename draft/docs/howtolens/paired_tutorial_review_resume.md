# Resume: paired HowToLens / HowToGalaxy tutorial review

Saved: 2026-10-30. Status: paused at the user's request to wrap up; source edits are uncommitted.

## Intent and review contract
Review the courses together, following HowToLens order and pairing corresponding HowToGalaxy material by topic. One integrated review of prose, code, comments and factual accuracy; exploit shared structure without imposing lensing material on Galaxy. Show the full proposed text and associated code for FIVE coherent blocks at a time in chat, then apply after approval. Do not return to whole-tutorial batches or require clicking files to read proposals.
The user approved the overall plan and explicitly authorised development despite Heart RED. No merge/release authorisation. Use Brain's docs workflow and TUTORIAL_WRITING_STYLE.md. No dedicated docs conductor exists. No subagents have been used.

## Actual working state
- Worktree root: /home/jammy/Code/PyAutoLabs/.worktrees/howto-paired-review
- HowToLens and HowToGalaxy are real worktrees on feature/howto-paired-review; main checkouts remain untouched.
- Each has modified scripts/chapter_1_introduction/tutorial_0_visualization.py and tutorial_1_grids_and_galaxies.py.
- No task issue, active.md claim, PR, commit or push has been created. Workflow registration remains outstanding; do not claim it is complete.
- Internal helper scripts under the bundle's review/ are implementation temporaries, not deliverables.

## Completed and accepted
Tutorial 0 source review accepted. Shared directory, simulation, loading, plotting and customization guidance; Lens overlay identified as a separate illustrative unblurred lens image; Galaxy mask preserves dataset; contents aligned and Ask AI prompt added.
Tutorial 1 introductions and all blocks through 43 applied and accepted. Source prose/code review complete in both courses. Images now use autolens_assistant/docs/images/strong_lens_schematic.png and cosmos_web_ring_rgb_labelled.png; explain the extra galaxy without assigning its distance, and defer multiple-galaxy lenses to Chapter 4.
Grid sections distinguish pixel centres from edges, fix indexing, explain native/slim, and provide controlled experiments. Geometry copies grids, explains reference frames and clockwise inverse rotation, and fixes elliptical radius to sqrt(x^2 + (y/q)^2). Ellipticity ordering checked against convert.py.
Manual Sérsic calculation now includes intensity, uses circularised radius sqrt(q)*eta to match the implementation, identifies k=2n-1/3 as approximate, and explains effective radius. Library profile and Array2D blocks clarified. Radial sampling uses explicit major-axis coordinates, with distances measured from profile centre; intensity axis replaces incorrect luminosity label.

## Agreed terminology (carry through all later blocks)
Model = simplified mathematical description. Light-profile image = a single profile before PSF convolution. Galaxy image = summed profiles before convolution. Model image = observation-level prediction including PSF, suitable for comparison to data; it does not imply a completed fit and does not include added random noise. Lensing-only illustrations use “unblurred lensed image”. This correction has been applied across Tutorials 0 and 1.

## Exact resume point
Tutorials 0 and 1 are fully reviewed and accepted in both courses at source level. Final blocks 39–43 were explicitly approved and applied. No proposed blocks remain pending.
Next lesson in HowToLens order: scripts/chapter_1_introduction/tutorial_2_ray_tracing.py. HowToGalaxy tutorial_2_data.py is NOT its counterpart; defer the Galaxy data lesson until pairing it with HowToLens tutorial_6_data.py. Inspect topic correspondence rather than forcing unrelated lessons together.

## Latest user preferences and applied corrections
Review FIVE blocks at a time, with full prose and associated code in chat before editing. Preserve the original patient teaching tone and useful explanatory context; do not over-compress. Avoid unnecessary PSF mentions in early material and unsolicited foreshadowing. User specifically retained the original Lens paragraph explaining that lens/source redshifts differ while this tutorial builds intuition with a single Galaxy.
Blocks 25–43 include clearer log-colour motivation; kpc conversion corrected to ~3260 light-years; shared bulge/disc radial grid and intensity labels; accurate Galaxies grouping explanation; subplot_galaxy_images replaces subplot_galaxies (the latter plots lensing quantities); actual bulge radius conversion; corrected AB calibration and oversampling notes; linked actual workspace guide paths; matched contents; Ask AI prompt.

## Evidence, outstanding checks and risks
Syntax checks (ast.parse), exact contents-to-section-heading checks and git diff --check passed for all four edited scripts at this final checkpoint. Runtime imports blocked: shell python3 is 3.10, current stack requires >=3.12, missing dill (also JAX absent). Do not claim tutorial execution or rendered-image verification. Locate a supported existing environment before final validation; do not install or bypass blindly.
No notebooks/catalogues regenerated yet; use PyAutoHands after the source review. No full smoke runs. Mathematical corrections still need meaningful numerical/runtime validation.
Student findings source: PyAutoMind/draft/docs/howtolens/tutorial_correctness_and_howtogalaxy_parity.md. Source docstring issues (q squared, inverse axis ratio, circularised radius vs circular aperture) were observed; library sources were NOT edited.
The radial-grid helper in uniform_2d.py rotates clockwise. Explicit sin/cos coordinates avoid misalignment with the anticlockwise profile angle. The component radial comparison now uses one explicit x-axis grid, appropriate to the shared centre and angle of the actual example.
Earlier scratch tutorial0 copies are snapshots; worktree sources are authoritative. Refresh previews before using them.

## First steps next session
Read this note and applicable instructions; inspect both worktrees and active claims; retain prior approvals. Complete missing task registration within the established workflow. Resume the five-block conversation at HowToLens Tutorial 2: Ray Tracing. Apply only approved text/code and keep a clear distinction between static checks and actual execution.
