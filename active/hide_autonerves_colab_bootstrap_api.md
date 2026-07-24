# Hide `autonerves` behind the Colab bootstrap

Type: refactor
Target: PyAutoHands
Repos:
- @PyAutoHands
- @PyAutoHeart
Difficulty: medium
Priority: normal
Status: formalised

Change the generated Colab setup cell so workspace users are directed through
the product API (`autofit`, `autogalaxy`, or `autolens`) rather than taught to
import `setup_colab` directly from `autonerves`. Preserve `autonerves` as the
private bootstrap implementation on a fresh Colab runtime, where it must first
install the correct product stack.

## Original request

> autonerves should not be user facing API, but it is in many workspace examples: from autonerves import setup_colab   , update it so its not, but make sure the colab install still uses it as it needs the right install rhere I think.

> this is prob requied for PyautoGalaxy too

## Requirements

- Map all six Colab project keys to their existing product-level API:
  `autofit`/`howtofit` to `autofit`, `autogalaxy`/`howtogalaxy` to
  `autogalaxy`, and `autolens`/`howtolens` to `autolens`.
- In a fresh Colab runtime, continue installing `autonerves --no-deps` first
  and invoke its setup implementation privately so it can install the correct
  stack, clone the version-matched workspace, and configure paths.
- Outside Colab, resolve `setup_colab` through the mapped product package.
- Update PyAutoHands injection tests to guard both the public import boundary
  and the internal Colab bootstrap.
- Keep PyAutoHeart's end-to-end Colab simulation verbatim with the generated
  cell and verify the real bootstrap path remains covered.

## Follow-up

After this phase lands, run
`draft/refactor/workspaces/hide_autonerves_colab_workspace_rollout.md` to
regenerate and validate all six user-facing notebook repositories.
