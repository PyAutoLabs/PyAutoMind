## lensing-transient-citations
- issue: https://github.com/PyAutoLabs/PyAutoPaper/issues/3
- completed: 2026-06-22
- project-docs-pr: https://github.com/PyAutoLabs/PyAutoPaper/pull/4 (merged 5b0c247 into PR #2 branch)
- repos: PyAutoPaper
- notes: Migrated five lensed-supernova and plasma-lensing entries to verified claim-oriented citations. No ambiguous keys or aliases; citation validation and 5 tests passed.

## Original prompt

# Lensing transient citation migration

## Batch scope

Create the first small, reviewable migration PR for the lensed-supernova and
FRB/plasma-lensing source topics. Base the work on PyAutoPaper PR #2.

## Original request

Work in @PyAutoPaper.

Goal: incrementally migrate every legacy `*_wiki/sources/*.md` paper entry to
the canonical, claim-oriented citation schema introduced in PR #2.

Do not perform a blind mechanical rewrite. Metadata and claim context must be
verified from the paper or an authoritative public source.

For each entry:

1. Match the paper against `bibliography/pyautopaper.bib`.
2. Add `Canonical BibTeX key`, verified public `Reference`, relevant `Concepts`,
   2–5 concise `Supports` bullets, `Use when`, and `Do not use for`.
3. Remove legacy local `File:` paths.
4. Remove filename-inferred or unverified summaries.
5. If the paper or canonical key is ambiguous, add an explicit TODO instead of
   guessing.
6. Keep concept/entity pages and cross-links consistent.
7. Run `make validate-literature-citations`.

Stage the work by sub-wiki and topic rather than migrating all entries in one
PR: `lensing_wiki`, `smbh_wiki`, `cti_wiki`, `methods_wiki`, then
`galaxies_wiki`. Within each sub-wiki, create small reviewable PRs grouped by
source topic.

After each batch report entries migrated and left, missing or ambiguous
canonical keys, aliases added, and validation/test results.

Do not fabricate claims, identifiers, metadata, or keys; copy abstracts; add
PDFs or local paths; overwrite unrelated main-checkout work; or change LaTeX
without resolving downstream `.bib` keys. Use isolated worktrees.
