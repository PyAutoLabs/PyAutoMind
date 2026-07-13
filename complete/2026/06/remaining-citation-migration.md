## remaining-citation-migration
- issue: https://github.com/PyAutoLabs/PyAutoPaper/issues/11
- completed: 2026-06-23
- project-docs-pr: https://github.com/PyAutoLabs/PyAutoPaper/pull/12
- merged-into: PyAutoPaper `feature/literature-citation-layer` at `8c262074ca78b413d6652784d06757cf10ce1e6a`
- parent-pr: https://github.com/PyAutoLabs/PyAutoPaper/pull/2 merged to `main` at `324c23c4fe4e5a4136286e2945087132029886f2`
- validation:
  - `make validate-literature-citations`
  - `pytest -q` (`5 passed`)
  - `git diff --check`
- notes: Consolidated final citation migration after earlier topic PRs. Migrated remaining `*_wiki/sources/*.md` entries away from legacy `File:` paths and filename-inferred summaries. Final audit recorded 247 canonical claim-oriented entries and 390 explicit identity/key TODO entries for unresolved, ambiguous, or unsafe matches. No aliases added.

## Original prompt

# Remaining PyAutoPaper citation migration

Migrate every remaining legacy paper entry across `lensing_wiki`, `smbh_wiki`,
`cti_wiki`, `methods_wiki`, and `galaxies_wiki` in one consolidated PR based on
PyAutoPaper PR #2.

Verify canonical matches and claim context from papers or authoritative public
records. Add the canonical key, verified reference, relevant concepts, concise
support bullets, use guidance, and exclusion guidance. Remove local paths and
filename-inferred summaries. Use explicit TODOs for ambiguity. Keep concept and
entity links consistent, audit aliases, and run `make validate-literature-citations`
plus the repository tests.

The user explicitly replaced the earlier per-topic PR staging requirement with
one PR for all remaining entries. Topic-level commits and reports should still
be retained for reviewability.
