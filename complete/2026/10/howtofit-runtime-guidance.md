# HowToFit tutorial 4: realistic runtime guidance

HowToFit#72 → PR #74 (merge `03946b65c`, 2026-10-23).

## What shipped
Tutorial 4's runtime claim was rewritten to match a measured run of its 15-parameter DynestyStatic fit. The diff is prose only, and the notebook was regenerated. Before merging, main was merged in to pick up #75's smoke epilogue (BlackJAX + Nautilus). CI then passed: smoke on 3.12 and 3.13, Navigator and Tutorials Complete.

## Original prompt

# HowToFit tutorial 4 promises "under a minute" and takes six

Type: docs
Target: HowToFit
Repos:
- HowToFit
Themes:
- tutorials
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: notify
Review-minutes: 5
Unattended: ready
Witness: tutorial 4's prose states a runtime that matches a measured run of its 15-parameter DynestyStatic fit.
Issued: 2026-10-17
Filed: 2026-09-15

`scripts/chapter_1_introduction/tutorial_4_why_modeling_is_hard.py` says of its
15-parameter, five-Gaussian `DynestyStatic(sample="rwalk")` fit:

    "Consequently, the non-linear search takes slightly longer to run but still
     completes in under a minute."

Measured 2026-09-15 at real settings on a 4-core container: **385.1s** (6m25s),
the slowest script in the series by a factor of five. The `print` a few lines
below ("this could take a few minutes") is closer but still under.

Not a defect — the fit completes and the tutorial passes — but it is the single
longest wait in chapter 1 and the prose sets a workshop audience up to think
something has hung. Either restate the runtime honestly (and say it depends on
core count) or give the fit a smaller budget.
