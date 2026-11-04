# `batch watch`: a live terminal view of a running shift

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-04
Epic: autonomous-orchestrators
Consequence: glance
Witness: `pyauto-brain batch watch <brief>` run against a live slot directory shows every task's state, picked-reason, PR/CI health and the shift's budgets, and refreshes in place; a `--once` mode prints one snapshot that the tests assert on; it makes no write anywhere and no GitHub call beyond `gh pr checks`
Review-minutes: 15
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md. A follow-up from pilot slice 4c (PyAutoBrain#574). During shadow shift 1 (2026-11-04) the human asked for a "live feed" of a running shift. Today the only views are `tail -f <slot>/tick.log`, `journalctl --user -u pyauto-orchestrator.service -f` and the raw `counters.json`. Wanted before or alongside the first **live** pilot shift, when it matters which workers are mid-task.

1. **A new read-only verb `batch watch <brief> [--once] [--interval N]`** in `agents/conductors/batch/_batch.py`. It reads the brief and its slot directory under the orchestrator state root (`~/Code/PyAutoLabs-wt/.orchestrator/<slot>/`) and shows:
   - a header: slot, shadow or live, time left until `review-at:` (or "closed"), STOP present or not, the time of the last tick;
   - one line per task: state (proposed / lease held / running / done / PR open / parked / crashed / close-out running / merged unattended / refused), the pick reason, the PR link plus CI health via `_digest.pr_health`, and redispatch count;
   - budgets: sessions vs `max-sessions:`, tokens vs `token-budget:`, merges vs `merge-cap:`;
   - the last few `tick.log` actions.
2. **Reuse, don't re-derive.** Task states and wording come from what `_digest` already uses (`_line` and the counters), so the live view and the end-of-shift digest never disagree. If `_digest` needs a small refactor so both can use the same per-task state, do that.
3. **Liveness on a live shift:** at most one `claude agents --json` per refresh, to mark which workers are still running. That is a network surface the watcher already has (AUTONOMY.md "Watcher network surface"), so no doctrine change is needed. The default refresh interval is ≥ 30 s, so `gh pr checks` is not hammered.
4. **Strictly read-only.** No lease, counter, ledger, Mind or GitHub write; no comment. It must be safe to run while the timer ticks. A test asserts the slot directory is byte-identical before and after `--once`.
5. **Docs:** one paragraph in `agents/conductors/batch/AGENTS.md` and in the pilot README pattern ("during the shift").

Out of scope: a desktop side panel (it could reuse `--once` output later) and a phone-viewable page. The page would publish shift state off the laptop and so needs a ruling on the watcher's one-comment network surface; file it only if the live shifts show it is wanted.

Related: also found in the pilot, the watcher opens a brief on landing rather than at `dispatched:`. That is logged on PyAutoBrain#574 and is a separate fix.

<!-- filed by hand 2026-11-04 at the human's request (pilot 4c follow-up, "live feed" option 1); headers mirror intake's -->
