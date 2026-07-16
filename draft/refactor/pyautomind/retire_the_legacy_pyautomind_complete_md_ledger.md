# Retire the legacy PyAutoMind complete.md ledger in favour of the dated complete/ archive

Type: refactor
Target: PyAutoMind
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Retire the legacy PyAutoMind complete.md ledger in favour of the dated complete/ archive. User report (verbatim): 'The design of this seems to work very well, including the balance of tracking open issues, completed, etc. The only thing I am wary of when I look through it is that complete.md is getting huge, currently 4000 lines and counting. Is this something that will token burn or hurt context of an AI going forward? Should it link more concisely to the complete folder which now has date tracking?' Verified: complete.md is now 6,274 lines; the complete/ archive already exists (579 records, dated buckets, generated token-light index.md via lifecycle.py) and intake.md already calls complete.md 'legacy ... until retired'. Remaining work: repoint ship_library and ship_workspace in PyAutoBrain to write dated records into complete/ instead of appending to complete.md, repoint the memory faculty and intake reconcile to the archive, then migrate or freeze the legacy file so nothing grows it further.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from user-intake -->
