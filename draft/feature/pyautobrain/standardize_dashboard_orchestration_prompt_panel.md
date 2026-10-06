# Shared dashboard orchestration panels and durable organism standards

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoScientist
- PyAutoEars
- PyAutoHeart
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing

Primary target: @PyAutoBrain, owner of the shared board presentation layer. Determine affected dashboard repos from the authoritative board registry during planning; do not treat every audited repo as an implementation claim.

## Original user request (verbatim)

I also want us to standardized every dashboard having a button at the top which has a general prompt one copies to do the work associated with it and you can customize it based on certain tasks. I think Ears has exactly the right format or template albeit maybe it could be slightly prettier or cleaner. Lots of other dashboards have this, but I also want this to become a stadnard format for consistency. For HEart, this would see us move the "Fix Heart Systematically" button up to this. Intake a task to do this homogenization

## Additional user direction (verbatim)

Can we start to build into the PyAutoScientist and other repos AGENT.md or wherever appropriate these "standardization" tasks we are doing? Where would they belong? Feels like this should be a shared thing across all repos

ok work this in combined with organs/PyAutoMind/draft/feature/pyautobrain/standardize\_dashboard\_orchestration\_prompt\_panel.md, noting that I want this prompt panel to always link to the relevent GitHub repo from which work is done when relevent, PyAutoEars is a great template and example of how to approch this.

## Objective
Make the orchestration panel the next shared interface standard, and establish how this and future standardization work becomes durable guidance across repositories.

Give every organism dashboard a consistent panel near the top for copying a general prompt that manages the work associated with that dashboard in one ongoing AI chat. Allow optional task-specific direction without losing the default whole-dashboard remit. Use Ears as the functional and visual reference, with modest refinement where it improves clarity. Include a visible link to the relevant GitHub repository where the work is performed whenever applicable; make that destination part of the portable prompt context too.

## Shared standards ownership and discovery

- @PyAutoBrain owns the canonical standards index in `docs/` and the shared board implementation. Index the existing `docs/board-sizing.md` and `docs/board-navigation.md`, then add the orchestration-panel contract. Keep one source for each standard and link to its implementation and verification.
- @PyAutoMind owns distribution through `scripts/repos_sync.py`: generate a short standards-discovery block into registered repositories' `AGENTS.md`, using the existing synchronization and drift-check machinery. Source the rule once; never hand-maintain copies in every repo. Keep general discovery guidance universal and board-specific requirements scoped to board owners. Repository-local exceptions must be explicit and justified.
- @PyAutoScientist exposes the standards through its README/documentation entry points and agent guidance. Its published documentation currently lives in Brain; do not move the documentation source as part of this task.
- An agent changing a shared interface must consult the applicable standard, reuse its shared implementation, identify affected consumers and validate adoption. A new standardization task is complete only when its durable contract, discovery guidance, implementation and appropriate drift checks agree.
- Keep always-loaded instructions short. Link to relevant standards on demand, with usable repository links for single-repo/remote sessions; do not require every agent to load every standard or have a full multi-repo checkout.
- These are one coordinated initiative: the panel is the concrete implementation and first application of the reusable standards-discovery rule. Use bounded implementation phases and individual repo PRs where necessary, rather than treating the entire workspace as one claim.

## GitHub work destinations — required panel contract

- Every panel must expose a clearly labelled, keyboard-accessible GitHub link to the relevant work repository whenever one exists. This link belongs in the panel beside its main controls, not only in a distant footer or hidden preview.
- Identify the repository where the prompted work is actually performed. A board's hosting/source repository and its work repository can differ; never substitute a generic Brain link or the board's Pages URL without checking the domain routing.
- Include the relevant repository URL(s) in the default portable prompt and exact preview so a pasted prompt carries its work context into a new chat. This is contextual routing, not permission to mutate a repository.
- Ears is the reference for the whole panel, including its prominent `Open Community Hub` action. Preserve that link to the actual community work surface. A community hub is a valid companion destination; document the appropriate repository link(s) separately where repository work is relevant rather than relabelling the hub as a repository.
- For multi-project boards, expose clearly named work-repository links and include the relevant project destination when a focus/project is selected. Do not silently choose an arbitrary project for a whole-board check-in. Keep optional free-text direction separate from trusted destination metadata.
- Derive destination identity from the authoritative body map or the domain's existing project registry; labels, URLs and any absence/exception are owner-supplied. Escape text and validate link schemes. Missing identity must not produce a fabricated repository or imply there is no work.
- The adoption matrix must record the board renderer owner, prompt owner, primary work destination(s), any community/project companion links and justified exceptions.

