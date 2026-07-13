# EP analytic updates — implement the four planned work packages

Type: feature
Target: PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

The complete, self-contained implementation plan lives in
**PyAutoFit#1338** (plan-only issue; nothing implemented). Scoping
verdict behind it: PyAutoFit#1337 (EP review Phase 6); umbrella:
`research/graphical_ep/ep_framework_review.md`.

Work packages (sequence; each becomes its own issue/PR at pick-up —
do not bulk-issue):

1. **WP1** — exact PriorFactor updates in the declarative path +
   document the analytic-projection contract (~2–3 days). Start here.
   Note: rebase over / land after PyAutoFit#1334 (owns README.md).
2. **WP2** — first-class linear-Gaussian factor; validate against an
   IC50-shaped integration script (~1 week).
3. **WP3** — Gamma–Poisson / Beta–Bernoulli conjugate factors.
   **Gated**: needs the #1331 fix batch (Gamma from_mode) and #1332 F2
   (KL direction) merged first.
4. **WP4** — truncated-normal analytic moments (+ optional exact
   truncated KL, fixing F6). **Gated**: needs #1331-04 merged first.

Pick-up may be a different session or model (e.g. Opus): read #1338,
#1337 and `PyAutoFit/autofit/graphical/README.md` (PR #1334) — no other
context required. Full `test_autofit/` + the
`autofit_workspace_test/scripts/graphical/` scripts must stay green;
library unit tests numpy-only; speed-up evidence via the Phase 4
`ep_history.csv` tooling (#1335).
