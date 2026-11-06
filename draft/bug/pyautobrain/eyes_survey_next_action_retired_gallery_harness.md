# `eyes survey` still tells people to run the retired `gallery/gallery_run.sh`

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-11-06
Consequence: glance
Witness: `pyauto-brain eyes survey` output and the `_eyes.py` docstring no longer mention `gallery/gallery_run.sh`; the next action names the current route (render via the domain's `*_visualization` producers, then `eyes review`); a test pins the next-action text; the Brain suite passes
Review-minutes: 5
Unattended: ready
Lane: any

The gallery harness (`gallery/gallery_run.sh`, `gallery_build.py`) was retired on 2026-09-30 (autolens_workspace_test 0dc177b, PyAutoEyes phase 5). Lens figures now render in `autolens_visualization` and are collected by the PyAutoEyes dashboard. `PyAutoBrain/agents/conductors/eyes/_eyes.py` still says, at lines 29 and 144:
- docstring: "rendering is the workspace's `gallery/gallery_run.sh`"
- `next_action`: "run the workspace's gallery/gallery_run.sh for stale/missing renders, then `eyes review`"

Found by a pilot live-shift worker (2026-11-06, autolens_workspace_test#354, record `complete/2026/11/gallery-runner-missing-tiers.md`). Fix the two strings to the current route (check `agents/conductors/eyes/AGENTS.md`) and add a test asserting the next action never names `gallery_run.sh`. Weekend cloud-lane task 1 (`draft/feature/pyautobrain/mobile_shift_operation.md`).

<!-- filed by hand 2026-11-06 for the weekend cloud shift; headers mirror intake's -->

## Verified 2026-11-06 (cloud queue session): premise false — recommend retire

The retired harness was the copy in `autolens_workspace_test/gallery/` only.
The four registered instances the conductor targets still ship it:
`autolens_visualization/gallery/gallery_run.sh` and
`autogalaxy_visualization/gallery/gallery_run.sh` exist on `main` (checked by
clone; autolens_visualization 51c7e4d, 2026-10-23), their AGENTS.md/README tell
you to run `bash gallery/gallery_run.sh --all`, and
`PyAutoBrain/agents/conductors/eyes/AGENTS.md` ("project repos … the
`gallery/gallery_run.sh` harness") agrees. So `_eyes.py`'s next action
("run the workspace's gallery/gallery_run.sh …, then `eyes review`") is
correct, and the Witness (never mention `gallery_run.sh`) would make it wrong.
Not changed. Needs a human ruling to retire (as with
`gallery-runner-missing-tiers`). Do not run weekend cloud task 1.
