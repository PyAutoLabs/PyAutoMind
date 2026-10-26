## workspace-prior-copies
- issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/90
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/91
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/164
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/38
- workspace-pr: https://github.com/PyAutoLabs/autocti_assistant/pull/38
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/131
- completed: 2026-10-26
- summary: Applied remaining Galaxy #618 config-copy corrections across six roots in five repositories. Independent audit: 496 YAML files parse without duplicate keys, 54 mappings match intended transformations, six scatter moves preserve values, 30 model checks pass. HowToGalaxy: 32 executed scripts passed (39 discovered); Galaxy test workspace: 43 passed. Two identical pre-existing radius_break duplicates were removed without changing values. Euclid copies were untouched.
- close-out: Human invoked /prm; every applicable CI run/job was green and all claimed branch tips are contained in main.
- cleanup-approval: Human approved deletion of completed-task worktrees and outputs.
- human-review: Merged unchanged, confirmed explicitly in this session.

## Original prompt

# Sync remaining workspace config/priors copies

Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/90
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
Status: issued
Consequence: glance
Witness: A diff of every listed `config/priors` copy (HowToGalaxy, both autogalaxy_workspace_test copies, the three assistants) against the packaged PyAutoGalaxy `config/priors` shows none of the #618 dead rows (the `ersic` typo, `NFWTruncatedMCRScatterLudlowSph`, the orphan `chameleon.yaml`/`eff.yaml`, `PointSourceChi`, `SersicCoreSph.mass_to_light_ratio`, linear-operated `Gaussian.intensity`, Voronoi in `mesh/README.md`), each repo's `general.yaml`/`plots_search.yaml` carries the replacements for the readerless keys, and the euclid pipeline copy is untouched.
Review-minutes: 3
Unattended: ready

Remaining config/priors copies still carry the drift rows fixed by PyAutoGalaxy#618. PR #619 fixed the packaged `autogalaxy/config/priors/` and the workspace PRs on #618 re-synced autolens_workspace, autogalaxy_workspace, HowToLens and autolens_workspace_test. The same dead rows (`ersic` typo in `light/operated/sersic.yaml`, `NFWTruncatedMCRScatterLudlowSph` under `nfw_truncated_mcr.yaml`, orphan `light/linear/chameleon.yaml` + `eff.yaml`, `PointSourceChi`, `SersicCoreSph.mass_to_light_ratio`, linear-operated `Gaussian.intensity`, Voronoi in `mesh/README.md`) still exist verbatim in: `HowToGalaxy/config/priors`, `autogalaxy_workspace_test/config/priors` and its second copy `autogalaxy_workspace_test/scripts/misc/aggregator/config/priors`, `autolens_assistant/config/priors`, `autogalaxy_assistant/config/priors`, `autocti_assistant/config/priors`. Apply the same edits (as edits, not blind copies; check each repo's `general.yaml` for the readerless `fits.flip_for_ds9` and `visualize/plots_search.yaml` for the unread per-search `dynesty:/emcee:/nautilus:/zeus:` form, replace with PyAutoFit's `nest/mcmc/mle` file). `euclid_strong_lens_modeling_pipeline` keeps its copy by design (euclid#43). Also note `autogalaxy_workspace/config/priors/ellipse/ellipse_multipole.yaml` has no `EllipseMultipoleScaled` block (falls through to the packaged one; informational). Consider a shared parity check that diffs every workspace `config/priors` against the packaged PyAutoGalaxy copy.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from user-intake -->
