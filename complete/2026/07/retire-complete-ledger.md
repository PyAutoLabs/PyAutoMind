## retire-complete-ledger (complete.md retired — the dated records ARE the ledger; first record written via the new record --from-file path)
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/81 (CLOSED)
- completed: 2026-07-16
- prs: PyAutoMind#83 + PyAutoBrain#123 (pending-release) + PyAutoHeart#82 (pending-release) — ALL MERGED same day.
- summary: retired the 6,274-line / 590-entry complete.md monolith; complete/<YYYY>/<MM>/<slug>.md records + generated index.md are the sole completion ledger. Backfilled 8 ledger entries that had NO record (the ledger→record direction was never check-guarded and drifted within days — the decisive argument for one source of truth); keck-ao backfill also recovered its stranded active/ prompt. lifecycle.py: record <slug> --date --from-file <body> (ship skills draft the rich body; no complete.md parsing), move infers the bucket from an existing record, check gains post-retirement invariants (active.md slug with a record = drift; no file in two states), spent one-time split-complete/migrate DELETED. Brain: ship_library/ship_workspace write the record directly (double-write gone), memory faculty digests per-record files (citations now land on one record, not a 6k-line blob), intake reconcile reads record contents + H2s. Heart: pyauto-status reads recent-5 from index.md (reverse-chronological). status.sh counts exclude archive/.
- origin: user question at intake — "complete.md is 4000 lines and counting; will it token-burn an AI going forward?" Answer: yes; and the retirement was already designed for (check's pairing invariant was annotated "(pre-retirement)").
- concurrency: all THREE repos were claimed at start (memory-structure-cleanup, community-voice-agent + ic50-assistant-seed, delete-pyautoheart-shim) — user-approved parallel claims after verifying file-level overlap (Brain/Heart zero; Mind = spawn.py only, EXCLUDED and filed as a rider). The rider then folded into #83's merge-resolution commit when memory-structure-cleanup merged mid-task. Merge conflict on #83 was the retirement thesis in miniature: 4 tasks shipped on main mid-flight, all 4 wrote ledger+record pairs, resolution = verify pairing, keep the deletion, regenerate index.
- heart: shipped through unrelated organism-scope RED on explicit user authorization ("I authorize, go"); 6 reasons verbatim in active.md heart-ack at the time + on #81; diff contained zero library source.
- trap for future sessions: complete.md is GONE — any habit/doc/memory that greps it must use complete/index.md (navigation) or complete/**/*.md records (content). Completion recording = draft body → lifecycle.py record --from-file → index --apply → drop the active.md entry.

## Original prompt

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
