# Standardize dashboard orchestration prompt panels

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoEars
- PyAutoHeart
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing

# Standardize dashboard orchestration prompt panels

Type: feature
Difficulty: large
Priority: normal
Autonomy: supervised

Primary target: @PyAutoBrain, owner of the shared board presentation layer. Determine affected dashboard repos from the authoritative board registry during planning; do not treat every audited repo as an implementation claim.

## Original user request (verbatim)

I also want us to standardized every dashboard having a button at the top which has a general prompt one copies to do the work associated with it and you can customize it based on certain tasks. I think Ears has exactly the right format or template albeit maybe it could be slightly prettier or cleaner. Lots of other dashboards have this, but I also want this to become a stadnard format for consistency. For HEart, this would see us move the "Fix Heart Systematically" button up to this. Intake a task to do this homogenization

## Objective
Give every organism dashboard a consistent panel near the top for copying a general prompt that manages the work associated with that dashboard in one ongoing AI chat. Allow optional task-specific direction without losing the default whole-dashboard remit. Use Ears as the functional reference, with modest visual refinement where it improves clarity.

## Reference and design direction
- Ears implementation: `PyAutoEars/ears/presentation.py` (CHECKIN, copy_button and styling) and `ears/board.py` (panel, optional direction, prompt preview, clipboard/fallback behavior), shipped in PyAutoEars PR #10.
- Standard structure: clear dashboard-specific heading and short description, prominent copy action, labelled optional task/focus input, expandable selectable preview of the exact prompt copied, and accessible success/failure feedback.
- Keep input, preview and clipboard payload in sync; an empty optional field must yield a useful general prompt. User direction should be data appended to the instruction, with no hidden execution from the page.
- Improve Ears' cleanliness/spacing or wording if useful, then share that presentation contract rather than duplicating near-identical layouts. Preserve organ identity and distinct prompt semantics.
- @PyAutoHeart: move/adapt the existing "Fix Heart Systematically" action into this top panel. Reuse its current systematic repair instructions and gates, retain a recognizable action label, and avoid leaving competing duplicate primary actions elsewhere.

## Planning and rollout
1. Audit each registered dashboard: current general prompt action, its location, optional customization, owning renderer/theme, and domain-specific routing/permissions. Produce an adoption matrix; identify missing general prompts and justified exceptions explicitly.
2. Define the shared component/presentation contract and default copy/customization behavior. Ground it in the existing portable-prompt/copy contract and Ears pattern. Keep dashboard-specific payloads in their owning domain; homogenize appearance/interaction without flattening different work types into one generic instruction.
3. Pilot the agreed panel on Ears and Heart, then adopt it across the remaining boards in bounded phases if warranted. Size and claim only the repos in the approved implementation phase.
4. Preserve existing command routing, evidence freshness, source trust boundaries, domain workflows, and human approval requirements. A general check-in must not silently authorize replies, merges, release actions, compute or other mutations that its domain requires the user to approve.
5. Coordinate with the shipped sizing standard in `complete/2026/10/standard-board-sizing.md` (PyAutoBrain PR #462). The tasks are related but independently scoped: this task owns the common orchestration panel; that task owns page sizing. Check active claims before editing shared theme code. Neither task is automatically blocked on the other.

## Acceptance and validation
- Every registered dashboard has the agreed top panel, or a documented and reviewed exception; the adoption matrix records completion rather than assuming shared CSS reached independent renderers.
- Each default prompt covers its dashboard's actual work and supports one ongoing chat; optional direction can focus specific tasks without silently omitting the rest of the queue.
- Heart's systematic-fix action is in the standard top position and retains its existing workflow semantics.
- Consistent labels, spacing, typography, button treatment, preview and feedback across boards; domain identity remains visible.
- Verify keyboard access, accessible names, optional-direction escaping (including markup/quotes/newlines), exact preview/copy agreement, clipboard denial fallback, long payloads, mobile/tablet/desktop and light/dark appearance. No page-wide horizontal overflow.
- Reuse existing renderer/browser/copy-contract tests where applicable. Do not change data/feed contracts or introduce a styling framework solely for this panel.

Intake only: file for a later chat; do not start development, open an issue, claim implementation repos or deploy now. The next session runs start-dev, proposes the shared design and phases, and obtains the required plan approval.

<!-- formalised by the Intake (Conception) Agent on 2026-10-05 from file:tmp/dashboard-prompt-panel.md -->
