# Resume: paired HowToLens / HowToGalaxy tutorial review

Saved: 2026-10-31. Status: approved source work complete through Lens Tutorial 2; shipping blocked; edits are uncommitted.

## Shipping retry — 2026-10-31 (current status)

- Human explicitly authorized `/prm` and Heart RED override: “I approve you to prm and override heart RED”. Exact Heart reason: `release validation FAILED (stage integrate)`.
- Tracking issue now exists: https://github.com/PyAutoLabs/HowToLens/issues/103; task record `active/howto_paired_review_ship.md`; both worktrees claimed under `howto-paired-review`.
- Isolated Python 3.12 environments successfully built through Heart using CI install recipes. Reuse `scratch/ship/heart/smoke-envs/{howtolens,howtogalaxy}/py3.12` under workspace root. HowToGalaxy required explicit WorkspaceSpec through Heart functions because its CLI key is missing.
- Five changed notebooks regenerated with Hands functions; both catalogues regenerated. Notebook structural validation and code/source parity pass. Navigator path/banner checks pass.
- Full runtime results: HowToLens 48 passed / 2 failed; HowToGalaxy 31 passed / 1 failed. Both Tutorial 1 scripts pass. Failure details: Tutorial 0 in BOTH courses passes unsupported `figsize` to public `aplt.plot_array`; Lens Tutorial 2 passes unsupported `extent` to `aplt.plot_grid`, whose wrapper also lacks `indexes`.
- Root cause: reviewed low-level autoarray.plot signatures differ from public autogalaxy.util.plot_utils wrappers exported by aplt. Underlying functions support these options. Fix proposal: size Tutorial 0 through explicit Matplotlib axes; use autoarray.plot.plot_grid for Tutorial 2 zoom/mappings. No library changes needed.
- Per ship workflow, stopped on failed smoke without modifying source to evade the gate. No tutorial commits, pushes, PRs or merges. Generated work remains uncommitted alongside accepted scripts.
- Logs: `.worktrees/howto-paired-review/scratch/ship/{lens-smoke,galaxy-smoke,generation}.log`; structured results in each tutorial repo's `test-results/`. Review bundle now includes notebooks/catalogues, updated patches and `VALIDATION.md`.
- NEXT: correct plotting calls, regenerate the affected notebooks, rerun applicable validation, ship both repos and invoke `/prm` with green checks. Tutorial 3–5 human rewrite remains pending and outside this phase. Current-turn merge authority expires at turn end; do not arm automation.

## Latest checkpoint — 2026-10-31 (supersedes the resume point below)

- Human requested `/prm all our work` before making larger changes to Tutorials 3, 4 and 5. Scope to ship: HowToLens Tutorials 0–2 and HowToGalaxy Tutorials 0–1 only.
- HowToLens Tutorial 2 source review is complete and all approved edits are applied. Both schematic and COSMOS-Web Ring image are included. Early prose uses “lensed image”; avoid PSF/unblurred terminology until introduced.
- Deflection magnitude for IsothermalSph is constant away from the centre. Reduced-deflection discussion is explicitly deferred to Tutorial 3 (not yet written).
- Tutorial 2 now has an unheaded central-source-plane zoom before Mappings. Mappings follows Ray Tracing Grids, with three groups of five fixed slim indexes, shared colours and full default extents; prose invites zooming with `extent`. Tracer grid access stays near the end without duplicate plots. Wrap-up and contents updated.
- Tutorial 3 first five blocks were proposed in chat but NEVER approved or applied. Tutorials 3–5 remain untouched; human plans broader edits before resuming review.
- `/prm` did not ship or merge: no commits, pushes, PRs or issue registration. Five source scripts remain uncommitted in the existing feature/howto-paired-review worktrees.
- Fresh Heart readiness at 2026-10-31T12:13:10 UTC: RED; exact sole red reason: `release validation FAILED (stage integrate)`. Earlier permission to develop is not evidence of passing ship gates.
- Syntax checks pass for all five modified scripts; git diff --check passes in both repos. Tutorial 2 contents match headings in order; control-character check passed.
- Full runtime/smoke validation is missing. Shell Python 3.10 cannot run current stack. Available Python 3.12 cannot load system NumPy C extensions and lacks JAX/dill. No environment packages were installed.
- Notebook/catalogue generation has not run: PyAutoHands requires `ipynb-py-convert`, absent from PATH. Do not claim notebooks are current.
- Mappings preview used analytic SIS + NumPy/Matplotlib, matching plotted marker colours/sizes; all 15 displacements checked at 1.6 arcseconds. It is not PyAutoLens runtime evidence. Human accepted preview.
- Review bundle (source copies + binary-capable patches): `/mnt/c/Users/Jammy/Workspace/Science/scratch/howto_paired_review_ship_2026-10-31/`. Authoritative edits remain in worktrees.
- Next shipping step: supply supported runtime and notebook converter; regenerate using Hands, run required validation, resolve current Heart gate, then ship both repos and re-run `/prm` on green checks. Preserve earlier approvals and uncommitted edits; do not clean worktrees.



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
