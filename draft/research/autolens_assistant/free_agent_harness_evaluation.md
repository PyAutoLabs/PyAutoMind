# Record harness-smoke runs for free Codex, a named OpenCode configuration and Gemini CLI

Type: research
Target: autolens_assistant
Repos:
- @autolens_assistant
- @autofit_assistant
- @autogalaxy_assistant
Themes:
- assistant
- support-policy
Difficulty: low-medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 15
Unattended: needs-access
Filed: 2026-09-10

## Why

The assistants adopted an **agentic-only support policy** on 2026-09-10 (branch
`claude/agentic-only-support-policy-9jg8yz` across autolens/autofit/autogalaxy/autocti_assistant,
PyAutoBrain, PyAutoLens/PyAutoGalaxy/PyAutoFit docs and the two workspaces): Claude Code and Codex
recommended; OpenCode experimental; Gemini CLI a candidate for maintainer evaluation only; browser-chat
routes retired and archived. Every support statement now points at
`autolens_assistant/docs/evaluation/agent_evaluation.md` and the frozen card
`benchmarks/prompts/harness_smoke.md` (grounded answering · a small fit whose figure the agent must
inspect · recovery from a planted stale-API error) as the evidence a promotion needs.

**None of those runs could be performed in the adopting session** — a remote container with no
access to the agents. This prompt is the recorded gap.

## Do

On a laptop with the PyAuto stack, for each configuration below: scaffold with
`python autoassistant/benchmark.py new-run harness-smoke --model <m> --harness <h>`, run the three
messages verbatim in a fresh session, score, `report`, and commit the run directory. Record failures.

1. **Codex on a free ChatGPT account** — first verify the current position on
   `developers.openai.com/codex/pricing` (unreachable from the adopting session; the Codex README lists
   Plus/Pro/Business/Edu/Enterprise or an API key). If no free access exists, record that as the result
   and stop; do not purchase access for this.
2. **OpenCode with one named free provider/model** — pick a model whose card states tool use **and**
   image input (OpenCode Zen's free models are documented as limited-time; only one Zen model is
   documented as vision-capable and it is not free). A J3 fail (cannot see the fit figure) is the most
   useful negative result and disqualifies the configuration from the full workflow.
3. **Gemini CLI** — resolve the access conflict first (the retired setup page recorded free/individual
   access ending 2026-06-18; the CLI's quota document currently lists a free individual tier of
   1,000 requests/day). `.gemini/settings.json` already points it at `AGENTS.md`.

Then update `agent_evaluation.md`'s status table (dated), and only on a recorded pass of all three
checks promote OpenCode's tested configuration into `docs/setup/opencode_cli.md` with its test date
and limitations. Do not add a user-facing Gemini CLI page without a recorded pass.

## Witness

`benchmarks/runs/harness-smoke/` in autolens_assistant contains at least one scored run per
configuration attempted (or a dated "no access" note in the evaluation table), and
`benchmarks/RESULTS.md` regenerates with them.
