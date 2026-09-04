# Cortex by project: the "where is everything, which folders" summary and the two missing starting prompts

Type: feature
Target: pyautocortex
Repos:
- PyAutoBrain
- PyAutoCortex
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: high
Status: draft
Consequence: judge
Witness: the regenerated Cortex `dashboard.md` has a `## By project` section (one block per `status: active` project, then a folded one-liner for dormant projects) that renders each project's `local_path` / `mirror` / `ral_root`, each non-dropped phase with State + health, the phase's `## Where to look` bullets verbatim, and per phase the copy-ready prompt for its state, including two NEW ones: "accept → file and start the next phase" (wraps `cortex.py rule <phase> accept --body …` then `cortex.py new <project> <slug> --phase N+1` with the title-prefix rule from memory) and "rerun this phase" (`rule … rerun --body …`, `move ready`, `move submitted --run`); `pyauto-brain cortex checkin` prints the same by-project summary and prompts; `pyauto-brain cortex census --by-project` exists; dashboard `--check` current; Brain + Cortex tests cover the section, both new payloads and a phase with no `## Where to look`
Review-minutes: 20
Unattended: ready
Epic: cortex-checkin
Phase: 3
Filed: 2026-09-03
Issued: 2026-09-03

Phase 3 of `cortex-checkin`. Branch from phase 2's branches if unmerged. Two
PRs (Brain renderer + census + checkin summary; Cortex docs/REFERENCE for the
new section and the two prompts, plus any `check` rule that `## Where to look`
now needs, e.g. "every non-planned phase has at least one bullet").

## By-project summary

Today every dashboard section and `census` are keyed by phase STATE
(`SECTIONS` in `_cortex.py` ~L231-253), the Projects table omits
`local_path`/`mirror`/`ral_root`, and `## Where to look` is parsed
(`where_paths` ~L1231) only to locate artefacts, never rendered. Add:

- `## By project` in the dashboard (above the state sections or directly
  below the header — pick the one that reads first on a phone and say why):
  per active project, a header with the three paths, then its phases in
  state order (awaiting-ruling, running, submitted, ready, gated, planned;
  accepted/dropped folded into a count), each with health from the last
  scoring, its `## Where to look` bullets verbatim, and its prompt.
- `census --by-project` printing the same tree as text; `checkin` uses it for
  its closing summary (replace phase 2's minimal version).

## The two missing prompts

Dashboard rows already carry `_ruling_payload` (rule this),
`launch_payload` (submit + move), `_live_payload` (check jobs). Add:

- **`_next_phase_payload`** for an `awaiting-ruling` (or freshly `accepted`)
  phase: "the results are good — file the ruling and open phase N+1": the
  `rule … accept --body <file>` line with a body stub, then
  `cortex.py new <project> <next-slug> --phase <N+1>` (honour the title-prefix
  and rerun-flow conventions in memory `reference_cortex_new_title_prefix_and_rerun_flow`),
  then the launch prompt for the new phase. Where the epic ledger names the
  next phase's title, prefill it.
- **`_rerun_payload`** for `awaiting-ruling` / `pulled` / `running`: "rerun
  this": `rule … rerun --body <file>`, `move ready`, `move submitted --run`,
  with the phase's own submit command from `launch_payload`.

Both render as chips beside the existing rule prompt and appear in the
by-project summary and in `checkin`'s output. Keep the payload text short:
these are things a human pastes into a fresh chat, not scripts.
