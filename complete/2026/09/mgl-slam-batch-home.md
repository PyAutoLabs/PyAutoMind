- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/135
- completed: 2026-09-08
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/136
- merged: autolens_workspace_developer 96937c9 (PR #136)
- heart-ack: 2026-09-08 in-session YELLOW, reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772)", "release validation incomplete: no rehearsal evidence for v2026.9.8.1.dev75701" and "profiling drift on 3 pinned results"; none touch autolens_workspace_developer

**Summary.** `mgl_slam_batch.py` had been sitting at the PyAutoLabs workspace root inside no git repo — 1309 lines, untracked and unbacked-up since 2026-07-31 — which is why the 2026-09-08 sub-size-1 sweep (#311) missed it. It now lives at `autolens_workspace_developer/slam_pipeline/mgl_slam_batch.py` with its two `sub_size_list=[4, 2, 1]` sites swept to `[4, 2, 2]` and line endings normalised CRLF → LF. The untracked root copy is deleted.

**The home decision.** It is a real-data production run script, not a user-facing example: it takes a CLI `--dataset` tile id (`102022474_NEG590266584471556814`), reads a multi-HDU FITS by `_FLUX`/`_BGSUB` tag plus `info.json`, three centre JSONs and `extra_masking.fits` from a per-dataset directory, and writes under `path_prefix="mgl"` with `unique_tag=dataset_name`. That per-dataset CLI parameterisation is the "batch" in its name and makes it a sibling of `dspl.py` and `light_dark_mge.py`. It is not superseded by `autolens_workspace/scripts/multi_galaxy/features/scaling_relation/slam.py` (1138 lines, maintained to 2026-09-04), which is the *documented example* of the same science on a **simulated** dataset it generates via `should_simulate` → `simulator.py`.

**Witness.** Met: the file is tracked, no copy remains at the workspace root, and no `sub_size_list=[4, 2, 1]` survives in it. `python -m py_compile` passes; `diff --strip-trailing-cr` against the original orphan shows exactly the two bin lines and nothing else. The script cannot be run here — it needs a real tile with its FITS, three centre JSONs and `positions.json`.

**Traps / notes.**
- **The prompt's "last unswept site in the organism" claim was wrong.** A tree-wide grep after the sweep finds four more in `autolens_jax_joss/benchmarks/` (`imaging.py`, `multi_band.py`, `group.py`, `imaging_and_point_source.py`) — a repo no sweep has touched, whose benchmarks may be pinned to published JOSS numbers — plus generated `markdown/` pages in `autolens_workspace` (5) and `autogalaxy_workspace` (2), which regenerate in the release build. Corrected on the issue and in the PR body.
- The orphan was CRLF. A file that has lived outside git on a Windows-adjacent path arrives with CRLF; adopting it into a repo with no `.gitattributes` means normalising, or the whole file reads as changed on every later diff.
- No latent variables in this script, so the Euclid pipeline's `[4, 4, 2]` middle-bin raise (`euclid_strong_lens_modeling_pipeline#56`) does not apply; `[4, 2, 2]` matches `slam_pipeline/light_dark_mge.py` and the workspace's own `scaling_relation/slam.py`.
- Both `intake classify` and `pyauto-brain feature` graded this `too-large` / `large — split-into-phases` for one file move and a two-line edit; the score reads repo count and architecture keywords in the prose, not the work. `intake classify` also ignored the declared `Difficulty:` while honouring the declared `Type`, `Autonomy` and `Priority` in the same block — worth a look at that parse.

**Follow-ups.** None filed. `autolens_jax_joss/benchmarks/` is the open question above; it needs a decision on whether its pins may move at all.

## Original prompt

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
