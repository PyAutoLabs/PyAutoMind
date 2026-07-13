# Generate the command surface into AGENTS.md (agent-agnostic discovery)

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- every organ repo (the generated block lands in each organ's AGENTS.md)
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: complete

<!-- RESOLVED 2026-07-12 (via z_features/agents_md_standardization.md). Landed via
     recommendation (a): install.sh --write-agents-surface / --check-agents-surface,
     generated from the bin/pyauto-brain agent registry (the single source), drift-
     checked by two Brain CI tests. Scope change: the block is NOT duplicated into
     every organ — PyAutoBrain is guaranteed loaded in every session, so the surface
     lives once in Brain's auto-loaded AGENTS.md and reaches everywhere. See the
     epic's Outcome section.

     UPDATE 2026-07-12: the previously-deferred per-tool layer was then built too —
     install.sh --write/--check-project-discovery commits a .claude/ + .codex/
     discovery tree (relative symlinks into each repo's own skills/) so slash
     commands + skills register on Claude Code web/cloud and Codex, where the
     user-level ~/.claude symlinks don't travel. Per-repo (Mind/Brain/Heart/Build),
     single-source, drift-checked. -->


Generate the command surface into AGENTS.md. Make the PyAuto command surface
(`intake`, `route`, `start_dev`, `ship_*`, the conductor verbs, etc.)
discoverable to **every** agent on **every** tool, at session start, with **zero
per-tool discovery files** — by generating a drift-checked command-surface block
into each organ repo's agent-agnostic `AGENTS.md`, sourced from `skills/`.

**Demonstrated need (2026-07-12).** On Claude Code web/phone, verbs like
`/intake` are hard to find — a session hunts for the entrypoint instead of just
running the command. Root cause, confirmed in `PyAutoBrain/bin/install.sh`: it
registers slash commands by symlinking `skills/` into **user-level** roots
(`~/.claude/commands`, `~/.claude/skills`, `~/.codex/skills`;
`CLAUDE_HOME=${CLAUDE_HOME:-$HOME/.claude}`). Per the 2026-07-12 load-mechanics
research, user-level `~/.claude` (and the equivalent) are **not loaded in cloud/
web sessions** — only committed repo files and claude.ai-enabled skills travel.
So on CLI the symlinks exist and `/intake` is instant; on web nothing is
registered and the agent must reconstruct `bin/pyauto-brain intake` by reading
files. (That reconstruction *did* work this session — see below — which is the
whole point.)

**Why the fix is agnostic, and where the line is.** There is **no cross-tool
slash-command standard** (`AGENTS.md` is a standard for *guidance*, not for
commands); the slash prefix is irreducibly per-tool. So we do **not** chase an
"agnostic slash command" — that's a category error. Instead we lean on the layer
that is *already* agnostic: the deterministic **`bin/pyauto-brain <verb>`**
entrypoint, which any agent on any tool can run, plus the tool-neutral `skills/`
bodies. Both are surfaced through `AGENTS.md`, which every agent reads (Codex/
Cursor natively; Claude via the `@AGENTS.md` import landed the same day). Proof
it works: this session's `intake` run used **no** `/intake` registration — just
`bin/pyauto-brain intake`, discovered from `AGENTS.md`.

**Scope — the agnostic layer ONLY:**
- Add a generated, drift-checked **command-surface block** (its own
  `<!-- ...:begin/end -->` markers, like the `repos_sync:map` block) to each
  organ repo's `AGENTS.md`: one row per verb — verb · one-line purpose ·
  `bin/pyauto-brain <verb>` entrypoint — produced from the single `skills/`
  source (the `SKILL.md`/`<name>.md` the installer already enumerates). This
  formalises and replaces Brain's hand-maintained `## Running` list, and gives
  Mind (and the other organs) the same block they lack today.
- Because `AGENTS.md` is now auto-loaded and read by every tool, the full verb
  set + entrypoints are in context at startup, uniformly, with no per-tool files.

**Explicitly OUT of scope (deferred — the one thing that can't be agnostic):**
per-tool slash-command *sugar* (committed `.claude/` for Claude, the Codex
equivalent, claude.ai enablement). It's a per-tool loader, nice-to-have, and can
be added later as an opt-in generated from the same `skills/` — but it is not
required for the capability to work everywhere, so it is not built here.

**Decisions to settle during intake back-and-forth:**
- **Generator home.** The block is a function of `skills/` (across organs), which
  is `install.sh`'s domain, not `repos.yaml`/`repos_sync`'s. Options: (a) an
  `install.sh --write-agents-surface` (+ `--check`) mode reusing its existing
  skill scan; (b) a small dedicated generator drift-checked in CI like
  `repos_sync --check`. Recommend (a) — the installer already knows every verb.
- **Block scope: unified vs per-repo.** Recommend the **unified** surface (all
  verbs, wherever hosted) in every organ's block, so a single-repo web session
  still knows `/intake` exists and lives in PyAutoBrain. Caveat to state in the
  block: *discovery* is universal, but *invocation* of `bin/pyauto-brain <verb>`
  still needs the hosting organ checked out (web is single-repo) — the block
  should name the hosting organ so the agent knows what to mount.
- **Drift-check wiring.** Where the `--check` runs (Brain CI, or Heart's dev-loop
  legs), mirroring how `repos_sync --check` guards the body-map blocks.

**Boundaries:** this is the command-discovery twin of the CLAUDE.md
standardization (`maintenance/pyautomind/claude_md_standardization.md`) and rides
the same auto-loaded `AGENTS.md`. Content of the verbs stays in `skills/`
(agnostic, single source); this only surfaces a generated index of them. Does not
touch the entrypoint logic or the skills themselves.

**References:** `PyAutoBrain/bin/install.sh` (the `~/.claude`/`~/.codex` symlink
install); the auto-loaded `@AGENTS.md` + organism-map precedent (PyAutoMind
`main`; PyAutoBrain#100); the 2026-07-12 research pass (Claude Code reads
`CLAUDE.md` not `AGENTS.md`; user-level `~/.claude/skills|commands` absent on web;
web is single-repo and clone-based).

<!-- re-homed 2026-07-12 from a /remote-control conversation. maintenance/pyautobrain
     because the installer + command surface live in Brain. Scoped deliberately to the
     agent-agnostic layer only (command surface in AGENTS.md via the bin/ entrypoint);
     per-tool slash-command sugar is named and deferred, not built. Sibling to
     maintenance/pyautomind/claude_md_standardization.md. -->
