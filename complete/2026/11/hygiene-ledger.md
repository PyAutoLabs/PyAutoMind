Merged PyAutoBrain#736 (human /prm, 2026-11-27). Phase 14.0 of the maintenance orchestrator (SIG-3).

**Hygiene ledger** (`board/_hygiene_ledger.py`)
- Append-only JSONL, one line per UTC day.
- Each line holds per-mode counts, `status`, `not_scanned`, `absent_repos`, `unkeyed` and `evidence`.
- Per-finding keys have no line numbers: `refs:<repo>:<file>:<ref>`; `docstrings`/`escapes` at file level; `optdeps:<ws>:<script>:<dep>`; `extras:::<dep>`.
- A same-day merge never lets an incomplete mode replace complete keys.
- The board fills `history` (30 days) and draws a sparkline per row.

**How it is written: a Pages sidecar.** Workflow permissions are unchanged; a commit would need an App token under the M2.2 ruleset.
- The fetch bypasses the cache and fails closed.
- A 404 is accepted only on a true first publish, or with `--reset`.
- A corrupt body, or a ledger shorter than the live board's history, fails.
- `--apply` requires the ledger and its fetch marker, and never publishes fewer days than were fetched (exit 5).

**Scan-root fix.** The cloud reported 55–58 dead refs and the laptop 0. Now:
- the scan set comes from the body map (`workspace` + `howto`);
- every other declared repo is cloned reference-only (blob:none, no checkout) and indexed with `git ls-tree -r HEAD`;
- an absent repo makes refs `partial`.

Simulated cloud and laptop: refs 0 dead, 283 skipped.

Full suite 2733 passed. Independent Opus review, 3 rounds: two had majors (ledger durability, absent-clone completeness), the last was CLEAN. Heart dev-ship GREEN.

**Open follow-ups:**
- The witness (non-empty history over two days) needs two daily Brain Board runs after merge.
- Two declared repos are private, so their cloud clones fail; refs would stay `partial` if they're ever referenced.
- The laptop/cloud `tokens` row difference (the workspace-root AGENTS.md) remains.

## Original prompt

# Brain board: keep a hygiene ledger and show its trend

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-12
Issued: 2026-11-27
Epic: autonomous-orchestrators
Consequence: glance
Witness: after two board runs on different days the published `board.json` carries a non-empty `history` with one point per day per hygiene row; each hygiene row on the Brain board shows a sparkline; a test shows a run appends exactly one ledger line per day (idempotent on re-run)
Review-minutes: 10
Unattended: ready
Lane: any

Source: SIG-3 from the ecosystem review, **re-checked 2026-11-12 and holds** (during PyAutoHeart#338): `board/_board.py:647` sets `data["history"] = []`; `brain_board.yml` has `contents: read` and no commit step; Brain has no hygiene ledger file; the published `board.json` has `history: []` and 15 hygiene rows with counts that are never kept, though Brain Board has run 176 times since 2026-08-24. The SIG-2 half (unit-test trends on the Heart board) shipped in PyAutoHeart#338.

Change: an append-only hygiene ledger in Brain (one line per day: date, sha, each hygiene row's count), written by `brain_board.yml` (needs `contents: write` and a ledger-only commit step, or the Pulse/Heart pattern of a published sidecar if a commit is unwelcome — decide and say why); `_board.py` fills `history` from it and the board renders a sparkline per hygiene row.

<!-- filed 2026-11-12 by the programme lead session (split from PyAutoHeart#338) -->

## Phase 14 slice 14.0 (added 2026-11-27)

This draft is slice 14.0 of `draft/feature/pyautobrain/maintenance_orchestrator.md`, buildable before the M3 gate (human decision 1). It also needs:

- **Per-finding keys** in the ledger (`<mode>:<repo>:<file>:<reference>`, without the line number), so 14.5 can dedupe.
- **The scan-root fix:** on 2026-11-27 the cloud board reported 55 broken refs in 2 of 5 repos, while a laptop `hygiene refs --json` reported 0 in 0 of 8. Find why the roots differ, and make both scan the same set.
