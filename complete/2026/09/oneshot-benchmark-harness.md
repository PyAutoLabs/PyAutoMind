- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/126 (closed completed 2026-09-17)
- completed: 2026-09-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/127 (MERGED, merge `ddaa0fa5`; head `5bd7083c`, 4 commits)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/380 (MERGED, merge `383d3219`; head `58a775ac`) — the clone partition + VALIDATION_PLAN half, merged first
- ci: autolens_assistant `wiki-currency` green; `boundary` (clone-boundary against PyAutoBrain main) red on the first run, green on re-run after #380 merged — see traps. PyAutoBrain `pytest (3.12)` / `pytest (3.13)` green; mergeable_state CLEAN on both before merge.
- heart: not consultable in the session (no pyauto-heart in the web container); tooling-only change, no library touched; no freeze flag readable.
- surface: web-github session (session clones, no task worktree, no `gh`; issue/PR/merge driven through the GitHub MCP tools). Autonomy `supervised`: plan on the issue, human "Go / Continue" in-session; shipped to PR-open, then `/prm` typed by the human.

- summary: Rebuilt the autolens_assistant benchmarks around two rules decided
  2026-09-17 — a benchmark is **one-shot** (one prompt, a fresh headless
  session, no operator) and its result is a **computed number** (a per-card
  `score.py`, never a typed rubric). `autoassistant/benchmark.py` gained
  `run <card> --model M --harness H [--repeats N] [--dry-run] [--keep-workdir]`
  (git-archive workdir minus `benchmarks/truth/` and `benchmarks/runs/`, fixed
  no-further-input footer naming the run dir, harness argv from
  `benchmarks/harnesses.yaml` — Claude Code `-p --output-format stream-json`,
  Codex `exec --json` — PATH shims that time every interpreter call into
  `compute.log`, transcript parsing for tokens/cost/turns, hook-debris cleanup),
  `score-oneshot` (idempotent re-score, refreshes meta.yaml) and `freeze-check`
  (in `make test`). Score contract: common gates `finished` / `schema` /
  `compute_budget` / `run_budget`, card metrics in [0,1], `score = 100 ×
  mean(metrics) × Π gates` → `score.json`; RESULTS.md reports median and
  min–max per (version, model, harness). Prompt freeze: `prompt_sha256` in the
  card frontmatter + append-only `benchmarks/VERSIONS.lock`, compared against
  `origin/main`. First card `benchmarks/prompts/oneshot/oneshot-smoke/`
  (grounded answering, no fit; recorded run Claude Code / claude-sonnet-5 →
  score 100, 23.7 s wall, 0.3 s compute, $0.22). The four 2026-07 conversational
  cards retired to `benchmarks/prompts/conversational/` (kept, not run);
  `harness_smoke.md` stays as the operator-driven qualification card.
  PyAutoBrain: `benchmarks/harnesses.yaml` + `VERSIONS.lock` generic,
  `benchmarks/truth/*` domain, VALIDATION_PLAN names the one-shot check.
  Tests: 47 in the two benchmark test files (36 new, hermetic fake harnesses);
  Brain clone tests 44.
- execution: Fable session as architect; implementation delegated to one Opus
  subagent (~19 min, 3 commits) under the WORKFLOW.md prompt contract; review
  fixes in-session (sentence counter, debris cleanup, meta refresh).
- traps:
  - **`Brain-ref:` must start its own line.** `clone-boundary.yml` parses the PR
    body with `sed -n 's|^Brain-ref:…'`; written mid-line ("Closes #126.
    Brain-ref: …") it silently falls back to PyAutoBrain `main`, and the
    boundary check goes red on the very files the Brain PR classifies. Fix was
    the intended gate order anyway: merge the Brain PR, re-run the failed job.
  - **`claude --permission-mode bypassPermissions` refuses to run as root**;
    inside a root container the runner needs `IS_SANDBOX=1` in the operator's
    env or every run scores 0 with an empty transcript (documented in
    benchmarks/README.md "Adding a harness"). The first attempt was deleted and
    redone — the agent never started, so it was not a measurement.
  - **Sentence counting on '.' is wrong for this domain**: the first real run's
    two-sentence summary cited `skills/al_configure_search.md` and
    `af.Nautilus` and read as five sentences (score 75). A sentence now ends at
    terminal punctuation followed by whitespace/end; run re-scored to 100 under
    the same unpublished card version.
  - The benchmarked session's own SessionStart hook writes a `.claude/` beside
    the workdir (its parent looks like a workspace root); the runner now deletes
    dot-entries that appear during a run.
  - `pytest autoassistant/tests` aborts at collection in the web container
    (`test_mcp_tools.py` needs numpy) and 12 API-gate/preflight tests need an
    installed autolens — identical on `main`; `--ignore` the MCP file to see the
    rest. `test_repo_readme_prompts_match_cards` was already red on `main` and
    is gone with the retired tier.
  - `claude -p` works headlessly inside the Claude Code web container (probe:
    `--output-format json --max-turns 1` returns `total_cost_usd`, `usage`,
    `modelUsage`), so a harness can be exercised end to end there; the model
    under test defaults to sonnet unless `--model` is passed.
- follow-ups-open: `draft/feature/autolens_assistant/benchmark_positions_initialised_inference.md`
  and `benchmark_forward_model_consistency.md` (Blocked-by cleared by this
  record); three `oneshot-smoke` repeats on Claude Code and Codex on a laptop
  with the agents installed; the codex `exec --json --full-auto` template is
  unverified against a real Codex install; `freeze-check`'s origin/main leg
  first bites on the next card edit (the lock is new on main).

## Original prompt

# One-shot benchmark harness and computed-score contract for the assistant benchmarks

Type: feature
Target: autolens_assistant
Repos:
- autolens_assistant
- PyAutoBrain
Themes:
- assistant
- benchmarks
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `benchmark.py run harness-smoke --harness claude --repeats 1` executes headlessly end to end on a laptop and yields transcript, meta.yaml, result.json (or a gate failure with reason) and score.json; RESULTS.md regenerates from score.json only; the prompt-hash tests fail when a card body is edited without a version bump; the four 2026-07 cards sit under conversational/ and RESULTS.md no longer lists them as runnable.
Review-minutes: 15
Unattended: needs-access
Filed: 2026-09-17
Issued: 2026-09-17

## Why

The `benchmarks/` package that shipped 2026-07-10 (autolens_assistant#57/#58, record
`complete/2026/07/assistant-benchmarks.md`) has never recorded a run. The calibration
campaign was shelved on 2026-08-18 (`complete/archive/shelved/benchmark_calibration_runs.md`)
and its read-only audit explains why the design could not produce comparable numbers:

- the four cards are **conversational** — they assume an operator answering the agent
  back, so every run depends on who sat at the keyboard;
- the 100-point rubric is **typed by the operator** — `parse_score` sums whatever was
  entered, no row inspects `scripts/`, `output/` or a figure, and "machine-checkable"
  rows are prose, not checks;
- the **frozen-prompt rule is enforced by nothing** — a README+card edit passes CI with
  `version` unchanged, so `prompt_version` in `meta.yaml` can record the same version
  across a changed prompt.

Redesign decision (2026-09-17, author): assistant benchmarks are **one-shot** — "what
happens without user input" — and their result is a **computed number**. This prompt is
the harness and the scoring contract; the two first cards are filed separately
(`benchmark_positions_initialised_inference.md`,
`benchmark_forward_model_consistency.md`) and are blocked on this one.

## Do

**1. One-shot means headless.** A benchmark is one prompt sent once to a fresh session
through the harness's headless entrypoint (`claude -p --output-format stream-json` for
Claude Code, `codex exec` for Codex; one adapter per supported harness, in the same
place the agentic-only support policy of 2026-09-10 lists them). No operator turn ever
follows. Every card's prompt ends with the same fixed footer, held once in the harness
and appended verbatim:

