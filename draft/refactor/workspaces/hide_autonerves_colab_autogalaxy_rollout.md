# Remove direct `autonerves.setup_colab` imports from AutoGalaxy examples

Type: refactor
Target: autogalaxy_workspace
Repos:
- @autogalaxy_workspace
- @HowToGalaxy
Difficulty: medium
Priority: normal
Status: formalised

Roll out the product-level Colab setup API across the PyAutoGalaxy workspace
and HowToGalaxy after the PyAutoHands bootstrap change merged in #195.

## Original request

> autonerves should not be user facing API, but it is in many workspace examples: from autonerves import setup_colab   , update it so its not, but make sure the colab install still uses it as it needs the right install rhere I think.

> this is prob requied for PyautoGalaxy too

## Requirements

- Update the four hand-written setup sections in `autogalaxy_workspace`
  (`start_here.py` plus imaging/interferometer/multi `start_here.py`) to use
  the same public/private boundary as the merged generator.
- Resolve `setup_colab` through `autogalaxy` outside Colab while retaining the
  private `autonerves` fresh-Colab bootstrap.
- Regenerate notebooks through merged PyAutoHands; never hand-edit `.ipynb`.
- Regenerate all `autogalaxy_workspace` and `HowToGalaxy` notebook/catalogue
  outputs expected by their build targets.
- Run the script-size guard, smoke/navigator checks, and assert neither repo
  contains `from autonerves import setup_colab` afterward.

## Dependency

- PyAutoHands#195 and PyAutoHeart#107 are merged.
