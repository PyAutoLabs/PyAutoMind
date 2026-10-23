## prior-summary-ranges
- completed: 2026-10-17
- constraint: Human confirmed 2026-10-17 that existing model/search unique IDs and output-folder names must not change; baseline hashes and exact output paths checked across all four branches.
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1703
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1706
- head: ec8bbf6d91952f34bc2979381ec7528792c9efa1
- validation: Full serial suite: 3703 passed, 121 skipped, 1 xfailed; representation and GraphSpec 89 passed. Numeric suffixes, lexical fallback, padding, singletons, and integer gaps covered.
- identifier-evidence: Free/fixed/mixed model hashes, search IDs and output paths equal unmodified main 99d714c71; no identifier code changed.
- merge: 6579ab8bcd68717f23f5c89c9b2f4229028286ad
- authorization: Human /prm in this chat, 2026-10-17.
- merge-proof: Remote PR head is an ancestor of origin/main in unshallowed PyAutoFit; zero unmerged commits. GitHub confirms MERGED.
- ci: All head workflows and jobs completed successfully; Python 3.12, 3.13 and no-JAX test legs passed. Applicable docs and generated-search-docs passed. No review objections.
- freeze: pyauto-heart freeze --show returned not frozen. Readiness remains STALE; no release-readiness claim.
- release-link-repair: GitHub pending-release label verified; restored the missing Mind link during close-out.
- shadow-row: Human confirmed merged-unchanged in this chat on 2026-10-17; stage-1 glance row appended to autonomy_log.md.

## Original prompt

# PyAutoFit prior-model summary header prints wrong range labels for grouped priors

Issued: 2026-10-17
Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: a unit test over _find_groups (or its representative-key helper) with names lens_0..lens_29 asserts the collapsed key is 'lens_0 - lens_29', not 'lens_0 - lens_9'; same for source_0..source_19.
Review-minutes: 3
Unattended: ready

PyAutoFit prior-model summary header prints wrong range labels for grouped priors. It prints 'lens_0 - lens_9' and 'source_0 - source_9' despite there being 30 lens entries and 20 source entries. This is a real display bug, not a composition error: autofit/mapper/prior_model/representative.py:88 computes min(names)/max(names) on the full name strings, so 'lens_29' sorts below 'lens_9' lexicographically. The int fast-path (map(int, names)) raises ValueError for names like 'lens_29', so it falls through to the lexicographic branch, which then picks the wrong endpoints. The detailed dump and the N=290 total are correct — only the collapsed header range label is wrong. Fix should order by the numeric suffix when the names share a common non-numeric prefix, and leave genuinely non-numeric names on the existing lexicographic behaviour.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from user-intake -->
