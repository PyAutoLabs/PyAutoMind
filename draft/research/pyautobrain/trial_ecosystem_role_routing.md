# Trial ecosystem role routing against current guidance

Type: research
Target: @PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Consequence: judge
Filed: 2026-10-01
Status: draft

## Original user request (verbatim)

ok do it

## Accepted recommendation and context

In response to the completed layer-design research and terminology adoption,
the assistant recommended: "Trial the agent-routing convention. Use visualization,
profiling and inference examples to check whether agents correctly distinguish
the evidence producer, decision owner and repository needing a change. This is
the next step I recommend." The user authorized that next step above.

Research #440 / PR #441 proposed the convention; adoption #442 / PR #443
established responsibility terminology but did not change routing machinery.

## Plan

Run a bounded exploratory comparison of six hypothetical routing cases (two per
domain), using fresh isolated evaluation contexts and identical case/evidence
packets. Baseline is current guidance after terminology adoption; treatment adds
the proposed evidence/producer/decision/change-owner checklist. Use the same
available model and effort for both; record resolved model and settings. Do not
present model identity or a hypothesis as a preferred answer to evaluators.

Before evaluation, fix the protocol, cases, expected decisions and scoring.
Include project versus organ visualization defects, environment versus library
profiling drift, and scientific inference follow-up versus a code defect. Missing
information must permit a conditional route, not an invented owner or verdict.
Do not run scientific jobs or use the trial to change scientific conclusions.

Score evidence attribution, decision owner, change owner, existing action door,
approval/record boundary and proposed minimal context. Distinguish predicted
context choices from observed tool reads; do not claim token/cost savings from
answer length. Report per-case paired outcomes, not statistical significance.
Retain no-change as a valid outcome; recommend a larger/real-world trial only if
justified by the results. Do not alter runtime routing, role schemas or organs.

## Deliverables

- `docs/research/ecosystem_routing_trial.md`: protocol, outcomes, counterexamples,
  limits, and recommendation on whether to adopt the checklist, revise it, or
  retain current guidance.
- `research/ecosystem_routing_trial/`: bounded versioned protocol/cases, evaluator
  responses and assessment, with enough source/model/hash provenance to inspect
  the comparison. No new evaluation framework or reusable harness.
- Independent review of conclusions against raw evidence; Sphinx/link/JSON checks.

All outputs stay in Brain. Other repositories are read-only evidence, with no
new claims. The separately filed inference documentation and profiling-board
registration tasks are not silently folded in. Candidate follow-up work is
proposed before being appended to Mind ideas, per the research skill.
