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
