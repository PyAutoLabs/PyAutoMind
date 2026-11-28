# A second park of the same task files no new question

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-27
Epic: autonomous-orchestrators
Consequence: judge
Witness: a task lease-parks, is answered and restarted, then lease-parks again on the same issue; the second park files a fresh questions.md entry (Mind op queued) and an answer to it restarts the task once its library is free; the test fails on the base commit.
Review-minutes: 10
Unattended: never
Lane: any

Found while building PyAutoBrain#720 (PRs PyAutoBrain#726, PyAutoMind#611). `_questions.note_added` drops a second inbox entry with the same (task, issue). So when a task parks a second time on the same issue, its new question is never re-filed in Mind. The stop-then-release path then reuses the earlier, already-answered entry, and the stopped task cannot restart in-shift from a new answer. It stays held (fails closed), so a human has to act.

Fix direction: key the dedup on (task, issue, asked) or on the question text, or reopen the answered entry when the same task parks again on that issue.
