# HowTo tutorials still describe themselves as living inside the *_workspace repos

Type: docs
Target: workspaces
Repos:
- HowToFit
- HowToGalaxy
- HowToLens
Themes:
- howto
- tutorials
Difficulty: medium
Autonomy: safe
Priority: medium
Status: draft
Consequence: notify
Witness: No `<workspace>/{output,config,dataset}` path or clone/download URL in
HowToFit, HowToGalaxy or HowToLens refers to the HowTo repo's own files; the
HubbleTuningFork image renders from its HowToGalaxy home and its
`.url_check_allowlist.txt` grandfather entry is gone; genuine cross-references
to sibling workspace *examples* are untouched.
Review-minutes: 20
Unattended: ready
Filed: 2026-09-14

The HowTo lecture series were split out of the `*_workspace` repos into their
own `HowToFit` / `HowToGalaxy` / `HowToLens` repos. The prose did not move with
them: tutorials still tell the reader their working directory, config, dataset
and output folders live inside the workspace repo, and HowToFit's `__Paths__`
block sends a reader who wants to clone HowToFit to `autofit_workspace`.

User-reported (2026-09-14), from HowToFit tutorial 1:

> If you don't have a HowToFit clone, you can download it here:
> https://github.com/PyAutoLabs/autofit_workspace

## The distinction that governs every edit

Two classes of `*_workspace` reference live in these repos. Only the second is
stale, and the fix must not flatten them together:

- **KEEP — cross-references.** "See `autolens_workspace/*/guides/modeling/chaining.py`",
  "all examples in the `autogalaxy_workspace` use Nautilus", "the workspace
  scientific workflow example". These point at the sibling workspace as the
  reader's *next destination* and are correct post-split. There are dozens of
  them. Do not touch them.
- **FIX — self-location.** Text that assumes the HowTo tutorials live *inside*
  the workspace repo: clone/download URLs, and `<workspace>/{output,config,dataset}`
  paths that are now `<HowToRepo>/{output,config,dataset}`.

## Scope

- @HowToFit — 1 block. `scripts/chapter_1_introduction/tutorial_1_models.py:93`,
  the `__Paths__` section: the download URL must be
  `https://github.com/PyAutoLabs/HowToFit`. HowToFit is the only one of the
  three with a `__Paths__` section at all.
- @HowToGalaxy — 15 hits. `tutorial_2_practicalities.py` (`path_prefix`
  described as `autogalaxy_workspace/output/howtogalaxy/chapter_2`; "checkout
  the `autogalaxy_workspace/output` folder" x3; "`config`: the files in
  `autogalaxy_workspace/config`"), `tutorial_3_realism_and_complexity.py`
  (2 print strings), `tutorial_2_data.py:338`
  (`autogalaxy_workspace/dataset/imaging/howtogalaxy/`),
  `tutorial_0_visualization.py:33,102`
  (`autogalaxy_workspace/dataset/...`, `autogalaxy_workspace/config/visualize`).
- @HowToLens — 14 hits. `tutorial_2_practicalities.py`
  (`autolens_workspace/output` x4), `tutorial_3_realism_and_complexity.py`
  (2 print strings), and five `scripts/simulator/*.py` — `lens_x2`, `lens_x3`,
  `lens_sersic`, `lens_extra_galaxy`, `no_lens_light__mass_sis` — each saying
  "The dataset can be viewed in the folder `autolens_workspace/dataset/imaging/...`"
  when the script writes into `HowToLens/dataset`.

Counts are from a 2026-09-14 grep of `scripts/` only; re-run the survey across
each repo before editing, since `README.md`, `start_here.py`, `welcome.py`,
`llms.txt` and `llms-full.txt` may carry the same class of reference.

## Separate bug, same root cause (@HowToGalaxy)

`scripts/chapter_1_introduction/tutorial_1_grids_and_galaxies.py:9` links the
Hubble tuning fork image at
`https://github.com/PyAutoLabs/autogalaxy_workspace/blob/main/scripts/chapter_1_introduction/HubbleTuningFork.jpg`.
That URL has been broken since the move; the file now lives at
`HowToGalaxy/scripts/chapter_1_introduction/HubbleTuningFork.jpg`. Rather than
being fixed, it was grandfathered into `HowToGalaxy/.url_check_allowlist.txt`
so the weekly `url_check.yml` cron stays green.

Fix the link **and delete the allowlist entry**. Leaving the entry behind keeps
a green check over a fixed URL and re-hides the next breakage.

## Derived artefacts

Every prose fix lands in three mirrors per tutorial — `scripts/*.py`,
`notebooks/*.ipynb`, `markdown/*.md` — and `workspace_index.json`, `llms.txt`
and `llms-full.txt` carry some of the same links. Regenerate derived artefacts
through each repo's own regeneration convention rather than hand-editing the
notebook/markdown mirrors. ~90 edits total.

## Delivery

One issue and one PR per repo; the three legs are independent.

## Out of scope

Adding a `__Paths__` orientation block to HowToGalaxy and HowToLens for parity
with HowToFit. It is a real gap — those two repos have no "here is your working
directory, here is where to clone" section, which is why their stale paths are
scattered through prose instead of concentrated in one block — but it is new
authorship, not a correction. File it as a follow-up prompt.
