Pre-M3.1 fixes (epic `autonomous-orchestrators`). Shipped as PyAutoBrain#633 (2e6ef046c), merged 2026-11-14 on `ci-verdict` GREEN. Issue PyAutoBrain#632.

**Fixed what the M3.1 dry run found:**
- **B1:** a re-dispatch no longer jams the Mind writer. A repeat is skipped only for the shift's own re-dispatch; anything else is a loud conflict; critical watcher ops are held and retried, never set aside.
- **F1:** late close-outs are reaped and counted; none starts within 20 min of review-at; stage-2 rows are unique per PR.
- **F2:** only an explicit `verdict:` suppresses a push.
- **F3:** refusals are compacted and summarised.
- **F4:** one Mind fetch per shift, and claims on origin/main are respected.

**F5, human ruling 2026-11-14:** close-outs may exceed the budget but count against it, and none starts at 1.5×. Recorded in AUTONOMY.

**Witness:**
- Brain suite: 2004 passed.
- Dry-run re-run: 23 Mind commits after a kill (before: 78 failures and 31 stuck); a late merge counted; refusal lines down from 134/241 to 13/16; E5 refused at 1.5×.

**Review:** FINDINGS, then fixed, then CLEAN.
