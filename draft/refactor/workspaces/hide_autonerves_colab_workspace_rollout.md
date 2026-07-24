# Remove direct `autonerves.setup_colab` imports from workspace examples

Type: refactor
Target: workspaces
Repos:
- @autofit_workspace
- @autogalaxy_workspace
- @autolens_workspace
- @HowToFit
- @HowToGalaxy
- @HowToLens
Difficulty: large
Priority: normal
Status: formalised

Roll out the revised PyAutoHands Colab setup cell across all six Colab-enabled
workspace and HowTo repositories after the bootstrap/template phase lands.

## Original request

> autonerves should not be user facing API, but it is in many workspace examples: from autonerves import setup_colab   , update it so its not, but make sure the colab install still uses it as it needs the right install rhere I think.

> this is prob requied for PyautoGalaxy too

## Requirements

- Update the hand-written setup sections in the PyAutoGalaxy and PyAutoLens
  workspace source scripts to use the same public/private boundary as the
  generator.
- Regenerate notebooks through PyAutoHands; never hand-edit generated
  `.ipynb` files.
- Cover `autofit_workspace`, `autogalaxy_workspace`, `autolens_workspace`,
  `HowToFit`, `HowToGalaxy`, and `HowToLens`.
- Include PyAutoGalaxy explicitly.
- Verify no user-facing script or notebook still contains
  `from autonerves import setup_colab`.
- Run each repository's size guard where present, generated-artifact checks,
  and the relevant smoke/navigator checks.

## Dependency

This rollout follows
`draft/refactor/pyautohands/hide_autonerves_colab_bootstrap_api.md`; generation
must use that phase's accepted PyAutoHands implementation.
