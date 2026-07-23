# Delete the defunct grids.yaml config across every workspace

Type: maintenance
Target: workspaces
Repos:
- autolens_workspace
- autogalaxy_workspace
- autolens_workspace_test
- autogalaxy_workspace_test
- HowToLens
- HowToGalaxy
- autolens_assistant
- autocti_assistant
- euclid_strong_lens_modeling_pipeline
- PyAutoCTI
- PyAutoArray
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> Is [grids.yaml](../autogalaxy_workspace/config/grids.yaml) throughout all
> workspaces defunct? and howto etc defunct?
>
> — and, on confirming it is: "yes go" (delete the files, the two library
> `config/README.md` lines, and the `autocti_assistant/PENDING.md` TODO).

## Why

`config/grids.yaml` supplies a `radial_minimum:` mapping that no code has read
since PyAutoGalaxy `025ac7ac` "remove relocate_to_radial_minimum"
(2025-10-15), which followed `82622f74` "remove grid relocate radial"
(2025-04-03). Verified by grep:

- `radial_minimum` appears in **zero** `.py` files across PyAutoArray,
  PyAutoGalaxy, PyAutoLens, PyAutoCTI, PyAutoNerves.
- `radial_minimum` appears in **zero** files under the installed venv
  (`~/venv/PyAuto/lib/python3.12/site-packages`).
- Nothing reads a `"grids"` config section (the only `"grids"` hits are
  `dataset.grids` attribute lookups in `autoarray/dataset/plot/imaging_plots.py`).
- The library default configs (`PyAutoArray/autoarray/config/`,
  `PyAutoGalaxy/autogalaxy/config/`) already ship **no** `grids.yaml` — only
  the downstream copies survive.

This was already spot-confirmed once in
`PyAutoMind/complete/2026/05/external-potential-priors-and-jit.md`
("grids.yaml entry skipped — grep confirmed no library code reads
`radial_minimum` … the workspace copies are vestigial"), but the files were
left in place. Two of them prove nobody reads them:

- `autocti_assistant/config/grids.yaml` has the key misspelled
  `radiac_minimum` (a clone sed-substitution artifact) with no effect.
- `PyAutoCTI/test_autocti/config/grids.yaml` still lists `EllipticalSersic` /
  `SphericalNFW` class names retired years ago, plus a dead `interpolate:`
  section for mock classes.

Per the standing "delete the trap, don't document it" rule, the right move is
removal, not fixing the typo or refreshing the class names.

## Scope

Delete (10 files):

- `autolens_workspace/config/grids.yaml`
- `autogalaxy_workspace/config/grids.yaml`
- `autolens_workspace_test/config/grids.yaml`
- `autogalaxy_workspace_test/config/grids.yaml`
- `HowToLens/config/grids.yaml`
- `HowToGalaxy/config/grids.yaml`
- `autolens_assistant/config/grids.yaml`
- `autocti_assistant/config/grids.yaml`
- `euclid_strong_lens_modeling_pipeline/config/grids.yaml`
- `PyAutoCTI/test_autocti/config/grids.yaml`

Also remove the stale references that point at a file which will no longer
exist (and, for the two library READMEs, already does not exist in the
directory they document):

- `PyAutoArray/autoarray/config/README.md:11` — the `grids.yaml` bullet
- `PyAutoGalaxy/autogalaxy/config/README.md:11` — the `grids.yaml` bullet
- `autocti_assistant/PENDING.md:303` — the "review `config/grids.yaml`" TODO

Then re-grep the whole workspace for `grids.yaml` / `radial_minimum` /
`radiac_minimum` and confirm zero hits remain outside `.git/` and the Mind
historical records.

## Out of scope

- Any *other* config-file drift. The sibling prompt
  `draft/maintenance/workspaces/config_key_mirror_drift.md` covers keys the
  workspace configs are *missing*; this one only removes an orphan file.
- Reinstating `radial_minimum` behaviour. If profiles need a radial floor
  again that is a library feature, not a config restore.

## Verify

- `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1` load of an affected workspace script
  (e.g. an `autolens_workspace` start_here) still runs — no missing-config error.
- PyAutoCTI test suite green after `test_autocti/config/grids.yaml` is deleted
  (that config dir is the one the test conftest points `conf.instance` at).
- Grep sweep clean, as above.
