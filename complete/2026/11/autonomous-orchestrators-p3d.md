- epic: autonomous-orchestrators (phase 3d of 3a–3d — closes phase 3; epic draft/feature/pyautobrain/autonomous_orchestrators_epic.md)
- summary: the shift digest. PyAutoBrain#569: agents/conductors/batch/_digest.py (build — brief work vs backlog picks with the brief rule each was picked under, one proof packet per started task quoted from <task>.proof.md or an honest stub, every counter; validate — the digest half of `batch brief --check`; pr_health — one read-only `gh pr checks` per PR); _brief.pick_reason/_scoped_match; _orchestrator records picks at dispatch, keeps `.done` lines as outcomes and moves proofs to <slot>/proofs/ (the reap used to delete the PR URLs), and the first tick after review-at runs finish_shift — digest.md, append to the record via the one Mind writer, digest.html only under packet: yes, then digest.posted exclusive-created BEFORE the one `gh issue comment` (crash → no comment, never two; failed post never retried; nothing read back). `batch digest --record` prints read-only; _mind_writer.queue_op shared with bin/shift_ledger.py; worker template asks for proof.md and `merged <url>` lines. PyAutoMind#531: batches/AGENTS.md "where each part comes from".
- decisions: glance-auto-merges/reverts/pushes/drafts-filed/packets-sent read 0 until phases 4–5 (human); once-only via local marker (human). Departure: merges counted from workers' `merged <url>` lines, not batch collect (the watcher's surface has no merge-state read).
- witness: tests/test_orchestrator_digest.py 23 passed (control: no pick reason → 3 fail); real-git record append on Mind main; LIVE sandbox PyAutoMind#530 — one comment, second tick posted nothing (closed). Brain 1512 passed (+2 pre-existing test_prompt_budget failures, same on main); Mind 712; tenant firewall OK.
- next: phase 4 Dev pilot — prompt not filed; needs the shadow-row verb to route unattended merges into the stage-2 table (autonomy_log.md).
- heart: YELLOW (autofit_test MultiStartResumeNaNCounters.py timeout; no release rehearsal) acknowledged by the human at ship; judge tier, human /prm.

## Original prompt

# Autonomous orchestrators phase 3d: `batch digest` — digest + proof packets, digest validator, one issue comment per shift

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised
Filed: 2026-11-03
Issued: 2026-11-04
Epic: autonomous-orchestrators
Phase: 3
Consequence: judge
Witness: `batch digest` appends a `## Digest` to a fake shift's brief record matching `PyAutoMind/batches/AGENTS.md` (brief work vs backlog picks each with a one-line reason, one proof packet per task, every counter), `batch brief --check` gains a digest check that accepts it and refuses one missing a counter or a pick reason, and the digest is posted exactly once as a comment on a sandbox issue (a second run posts nothing); `pytest PyAutoBrain/tests -q` green
Review-minutes: 20
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md; slice of phase 3 (slicing: `complete/2026/11/autonomous-orchestrators-p3a.md`, prompt section "Slicing"; 3a shipped as PyAutoBrain#556).

Closes phase 3. The network surface for the comment is the one AUTONOMY.md names in 3a. The HTML packet stays opt-in (`packet: yes`).

<!-- filed by hand 2026-11-03 when phase 3 was sliced 3a–3d (human decision); headers mirror intake's -->
