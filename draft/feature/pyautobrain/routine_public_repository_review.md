# Routine review of public repository entry points

Type: feature
Consequence: judge
Status: proposal; implementation and cadence need a plan

## Original request

This work was extremely valueable and I feel like should be a part of the PYAutoScience infrastructure, it should be more routine we do this. I'm not sure whre it falls. Maybe Broca? But yeah this should be something we run and check in on routinely especially as we move to more autonomous PyautoScientist development.   and then put PRs up for this work and prm

## Ownership recommendation

@PyAutoBrain owns the review through its existing docs conductor and WRITING_STYLE.md. Hygiene flags repository debris and drift. @PyAutoMind holds findings and approved repair tasks. @PyAutoHeart should own any eventual standing mechanical measurement. Broca remains responsible for assistant evaluation; it should consume relevant findings rather than own this cross-repository review.

## Proposed routine

Use repos.yaml to select public libraries, main example workspaces and HowTo tutorials. Review README.md and README.rst, the first runnable example, compact topic tables, AI/contribution/conduct/citation pointers, and top-level files. Check relative paths and anchors, citation destinations, policy consistency and unused URL exceptions. Inspect notebook contents before pruning exceptions. Require evidence of consumers before removing files; preserve useful legacy notes in Mind with recovery refs.

Keep mechanical results separate from editorial judgment. A passing link check does not establish a good newcomer experience. Draft substantial prose for human review; retain concise introductions and compact topic tables. Check changed entry points after structural changes; propose a periodic broader check-in as part of the existing maintenance process. Choose cadence and wiring during planning, not via a new chat timer.

## Acceptance criteria for a future implementation

- A discoverable, bounded command reuses docs/hygiene rather than introducing an organ.
- Coverage, skipped/unavailable repos and exact revisions are reported; unscanned is never clean.
- Markdown and reStructuredText are supported; links, redirects and generated files are handled honestly.
- Findings point to exact files and suggested owners, with no automatic deletions or subjective rewrite churn.
- A compact report supports human review and routes accepted repairs through ordinary dev/PR workflows.
- Representative fixtures test broken pointers, valid exceptions, missing coverage and harmless root files.

## Founding evidence

PyAutoScientist#90: 14 approved README rewrites plus shared policy/root cleanup. The final review checked 185 local Markdown links and root-script syntax. Twenty-three unused URL exceptions were removed while 62 referenced exceptions remained. This is an example of a useful review, not a frozen repo list or a universal style score.
