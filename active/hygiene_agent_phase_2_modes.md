# Hygiene agent — phase 2: modes (absorb + consult)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 2 of the hygiene conductor (umbrella: `issued/hygiene_agent.md`; decision:
`research/pyautobrain/hygiene_agent_decision.md`; phase 1 scaffold shipped as
PyAutoBrain#88). Give the four non-perf modes real behaviour by wiring them to
the hygiene skills that already exist, and make the default no-arg run a single
prioritized worklist across them. (`perf` stays staged for phase 3.)

**Modes to implement:**
- `tidy` — drive `repo_cleanup`'s audit and emit its findings as HygieneDecision
  rows (stale branches / stashes / `[gone]` refs / dirty checkouts).
- `noise` — drive `cli_noise_clean`'s audit (warnings / stray prints / library
  chatter surfaced by tests + workspace scripts).
- `deps` — consult `dep_audit` (version-cap drift vs PyPI, risk-tiered).
- `docs` — consult `audit_docs` (stale `docs/api/*.rst` module paths).
- default (no-arg) — run the above audits and emit ONE prioritized
  `HygieneDecision` worklist (most-useful-next-action first), each row tagged
  with the mode and the delegate it routes to.

**Design fork — settle first (the plan's key decision).** The hygiene conductor's
charter is *reason and delegate; never edit source, never mutate other repos*
(it stays stdlib/bash, no JAX). So "absorb" must NOT mean moving destructive
logic into the conductor. Recommended resolution: **each mode owns the AUDIT +
prioritization and points at the existing skill for EXECUTION** — the skills stay
the executors (repo_cleanup keeps its interactive per-bucket git mechanics and
safety gates; cli_noise_clean/dep_audit/audit_docs keep their fix/report steps).
The conductor reads/parses their audit output (or re-implements only the
read-only audit portion where that is cleaner than shelling out) and unifies +
ranks. Confirm this boundary before coding; if the alternative (fold logic into
the conductor) is chosen, it must not put mutations in the Brain. Under
`--auto` supervised, if this fork is still open at implementation it becomes a
batched issue question (checkpoint-and-continue).

**Machine footing:** extend the `--json` HygieneDecision so each mode emits real
finding rows (not just `staged`), and the default run emits the ranked worklist —
the shape a Brain session and the future perf mode can consume.

**Update as modes land:** flip each mode's `LANDS`/staged notice in
`agents/conductors/hygiene/{AGENTS.md,hygiene.sh}` from "phase 2" to implemented;
update `skills/repo_cleanup/SKILL.md` (the `tidy` mode now exists) and the
`/hygiene` veneer's staged note.

**Out of scope:** `perf` mode and any PyAutoHeart legs (phase 3).

**Done when:** `pyauto-brain hygiene {tidy,noise,deps,docs}` each emit real audit
findings (human + `--json`); the no-arg run emits one prioritized worklist;
delegation targets are named; the four skills remain the executors; PyAutoBrain
tests green.

<!-- phase 2 of 3, filed 2026-07-11 immediately after P1 merged (Brain#88); phase 3
     (perf + Heart legs) filed as this nears shipping, per no-bulk-issue-queues. -->
