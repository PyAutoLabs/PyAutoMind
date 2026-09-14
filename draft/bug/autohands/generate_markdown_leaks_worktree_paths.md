# generate_markdown.py leaks local paths when run from a task worktree

Type: bug
Target: autohands
Repos:
- PyAutoHands
Themes:
- build
- docs
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: Rendering the same curated page from a canonical checkout and from a task worktree under `~/Code/PyAutoLabs-wt/<task>/` produces byte-identical markdown; neither contains `/home/`, `~/Code` or `PyAutoLabs-wt`.
Review-minutes: 20
Unattended: ready
Filed: 2026-09-14

`generate_markdown.py` redacts absolute paths out of rendered output via
`_redactions_for()`, which maps `workspace_path.parent` → `...`.

That assumption only holds in a canonical checkout. From
`~/Code/PyAutoLabs/HowToGalaxy`, the parent is `~/Code/PyAutoLabs`, so a library
warning renders as `.../PyAutoArray/...`. From a task worktree at
`~/Code/PyAutoLabs-wt/<task>/HowToGalaxy`, the parent is the worktree directory
instead, so the same warning renders the developer's real local layout —
`~/Code/PyAutoLabs/PyAutoArray/...` — straight into a published documentation
page.

Since the workflow routes essentially all development through task worktrees,
**the default path produces the leak and the exception produces the clean
output.** Nothing fails; the pages just quietly carry one contributor's
directory layout.

## Two adjacent traps found in the same session (2026-09-14, HowToGalaxy)

Both cost time and neither is documented; worth fixing or at least recording in
the workspace `AGENTS.md` regeneration sections alongside the above:

1. **`PYTHONPATH=../PyAutoHands/autohands` replaces rather than appends.** The
   documented invocation clobbers the ambient `PYTHONPATH` that makes the
   libraries importable, so the notebook kernel dies with
   `ModuleNotFoundError: No module named 'autogalaxy'`. Relative entries also
   break because nbconvert runs with cwd set to the script's directory, so the
   fix needs absolute paths.
2. **A source-installed stack bakes PyAutoNerves version-handshake warnings into
   the pages** ("Cannot verify the workspace…", "records library version X, but
   the installed library is Y") that appear in no committed page. Re-rendering
   with `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1` clears them. If that is the
   expected way to render, it belongs in the documented command.

## Scope

Derive the redaction root from the **repository root** (`git rev-parse
--show-toplevel`, or the workspace's registered root) rather than
`workspace_path.parent`, so a worktree render matches a canonical one. Add a
guard that fails the build when rendered output still contains an absolute home
path, so this cannot regress silently. Fix or document the two traps above.

## Provenance

Found while regenerating HowToGalaxy's curated markdown pages under
`howto-stale-self-location` (issue HowToGalaxy#75). The leak was caught and
worked around by hand before it reached the branch; the final pages are clean.
