# The Brain autonomy contract — make the Autonomy header load-bearing

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: human-required
Priority: high
Status: draft

## Why

The Mind prompt header already blesses `Autonomy: safe | supervised |
human-required` (@PyAutoMind/README.md "Prompt file format"), and the Intake
Agent persists it via the sizing faculty — but **nothing consumes it**. Every
workflow run stops at the same human checkpoints regardless of the value. This
prompt makes the field load-bearing: it is the doctrine every later task in
`feature/autonomy/` keys off.

## What

Write `@PyAutoBrain/AUTONOMY.md` — one canonical page, linked from
`WORKFLOW.md` and the Mind README (no duplicated prose), that:

1. **Enumerates every human checkpoint** in the dev workflow today: Plan-Mode
   approval in `start_dev`, ship PR sign-off (`## API Changes` / `## Scripts
   Changed`), Heart YELLOW acknowledgement, the merge/close prompt, the
   `pre_build` minor-version ask, post-merge cleanup confirmation.
2. **Defines behaviour per level at each checkpoint**:
   - `safe` → proceed and log (plan written to the issue, not held).
   - `supervised` → proceed, but batch questions to the issue
     (checkpoint-and-continue, see `5_checkpoint_and_continue.md`).
   - `human-required` → today's behaviour, unchanged.
3. **Per-work-type autonomy caps** — a prompt's header can never exceed the
   cap: `refactor`/`test`/`maintenance` may run `safe`; `feature`/`bug` are
   capped at `supervised` until the calibration log (below) justifies raising;
   `release` is always `human-required`.
4. **Activation rule** — autonomy levels only take effect when the human
   launches with an explicit `--auto` (or equivalent). Default runs behave
   exactly as today. Autonomy is opt-in per invocation, never ambient.
5. **Calibration log** — a small append-only record (in Mind, e.g.
   `autonomy_log.md`): for each autonomous run, was the PR merged unchanged,
   amended, or rejected? This is the evidence for later raising/lowering caps.
6. **Model doctrine refresh** — update `WORKFLOW.md`'s "Opus plans, Sonnet
   executes" split to the Fable era: Fable (or the strongest available model)
   for orchestration/judgment and tutorial prose; the split must be stated
   model-agnostically (strongest-available / mid / fast tiers) so nothing
   breaks if Fable access lapses.

## Boundaries (adversarial findings, keep these)

- The contract is **doctrine only** — no skill behaviour changes in this task;
  `4_auto_dev_mode.md` implements consumption. One PR, prose + pointers.
- Sizing (a model) assigns Autonomy; skipping approval purely on the model's
  own estimate is circular. The caps + explicit `--auto` + calibration log are
  the mitigations — they are not optional extras.
- Merging a PR stays a human act at every level (standing preference).

Blocked-by: nothing. Everything else in `feature/autonomy/` is blocked by this.
