# Standardize CLAUDE.md → AGENTS.md across the whole ecosystem

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
- every repo in repos.yaml (all organs, libraries, workspaces, howtos,
  assistants, pipelines, projects, admin — see body)
Difficulty: large
Autonomy: supervised
Priority: normal
Status: complete

<!-- RESOLVED 2026-07-12 (via z_features/agents_md_standardization.md). Landed as
     spec'd: check_claude_md_pointers + a --write pointer sweep + an AGENTS-less
     report in repos_sync.py; recommendation (a) taken (enforce the pointer only
     where an AGENTS.md exists; report AGENTS-less repos, never auto-stub); root-
     of-repo only. Sweep found every reachable AGENTS.md-bearing repo already
     carries a working @AGENTS.md pointer (organs fixed this session: Heart#67,
     Build#147, Memory#21). See the epic's Outcome section for the full report. -->

Standardize CLAUDE.md → AGENTS.md across the ecosystem. Sweep **every repo in
`PyAutoMind/repos.yaml`** so each one carries a `CLAUDE.md` that is a thin,
identical `@AGENTS.md` pointer, and add a `repos_sync.py` drift check that keeps
it that way. Motivated by a surprising gap found 2026-07-12: **PyAutoMind had no
`CLAUDE.md` at all**, so on Claude Code (which loads `CLAUDE.md`, not
`AGENTS.md`) a Mind session auto-loaded *nothing*; PyAutoBrain's `CLAUDE.md` was
a dead *prose* pointer ("read AGENTS.md") that never auto-expands into context.
Both were fixed (PyAutoMind `main`; PyAutoBrain#100) — this generalises that fix
so no repo silently loads nothing for Claude, and the convention can't drift back.

**The standard (settled, don't re-litigate):** guidance is agent-agnostic and
lives in `AGENTS.md` (read natively by Codex, Cursor, etc.). Claude Code reads
`CLAUDE.md`, not `AGENTS.md`, so each repo keeps a **content-free** `CLAUDE.md`
whose whole job is to import the agnostic source. The canonical body is the one
already committed to Mind and Brain:

```
@AGENTS.md

<!-- Guidance is agent-agnostic and lives in AGENTS.md (read natively by Codex,
     Cursor, etc.). Claude Code loads CLAUDE.md, not AGENTS.md, so this file exists
     only to import that one source. Keep it a pointer — put content in AGENTS.md. -->
```

`@AGENTS.md` is Anthropic's documented bridge (imports the file into context in
full at launch; recursive to a max depth of 4). Use the **import, not a symlink**
— it keeps a real, greppable `CLAUDE.md` that can carry a Claude-only section
later if ever needed, and avoids Windows symlink friction.

**Mechanism (extend the existing drift-check system, don't build a parallel one):**
add a `check_claude_md_pointers(root, repos)` to `PyAutoMind/scripts/repos_sync.py`
alongside the current checks. For every repo in the manifest that is checked out,
verify: (1) an `AGENTS.md` exists, and (2) a `CLAUDE.md` exists and contains an
`@AGENTS.md` import (not just prose mentioning it). Report each miss as drift.
Pair it with a `--write` sweep step (mirroring the new `write_block` /
`system_map` work) that *creates* the standard pointer where a repo has an
`AGENTS.md` but no compliant `CLAUDE.md`. Absent repos are skipped, exactly like
the map-block generation, so it runs in a partial/web checkout.

**Decisions to settle during intake back-and-forth:**
- **Repos with no `AGENTS.md` yet** (several workspaces are code-heavy / doc-light
  and may have neither file). The pointer is meaningless without a target. Options:
  (a) enforce the pointer *only where an `AGENTS.md` exists* and separately flag
  repos missing an `AGENTS.md`; (b) also generate a minimal stub `AGENTS.md`.
  Recommend (a) for this task — writing real per-repo `AGENTS.md` guidance is its
  own work, out of scope here; the check should *report* AGENTS-less repos, not
  auto-stub them.
- **Nested pointers.** Brain has per-agent nested `AGENTS.md` files; Claude loads
  nested `CLAUDE.md` lazily. Recommend **root-of-repo only** for now — the nested
  agnostic `AGENTS.md` are read on demand and don't need per-dir Claude pointers.
- **Execution shape.** These are ~28 separate GitHub repos. Decide one-PR-per-repo
  vs a batched sweep, and whether the hygiene conductor's `tidy`/drift surface
  should later *consume* this check rather than it running only in `repos_sync`.

**Boundaries:** this is repo hygiene enforced by `repos_sync` (Mind's body-map
drift-checker), which already validates every repo against `repos.yaml`; it is
the right home because the check is a pure function of "is this repo in the
manifest?" It is adjacent to — not part of — the hygiene *conductor*
(PyAutoBrain), which could later surface the finding; keep the check in Mind.

**References:** the landed precedent — organism-map block + `@AGENTS.md`
convention (PyAutoMind `main`, `repos_sync.py` `system_map`/`write_block`;
PyAutoBrain#100). The load-mechanics behind the standard (Claude Code reads
`CLAUDE.md` not `AGENTS.md`; `@import` is the official bridge, loads in full,
max depth 4; web sessions are single-repo and clone-based) come from the
2026-07-12 research pass on agent context-loading.

<!-- re-homed 2026-07-12 from a /remote-control conversation. The mechanical
     intake scorer classified this triage/low-confidence (weak keyword signal on
     "standardize/CLAUDE.md", default target PyAutoBrain); re-homed by reasoning to
     maintenance/pyautomind because the enforcement is a repos_sync drift check
     over repos.yaml. Follows the CLAUDE.md→AGENTS.md fix landed the same day. -->
