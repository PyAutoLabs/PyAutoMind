# bootstrap-smoke: run Codex on the v2 prompt, then merge the post-merge bench record

Type: feature
Target: autolens_assistant
Repos:
- autolens_assistant
Themes:
- assistant
- benchmarks
- onboarding
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 10
Unattended: needs-input
Follows: complete/2026/09/self-bootstrapping-greeting.md (autolens_assistant#138 / #139, merged 2026-09-26)
Filed: 2026-09-26

## Why

The self-bootstrapping greeting shipped (#139) with these verification records under
`benchmarks/runs/bootstrap-smoke/`: Claude Code v1 prompt 97, Codex v1 prompt 13 ×2 (zero
tool calls, the finding that added the clone sentence to the prompt), Claude Code v2 prompt
100. After the merge a real-URL Claude Code run scored 98 and is committed on branch
`bench/bootstrap-smoke-stage-b` (head 7ca904b, pushed, no PR — held by James on 2026-09-26
because Heart was YELLOW on two manifest-drift reasons). Codex could not be run on the v2
prompt: its usage limit resets 2026-09-26 20:36.

## Plan

1. In a fresh worktree of `bench/bootstrap-smoke-stage-b`, run the Codex check from an EMPTY
   directory with the exact README starting prompt (real URL):
   `codex exec --json -s workspace-write -c sandbox_workspace_write.network_access=true --skip-git-repo-check "<prompt>"`
   (codex-cli 0.157 has no `--full-auto`). Score M1-M5/J1-J3 per
   `benchmarks/prompts/bootstrap_smoke.md` v2, record with `benchmark.py new-run bootstrap-smoke
   --model <model> --harness codex`, `score`, `report`; update the Check 4 row in
   `docs/evaluation/agent_evaluation.md`.
2. If Codex still asks the background question without cloning, that is the finding: record it
   and file a follow-up on prompt wording / Codex AGENTS discovery rather than retrying.
3. Open one PR for the branch (both post-merge records), acknowledging Heart YELLOW if still
   yellow; human `/prm`.
4. Already on the branch (2026-09-26 17:06, head ca19325): the `wiki/core/operations/installation.md`
   Python 3.12 floor via `al_update_wiki` (provenance re-pinned to the 2026.9.26.1 SHAs, currency
   checks clean) and the README/first_prompts Colab badge pinned to `blob/2026.9.26.1/`. The
   website's Colab links are pinned to the same tag (Jammy2211.github.io 3e78dca, live). So the
   PR in step 3 ships three things: the post-merge Claude record, the Codex record, the wiki +
   badge follow-ups.
