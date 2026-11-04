- epic: autonomous-orchestrators (pilot 4c follow-up; issue PyAutoBrain#575)
- summary: `pyauto-brain batch watch --record <brief> [--once] [--interval N]` (PyAutoBrain#576, new `_watch.py`): a live, read-only terminal view of a running shift. It shows SHADOW/LIVE, time left until review-at, STOP and digest.posted; each task's state, pick reason, PR + CI health and re-dispatch count; budgets (live workers / max-workers, sessions / max-sessions, tokens, merges / merge-cap, crashes); and the last 5 ticks. Task wording is shared with the digest via the new `_digest.task_state` (`_line` delegates to it, so digest output is unchanged), plus live-only states that only a held lease shows. Reads only the watcher's own surface: one `claude agents --json` per refresh, only when live with real leases; `gh pr checks` cached per interval (minimum 30 s).
- witness: PASS. `--once` on the real shadow slot 2026-11-05-am mid-shift (6 proposed picks with reasons, budgets, ticks) plus the live fixture (running / blocked / PR RUNNING / close-out running / merged unattended / parked / crashed), both pasted in the PR. tests/test_batch_watch.py 8 passed (byte-identical slot after --once; no slot created by looking; digest/watch wording parity); existing digest/shadow/close-out tests unchanged; Brain 1548 passed, 1 skipped; tenant firewall OK.
- note: run from a task worktree, the default state home resolves under that worktree's own `-wt` root (same as `batch digest`), so pass `--home ~/Code/PyAutoLabs-wt/.orchestrator` there; from the canonical checkout the default is right.
- heart: YELLOW (workspace smoke / autofit_test reds, validation timeout, other sessions' dirty checkouts) acknowledged by the human at ship; glance tier, in-turn merge.

## Original prompt

# `batch watch`: a live terminal view of a running shift

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-11-04
Issued: 2026-11-04
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
