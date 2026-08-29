## anonymise-wfc3-ir-hole-regression-target
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/73
- completed: 2026-08-28
- library-pr: PyAutoReduce#74 (merged 5ee7c4e1a8cb1b2a75863ff4c4193262f422a5cf -> main)
- what shipped: the WFC3-IR mosaic-hole regression no longer names the real science target it was found on. It is identified by the dataset shape it encodes — HST program 14653, F160W, a five-exposure mosaic with a 123-px hole at r = 5.3" — in all three sites: the IR adapter's `dq_bits_rows` rationale comment (`autoreduce/instruments/wfc3_ir.py`), the regression test's name and comment (`test_pj011646_would_not_have_holed` -> `test_five_exposure_f160w_mosaic_would_not_have_holed`), and the "Blobs (DQ 512)" paragraph of `docs/design/wfc3.md`.
- scope: comment / test-name / prose text only — no executable line changed, no assertion touched, no exported symbol, signature, default or behaviour change.
- validation: `pytest test_autoreduce/ -q` 299 passed, 3 skipped (2026-08-28); `grep -rIn -i -e pj011646 -e 011646 --exclude-dir=.git` over the repo returns nothing. CI on the PR: `Tests` green — `unittest (3.12)`, `unittest (3.13)` success, `unittest-nojax` skipped (conditional leg).
- deliberate non-change: PyAutoMind history records (`complete/`, `condemned.md`, `autonomy_log.md`) keep the old name — they are records of work that happened, not library source. The only other place the string lived, `scripts/cache/cache_manifest.json`, is gitignored.
- heart-ack: opened + merged under human-acknowledged RED, verbatim authorisation "open prs under red and merge i acknowledge" (2026-08-28). RED reason verbatim: "release validation FAILED (stage integrate)". YELLOW reasons verbatim: "workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, rectangular_mge_rtu.py)"; "manifest drift: session-start hooks (generated) — 32 mismatch(es) vs PyAutoMind/repos.yaml". None of them touches PyAutoReduce.

## Original prompt

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
