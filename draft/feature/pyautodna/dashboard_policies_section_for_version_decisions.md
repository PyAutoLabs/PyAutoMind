# DNA dashboard: a Policies section that shows version choices and the research behind them

Type: feature
Target: PyAutoDNA
Repos:
- PyAutoDNA
Priority: medium
Consequence: glance

Source: human 2026-11-11, after jax-version-policy (PyAutoNerves#213, complete/2026/11/jax-version-policy.md): "did we write and update the DNA dashboard with this work? E.g. the choice of versions and maybe some research findings? Dashboard might not be fully designed to support this yet". Needs /intake to formalise.

## Today (live board after PyAutoDNA#5)
- JAX CPU policy: a flat hang-matrix table (one row per jax x XLA flags x environment); a yellow item for an environment on a hanging setup; an XLA-options column.
- Decisions render only as raw markdown in a collapsed `<pre>`.
- Missing: what the requirement IS vs what is RECOMMENDED vs its status; the headline findings (hang depends on cores: 4 always, 16 never; 0.12 clean; eigen flag +18-50 % on pixelized at 0.12); flag cost; core-count dimension.
- Board `updated` reads 2026-10-08 (oldest observation); RAL shared environment is stale (it runs jax 0.11.2 and would be flagged once re-observed).

## What
1. Structured policy fields per decision (front matter or a sibling YAML): name, status (recommendation / validating / adopted / superseded), declared range (read from the live PyAutoNerves pyproject via `dna audit`, not copied), recommended range, review date, 2-5 headline findings with numbers, links (issue, evidence).
2. A "Policies" section at the top of the board: one card per policy showing declared vs recommended, its status and the findings; the full decision text rendered as readable prose, not `<pre>`.
3. The hang matrix as a version x flag grid with core counts as a sub-dimension (pass/hang counts), plus a flag-cost table from the matrix rows' `steady_median_call_s` (already in the records' checks).
4. Refresh the RAL shared-environment observation (`dna collect ral-login --probe-backend` on RAL, import privately) so the board shows whether it is on a hanging setup.
5. Writing per PyAutoBrain skills/WRITING_STYLE.md; mobile width; tests for the projection and render.
