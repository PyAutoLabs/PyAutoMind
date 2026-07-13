# Hygiene agent — phase 3: perf mode

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 3 (final core phase) of the hygiene conductor (umbrella:
`issued/hygiene_agent.md`; P1 scaffold Brain#88, P2 modes Brain#90). Bring the
`perf` mode live — developer-loop cost: slow unit tests, slow integration-mode
workspace scripts, and import time — completing the conductor's five modes.
Keep the phase-2 shape: cheap read-only pre-scan + delegate; the conductor never
runs heavy audits and never mutates a repo.

**`perf` mode:**
- **import-cost pre-scan** (the cheap local signal): time `python3 -c "import
  <pkg>"` for each library in a **subprocess**, best-effort — this measures the
  import without the conductor itself importing anything (it stays bash/stdlib and
  never drags the JAX stack into the Brain, per the charter). Report per-library
  import seconds; mark a library `advisory` if it isn't importable in the ambient
  env (no venv resolved). Flag libraries over a threshold as the actionable
  signal (typed like phase-2 `debris`: a real, rankable number).
- **consult Heart for the heavy signals** — slow tests and slow scripts are
  already observed and tracked by PyAutoHeart's `script_timing` / `test_run`
  legs. `perf` reads/surfaces those (via the vitals faculty or `pyauto-heart`)
  rather than re-running pytest / workspace scripts itself, and routes the slow
  items. This is the "measurement lives in Heart; hygiene acts" split made real.
- **delegate the fix** — a slow function → `/refactor` (restructure) or `/bug`
  (regression-shaped); JAX-adaptation is a judgement call surfaced as a
  recommendation, never an automatic rewrite (no quick fix ⇒ flag, don't force).
- extend the `--json` HygieneDecision `perf` row from `staged` to real rows
  (per-library import timings + surfaced Heart timing findings + delegate).

**Wire-up:** flip `perf` from staged → live in
`agents/conductors/hygiene/{AGENTS.md,hygiene.sh}` and the `/hygiene` veneer
(nothing then remains staged); the default no-arg worklist now ranks `perf`
import signal alongside `tidy` debris.

**Deferred (explicit future, NOT this phase):** a *standing* PyAutoHeart
`import_time` leg (and any `cli_noise` leg) — adding Heart legs is a PyAutoHeart
change; keep phase 3 PyAutoBrain-only and note the leg as a follow-up if the
conductor's import pre-scan proves worth promoting to a tracked Heart signal.

**Done when:** `pyauto-brain hygiene perf` emits real import-cost timings +
surfaced Heart slow-test/script findings (human + `--json`), routing slow items
to refactor/bug; nothing in the conductor reports `staged`; the import timing
runs in a subprocess (conductor never imports JAX); PyAutoBrain tests green
(extend the hermetic contract test for the perf row shape).

<!-- phase 3 of 3, filed 2026-07-11 immediately after P2 merged (Brain#90). Final
     core phase; the standing Heart import_time leg is a deferred optional follow-up. -->
