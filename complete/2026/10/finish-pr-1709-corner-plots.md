## finish-pr-1709-corner-plots
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1710
- completed: 2026-10-21
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1709
- scope recorded: phase 1 (PyAutoFit) only. Phases 2 and 3 re-filed as `draft/feature/autogalaxy/latent_parameter_declarations_pr1709_phase2.md` and `draft/docs/workspaces/corner_plot_config_keys_pr1709_phase3.md`
- summary: Community PR by @samlange04 (proposal .github#38) merged as d3a772129. Maintainer commit f9377f3f6 was pushed onto the contributor's branch instead of another review round. It resolves review findings 1–8:
  - per-component plots follow corner_anesthetic when unconfigured;
  - a raising latent conversion is logged, and the latent plots are skipped in test mode;
  - new output.yaml latent_model_parameters switch;
  - unique, consistently cut deep-path superscripts (superscripts_from_component_paths);
  - shared priors converted for every holder (_prior_holders);
  - Periodic latents recentred for plots only (latent.csv keeps the conversion range);
  - "model_root" group when a component is named model;
  - component paths frozen-cached.
- validation: test_autofit 3881 passed; 13 new or changed tests fail on bf43aa623; smoke 165/165 (autocti envs not built locally, missing GSL); independent review (same model family, stage 1) found no code defects; exact-head CI 3.12/3.13/no-JAX/docs green.
- heart: readiness STALE, monitoring feed RED. Development-only override ("do 2, Override and proceed"); merge by the human's separate /prm with all checks green.
- traps:
  - Pushing to a fork PR triggers only pull_request runs, never push runs.
  - The auto-mode classifier denied `gh pr merge`; the human merged with `! gh pr merge`.
  - Mind's prompt_sync_push stages everything (`git add -A`) and would have swept an unrelated local policy/hpc_ral.md edit, so task files were committed explicitly.
- decision to revisit: latent.results summaries of an angle straddling its branch cut are split, because latent.csv is no longer recentred (documented in output.yaml).

## Original prompt

# Finish community PR PyAutoFit#1709…

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoGalaxy
- autolens_workspace
- HowToGalaxy
- HowToLens
Difficulty: too-large
Autonomy: supervised
Priority: high
Memory: wiki/galaxies/sources/massive-ellipticals.md; reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md
Status: formalised
Issued: 2026-10-21
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1710
Consequence: glance
Witness: PyAutoFit PR #1709 CI green with new tests for (i) `corner_anesthetic: false` and the components key absent writes no per-component plots, (ii) a raising latent conversion logs instead of propagating from the final visualize, (iii) a power law's ell_comps linked into a multipole still yields the mass's axis_ratio/angle latents, (iv) deep-path labels stay unique
Review-minutes: 3
Unattended: needs-slicing

# Finish community PR PyAutoFit#1709 (corner plots: per-component labels, per-component plots, latent-parameter corner plot) — maintainer applies the review changes

Community PR https://github.com/PyAutoLabs/PyAutoFit/pull/1709 by @samlange04 from proposal https://github.com/PyAutoLabs/.github/discussions/38 (Ideas & Proposals). Maintainer decision 2026-10-21: (a) superscripts become the component's dot-joined path everywhere including `model.results` text; (b) the latent corner plot stays a separate plot, switched from config (`visualize/plots_search.yaml` `nest.corner_anesthetic_latent`, default off), written next to `corner_anesthetic.png` inside PyAutoFit. The maintainer will push the review fixes onto the contributor's branch (as done for PyAutoGalaxy#635) and merge, rather than asking for another round. user-facing: post a progress update on the PR and the discussion, mark the discussion verdict as the answer, and update the contributor on release.

## Review findings to resolve (PR head bf43aa623; 91 targeted tests pass, 158 across the touched test files)

1. Per-component plots ignore `corner_anesthetic` and default on when `corner_anesthetic_components` is absent (`posterior_kind.py:134-146`) → fall back to the `corner_anesthetic` value.
2. `latent_parameters_from` in `plot_latent_results` (`posterior_kind.py:173`) runs outside `@log_plot_exception`; updater catches only `FileNotFoundError` (`updater.py:239`) → guard like `_model_latent_parameters`; also respect test mode.
3. Model latents appended to `latent/samples.csv`, `latent.results`, `latent_summary.json` with no switch (`analysis/latent.py:165,277,380`) → add a key in `output.yaml`'s latent block (default on); give per-component latent plots their own control or document the coupling to `corner_anesthetic_components`.
4. Deep-path 3-char truncation collides (`lens.bulge_inner.shear` / `lens.bulge_outer.shear` → `lens.bul.she`; shared-centre basis reads `lens.bulge` and `lens.bul.0`) (`abstract.py:181`) → truncate only while unique.
5. Shared prior between differently named components follows the last holder (`_prior_owner_and_leaf_names`, `abstract.py:2557`): power-law ell_comps linked into a multipole can drop the mass's latents → declarations must see shared priors from every holder; add the test.
6. Periodic recentring writes a fit-dependent angle branch into `latent.csv` → decide (recommend: recentre for plots only) and document.
7. Docs: `notation.yaml` `superscript:` block now applies only to a bare unnamed `Model` → update comments in PyAutoGalaxy and the three workspace `notation.yaml`, release note; land workspace `plots_search.yaml` key PRs (contributor has branches `feature/corner-plot-labels` on autofit/autogalaxy/autolens_workspace, HowToLens, HowToGalaxy) and PyAutoGalaxy `feature/latent-parameters`.
8. Minor: component literally named `model` collides with root group; cache `component_paths`.

## Delivery

PyAutoFit first (push onto contributor's branch `samlange04:fix/corner-anesthetic-duplicate-labels`, merge #1709), then PyAutoGalaxy latent declarations PR, then workspace config/docs PRs after release (workspace smoke CI installs the released library).

<!-- formalised by the Intake (Conception) Agent on 2026-10-21 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/16b1291e-5d7e-43ae-8250-0eea830cc6ed/scratchpad/intake1709.md -->
