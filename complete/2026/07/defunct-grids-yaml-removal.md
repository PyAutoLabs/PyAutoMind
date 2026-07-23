## defunct-grids-yaml-removal
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/317
- completed: 2026-07-23
- prs: autolens_workspace#318, autogalaxy_workspace#146, autolens_workspace_test#200, autogalaxy_workspace_test#81, HowToLens#45, HowToGalaxy#36, autolens_assistant#87, autocti_assistant#8, euclid_strong_lens_modeling_pipeline#32, PyAutoCTI#97, PyAutoArray#401, PyAutoGalaxy#519 — ALL MERGED
- summary: Deleted the 10 orphan `config/grids.yaml` copies plus 3 references (2 library `config/README.md` bullets, 1 `autocti_assistant/PENDING.md` TODO). The `radial_minimum:` mapping had been unread since PyAutoGalaxy `025ac7ac` "remove relocate_to_radial_minimum" (2025-10-15), which followed `82622f74` (2025-04-03); the library default configs already shipped none. Zero `.py` hits across all five libraries and zero hits in the installed venv. Two copies were self-evidently unread: autocti_assistant had the key misspelled `radiac_minimum` (clone sed artifact) and PyAutoCTI's still listed `EllipticalSersic`/`SphericalNFW` names retired years ago. Verified post-delete: PyAutoCTI 271 passed (its conftest points conf.instance at that dir — the only real failure mode), workspace config loads, and profiles return finite values at exactly (0,0), the case radial_minimum used to guard. Final sweep: zero hits outside Mind records.
- gotchas:
  - **RED acknowledgement must be sought against `pyauto-heart readiness --json`, NOT the `pyauto-brain vitals` summary.** The summary showed 1 RED reason; the JSON had 7. The human authorization was initially given against the 1-reason quote, which does not satisfy AUTONOMY.md — re-sought against the full verbatim list before any commit.
  - `gh pr create` fails on this workspace's SSH remotes (`/usr/bin/git: exit status 128`) — used `gh api repos/O/R/pulls -X POST` for all 12.
  - `gh api .../labels -X POST -f "labels[]=x"` returns **422** ("`labels[]` is not a permitted key"). Working form: `echo '{"labels":["x"]}' | gh api ... --input -`. The flag form fails silently if stderr is suppressed.
  - Brain Feature Agent scored this `too-large (32)` → 4-phase split + library-first API handoff. Repo-count-driven false signal (same as rename-autobuild-to-autohands); no API surface existed. Overridden.
  - `worktree_check_conflict` flagged 9 of 12 repos against two parked tasks; file-level overlap verified zero, ran concurrently.
  - Two CI failures on merge were **pre-existing main defects**, both proven unrelated: autolens_assistant `boundary` (4 unclassified `docs/images/*` files, all on main) and autocti_assistant `wiki-currency` (main's `cecdb67` rewrote the checker to gate on API-surface hash and landed without a wiki-currency run; our PR was the first to exercise it).
- follow-ups:
  - **The `/hygiene config` audit has a structural blind spot** that let this orphan survive ~1 year: it diffs library config keys against workspace config keys, so a workspace config file with NO library counterpart is invisible to it. Sibling prompt `draft/maintenance/workspaces/config_key_mirror_drift.md` covers the opposite direction (keys missing from workspaces). Neither catches an orphan FILE.
  - autocti_assistant `wiki-currency` is red on main and needs its own fix (see gotcha above).
  - autolens_assistant `boundary` is red on main — 4 files need classifying in `modes/maintainer.md` + `_clone.py` REFERENCE_PROFILES.

## Original prompt

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
