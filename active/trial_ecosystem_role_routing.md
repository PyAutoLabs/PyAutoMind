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
Status: issued
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/444

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

## Result — awaiting merge

PR: https://github.com/PyAutoLabs/PyAutoBrain/pull/445
Commit: 6ea15719854f19a3c9a8f2d0c828fbfdfbc8e3cc

Both conditions name all six change targets correctly. Checklist decision-owner
fields conflate repair repository and conductor in three cases, but action routes
remain appropriate. Retain current guidance; do not mandate an extra checklist.
Scores 36/36 versus 33/36 depend on disclosed grading-time context leniency;
contract coverage can favour the checklist under a stricter reading. No measured
retrieval or efficiency claim. Full frozen inputs, exact answers and assessment
are versioned with the report. No runtime/schema/organ change.

Independent Claude Fable review: FINDINGS (context grading transparency and extra
output-field disclosure), corrected; focused re-review CLEAN. Reviewed file hashes
match committed bytes. Sphinx passes with zero warnings; input/response integrity,
JSON, score totals, local download paths and pinned source excerpts verified.
Heart GREEN score 100, 2026-10-01T19:53:08.542623+00:00. Earlier transient manifest
YELLOW cleared after canonical vitals refresh; no override was used.
