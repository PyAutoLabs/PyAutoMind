# DNA dashboard: a Policies section for version decisions

PyAutoDNA#6, merged as PyAutoLabs/PyAutoDNA#7 (44e6d789) on 2026-11-12. Tier glance: tiered auto-merge after the
human acknowledged Heart YELLOW; Witness checked on the exact head render before merge and on the live board after.
Follow-up of jax-version-policy (PyAutoNerves#213).

## What shipped
- Decision front matter (`dna/policy_docs.py`): policy, status, packages, declared_in, recommended, review_date,
  findings, links; `decisions/jax-cpu-policy-2026-11.md` is the first.
- Policies section first on the board: declared range from the newest dependency audit vs recommended, derived
  status (adopted / recommended, not yet declared / not audited), versions the declared range allows that hang with
  no flag (card warning + yellow state item), findings, links.
- Safe built-in markdown renderer for decision pages (replaces raw `<pre>`).
- Hang matrix as pass/hang counts per jax x XLA flag x cores per environment + per-call cost on the newest version.
- Fresh dependency audit of the five library mains (2026-11-11) in inventories/public.json. 32 tests.

## State on merge
Live board: "JAX CPU policy — recommended, not yet declared"; PyAutoNerves declares `!=0.10.*,!=0.11.0,<0.12.0,>=0.7.0`
vs recommended `<0.13,>=0.12.0`; 0.11.2 flagged. Becomes `adopted` after jax-floor-0-12 (Nerves#215) ships and a
fresh `dna audit` is exported.

## Not done (follow-up)
RAL shared-environment observation: `dna collect ral-login --probe-backend` on the login node stalled in NFS D-state
for 24+ min and died without a receipt. Filed: draft/maintenance/pyautodna/ral_shared_environment_observation.md.

## Original prompt

# DNA dashboard: a Policies section that shows version choices and the research behind them

Type: feature
Target: PyAutoDNA
Repos:
- PyAutoDNA
Priority: medium
Consequence: glance
Witness: the live board shows the JAX CPU policy card with declared vs recommended range, status and the hang-matrix check flagging allowed hanging versions, plus the version x flag x cores grid and the flag-cost table.
Issued: 2026-11-11

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
