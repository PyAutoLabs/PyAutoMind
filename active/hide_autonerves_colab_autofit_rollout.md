# Remove direct `autonerves.setup_colab` imports from AutoFit examples

Type: refactor
Target: autofit_workspace
Repos:
- @autofit_workspace
- @HowToFit
Difficulty: medium
Priority: normal
Status: formalised

Regenerate the PyAutoFit workspace and HowToFit notebooks with the product-level
Colab setup API introduced by PyAutoHands#195.

## Original request

> autonerves should not be user facing API, but it is in many workspace examples: from autonerves import setup_colab   , update it so its not, but make sure the colab install still uses it as it needs the right install rhere I think.

> this is prob requied for PyautoGalaxy too

## Requirements

- Regenerate notebooks through merged PyAutoHands; never hand-edit `.ipynb`.
- Use `autofit.setup_colab` as the non-Colab public API while retaining the
  private `autonerves` fresh-Colab bootstrap.
- Regenerate all `autofit_workspace` and `HowToFit` notebook/catalogue outputs
  expected by their build targets.
- Run smoke/navigator checks and assert neither repo contains
  `from autonerves import setup_colab` afterward.

## Dependency

- PyAutoHands#195 and PyAutoHeart#107 are merged.
