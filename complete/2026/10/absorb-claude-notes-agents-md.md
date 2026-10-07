## absorb-claude-notes-agents-md
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/492
- completed: 2026-10-07
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/493

- Merged as `8048a2f3` (2026-10-07); sibling of `retire-claude-md-pointers` (PyAutoMind#483).
- `policy/workspace_model_delegation.md` absorbs the root `CLAUDE.md` "Claude-specific notes", corrected: points at `MODEL_DELEGATION.md`'s bounded-worker contract and heartbeat (the `WORKFLOW.md` template left in a7d8fce), Sonnet floor is ship_* step 4, slash commands are the installed skills. Body 1069 B.
- `skills/WORKFLOW.md` / `skills/MODEL_DELEGATION.md`: "Model delegation" and "No OpenAI API fallback" have one home in MODEL_DELEGATION.md; the independent-review rule stays in WORKFLOW.md (pinned by `test_chat_orchestration_contract.py`).
- Stale `CLAUDE.md` references dropped or marked legacy across ORGANISM.md, BUILD/HEART capabilities, repo_cleanup skill, agent_harness_smoke doc, `bin/install.sh`, tests; `_memory.py` reads only `wiki/AGENTS.md`.
- 11 skill descriptions over 300 chars trimmed to ≤ 250, trigger phrases kept, no renames. Brain suite 1291 passed (clean shell).
- Measured fact worth keeping: a fresh delegated `general-purpose` subagent DOES receive the full AGENTS.md hierarchy plus skill descriptions (~18-22k tokens); only built-in Explore/Plan skip it.
- Partial vs done-when: `_clone.py` / `regroup_workspace.py` keep `CLAUDE.md` as tolerated-legacy until #482's wave lands — re-filed as `draft/maintenance/pyautobrain/drop_legacy_claude_md_patterns.md`. Human follow-up: re-run `bin/install.sh` in the root workspace and delete root `CLAUDE.md`.
- Remainder shipped 2026-10-07: PyAutoBrain#495 (`766c0063`) dropped the tolerated-legacy patterns — `complete/2026/10/drop-legacy-claude-md-patterns.md`; the "no file in PyAutoBrain names CLAUDE.md" done-when is now met.

## Original prompt

# Fold the Claude-specific notes into the generated AGENTS.md policy block; drop stale CLAUDE.md references; trim skill descriptions

Type: maintenance
Target: pyautobrain
Repos:
- @PyAutoBrain
Difficulty: medium
Autonomy: supervised
Consequence: judge
Priority: high
Status: draft
Filed: 2026-10-07
Issued: 2026-10-07

## Request (verbatim, from the 2026-10-07 token-efficiency review)

> Do a review of the Pyauto ecosystem, mostly with a view to ensure we have
> things set up to ensure efficient token use [...] Note that claude supports
> AGENT.md now so maybe we can remove all CLAUDE.md? Also, I have read how opus
> agents dont read these .md files now, or dont when delegated, so given our
> Fable delegation default we may also want to update certain things based on
> how most recent Claude versions run? [...] yes do 1, sort other findings
> [...] Make sure you dont do a change which would impact codex or other agents.

## Measured facts (Claude Code 2.1.292, 2026-10-07)

- AGENTS.md loads natively; every CLAUDE.md is being retired (sibling Mind
  prompt `draft/maintenance/pyautomind/retire_claude_md_pointers.md`). The
  unversioned workspace-root `CLAUDE.md` goes too, so its "Claude-specific
  notes" need a versioned, agent-agnostic home that `bin/install.sh` already
  regenerates into the root AGENTS.md: `policy/workspace_model_delegation.md`
  (the `pyauto:model-delegation` block, install.sh L184-208).
- The claim "delegated Opus subagents don't read CLAUDE.md" is **false**: a
  fresh `general-purpose` subagent receives the full CLAUDE.md/AGENTS.md
  hierarchy plus the skill-description list (~18-22k tokens per delegation).
  Only built-in Explore/Plan skip it. So the per-delegation cost is what to
  trim, and nothing needs to be re-stated in subagent prompts for safety.
- Skill `description:` fields are listed in every session AND every delegated
  subagent (~2.8k tokens today). SKILL.md is installed into both the Claude and
  Codex skill roots, so shorter descriptions help both.

## Scope (this repo only)

1. `policy/workspace_model_delegation.md` — absorb the root CLAUDE.md
   "Claude-specific notes" (text below) in provider-neutral wording ("Anthropic
   sessions…"), **corrected**: the subagent prompt template and "Progress
   heartbeat" section no longer exist in `skills/WORKFLOW.md` (removed in
   a7d8fce, 2026-09-18) — point to `skills/MODEL_DELEGATION.md` ("Bounded worker
   contract" and the heartbeat paragraph, L79-95) instead; the Sonnet floor is
   ship_* **step 4** (execution), not step 3; slash commands resolve through the
   installed skills (`bin/install.sh`), not a hand-made symlink dir. Keep the
   block ≤ ~1.2 KB. Check `workspace_model_delegation_pointer.md` still reads
   right. Verify with `bin/install.sh --write-agents-surface` (or whichever
   flag regenerates the root block) that the block renders.
2. `skills/WORKFLOW.md` — collapse the duplicated passages to one-line pointers
   into MODEL_DELEGATION.md: "Model delegation" (L102-114), "no OpenAI API
   fallback" (L92-100), the independent-review rule (L73-80, keep one home).
3. Stale CLAUDE.md references → AGENTS.md or deleted: `ORGANISM.md:102` ("a
   CLAUDE.md stub"), `agents/conductors/build/BUILD_CAPABILITIES.md:6,54`
   (cites `PyAutoHands/CLAUDE.md`), `skills/repo_cleanup/SKILL.md:35`,
   `agents/faculties/vitals/HEART_CAPABILITIES.md:98`,
   `docs/agent_harness_smoke.md:10,78`, `agents/conductors/clone/_clone.py:75,96`,
   `agents/faculties/memory/_memory.py:44`, `bin/regroup_workspace.py:138,151`
   (tolerate absence), `bin/install.sh` header comments, and the tests
   `tests/test_skill_install.py`, `tests/test_memory_surfaces.py`.
4. Trim every skill `description:` over 300 characters to ≤ 250 while keeping
   its trigger phrases (cortex 508, sampler_pipeline 445, ci_speedup 425,
   community 409, intake 396, batch 383, board 346, issue_cleanup 343,
   hygiene 324, eyes 321). Descriptions live in `skills/<name>/SKILL.md`.
   Re-run `bin/install.sh` afterwards only if a skill name changed (none should).
5. Brain test suite green; `python3 PyAutoMind/scripts/repos_sync.py --check`
   still passes for the Brain-owned generated blocks.

### Root CLAUDE.md text being absorbed (for reference; do not copy its errors)

- Workflow steps are slash commands (`/start_dev`, `/ship_library`…).
  "Plan before editing" = Plan Mode + ExitPlanMode approval.
- Model split: planning, judgment and orchestration stay in the session's
  model; execution is delegated via the Agent tool along Fable > Opus > Sonnet.
  Fable session → architect: plans and decomposes, delegates ALL remaining work
  (implementation, edits, tests, tutorial prose, ship phases) to Opus subagents.
  Opus session → plans in-session, delegates execution to Opus; Sonnet only for
  the fixed ship_* / pre_build shell-and-git recipes. If weighing whether a
  phase is mechanical enough for Sonnet, it isn't.
- Applies to every task in the workspace, not only start_dev runs. State the
  session model in the opening line; delegate anything more than a few lines
  of edits or a couple of file reads. Stay in-session only for answering from
  loaded context, a handful of reads, few-line edits in files already read, and
  anything that is itself a conversation with the user.
- Long delegations report back: pass every subagent a progress file and arm a
  Monitor on it so milestones surface as one-line notifications.

## Out of scope

Organ map blocks in the 8 organ AGENTS.md (they serve standalone clones and
Codex sessions started inside one repo — keep). The per-repo `.claude/skills`
re-listing when a repo file is read (needed by remote sessions — keep, note
only). Root-file edits (unversioned; the human session does them).

## Done when

The regenerated root block carries the corrected Claude notes; no file in
PyAutoBrain names CLAUDE.md as a thing that exists; all skill descriptions
≤ 300 chars; tests green.
