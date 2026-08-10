# Profiling Agent phase 3 — `triage --axis compile`: classify compile drift, route the real ones

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

> Depends on phase 2, `draft/feature/profiling/compile_warm_baseline_dashboard.md`
> (its pins). Not declared as `Blocked-by:` yet because that key grades **issue**
> refs and phase 2 has no issue — add the real ref at `/start_dev` time.

Phase 3, and the point of the arc: phases 1–2 make compile drift *visible*; this
makes it *actionable*. Read `profiling_agent_jax_compile_time_scope.md` first.

## Scope

Extend `triage` with `--axis compile`, classifying each drifted pin from phase 2
into one of four outcomes — the same shape as the runtime triage's per-finding
classification.

| classification | signal | action |
|---|---|---|
| **cache regression** | a `warm` row's compile reverts toward its `cold` scale on an unchanged key | **the alarm this arc exists for** — the persistent cache is not being hit; route to config/stack, not to the library |
| **autotune regression** | GPU compile jumps ~an order of magnitude on the pathological shapes | `--xla_gpu_autotune_level=0` is not reaching XLA — the exact PyAutoNerves#127 `XLA_FLAGS`-clobbering failure, which went undetected for two months |
| **expected recompile** | `jax_version` moved | **not drift** — cache keys include jax version, so one recompile is by design. Re-pin, do not report |
| **stale pin** | measurement conditions changed (host, core count, `mixed_precision`) | re-pin here |
| **library regression** | compile grows on an unchanged key with no config explanation | route to `bug/` via intake — *classify and route only* |

## The two constraints inherited from the agent's existing contract

- **Profiling records and flags; it never adjudicates library correctness.** A
  suspected library regression is routed to `bug/` via intake; the debug is never
  planned inside the profiling repo. This is the existing `triage` boundary and it
  applies unchanged.
- **Never compare across the comparability key.** `(hardware, jax_version,
  mixed_precision, cache_state)`. Compile timings are host-load-sensitive — the
  7×-wrong measurements (851 s vs 117 s, same compile) are the standing reminder.

## Close the arc

- Move "JAX compilation-time profiling of likelihood functions" from **Future
  modes** to the **Modes** table in `agents/conductors/profiling/AGENTS.md`.
- Record in **Boundaries** that release-validation script cost stayed with the
  hygiene conductor's `perf` mode, so the question does not get re-opened a third
  time.

## Acceptance

- `pyauto-brain profiling triage --axis compile` classifies every phase-2 drift row
  into exactly one of the five outcomes, with the evidence that drove it.
- A synthetic warm-reverting-to-cold row classifies as **cache regression**.
- A drift explained solely by a `jax_version` bump classifies as **expected
  recompile** and is not reported as a regression.
- Nothing is written to `autolens_profiling`; library findings are emitted as
  intake-routable `bug/` candidates only.
- `AGENTS.md` Modes/Boundaries updated as above.

<!-- filed 2026-08-10 as phase 3 of the compile-axis arc. -->
