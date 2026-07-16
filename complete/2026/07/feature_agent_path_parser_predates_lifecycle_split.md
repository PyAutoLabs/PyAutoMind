# Feature Agent path parser predates the Mind lifecycle split — misroutes every draft/ prompt

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

`bin/pyauto-brain feature draft/release/pyautoheart/<x>.md` parsed
work-type=`draft`, target=`release`, resolved no repos, and recommended
"re-home as a research task" (observed 2026-07-15, recorded as finding 4 of
`draft/research/pyautoheart/readiness_evidence_chain_audit.md`). The Feature
Agent's path parser predates the Mind lifecycle split to
`draft/ → active/ → complete/` (PyAutoMind#71, closed 2026-07-13), so it reads
the lifecycle folder as the work-type and will misroute **every prompt filed
since the split**. It was overridden by hand on the day.

Sibling of `draft/bug/pyautobrain/intake_writes_legacy_layout.md` (the Intake
Agent's *writer* has the same pre-#71 layout assumption; this prompt is the
*reader* side in the Feature Agent). Fix in @PyAutoBrain: teach the parser to
strip a leading lifecycle folder (`draft/`, `active/`) before reading
`<work-type>/<target>/`, keep legacy flat paths resolving, and add a
regression test with a `draft/...` path. While there, sweep the other
conductors for the same path assumption — this is the second Brain-agent
misroute in two days (`autonomy_log.md` records an arXiv-digest one), so
assume the parser is shared or copied.

<!-- filed 2026-07-16 while decomposing the build-chain umbrella; source: readiness_evidence_chain_audit.md finding 4 (OPEN, unfiled) -->
