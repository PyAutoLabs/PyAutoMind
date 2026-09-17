# PyAutoFit prior-model summary header prints wrong range labels for grouped priors

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
