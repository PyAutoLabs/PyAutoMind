M3.5 questions inbox (Build B). Shipped as PyAutoMind#576 (88c408df7) and PyAutoBrain#649 (e69b7e821), merged 2026-11-16, Mind first. Issue PyAutoBrain#645. Design: `Science/scratch/m3_4_m3_5_design/DESIGN.md` §4. Human decisions all as recommended (H7 a, H9 a, H11 a/a).

**Built:**
- **Landing:** parked or blocked worker questions go to Mind `questions.md` through the one Mind writer, as a critical, held-and-retried `question-add`. There are no mid-run @mentions; the digest gets one inbox line plus unfiled lines.
- **Release:** only an answered entry on origin/main releases #637's hold, and the first later pick uses up the answer.
- **Resume:** a claimed task resumes only from the exact shift-worker session line, with every other claim checked, and its prompt carries `RESUME_NOTE` and the answer.
- **Drop** shelves the task. A merged close-out queues `question-retire`.
- `questions_edit.py`, the `/questions` skill, a read-only dashboard section, `batch questions --backfill`, and AUTONOMY items 4–5.

**Review:** independent Opus, FINDINGS: a resume could bypass a repo claim, one answer released the task in every shift, and entries dangled after a merged close-out. Fixed, CLEAN, and the post-rebase review CLEAN. Real `gh` is blocked in tests (zero calls logged).