> You will receive no further input. Do not ask questions. Decide, proceed, and finish by
> writing `result.json` to the run directory named in this prompt.

If the agent stops to ask anything, the run ends there and is scored on what exists.
The harness records the transcript (JSONL), token counts and cost as the CLI reports
them, wall time of the whole run, and wall time of the compute the agent launched
(the harness owns a timer around every subprocess the agent spawns, or reads the
search's own timing from `output/`).

**2. The score is computed, never typed.** Each card ships a `score.py` beside its
prompt. `benchmark.py score <run>` imports it and writes `score.json`; `RESULTS.md` is
regenerated from `score.json` files only. Every card's score has the same shape:

- **Gates** — binary, each with a machine reason. Common gates every card inherits:
  finished without asking a question (transcript has no unanswered user-turn
  request); `result.json` exists and parses against the card's schema; compute wall
  time under the card's budget (5 minutes on a laptop CPU for both first cards);
  whole run under the harness cap (15 minutes). A failed gate → score 0, `reason` set.
- **Metrics** — each a number in [0, 1] with its mapping written in the card (e.g.
  "relative error e → max(0, 1 − e/0.05)"). Score = 100 × mean(metrics) × Π gates.
- **Secondary columns** recorded and reported but never in the score: wall times,
  tokens, cost, model, harness, library versions (`pip freeze` of the PyAuto stack),
  hardware, date.
- **Truth is hidden.** Reference values live under `benchmarks/truth/<card>/` and the
  harness runs the agent in a working directory that does not contain it (a copy of the
  assistant checkout with `benchmarks/truth/` removed, or truth outside the checkout).
  A simulated dataset given to the agent ships **without** its `info.json`. The prompt
  never says it is a benchmark.
- **Repeats.** `benchmark.py run <card> --model M --harness H --repeats 3` is the unit
  of a campaign row; `RESULTS.md` reports the median and min–max per (card version,
  model, harness). Scores compare only within a card version.

**3. Freeze the prompt for real.** Each card's frontmatter carries `prompt_sha256`; a
test asserts the hash of the prompt body equals it, and a second test asserts that a
changed hash comes with a changed `version` (compare against the file at `origin/main`
in CI, or keep a `benchmarks/VERSIONS.lock` of `card → version → sha`).

**4. Retire the conversational tier honestly.** Move the four 2026-07 cards to
`benchmarks/prompts/conversational/` with a README line saying they are retained for
history and are not run: they require an operator and cannot produce comparable
scores. `harness_smoke.md` stays — it is the newborn gate, not a benchmark.

**5. PyAutoBrain.** Update the clone conductor's `VALIDATION_PLAN`
(`agents/conductors/clone/_clone.py`) so the newborn gate names the harness smoke *and*
the one-shot cards a sibling must carry, and the clone partition treats
`benchmarks/prompts/*/score.py` + `benchmarks/truth/` as **domain** (regenerated per
sibling, never copied blind). Second PR, same task.

## Out of scope

The cards themselves (filed separately). Cross-model campaigns — the first runs are
with one model (Claude Code, the current default model) to calibrate the scorer; the
comparison table comes after. Any LLM-as-judge column: allowed later as a secondary
column, never inside the score.

<!-- formalised by the Intake (Conception) Agent on 2026-09-17 from file:/tmp/claude-0/-home-user/cd566620-fbff-5429-9770-c1c4988273f5/scratchpad/raw_harness.md -->
