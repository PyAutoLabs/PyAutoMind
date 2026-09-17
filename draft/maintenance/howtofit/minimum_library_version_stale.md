# The workspace staleness warning keys off a value documented never to move

Type: maintenance
Target: PyAutoNerves
Repos:
- PyAutoNerves
- HowToFit
Themes:
- version-handshake
- tutorials
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Review-minutes: 3
Unattended: ready
Witness: a fresh clone of a release-tagged workspace with the matching released library emits no workspace-version UserWarning.
Filed: 2026-09-15
Revised: 2026-09-15 — the first version of this prompt proposed bumping HowToFit's floor. That is wrong; see below.

## What a reader sees

On HowToFit main with a current `autofit`, the first import prints:

    UserWarning: The workspace at .../HowToFit records library version
    2026.7.9.1, but the installed library is 2026.8.17.1 — more than 30 days
    newer. The workspace examples and configs may lag the installed API.
    Pull the latest workspace:
        cd .../HowToFit && git pull origin main

The advice is not actionable for the reader it reaches — they are already on
main, or on the release tag. It is the first thing a workshop attendee sees.

## Why "just bump the floor" is the wrong fix

`autonerves/workspace.py:check_version` resolves the floor from
`config/general.yaml: version.minimum_library_version` first, and that key's
own comment in HowToFit reads:

    Bump DELIBERATELY — only when a script starts needing new API — never per
    release. Must always name an INSTALLABLE (non-yanked) release.

So the value is a **compatibility floor**, correctly old. The staleness
warning then reuses that same floor as a **freshness** signal
(`_STALENESS_WINDOW_DAYS = 30`, `workspace.py:18`), which guarantees the
warning fires for every workspace whose scripts have not needed new API for a
month — i.e. every healthy workspace. Bumping the floor to silence it would
misuse the key and lose the floor's real meaning.

## The actual options

1. Warn on a freshness stamp, not the floor: only run the staleness comparison
   against `version.workspace_version` (the release stamp) where one exists,
   and skip it entirely when only `minimum_library_version` is set. A floor is
   not evidence about how old the clone is.
2. Or drop the staleness warning and keep only the hard "installed library is
   older than the floor" error, which is the check that carries information.
3. Or, if the warning is wanted for tag clones, have the release stamp
   `workspace_version` at tag time so there is a real freshness value to
   compare.

Whichever is chosen, the same drift is sitting in the sibling teaching repos
(HowToGalaxy, HowToLens) and the workspaces, so fix it in autonerves rather
than per repo.