## Reference and design direction
- Ears implementation: `PyAutoEars/ears/presentation.py` (CHECKIN, copy_button and styling) and `ears/board.py` (panel, optional direction, prompt preview, clipboard/fallback behavior), shipped in PyAutoEars PR #10.
- Standard structure: clear dashboard-specific heading and short description, prominent copy action, visible GitHub work destination(s), labelled optional task/focus input, expandable selectable preview of the exact prompt copied, and accessible success/failure feedback. Placement follows the shipped header order: logo/banner → section navigation cards → orchestration panel, with truthful freshness/context near the panel as needed.
- Keep input, preview and clipboard payload in sync; an empty optional field must yield a useful general prompt. User direction should be data appended to the instruction, with no hidden execution from the page.
- Improve Ears' cleanliness/spacing or wording if useful, then share that presentation contract rather than duplicating near-identical layouts. Preserve organ identity and distinct prompt semantics.
- @PyAutoHeart: move/adapt the existing "Fix Heart Systematically" action into this top panel. Reuse its current systematic repair instructions and gates, retain a recognizable action label, and avoid leaving competing duplicate primary actions elsewhere.

## Planning and rollout
1. Audit each registered dashboard: current general prompt action, its location, optional customization, owning renderer/theme, and domain-specific routing/permissions. Produce an adoption matrix; identify missing general prompts and justified exceptions explicitly.
2. Define the shared component/presentation contract and default copy/customization behavior. Ground it in the existing portable-prompt/copy contract and Ears pattern. Keep dashboard-specific payloads in their owning domain; homogenize appearance/interaction without flattening different work types into one generic instruction.
3. Pilot the agreed panel on Ears and Heart, then adopt it across the remaining boards in bounded phases if warranted. Size and claim only the repos in the approved implementation phase.
4. Preserve existing command routing, evidence freshness, source trust boundaries, domain workflows, and human approval requirements. A general check-in must not silently authorize replies, merges, release actions, compute or other mutations that its domain requires the user to approve.
5. Build on the shipped sizing and navigation standards: `complete/2026/10/standard-board-sizing.md` (PyAutoBrain#462) and `complete/2026/10/standard-board-banner-and-navigation.md` (core PyAutoBrain#464 plus ten consumer PRs). Preserve their layout and navigation contract.
6. Add the standards index and generated discovery rule with the panel contract, then distribute through the existing repo-sync mechanism in bounded phases. Generated `AGENTS.md` changes still count as touched repositories: survey and respect claims, including active library/workspace tasks, and record deferred destinations explicitly.
7. Validate both kinds of adoption: all registered boards use the panel or have a reviewed exception, and all intended repositories receive the correct standards-discovery guidance. Update the adoption matrix and verify generated/published HTML after the authorized merges. Source changes alone are not evidence of publication.

## Acceptance and validation
- Every registered dashboard has the agreed top panel, or a documented and reviewed exception; the adoption matrix records completion rather than assuming shared CSS reached independent renderers.
- Each default prompt covers its dashboard's actual work and supports one ongoing chat; optional direction can focus specific tasks without silently omitting the rest of the queue.
- Every applicable panel has a visible, correctly labelled link to the actual GitHub work repository; the copied prompt and preview contain the same destination context. Multi-repo boards and Ears' Community Hub are handled explicitly. No arbitrary or fabricated destination, and no lost human-approval boundary.
- Heart's systematic-fix action is in the standard top position and retains its existing workflow semantics.
- The canonical standards index documents sizing, banner/navigation and orchestration panels, links their shared implementations and verification, and explains how future cross-repo standards are added.
- Generated `AGENTS.md` discovery guidance reaches the intended repos and passes repo-sync drift checks; isolated-repo links work, board-only guidance stays scoped, and Scientist exposes the same canonical standards without copying their full text.
- Consistent labels, spacing, typography, button treatment, preview and feedback across boards; domain identity remains visible.
- Verify keyboard access, accessible names, optional-direction escaping (including markup/quotes/newlines), exact preview/copy agreement including work URLs, correct/escaped destination links, clipboard denial fallback, long payloads, mobile/tablet/desktop and light/dark appearance. No page-wide horizontal overflow.
- Reuse existing renderer/browser/copy-contract tests where applicable. Do not change data/feed contracts or introduce a styling framework solely for this panel.

## Next development step

The user combined the shared-standards guidance with this panel task on 2026-10-05. The earlier intake-only instruction described the original filing, not a permanent prohibition on starting this work. Run start-dev on this combined prompt, audit the registered board owners and work destinations, and present the concrete shared design and bounded phases before source edits. The user has approved combining these requirements; do not ask again whether to combine them. Implementation approval must cover the actual affected repos and rollout. Declared tier: judge; merge mode: human /prm.

<!-- formalised by the Intake (Conception) Agent on 2026-10-05 from file:tmp/dashboard-prompt-panel.md -->

## Execution progress

User approved the combined implementation with “ok go”. Phase 1 merged as PyAutoBrain#466 (5d764f6), closing issue #465. The shipped scope is recorded in `complete/2026/10/orchestration-panel-core.md`: shared API, canonical standards index and Brain/Mind/Cortex renderer adoption. Validation: 1,195 tests, strict docs and browser witness; all three CI jobs green.

Remaining approved work: Ears/Heart pilots and remaining boards, Mind-generated instruction discovery, Scientist entry links and published verification. The shared API dependency is now merged; continue through bounded start-dev phases. This parent prompt remains open for that remaining scope.

## Presentation refinement — 2026-10-05

Remove dashboard-purpose and usage/tutorial prose from the visible boards, including masthead ledes and orchestration-panel descriptions. Keep concise headings, button labels, GitHub destinations, optional-direction inputs and prompt previews. Do not substitute new explanatory prose. This is the single-user presentation standard and applies across the remaining board rollout as well as Brain-owned renderers already migrated.

Specific requirements:
- Mind: remove the entire “Every task the Mind is holding…” masthead paragraph.
- Ears: remove the visible “Last checked …” line entirely; preserve snapshot timestamps in the data contract.
- Heart: remove the “Is it safe to release?…” introduction and place the main “Fix Heart systematically” action in the top shared panel after navigation. Reuse the exact existing fix-plan prompt plus the shared GitHub destination context; remove the duplicate bottom primary action. Retain the distinct missing-evidence action.
- Audit static dashboard-purpose/usage paragraphs across the board family. Operational results, failure reasons, real stale/unknown evidence states, selectable prompt contents and repository links remain meaningful data, not tutorial text.

Implementation plan: first update Brain's shared hero/panel rendering and presentation contract so optional/removed description text produces no empty spacing; adjust Brain/Mind/Cortex consumers. Then update Ears' top section and adopt the shared panel on Heart with its configured repository link and existing fix-plan payload. Finish owner-specific tutorial prose removals during the recorded all-board rollout. Validate representative rendered pages at mobile/desktop widths, action location and exact copy payloads; run affected existing suites and browser witness. Tier: judge; merge mode: human /prm.

### Original refinement request (verbatim)

Remove all explanatory text which says what a dashboard does and how to use it -- only I use this I dont need a reminder, on Mind this is "Every task the Mind is holding. Tap a task's 📋 and its start-dev skill prompt is on your clipboard — paste it into an AI assistant chat to route the assistant straight to that task. Recent is the same work by date — what has been happening rather than what to do next.", on Ears, just remove the "Last checked 05 Oct 2026, 17:30 UTC2 as its text whic breaks dashboard symmnetry, on heart remove the text "Is it safe to release? See what needs attention, then copy a prompt to work through it in your coding chat." and get the main button up there which basically will replace the "Fix Heart Systematically" button at the bottom.

Refinement shipped: `complete/2026/10/dashboard-minimal-text.md` — Brain#468, Ears#13 and Heart#284 merged. Shared introductions removed; Ears timestamp removed; Heart top panel adopted. Remaining initiative scope is other panel consumers, generated guidance and published verification. Do not re-file these completed changes.

All-board live prose audit follow-up: `complete/2026/10/dashboard-prose-followup.md` (Hands#300; PRs Hands#301/Eyes#18/Insight#6). Seven shared-theme renders refreshed; quoted Heart/Hands/Nerves intros absent live. Custom owner prose removals merged as Hands#301/Eyes#18/Insight#6; publication dispatched; GitHub runner queue still pending at close-out.

## Organ-named prompt headings — shipped 2026-10-06

Replace generic panel headings with concise action sentences containing the organ name in bold. No explanatory subtitle. Cover all dashboards and validate mobile/desktop line length without horizontal overflow. Mind quoted subtitle is absent from the live HTML as verified during this request. Wording approved in session; user then instructed “ok go”: Brain — Plan your next move with your Brain; Mind — Put your Mind to work; Cortex — Explore science with your Cortex; Ears — Use your Ears to hear the community; Heart — Keep your Heart healthy; Hands — Ship with your Hands; Memory — Build your Memory; Pulse — Check your Pulse; Insight — Find your next Insight; Nerves — Check your Nerves for config drift; Gut — Clear out your Gut; Eyes — Review figures with your Eyes; Scientist — Work with your Scientist.

Original request (verbatim):

At the top of mind "Plan and coordinate devleopment" button is good, remove the text "Review the task queue, choose
priorities and carry accepted work through the development workflow." as this again is just elling me what I aleady know.
instead of "Plan and coordinate development" be more direct what the prompt does or link it to Mind. It could
be "Do some tasks on you Mind". For ears it could be One chat. The whole
community. -> "Use your Ears to listen to the community". I want each setense to be concise, span one line, but use the
organ name to remind us where we are. The organ name should be in bold.   Then do this across all dashboards, thinking carefully aobut how the organ name makes its way into the text.

Heading implementation checkpoint — 2026-10-05: wording approved, including “Explore science with your **Cortex**”. Entry Heart verdict STALE (PyAutoNerves rehearsal source drift). Worktree conflict guard blocks PyAutoBrain: active issues #469/#470/#471/#472 (worktree-sh-root-activate-clobber, unregistered-worktree-guard, cortex-find-script-symlink, intake-declared-header-fields). No source edited or worktree created. Git fetch is unavailable in this restricted session (github.com DNS resolution failure); this checkpoint is local, not pushed. Resume the approved heading work after the Brain claims clear; do not ask for wording approval again.

Resume verification — 2026-10-06: GitHub access restored; fetched Mind before editing and preserved all five saved local files. Issues #469–#472 remain OPEN; current active.md and worktree_check_conflict confirm all four Brain claims. Heading implementation remains blocked; approved wording persists. Heart entry reports STALE (release STALE, monitoring RED). Publication verification: Hands run 37363739823, Eyes run 37363681281 and Insight run 37363693166 all completed with failure and cancelled deployment jobs. No later publication runs were present. Live Pages HTML still contains the removed Hands relationship paragraph, Eyes introduction/tutorial and Insight check-in/ledger guidance. The merged prose cleanup is not yet live; verification did not rerun deployments.

Heading phase completed: `complete/2026/10/organ-prompt-headings.md` records all eleven merged owner PRs covering thirteen dashboards (Brain#481 plus ten consumer PRs). The approved wording and responsive single-line styling shipped, with exact prompt payloads/copy controls/work links retained. Historical blocked checkpoints above are superseded. Remaining parent scope is broader panel adoption and generated standards-discovery guidance; do not re-file the completed headings. Previously merged Hands#301/Eyes#18/Insight#6 prose cleanups are now confirmed live.

## Remaining rollout PRs — 2026-10-06

Approved remaining phases implemented and tested: `active/orchestration_panel_consumers.md` (Ears#15; nine owner PRs) and `active/shared_standards_discovery.md` (Mind#474; 35 PRs including generator Mind#475 and contract Brain#483). Scientist README standards links are included in Scientist#45. All nine panels passed 1,441 owner tests and 72 browser layouts with clipboard/fallback/budget validation. Generator passed 652 tests and independent adversarial re-review. Forty-four of 46 source destinations now have generated guidance on open PRs; PyAutoArray and euclid_strong_lens_modeling_pipeline remain explicitly deferred for other active claims. Merge is human /prm; post-merge publication remains unverified for this new panel phase. Preserve these active tasks and PRs rather than filing replacements.
