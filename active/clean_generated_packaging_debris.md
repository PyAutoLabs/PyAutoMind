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
