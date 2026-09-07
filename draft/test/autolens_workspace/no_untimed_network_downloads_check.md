# Guard every workspace script against untimed network downloads

Type: test
Target: autolens_workspace
Repos:
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- PyAutoHeart
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Witness: a repo-level check (pytest or a PyAutoHeart/PyAutoHands lint) fails on any `urllib.request.urlretrieve(` or `urlopen(` call without `timeout=` under `scripts/`, and passes on current main after autolens_workspace#537 merges.
Unattended: ready
Filed: 2026-09-07

On 2026-09-07 `scripts/multi_dataset/features/imaging_and_point_source/modeling.py`
timed out at the 300 s smoke cap in PyAutoHeart run 34099198772 because an untimed
`urlretrieve` to hips2fits stalled in `ssl.read` (CI artifact traceback).

autolens_workspace#293 (commit 3920ed30, 2026-07-19) had fixed the identical defect in
`scripts/cluster/start_here.py`, and it came back in four scripts within three weeks
(`multi_dataset/.../modeling.py`, `weak/start_here.py`, `weak/real_data/a2744.py`,
`weak/features/strong_lensing/a2744.py`; fixed in autolens_workspace#537).

Add a durable check so the pattern cannot return: scan `scripts/**/*.py` in each
workspace for `urlretrieve(` and for `urlopen(` without a `timeout=` kwarg, fail with
the file:line. Decide where it lives (a workspace `test_*` file that Heart's PR gate
already runs, or a shared PyAutoHands lint that every workspace gate calls) and mirror
it to the other workspaces that download data.

Do not add retry logic here; the check is the deliverable.
