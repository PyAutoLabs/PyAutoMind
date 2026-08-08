# workspace-version

- shipped: 2026-07-17
- commit: autolens_workspace `21702119` — "config: adopt version.minimum_library_version floor (2026.7.9.1)"
- repos:
  - autolens_workspace (verified); the sibling workspaces adopt the same key

## Summary

Users pairing a workspace checkout with a differently-versioned library
installation hit API inconsistencies and config mismatches with no clear signal
about the cause. The prompt asked what could be done; the answer that shipped is
a **version floor declared in workspace config**, checked on import.

`autolens_workspace/config/general.yaml`:

```yaml
  minimum_library_version: 2026.7.9.1
  workspace_version_check: True     # If False, bypass the workspace/library version check.
```

The config comment records that this key is "Preferred over `workspace_version`"
— i.e. a **floor** rather than an exact pin, which was the open design question
in the prompt. `workspace_version_check` gives the documented escape hatch for
`main`-branch clones, where mismatches are expected and not actionable because
`main` moves faster than releases.

## Bookkeeping note

Reconstructed 2026-08-08 during the orphaned-prompt triage
(`draft/maintenance/pyautomind/active_prompt_orphan_triage.md`). The prompt sat
in `active/` unclaimed by any registry entry, so no ship-time record exists.
Dated from the adopting commit, not from a merge record.

## Related, still open

`draft/feature/workspaces/minimum_library_version_adoption.md` covers adopting
the same key across the remaining workspace configs. Only `autolens_workspace`
was verified here — that draft should be re-checked against each workspace
before being treated as pending.

## Original prompt

A common problem is users pair a workspace with a different version to their installed software, leaidng to API
inconsistencies and config mismatches.

What do you think we can do about this? One option would be if they are running inside a workspace, it has its
version stored somewhere which is compared to their source code on import. However, you could still end up
with users doing work outside their workspace and copy and pasting old code and API and whatnot. This version number 
could be put in configs to be a bit more secure (e.g. even in their own drive they probably need a config)
but not clear cut.