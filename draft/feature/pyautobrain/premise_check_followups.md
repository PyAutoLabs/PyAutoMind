# Premise check and lane inference: follow-ups from M1.3

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: one test per item fails on c7e7c1c16 and passes after; the pool premise sweep still returns no false `obsolete`
Review-minutes: 10
Unattended: ready
Lane: any

Source: worker and independent review of PyAutoBrain#608/#609 (programme M1.3), 2026-11-12.

1. The planner does not yet prefer recently `Verified:` drafts.
2. Negation does not end at a dash: "needs the A100 — not the laptop" infers `any` (`_intake.py` `_negated`).
3. Lane words need a run-type verb: "clean up … on RAL" is missed (this dropped a real RAL item from `point_source_cpu_campaign_owed_leftovers`, which is human-gated).
4. Paths have no age bound, unlike functions: a 2022 removal still counts as GONE evidence.
5. The sweep flags `draft/.../remove_eden_packaging_tooling.md` obsolete (`eden.yaml` deleted 2026-11-10, fd1e76d65): a human should retire it.

<!-- filed 2026-11-12 by the programme lead session -->
