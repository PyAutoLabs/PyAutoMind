# Ecosystem AGENTS.md / CLAUDE.md / command-surface standardization (epic)

Type: maintenance
Target: PyAutoBrain
Repos:
- every repo in repos.yaml
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Epic tracker for three filed standardizations that share one root cause — *web/
mobile sessions load only committed, agent-agnostic repo files* — and should be
executed together as one cross-repo sweep. Built to be run from a new chat that
has **only PyAutoMind + PyAutoBrain** open, updating **every repo in
`repos.yaml`**.

## How to run it (new chat, phone-friendly)

Open a new chat with PyAutoMind + PyAutoBrain, and send just:

> Read and execute `PyAutoMind/z_features/agents_md_standardization.md`.

The kickoff below is the full instruction; the chat should follow it verbatim.

## Specs (the three pieces — read first)

1. `maintenance/pyautomind/claude_md_standardization.md` — every repo gets a
   content-free `CLAUDE.md` that is `@AGENTS.md`, plus a `repos_sync` drift check.
2. `maintenance/pyautobrain/command_surface_in_agents_md.md` — a generated
   command-surface block in each organ's `AGENTS.md` (verb · purpose ·
   `bin/pyauto-brain <verb>`); **agent-agnostic layer only**.
3. Already-built: `scripts/repos_sync.py` `system_map` + `write_block` (the
   `<!-- repos_sync:map -->` block) — applied only to Mind and Brain so far;
   roll it out to the remaining organ repos (Heart, Build, Memory).

`AGENTS.md` is auto-loaded and gives you the organism map + boundaries.

## Kickoff prompt

You have PyAutoMind and PyAutoBrain checked out. This is an ecosystem-wide
standardization that must be applied to EVERY repo in `PyAutoMind/repos.yaml`,
even though only these two are open — bring the others in as needed.

**Goal — every repo in `repos.yaml` ends compliant:**
- Any repo that HAS an `AGENTS.md` → a `CLAUDE.md` that is exactly spec 1's
  canonical `@AGENTS.md` pointer.
- Organ repos (category `organ`) → also the generated map block and the new
  command-surface block at the top of `AGENTS.md`.
- Repos with NO `AGENTS.md` → do NOT auto-create one; record them in the report
  for a human.

**Order of work:**
- A. Build the tooling first, in Mind + Brain (open): spec 1's
  `check_claude_md_pointers` + `--write` sweep in `repos_sync.py`; spec 2's
  command-surface generator (recommend an `install.sh --write-agents-surface`
  mode reusing its skill scan) + check; spec 3's rollout of the map block to all
  organ repos. Verify generators + drift checks pass on Mind and Brain, then
  commit the tooling.
- B. Sweep every other repo, running the generators against each.
- C. Verify with the drift checks; open PRs.

**Reaching the other repos:** enumerate every repo from `repos.yaml`. For each
not already open, add it with `add_repo` (confirm with `list_repos`), run the
generators locally, and push. Prefer local checkout + generation so the drift
checks run; fall back to the GitHub API for a file-only patch if a checkout
isn't available.

**Guardrails:**
- Agent-agnostic ONLY. No per-tool slash-command sugar (no committed `.claude/`,
  no Codex dirs, no claude.ai enablement). The command surface is the
  `bin/pyauto-brain <verb>` entrypoint documented in `AGENTS.md`; content stays
  in `skills/` and `AGENTS.md`.
- `CLAUDE.md` is content-free — the `@AGENTS.md` pointer only.
- Never rewrite history (see Mind `AGENTS.md` hard rules). Respect the tenant
  firewall (`repos_sync.py` FIREWALL_ALLOWLIST).
- One branch + PR per repo (e.g. `chore/agents-md-standardization`). Do NOT merge
  without the user's go-ahead; you may auto-merge a trivial pointer-only PR if CI
  is green, but say which.
- Idempotent: skip any repo already compliant.

**Deliverable:** a compliance report table — repo · had CLAUDE.md? · had
AGENTS.md? · map block? · command-surface block? · action taken · PR link — and a
separate list of every repo missing an `AGENTS.md`.

## Scope split (matches the specs)

- `CLAUDE.md` `@AGENTS.md` pointer → **all** repos that have an `AGENTS.md`.
- map block + command-surface block → **organ** repos only (the "you are one
  organ" framing doesn't fit libraries/workspaces).

<!-- filed 2026-07-12 from a /remote-control conversation as the runnable epic
     over the three same-day maintenance specs. Root cause shared: web/mobile
     loads only committed agent-agnostic repo files, not user-level ~/.claude. -->
