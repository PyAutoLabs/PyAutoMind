## markdown-renderings-workspaces
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/264 (closed)
- completed: 2026-07-11
- prs: autofit_workspace#90 (afc384a) + autogalaxy_workspace#127 (04f0d8b9) + autolens_workspace#270 (632c776a) — all MERGED 2026-07-11 (human-directed)
- summary: batch 2a executed-markdown for the 3 workspaces (autofit 3 overview, autogalaxy 18, autolens +21 → index 30). cluster + ellipse/modeling excluded (runtime/timeout, follow-up). Traps: shared-venv matplotlib 3.11 broke corner→arviz-plots mid-build (downgraded 3.10.9; one-off, arviz nss-only, no pin); machine reboot mid-build resumed from cache; fits bank BEFORE plot cell so crashes never lose sampling. Calibration merged-unchanged. Leftovers: docs/pyautobuild/markdown_renderings_2a_leftovers.md.
