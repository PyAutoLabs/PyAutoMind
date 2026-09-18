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
