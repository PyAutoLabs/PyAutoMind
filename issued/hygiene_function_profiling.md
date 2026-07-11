# PyAutoBrain — hygiene perf function profiling (phase 4c)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Phase 4c of the hygiene `perf` mode — the third and hardest uncovered capability
from the original hygiene prompt: **profile a normal-mode script run and surface
the slowest NON-likelihood functions** as optimization / JAX-adaptation
candidates. Unlike 4a/4b (tracked regression signals → Heart legs), this is a
**one-shot investigation**, so it belongs in the hygiene conductor as an
on-demand `perf` sub-action that emits a `HygieneDecision`, **not** a Heart leg.

**Research grounding (2026-07-11):** no function-profiling framework exists (only
two incidental `cProfile` uses inside PyAutoFit internals — `_erf_helpers.py`,
`sneaky.py`). `autolens_profiling` is **likelihood-only** (JAX likelihood sweeps
— the profiling agent's domain), so non-likelihood function profiling is
genuinely unbuilt.

**The crux — the likelihood/non-likelihood boundary (settle first).** `/profiling`
owns the likelihood/modeling compute (the `log_likelihood_function` / fitness on
the science grid, GPU tiers, A100). This capability owns **everything else** the
dev loop spends time in — simulation, data prep, model composition, plotting /
visualization, the aggregator, config/serialization. The profiler MUST **exclude
likelihood frames** so it never overlaps `/profiling`: define the exclusion by
module/qualname (e.g. drop frames under the likelihood/fitness call tree and the
JAX-traced regions), and hand any likelihood-dominated result straight to
`/profiling` instead of reporting it here. Getting this filter right is the
main design risk — prototype it against a real script before finalising.

**Build (in `agents/conductors/hygiene/`):**
- `perf` gains an on-demand profiling action (e.g. `hygiene perf --profile
  <script>` or a `profile` sub-mode): run the target script **in normal mode**
  (real workload, not TEST_MODE) under `cProfile` in a **subprocess** (the
  conductor stays stdlib/bash and never imports the science stack itself),
  collect the `pstats`, rank the top-N by cumulative/total time **after
  excluding likelihood frames**, and emit a `HygieneDecision` listing the
  candidates with their cost + call counts.
- Each candidate routes to `/refactor` (restructure / vectorize) or, where a
  clear win exists, is flagged as a **JAX-adaptation candidate** — a
  *recommendation*, never an automatic rewrite (the original prompt's "judgement
  may be needed if no quick fix"). No quick fix ⇒ flag, don't force.
- `--json` footing consistent with the other `perf` rows (kind `timing` /
  a new `profile` kind), so a Brain session can consume the candidate list.

**Scope / cost:** profiling a normal-mode run is heavy and per-target — strictly
on-demand (the human points it at a script), never in the default fast scan and
never a Heart tick. Keep the profiler subprocess timeout-guarded.

**Deferred:** a *standing* tracked signal for function hotspots (a Heart leg) is
out of scope — hotspot lists are investigation output, not a regression gate;
promote later only if a recurring need appears (the same demonstrated-need bar
`import_time` cleared).

**Done when:** `hygiene perf` can profile a named normal-mode script, exclude
likelihood frames, and emit a ranked non-likelihood hotspot `HygieneDecision`
routing candidates to `/refactor` (JAX-adaptation flagged as judgement),
human + `--json`; PyAutoBrain tests cover the exclusion filter + candidate
ranking on a fixture pstats. Siblings: [[hygiene_unit_test_timing]] (4a),
[[hygiene_workspace_testmode_timing]] (4b).

<!-- filed 2026-07-11 from the hygiene perf-scope reopening; phase 4c of 3. The
     judgement-heavy one — the likelihood/non-likelihood filter is the crux and
     the profiling-agent boundary. large + supervised for that reason. -->
