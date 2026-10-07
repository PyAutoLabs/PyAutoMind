# Skip the workspace version warning outside a workspace

Completed 2026-10-07 under human `/prm` (merged by the human 2026-10-07T09:58:10Z).

Merged PyAutoNerves#192 (https://github.com/PyAutoLabs/PyAutoNerves/pull/192,
merge commit 91c2d0e6); feature head e4fd690 verified an ancestor of
origin/main. Issue https://github.com/PyAutoLabs/PyAutoNerves/issues/191 closed.

`autonerves.workspace.check_version` now returns silently when no version floor
is found and the working directory does not look like a workspace (no `config/`
directory), so running a plain script from a data directory no longer emits the
"Cannot verify the workspace" warning on import of autofit/autogalaxy/autolens.
A `config/` with no version keys still warns (genuinely misconfigured
workspace). No walk-up to a parent workspace root. Workspace impact: none —
every workspace root ships `config/`.

Source: community GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13
(external contributor @HRSAstro), comment
https://github.com/PyAutoLabs/.github/discussions/13#discussioncomment-18741541.

Not released: the fix reaches users with the next PyAutoNerves release.

- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/192

## Original prompt

# autonerves check_version warns 'Cannot verify the workspace' from directories that are not a workspace

Type: bug
Target: PyAutoNerves
Repos:
- PyAutoNerves
Themes:
- config
- community
Autonomy: supervised
Priority: low
Status: draft
Filed: 2026-10-07
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/191
Difficulty: small
Consequence: judge
Witness: with a bare tmp dir (no `config/`, no `version.txt`, no `setup.py`/`pyproject.toml`) as cwd, `check_version("2026.8.17.1")` emits no warning (under `warnings.simplefilter("error")`); a tmp dir with an empty `config/` dir still warns; the existing `test_missing_sources_warns` is updated to create `config/` first and still passes.
Review-minutes: 4
Unattended: ready
Source: GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13 (external contributor @HRSAstro, pyuvimage), comment https://github.com/PyAutoLabs/.github/discussions/13#discussioncomment-18741541; technical review 2026-10-07 (Item D, accept).

## Request (verbatim)

> - Running a plain script from a data directory triggers the autonerves workspace version warning. It's harmless, but it might be worth skipping when there is no workspace config at all.

## What

`check_version` (`autonerves/workspace.py:175`) defaults `root = Path.cwd()`; with no `config/general.yaml` version keys and no `version.txt` it warns unless `_is_source_checkout(root)` (`:98`, setup.py/pyproject.toml). A plain data directory has none, so `_warn_once(_missing_version_warning(...))` (`:250-253` region) fires. It runs on import of autofit/autogalaxy/autolens (`autofit/__init__.py:175`, `autogalaxy/__init__.py:141`, `autolens/__init__.py:163`); autoarray does not call it.

## Plan

1. In the no-floor branch:
   ```
   if floor_version is None or floor_version == "":
       if _is_source_checkout(root) or not _looks_like_workspace(root):
           return
   ```
   with `_looks_like_workspace(root) = (root / "config").is_dir()` (every workspace ships `config/`; `version.txt` is already consumed above). A `config/` with no version keys still warns (genuinely misconfigured; keeps `test_yaml_without_version_key_falls_through_to_warning`).
2. Update the `check_version` docstring (`:198-202`) and `_is_source_checkout`'s.
3. No walk-up to a parent workspace root: a workspace script run from a subdirectory goes from a false warning to silent (floor unchecked, same as outside a workspace); walking up could find an unrelated parent `config/`.

Tests (`organs/PyAutoNerves/test_autonerves/test_workspace.py`): `test_missing_sources_warns` (`:31`) uses a bare tmp_path and will flip — create `config/` first; add `test_missing_sources_without_config_dir_is_silent`; add "config/ present, no general.yaml, no version.txt → warns". Source-checkout tests (`:37`, `:47`) unaffected.

Reliance check: no repo asserts the warning text. Heart (`workspace-validation.yml:77`), Hands (`release.yml:474,776`) and PyAutoLens subprocess tests (`test_tracer_fields.py:527,649`, `test_analysis_point_gradient_mode.py:214`) only set `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`; unaffected. Risk: a real workspace clone missing `config/` stops warning — not a realistic layout.
