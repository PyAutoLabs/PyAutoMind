# Align ecosystem documentation with the current HowToLens and HowToGalaxy courses

Type: docs
Difficulty: large
Autonomy: supervised
Consequence: judge
Issued: 2026-11-04
Issue: https://github.com/PyAutoLabs/HowToLens/issues/127
Target: @PyAutoLens @PyAutoGalaxy @autolens_assistant @autogalaxy_assistant @HowToLens @HowToGalaxy @autolens_workspace @autogalaxy_workspace

## Original request
can we now do a sweep of all docs and make sure the way they link to HowToLens and HowToGalaxy reflects these updates, really check this for the whole ecosystem.

## Approved audit and plan
Audited current default-branch tracked references across all 51 registered repositories plus the organization profile (52 checkouts). Refreshed refs, using HTTPS without changing origin configuration for two SSH-auth failures. Full inventory and raw results: /mnt/c/Users/Jammy/Workspace/Science/scratch/tutorial_link_sweep_2026-11-04/.

Initial URL validation finds 348 distinct file/URL pairs targeting missing main-branch tutorial paths across six repositories. Most are assistant-generated notebook guidance: fix the source skills and routing first, then regenerate consumers. This count excludes version-pinned pages: library docs still describe the previous 12-lesson Lens chapter and 6-lesson Galaxy chapter. Check prose-only chapter/tutorial references and pinned destinations as well as URLs.

1. Finish a contextual mapping of old topics to current lessons across all chapters, using current HowToLens and HowToGalaxy scripts/contents as authority. Distinguish renamed, merged and removed topics; link to production guides when no current lesson teaches the promised content.
2. Update the two libraries' docs/howto* chapter indexes and relevant overview descriptions. Make current-course links follow the current course; retain intentionally historical/version-specific records. Review release URL-bumping policy before changing pins.
3. Repair the two assistant skill sets' tutorial links, labels and explanations, plus colab/contexts.yaml number-sensitive routing. Update relevant chapter summaries/routing in the courses. No unrelated science/API rewrite.
4. Regenerate affected notebooks and navigation in both courses and both workspaces using the repaired assistant sources; never hand-edit generated notebook instruction cells.
5. Repeat the whole-ecosystem audit (52 coverage receipts), validate local/remote tutorial targets and promised topics, verify routing and generated-source parity, build affected docs, run appropriate repository checks and independent review. Produce a before/after report and open linked PRs for affected repositories.

Tier: judge — merge mode: human /prm. Approved for autonomous implementation and PR creation on 2026-11-04. Existing historical records remain historical. Branch/claim conflicts must be checked before worktrees are created.

## Branch/claim survey
All eight affected canonical checkouts are on main and clean at audit time. Existing active claims cover PyAutoLens/PyAutoGalaxy (`magnification-maps-wiring`) and autolens_assistant (`results-library-p5a-assistant`, open PR177). Do not overlap or remove those claims. Phase implementation around available owners; queue the claimed-repository phases through start_dev unless their owners release them. No API dependency is introduced by these documentation changes, despite the generic FeatureDecision's library/API warnings.

Suggested phases: (1) canonical teaching links, topic descriptions and Colab routing in available assistant/docs owners, with claimed owners queued; (2) regenerate the four consuming notebook repositories after the relevant canonical source changes are ready; (3) repeat ecosystem-wide verification and ship documentation-only PRs with coverage/limitations recorded. One approval covers these phases; each merge remains human /prm.

## Approved steering
User explicitly approved autonomous source fixes, regeneration and ecosystem checks, stressing that correct .py sources can coexist with stale notebooks. Compare source, generated notebook and injected assistant guidance separately.
