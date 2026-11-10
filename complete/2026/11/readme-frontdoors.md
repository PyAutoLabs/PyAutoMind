# Public README and repository-root cleanup

Completed: 2026-11-10
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/90

## Shipped

All 17 PRs merged; every feature branch verified as an ancestor of origin/main. Human-approved newcomer README wording and compact topic tables, shared policy/citation pointers, open Slack guidance, welcome-path corrections, legacy root-file retirement and unused URL exceptions. Useful CTI notes and recovery refs preserved in draft/maintenance/autocti/legacy_root_notes_followup.md.

## Validation and explicit exceptions

185 relative Markdown links resolve; root welcome/start Python syntax and diff whitespace pass. Exact-head CI inspected. Intentional smoke/no-JAX exclusions explicitly accepted by the human. Shared .github no-checks merge explicitly accepted. Fit, Array, CTI and Reduce applicable Python jobs passed.

Lens and Galaxy numerical failures predate this change: current main and PR no-JAX runs share the same 16 and 11 failing tests, respectively. One requested retry reproduced them. Human explicitly authorized the final merge exception: "$prm can we over rule the criteria and then ill try fix the failures". Normal GitHub merges; no protection override, release or claim of green numerical tests. The human will address the numerical failures separately.

## Follow-up

The routine-review proposal remains draft/feature/pyautobrain/routine_public_repository_review.md. Brain docs is the recommended editorial owner, hygiene flags debris, Mind tracks repairs, Heart owns standing mechanical checks. No scheduler or review implementation was installed. The unrelated feature_introductions_and_images.md draft and all concurrent science work were preserved.

## PRs

- https://github.com/PyAutoLabs/PyAutoLens/pull/821
- https://github.com/PyAutoLabs/PyAutoGalaxy/pull/697
- https://github.com/PyAutoLabs/PyAutoFit/pull/1766
- https://github.com/PyAutoLabs/PyAutoArray/pull/686
- https://github.com/PyAutoLabs/PyAutoCTI/pull/127
- https://github.com/PyAutoLabs/PyAutoReduce/pull/83
- https://github.com/PyAutoLabs/autolens_workspace/pull/625
- https://github.com/PyAutoLabs/autogalaxy_workspace/pull/272
- https://github.com/PyAutoLabs/autofit_workspace/pull/183
- https://github.com/PyAutoLabs/autocti_workspace/pull/48
- https://github.com/PyAutoLabs/autoreduce_workspace/pull/7
- https://github.com/PyAutoLabs/HowToLens/pull/133
- https://github.com/PyAutoLabs/HowToGalaxy/pull/106
- https://github.com/PyAutoLabs/HowToFit/pull/78
- https://github.com/PyAutoLabs/PyAutoScientist/pull/91
- https://github.com/PyAutoLabs/.github/pull/44
- https://github.com/PyAutoLabs/PyAutoMind/pull/552

## Original prompt

# Public README and root cleanup

Type: docs
Consequence: judge
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/90
Issued: 2026-11-10

Ship the human-approved README, policy, citation, welcome-pointer and legacy-root cleanup across the 17 repositories listed in active.md. Preserve unrelated edits. Current /prm authorization is this-turn only.

## Original request

This work was extremely valueable and I feel like should be a part of the PYAutoScience infrastructure, it should be more routine we do this. I'm not sure whre it falls. Maybe Broca? But yeah this should be something we run and check in on routinely especially as we move to more autonomous PyautoScientist development.   and then put PRs up for this work and prm
