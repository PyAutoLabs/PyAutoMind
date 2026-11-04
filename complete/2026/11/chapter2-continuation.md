## Chapter 2 continuation
- completed: 2026-11-04
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/124
- summary: All continuation scope merged: Tutorials 5 and 6, optional speed and runnable model_centred prior passing, summary, final numbering and navigation.
- canonical-record: complete/2026/11/howtolens-ch2-explanations.md

## Original prompt

# HowToLens Chapter 2 — remaining review and restructure

Completed checkpoint: complete/2026/11/howtolens-chapter2.md; PR https://github.com/PyAutoLabs/HowToLens/pull/115 merged approved lessons 1–4 on 2026-11-01. Do not repeat their review. Galaxy Chapter 2 already merged in PR #96; both Chapter 3 checkpoints merged.

Tutorial 5 Data and Likelihoods is now reviewed, implemented and validated locally in feature/howtolens-ch2-explanations at 327080e. See active/chapter2-explanations.md for the canonical checkpoint and worktree. Tutorial 6 Search Chaining is also approved, implemented and validated locally at 359af1f on the same branch. Continue the five-coherent-block review with optional speed/historical prior passing and the summary, then final consecutive numbering/navigation. Plan approval is not approval of unreviewed Lens prose.

Approved structure intent: data/masks/positions/contaminant noise scaling, concise interferometer/point/weak data reminders, prose-only multi-dataset signpost; component-based Prodigy-to-Nautilus chaining, fixing fitted lens-light geometry with .instance while solving intensities and acknowledging conditional uncertainty, auto positions and a SLaM signpost. Validate current APIs; no full convergence claims from smoke.

Later scope includes optional speed/historical prior passing, summary and final consecutive renumbering/navigation. Current later Lens lessons retain their old numbering 6–11 and content with reference corrections. The first four lessons and optional Prodigy introduction are implemented, validated and merged; do not describe them as drafts awaiting application.

Original detailed design checkpoint: C:\Users\Jammy\Workspace\Science\scratch\howto_chapter2_review_2026-10-31\RESUME.txt (its old implementation status is superseded by PR #115).
Updated checkpoint: /mnt/c/Users/Jammy/Documents/Codex/2026-11-01/can-x20/outputs/chapter2-checkpoint.txt
Original review chat: 01a1921a-9586-7c13-837d-8a7b2e1a3f37. Current ship chat: 01a197a6-fbee-7b52-94d9-c5f72b126a44.

## Final checkpoint — 2026-11-02
Chapter 2 content, historical consistency and final navigation are complete locally at 8362371 on feature/howtolens-ch2-explanations. See active/chapter2-explanations.md for the canonical completion record, validation and review bundle. Main lessons are now 1–6 plus tutorial_7_summary.py; speed and historical prior passing are optional. All 10 scoped smoke scripts passed; generation 43 passed. No remaining prose review requested. No HowToLens push, PR or merge performed.

## Prior passing correction — 2026-11-04
User requested restoring the runnable model-centred example. HowToLens local commit 1ad71f3 supersedes the non-executing historical lesson in 8362371. scripts/chapter_optional/tutorial_prior_passing.py now runs two Nautilus fits using result_1.model_centred for lens, source and shear prior transfer. Retains optional/historical-workflow framing; current API remains supported. Correct prose: posterior medians (max-likelihood fallback), truncated Gaussian priors, configured width modifiers rather than posterior error bars, absolute/relative alternatives. Uses its own chapter_optional output names and circular radius 3.0. README descriptions and generated notebook/catalogue updated.
Validation: scoped official smoke passed 30.4s; generation 43 passed; navigation, whitespace, syntax and executable notebook structure passed. Controlled actual Result/SamplesSummary check with deliberately distinct median/max-likelihood samples verified 11 centred priors, positive widths, fixed/shared parameters, actual second-model transfers and explicit absolute width; model counts 11 -> 17. Test mode smoke and constructed result validation do not establish search convergence. Logs .task-logs/{smoke-prior-restored,generate-prior-restored-report,check-centred-prior.log}. Final scratch bundle updated in place. No HowToLens push/PR/merge.

## PR opened — 2026-11-04
Pushed feature/howtolens-ch2-explanations at 1ad71f3f9cd57d281f3680458a40b6d11d035822; PR https://github.com/PyAutoLabs/HowToLens/pull/124 is open and attached to the Codex chat. Full canonical Heart-managed HowToLens smoke passed 42 scripts before shipping. User explicitly acknowledged current Heart YELLOW warnings; exact warnings and authorisation recorded in PR body, issue comment and active.md. Awaiting human review/merge; no merge or recurring monitor armed.
