# Sync remaining workspace config/priors copies

Type: maintenance
Target: workspaces
Repos:
- HowToGalaxy
- autogalaxy_workspace_test
- autolens_assistant
- autogalaxy_assistant
- autocti_assistant
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready

Remaining config/priors copies still carry the drift rows fixed by PyAutoGalaxy#618. PR #619 fixed the packaged `autogalaxy/config/priors/` and the workspace PRs on #618 re-synced autolens_workspace, autogalaxy_workspace, HowToLens and autolens_workspace_test. The same dead rows (`ersic` typo in `light/operated/sersic.yaml`, `NFWTruncatedMCRScatterLudlowSph` under `nfw_truncated_mcr.yaml`, orphan `light/linear/chameleon.yaml` + `eff.yaml`, `PointSourceChi`, `SersicCoreSph.mass_to_light_ratio`, linear-operated `Gaussian.intensity`, Voronoi in `mesh/README.md`) still exist verbatim in: `HowToGalaxy/config/priors`, `autogalaxy_workspace_test/config/priors` and its second copy `autogalaxy_workspace_test/scripts/misc/aggregator/config/priors`, `autolens_assistant/config/priors`, `autogalaxy_assistant/config/priors`, `autocti_assistant/config/priors`. Apply the same edits (as edits, not blind copies; check each repo's `general.yaml` for the readerless `fits.flip_for_ds9` and `visualize/plots_search.yaml` for the unread per-search `dynesty:/emcee:/nautilus:/zeus:` form, replace with PyAutoFit's `nest/mcmc/mle` file). `euclid_strong_lens_modeling_pipeline` keeps its copy by design (euclid#43). Also note `autogalaxy_workspace/config/priors/ellipse/ellipse_multipole.yaml` has no `EllipseMultipoleScaled` block (falls through to the packaged one; informational). Consider a shared parity check that diffs every workspace `config/priors` against the packaged PyAutoGalaxy copy.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from user-intake -->
