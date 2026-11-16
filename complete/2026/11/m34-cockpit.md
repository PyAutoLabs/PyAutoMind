M3.4 build C, the cockpit. Shipped as PyAutoMind#575 (064168672; carve-out + hook), PyAutoBrain#648 (/cockpit skill) and PyAutoMind#577 (REFERENCE pointer; human merge, no CI on docs), merged 2026-11-16. Issue PyAutoBrain#646. Human decisions H1–H3 as recommended.

**Doctrine:** `policy/shift_cockpit_watch.md` carries the carve-out: one human-requested Monitor on the shift's local stream, from 30 min before dispatched to review-at + 45 min, ending with the shift. `end_at_deliverable.md` now bans a Monitor or background loop on GitHub.

**Hook:**
- **Stream command:** the canonical stream is matched whole, with a restricted character set, and pinned to the resolved checkouts. The window comes from the shift record and fails closed.
- **GitHub polls blocked:** a Monitor or background Bash on `gh`, `git fetch`, `github.com`, `ci_verdict` or a WebSocket is refused.
- **Payload and speed:** the payload is read on stdin, and a fast path keeps foreground Bash at about 9 ms.
- **Rollout:** `repos_sync.py` now propagates the matcher, and it was propagated to every repo.

**Skill:**
- **Attaching:** `/cockpit` attaches only on an explicit request; a question gets a one-shot read. It re-arms only at a segment end.
- **Steering:** one comment per plain-words request, from the human's login, with `/stop`, `/kill` and every `/cap` confirmed (number shown). Unclear wording means ask. It pushes only on NEEDS YOU.

**Reviews:** hook FINDINGS (stream-command injection, payloads over 128 KB failing open), fixed, CLEAN. Skill FINDINGS (a question could arm the watch, `/cap` guessing, the `/stop` wording), fixed, CLEAN. The firewall gate now skips the generated-block leg on policy PRs.
