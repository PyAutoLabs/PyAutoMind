# Give the orphan mgl_slam_batch.py a home and sweep its lp bins

Type: refactor
Target: workspaces
Repos:
- autolens_workspace_developer
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `mgl_slam_batch.py` is tracked by a git repo (or deleted), no copy remains at the PyAutoLabs workspace root, and no `sub_size_list=[4, 2, 1]` survives anywhere in it.
Review-minutes: 3
Unattended: ready
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/135

The file sits at the PyAutoLabs workspace root, inside no git repo — 1309 lines, 45 KB, last modified 2026-07-31, tracked by nothing. It holds the last two unswept `sub_size_list=[4, 2, 1]` lp over-sampling sites in the organism, at lines 1183 and 1201. The 2026-09-08 sweep (issue #311, PRs #312 and #134) missed them because the file is in no repo: the #311 prompt listed `mgl_slam_batch.py` under the developer workspace, but no copy exists there.

It is an MGL (multi-galaxy lens) SLaM pipeline with main / extra / scaling galaxy categories and a BGC-anchored scaling relation. It is distinct from and larger than `scripts/multi_galaxy/slam.py` (800 lines; the diff between them runs to 1750 lines), so it is not simply a stale copy of that script.

Deciding the home is the human call, and is the whole of the work — the sweep afterwards is two lines. Candidates:

1. `scripts/multi_galaxy/features/` in the user-facing workspace, if the scaling-relation MGL pipeline is meant for users. Its docstring is written in the user-facing tutorial register, which argues for this.
2. `slam_pipeline/` in the developer workspace, alongside `dspl.py` and `light_dark_mge.py`, if it is a research script.
3. Retire it, if `scripts/multi_galaxy/slam.py` has superseded it — in which case check nothing in the 1750-line diff is worth keeping first.

Once it has a home under git, sweep the two sites to `[4, 2, 2]` per the profiling sweep in issue #235.

Surfaced at the /prm close-out of issue #311 on 2026-09-08.

<!-- formalised by the Intake (Conception) Agent on 2026-09-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/39f79ba7-a389-4860-b4fc-37f12f63b54b/scratchpad/intake_mgl.txt -->
