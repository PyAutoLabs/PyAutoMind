## Summary

Shipped in PyAutoPulse#65 (merge f6967ccc, 2026-10-15). A `## Knowledge` section was added to
`tasks/interferometer_large_mask_aris.md`, and two decision records were published and indexed
in `decisions.yaml`: `decisions/adaptsplit-zero-weight-delaunay-only.md` and
`decisions/interferometer-route-gate-cost-model.md`. The `campaigns.yaml` next-lines were
refreshed and the board was re-rendered. Anchor issue PyAutoPulse#62 stays open as the
campaign anchor.

## Ship notes

- Heart RED override: granted by the live human in session 3e3dea38 on 2026-10-15 (late),
  "Yes, override (Recommended)".
- Both decision records were explicitly directed by the human: "Yes, record it as my decision".
- Consequence: notify, so no shadow row. PyAutoPulse is not in the published set, so there is
  no pending-release.

## Where to pick up

autolens_profiling #420 has merged (33779e46): re-pin the six-cell table at the next Pulse
check-in. The project-side pointer to these pages is queued by the #420 close-out as the Mind
draft `draft/docs/autolens_profiling/decision_matrix_note_gate_wording.md`.

## Original prompt

# Interferometer large-mask profiling: write the knowledge section and record two human decisions in PyAutoPulse

Type: docs
Target: PyAutoPulse
Repos:
- PyAutoPulse
Difficulty: small
Autonomy: safe
Consequence: notify
Status: formalised
Issued: 2026-10-15
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/62

Write the 2026-10-15 interferometer CPU profiling work (Aris 125×125 and 512×512, PyAutoArray #630/#631/#632,
autolens_profiling PR #420 phase-2 record at PR-open, the CPU speed-up research of PyAutoPulse#62
issuecomment-6203354375) into PyAutoPulse per its own standard:

- `tasks/interferometer_large_mask_aris.md`: a `## Knowledge (2026-10-15)` section for whoever plans the next
  interferometer CPU campaign (cost structure, memory fix, log-det root cause and jitter residual, routing cost
  model, phase-2 six-cell table with its limits, ranked levers L1/L2/preload and the not-worth-it list, collaborator
  runtime settings); refresh header and Results next-line.
- `decisions/adaptsplit-zero-weight-delaunay-only.md` and `decisions/interferometer-route-gate-cost-model.md`
  (human decisions 2026-10-15; the human explicitly directed both records: "Yes, record it as my decision"),
  indexed in `decisions.yaml`.
- `campaigns.yaml` task and campaign `next:` lines; re-render the board; `check --offline` OK; tests pass.

Ledger-only change: no library, compute, default or release change. Stops at PR-open; merge is human `/prm`.
Branch `feature/pulse-interferometer-knowledge`. Heart RED development override (live human, session 3e3dea38,
AskUserQuestion "Yes, override (Recommended)", 2026-10-15 late).
