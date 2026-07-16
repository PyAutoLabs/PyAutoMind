# Intake Agent writes prompts to the legacy flat layout, not draft/

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

`bin/pyauto-brain intake --apply` still writes prompt files to the pre-#71 flat
layout `PyAutoMind/<work-type>/<target>/<name>.md` (observed 2026-07-16: a new
prompt landed at `docs/autoreduce/...` at the Mind top level). Since the Mind
lifecycle split (PyAutoMind#71), the backlog home is
`draft/<work-type>/<target>/<name>.md`; Mind's AGENTS.md documents intake as
filing into `draft/`. `PyAutoBrain/agents/conductors/intake/_intake.py` contains
no reference to `draft` — the proposed-path construction was never rewired.

Fix in @PyAutoBrain: prefix the intake writer's proposed path with `draft/`
(classify, ideas, and formalise paths alike), and check census/reconcile still
scan both layouts during the transition. Add a regression test asserting the
written path starts with `draft/`.

Also note (separate, judgment-level): the classifier misroutes Target when the
raw text mentions library names in context (see
feedback_intake_target_handfix) — this prompt is only about the layout drift.

## Resolution

Fixed on PyAutoBrain main by 5f54aae ("intake: migrate the conductor to the Mind#71 lifecycle layout") — verified: `_intake.py` now writes `draft/<work-type>/<target>/`. Retired from draft/ without a dedicated issue (fixed same-day by a parallel session).
