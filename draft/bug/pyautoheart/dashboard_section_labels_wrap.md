# Heart dashboard section names wrap into narrow columns

Type: bug
Target: PyAutoHeart
Difficulty: small
Priority: medium
Autonomy: human-required
Status: draft

## Original request (verbatim)

The size of things like "Libraries" is meaning the words are over multiple columns making them harder to read, Workt-ee-drift is 3 columns

## Reproduction and approved corrective scope

The Fable-reviewed dashboard plan, approved and delivered in PRs #246, #248, #250, included readable desktop/mobile layout. This user report corrects that implementation. Published board at 768px renders the Libraries name cell at about 48px high and 48px wide, splitting the name; Worktree drift also wraps. At 375px the existing stacked card layout gives labels their natural width.

Plan: keep mobile stacked rows, set a stable natural width for section names in desktop/table mode, and verify the longest section name and summary at 320/375/390/768/1280px including 200% text and no page overflow. Use a Heart-local CSS override. No readiness or payload change. This is within the previously approved readability scope.

Proposed branch: `fix/heart-dashboard-section-labels` (or `feature/` prefix required by worktree workflow).
