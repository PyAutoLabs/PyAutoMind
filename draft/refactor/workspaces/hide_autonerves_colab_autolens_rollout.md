# Remove direct `autonerves.setup_colab` imports from AutoLens examples

Type: refactor
Target: autolens_workspace
Repos:
- @autolens_workspace
- @HowToLens
Difficulty: large
Priority: normal
Status: formalised

Roll out the product-level Colab setup API across the PyAutoLens workspace and
HowToLens after the PyAutoHands bootstrap change merged in #195.

## Original request

> autonerves should not be user facing API, but it is in many workspace examples: from autonerves import setup_colab   , update it so its not, but make sure the colab install still uses it as it needs the right install rhere I think.

> this is prob requied for PyautoGalaxy too

## Requirements

- Update the eight hand-written setup sections in `autolens_workspace`
  (`start_here.py` plus cluster/group/imaging/interferometer/multi/point_source/
  weak `start_here.py`) to use the merged public/private boundary.
- Resolve `setup_colab` through `autolens` outside Colab while retaining the
  private `autonerves` fresh-Colab bootstrap.
- Regenerate notebooks through merged PyAutoHands; never hand-edit `.ipynb`.
- Regenerate all `autolens_workspace` and `HowToLens` notebook/catalogue
  outputs expected by their build targets.
- Run the script-size guard, smoke/navigator checks, and assert neither repo
  contains `from autonerves import setup_colab` afterward.

## Dependency

- PyAutoHands#195 and PyAutoHeart#107 are merged.
