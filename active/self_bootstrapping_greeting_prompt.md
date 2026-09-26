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
