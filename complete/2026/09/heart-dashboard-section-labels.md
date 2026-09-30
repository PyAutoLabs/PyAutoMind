# Heart dashboard section labels

Merged PyAutoHeart PR #252 on 2026-09-30 as `d3906f06dc860a066f0a52c3f072438419cd31b3`, from head `7241a4fcee19317907764cda83fe0a103d80b38b`; the head is an ancestor of origin/main. Issue #251 closed.

The Heart-local table style now keeps section names together at tablet and desktop widths. On the published board, “Libraries” had been squeezed into about 48px at 768px and split midword. The phone layout remains stacked. No readiness, score, or payload data changed.

Validation: 1099 Heart tests and 158 targeted dashboard/fix tests; browser checks against published board HTML with the change at 320, 375, 390, 430, 768, 900 and 1280px in light/dark themes, plus 200% text and no horizontal overflow. Exact-head CI run 36773166968 passed Python 3.12 and 3.13 jobs and every step.

Dashboard publisher dispatched after merge: https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/36773535274. Existing release-integration failure is unrelated; no scientific release performed.

## Original prompt

# Heart dashboard section names wrap into narrow columns

Type: bug
Target: PyAutoHeart
Difficulty: small
Priority: medium
Autonomy: human-required
Status: active
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/251

## Original request (verbatim)

The size of things like "Libraries" is meaning the words are over multiple columns making them harder to read, Workt-ee-drift is 3 columns

## Reproduction and approved corrective scope

The Fable-reviewed dashboard plan, approved and delivered in PRs #246, #248, #250, included readable desktop/mobile layout. This user report corrects that implementation. Published board at 768px renders the Libraries name cell at about 48px high and 48px wide, splitting the name; Worktree drift also wraps. At 375px the existing stacked card layout gives labels their natural width.

Plan: keep mobile stacked rows, set a stable natural width for section names in desktop/table mode, and verify the longest section name and summary at 320/375/390/768/1280px including 200% text and no page overflow. Use a Heart-local CSS override. No readiness or payload change. This is within the previously approved readability scope.

Proposed branch: `feature/heart-dashboard-section-labels`.

## Delivery (2026-09-30)

PR https://github.com/PyAutoLabs/PyAutoHeart/pull/252 is open at 7241a4f. 1099 Heart tests, 158 targeted tests and browser checks passed. Exact-head CI pending; await human /prm. Dispatch heart-health.yml after merge.
