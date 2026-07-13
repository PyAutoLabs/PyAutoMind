## euclid-assistant-style-guide-sweep
- issue: https://github.com/Jammy2211/euclid_assistant/issues/3
- completed: 2026-06-25
- project-docs-pr: https://github.com/Jammy2211/euclid_assistant/pull/4
- merged-into: euclid_assistant `main` at `785736e7af2c3a21fedbf7c8c5775718f249d2a7`
- repos: euclid_assistant
- validation:
  - `make test` (`35 passed, 1 skipped`)
  - `git diff --check`
- notes: Extended the Euclid name italicisation check for full named-after-person satellite names, including an inferred James Webb Space Telescope case, while keeping acronyms roman. Added authors-only draft front-matter guidance from local Euclid/A&A source-paper conventions: initials-plus-surname author names, lead-author email only unless requested, and unresolved affiliations left as placeholders when affiliations can wait. Also made optional root-level `euclid.bib` source-discovery fixture handling robust in clean worktrees.
