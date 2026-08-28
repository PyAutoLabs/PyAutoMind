# Anonymise the named science target in the WFC3-IR hole regression

Type: maintenance
Target: PyAutoReduce
Repos:
- PyAutoReduce
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Issued: 2026-08-28

# Anonymise the named science target in the WFC3-IR hole regression

Type: maintenance
Difficulty: small
Autonomy: safe
Priority: low

Library repos must not name science targets — "these repos shouldnt have science specific paths". The WFC3-IR mosaic-hole regression in autoreduce is named after the real target it was found on. Rename the references to the generic regression (HST program 14653, F160W, 5-exposure mosaic with a 123-px hole) and drop the target name:
- `autoreduce/instruments/wfc3_ir.py:37` (comment)
- `test_autoreduce/test_target_and_instruments.py:157-158` (test name `test_pj011646_would_not_have_holed` and its comment)
- `docs/design/wfc3.md:52`

No behaviour change. Mind history records (complete/, condemned.md, autonomy_log.md) stay untouched — they are records of work that happened.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/069a02ef-b14f-4a43-b0c3-92e461ddef66/scratchpad/intake_reduce.md -->
