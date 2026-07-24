## clean-packaging-debris
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/159
- completed: 2026-07-24
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/160
- merge-sha: cede6805534375450ac7c2188276aef3be9f5e0b
- summary: Added Hygiene's read-only `packaging` debris mode and a narrow `clean_slate.sh --packaging` executor for ignored, fully-untracked top-level `*.egg-info/` and `build/` directories in managed library repositories. The normal morning clean-slate now includes the same cleanup.
- safety: Detection and deletion share repo-set, exact-name, root-depth, ignored-path, and tracked-file guards. Nested or tracked `build/` directories, unignored paths, and assistant/workspace products such as `euclid_assistant/build/` are left alone.
- validation: 19 targeted tests and 157 remaining PyAutoBrain tests passed; `test_every_public_agent_has_a_skill_wrapper` was deselected because its missing `sizing` wrapper failure reproduces on `main`. A real dry-run found five removable library products, including `PyAutoGalaxy/autogalaxy.egg-info/` and `PyAutoFit/build/`.
- workspace-impact: None — Brain operational tooling only; no scientific-library Python API changed, so workspace smoke was not applicable.
- heart: YELLOW reasons (workspace validation failures, stale parked scripts, tenant-firewall manifest drift, stale release rehearsal) were surfaced and explicitly acknowledged before PR publication.
- concurrency: The user authorized a concurrent PyAutoBrain claim with `profiling-mirror-taxonomy`; its only changed Brain file at ship time was `agents/conductors/profiling/_profiling.py`, with no overlap.

## Original prompt

# Clean generated packaging debris through Hygiene

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Original request

If not there already can we make removing autogalaxy.egg-info and build folders / file part of the hygeine agent

## Initial finding

The current Hygiene Agent does not detect ignored local packaging products.
`PyAutoGalaxy/autogalaxy.egg-info/` is present and ignored; a top-level
`PyAutoGalaxy/build/` directory is not currently present. Hygiene's `tidy` mode
only covers git branches, stashes, gone refs, and dirty checkouts, while
`artifacts` only covers tracked leaked outputs/data.

## Intent

Extend Hygiene's generated-cruft coverage so top-level Python packaging products
such as `*.egg-info/` and `build/` are safely identified and removed through the
existing cleanup boundary. Keep the Hygiene conductor read-only: it should
surface and delegate the cleanup rather than directly mutating repositories.

## Acceptance

- A Hygiene scan reports ignored top-level `*.egg-info/` and `build/` packaging
  directories in managed library repositories.
- The delegated cleanup removes only those narrowly matched, untracked/ignored
  generated directories, never tracked source or arbitrary nested `build/`
  directories.
- Tests cover detection, tracked-file protection, dry-run behavior, and cleanup.
- Hygiene documentation names the new generated-packaging-debris behavior and
  its safety boundary.
