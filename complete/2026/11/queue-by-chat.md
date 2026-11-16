Human ruling 2026-11-16: `queue.md` is maintained by chat only. Shipped as PyAutoBrain#643 (67a03a953) and PyAutoMind#574 (329f1e71f), merged 2026-11-16, Brain first, on `ci-verdict` GREEN. Issue PyAutoBrain#640.

**Removed:** the design C dashboard input path:
- Mind `dashboard_input.yml` and `dashboard_input.py`, plus the spawn rule and spec row;
- Brain `dashboard_edit.js` and its tests;
- the page's ★ toggle, Goals editor and 🔑 token panel; the CSP drops `connect-src`;
- the token-policy section;
- the dead goal-provenance code;
- the `dashboard-input` label and `HUMAN_LOGIN` variable, deleted by the lead.

**Added:**
- Read-only ★ and `#n` on queued tasks, from the planner's own `read_queue`.
- A copy button per task, reusing `Use the start-dev skill. <path>`.
- The `/queue` skill (Brain `skills/queue/`). A paste in that chat means add to queue, never start dev. Verbs: add, remove, move, show.
- Mind `scripts/queue_edit.py`. A paste resolves from its first line only.
- The root workspace `AGENTS.md` records the `/queue` exception.

**Witness:**
- Brain 2029 passed; Mind 903 passed.
- A test resolves every live prompt that cites another to itself.
- The dashboard check is current.

**Review:** independent Opus, FINDINGS: a pasted whole prompt could queue the wrong task, the Mind branch needed a rebase, and the push fallback skipped the helper. Re-review CLEAN.
