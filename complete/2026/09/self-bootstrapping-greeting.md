## self-bootstrapping-greeting
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/138 (closed)
- completed: 2026-09-26
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/139 (merge ab6acde6)
- follows: complete/2026/09/cosmos-web-ring-greeting.md (#136/#137)
- summary: |
    The public greeting prompt is now self-bootstrapping from any directory: an agent handed the prompt
    and the repository URL clones autolens_assistant and follows its AGENTS.md. README, llms.txt and
    AGENTS.md carry the bootstrap block; the prompt gains the "First clone that repository" sentence; the
    greeting skill gains a Step 0 bootstrap check; the setup pages are aligned; a `bootstrap-smoke`
    benchmark card records the check; the Python floor is 3.12; the Codex invocation flags are
    documented. Verification: Claude Code v1 97, Codex v1 13x2, Claude Code v2 100. The website commit
    (Jammy2211.github.io a07c38d, simplifying the line to "Open Claude Code, Codex or another AI coding
    agent and paste this:") is pushed after the assistant merge.
- heart-red-override: "2026-09-26 live human, in direct response to the question naming this task, authorised the development-only override: push feature/self-bootstrapping-greeting and open the PR (no merge, no release, no CI bypass; merge via /prm on green checks). RED reason when authorised: release validation FAILED (stage integrate). At ship time (readiness ts 2026-09-26T15:24:39Z) Heart was YELLOW, no red_reasons; YELLOW: manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml. Gates passed: make test 130 passed 1 skipped + freeze-check OK; bootstrap-smoke Claude Code v2 100/100; no workspace smoke applies (no library change, script change formatting-only)."
- merge-authority: human typed /prm (separate explicit merge command); every check green at head 7ee29f3 (assistant boundary + wiki-currency, pull_request runs; no push-event workflows).
- follow-ups: |
    - Codex v2 bootstrap-smoke run (Codex limit resets 20:36).
    - Stage (b): re-run bootstrap-smoke from an empty directory with the real prompt and real URL on Claude Code and Codex, and record.
    - Wiki installation.md Python floor (3.12) via al_update_wiki.

## Original prompt

# Make the assistant greeting prompt self-bootstrapping from any directory

Type: feature
Target: autolens_assistant
Repos:
- autolens_assistant
Themes:
- assistant
- onboarding
- website
Difficulty: medium
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/lensing/log.md; wiki/galaxies/sources/cosmos-survey.md
Status: issued
Consequence: judge
Review-minutes: 20
Unattended: needs-input
Follows: complete/2026/09/cosmos-web-ring-greeting.md (autolens_assistant#136 / #137, merged 2026-09-26)
Filed: 2026-09-26
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/138

## Request

Verbatim from James's handoff note:

> The line 'Install the PyAutoLens Assistant, open Claude Code, Codex or another AI coding agent, and paste this:'. I want installation to happen inside the assistant task itself. Today the autolens_assistant README has the HUMAN clone the repo and start the agent inside it. PyAutoLens itself is auto-installed after the first prompt, but an agent opened elsewhere and handed the prompt + URL has nothing telling it to clone the repo and follow its AGENTS.md. Plan: /intake a prompt for autolens_assistant to make the greeting prompt self-bootstrapping from any directory. For example, an agent-facing section at the top of README telling an agent that arrived via the URL to clone, cd in and follow AGENTS.md; verify from an empty directory with Claude Code and Codex. Once that ships, simplify the website line to 'Open Claude Code, Codex or another AI coding agent and paste this:'.

## Context

The public greeting prompt — on the jamesnightingale.net home page and `/natural_language/`, in the
autolens_assistant README and `docs/setup/first_prompts.md`, and keyed by
`skills/al_greeting_cosmos_web_ring.md` — begins:

> I want to use the PyAutoLens Assistant: https://github.com/PyAutoLabs/autolens_assistant

An agent started in an arbitrary directory sees only that URL. Nothing at the URL today tells an
agent (as opposed to a human) to clone the repository and follow its AGENTS.md, so the greeting only
works when the human has already cloned the repo and launched the agent inside it.

## Deliverable sketch

1. **Agent-facing bootstrap block** near the top of `README.md` (and mirrored wherever agents read
   first — e.g. a short `BOOTSTRAP.md` or the README's first section): if you are an AI agent that
   arrived here from the starting prompt and this repository is not your cwd, `git clone` it, `cd`
   in, then follow `AGENTS.md` (which handles installing PyAutoLens and the greeting).
2. **Greeting skill tolerates a pre-clone start** — make sure the first step of
   `skills/al_greeting_cosmos_web_ring.md` works when invoked before the clone exists.
3. **Verification protocol** — from an EMPTY directory, paste the exact website prompt into Claude
   Code and into Codex; confirm both clone, install, and show the F444W picture with the one
   background question. Record both transcripts' outcomes under `docs/evaluation/` or the benchmarks
   `harness_smoke` rubric. This two-agent leg is human-watched.
4. **Website line** — after shipping, simplify the line on both pages to
   "Open Claude Code, Codex or another AI coding agent and paste this:" (website repo
   Jammy2211.github.io: `index.html` and `natural_language/draft.md` + `render.py`).

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b27801cc-44cb-4171-8182-25240f31b06e/scratchpad/self_bootstrapping_greeting_prompt.md -->
