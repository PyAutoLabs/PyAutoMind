# Repository guidance and assistant cleanup

Type: docs
Consequence: judge
Status: draft

## User request (verbatim)

Can you put together a plan to fix the stale guidance and broken links, clean up the CTI PENDING.md and remove the archived autolens docs, keeping llms.txt and the other files that are still used?

## Scope

Planning only until the human approves implementation. Primary repositories:
@autolens_assistant and @autocti_assistant. Cross-repository guidance updates
follow the verified stale CLAUDE.md references; shared sources are @PyAutoMind
and @PyAutoBrain only if the audit finds generation ownership there.

Retain llms.txt, llms-full.txt, workspace_index.json, skill symlinks and generated
adapters, AI_OPTIONS.md redirect stubs, active setup docs and scientific artifacts.
Align chat guidance with the existing shared AI-options distinction: discussion
and planning in chat; execution/data inspection/fitting in a coding agent.
Remove the nine tracked autolens docs/archive files and repair inbound references.
Repair the 13 CTI broken-link occurrences using existing CTI material where
possible; replace inherited lensing/Euclid PENDING items with a grounded CTI backlog.
No runtime/config deletion or scientific API changes.

## Review evidence

Human-readable review:
/mnt/c/Users/Jammy/Workspace/Science/scratch/repository_relevance_review_2026-11-12/review.html
Exact local revisions: inventory.json in the same folder.

## Coordination

Check live claims before worktree setup. At planning time PyAutoFit,
PyAutoGalaxy and PyAutoLens are claimed by three-autos-public-framing;
autolens_workspace_developer by pyautolens-ii-case-studies; PyAutoMind and
PyAutoBrain by prompt-sync-explicit-paths. euclid_assistant has local user
changes. Do not edit those working trees or assume plan approval overrides claims.

Split implementation into coherent tracked tasks/PRs: Autolens onboarding and
archive removal; CTI routing/backlog cleanup; cross-repository retired-pointer
prose. Create issues/register implementation only after plan review.
Tier: judge — merge mode: human /prm.

## Proposed implementation plan

1. Autolens onboarding and archive removal (one task/PR).
   - Edit README.md, llms.txt and docs/setup/troubleshooting.md to use the
     shared AI_OPTIONS policy: chat for reading/discussion/planning, coding
     agents for execution and fits. Retired custom GPT/pasted-bundle products
     remain retired; do not restore their infrastructure.
   - Remove the nine tracked documents under docs/archive/: README.md,
     CHOOSING_YOUR_AI_TOOL.md, README_ai_chat_assistant_section.md,
     README_choosing_your_ai_tool_section.md, and chat/{chatgpt_custom_gpt,
     chatgpt_paid_connector,claude_chat_free,claude_chat_paid,paste_bundle}.md.
   - Repair archive references in llms.txt, docs/setup/troubleshooting.md and
     modes/maintainer.md; search tracked content, including hidden adapters,
     notebooks and other repos, for additional inbound links before deletion.
   - Correct the retired CLAUDE.md import claims in AGENTS.md and llms.txt.
     Keep historical retirement context only where useful; git retains originals.

2. CTI routing and growth queue (one task/PR).
   - Edit AGENTS.md, skills/_style.md and skills/ac_setup_environment.md to
     resolve the 13 observed broken-link occurrences.
   - Use ac_mask_and_extract.md and ac_fit_cti_model.md for the relevant data
     preparation/fitting routes, ac_plot.md for existing plotting guidance,
     ac_setup_environment.md for setup and ac_workspace_navigation.md for
     example discovery, after checking each destination actually covers the claim.
   - Remove inherited operation/wiki promises with no CTI implementation;
     retain safety requirements inline where no suitable destination exists.
     Do not create placeholder pages just to make link checks green.
   - Rewrite PENDING.md as a short CTI-specific queue: retain verified unmet
     CTI needs, reconcile entries against skills/README.md and existing files,
     drop lensing/Euclid/SLaM inheritance and duplicated adapter-level tasks.
     Preserve useful unfinished configuration-review intent as one scoped item;
     do not delete or change runtime YAML. Update README.md's queue description.

3. Retired-pointer guidance sweep (coordinated per-repository docs PRs).
   - Update stale root AGENTS.md wording in PyAutoNerves, PyAutoFit,
     PyAutoArray, PyAutoGalaxy, PyAutoLens, PyAutoCTI, autoreduce_workspace,
     autofit_workspace_developer, autolens_workspace_developer,
     euclid_assistant, euclid_strong_lens_modeling_pipeline,
     PyAutoScientist and pyautolabs.github.io; include root PyAutoLabs AGENTS.md
     if the on-disk workspace copy still contains the same obsolete claim.
   - Repair euclid_assistant/README.md's dead CLAUDE.md link and
     autolens_profiling/README.md's developer-instruction link.
   - Describe AGENTS.md as canonical; do not recreate CLAUDE.md or change hooks.
   - Verify generation ownership before editing. If a source template generates
     affected text, change the owner and regenerate only the intended surfaces.
     Leave explanatory history and retirement implementation references intact.
   - Queue claimed repos; handle euclid_assistant from a clean task worktree,
     preserving all existing local edits. Recheck claims before each task.

## Validation and acceptance

- Verify all changed Markdown destinations and fragments, including local
  equivalents of GitHub/raw URLs; no active reference points to removed archives.
- Confirm all nine archive documents are removed and no other deletion occurs.
- Re-run the scoped CTI link scan: all 13 occurrences resolved without losing
  real-data inspection, API-verification or environment safety instructions.
- Check remaining PENDING items are relevant, unimplemented and represented once.
- Verify discovery symlinks resolve; use the owning generator's check mode if
  generated surfaces change. Avoid broad regeneration of unrelated files.
- Re-run PyAutoHands navigator checks for the five workspaces and three HowTo
  repos; run applicable existing documentation/discovery checks in affected repos.
- Inspect diffs for accidental runtime/config/data changes and stale import claims.
  No full scientific fitting suite is needed for prose-only changes.
- Refresh Heart at shipping and apply the normal PR checks. Human review/merge.

## Routing and execution notes

Brain feature routing succeeded on the draft and recommends splitting work.
Its heuristic 'core API' and 'workspace examples' phases are inapplicable:
this scope changes documentation only. Use the three coherent groups above.
No new scientific or architectural design requires extra science context.

Suggested branches: feature/autolens-guidance-cleanup,
feature/cti-guidance-cleanup, feature/retired-pointer-guidance.
After approval, create isolated worktrees through the owning start workflow,
using a workspace-local root (the current workspace path rule applies).
Open separate tracked tasks and per-repository PRs; no implementation issue,
claim, worktree, commit or push is created by this planning turn.

Tier: judge — merge mode: human /prm.
