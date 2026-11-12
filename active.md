
## autonomous-orchestrators-p4c
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/574
- issued: 2026-11-04
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: human-ops (pilot run; no worktree — briefs land in PyAutoMind/batches/ by the human)
- prompt: active/autonomous_orchestrators_p4c_pilot_run.md
- epic: autonomous-orchestrators (phase 4c of 4a–4c)
- pre-check: open shadow tick on system python3.10, minimal env — 6 notify proposals, 0 spawns (2026-11-04)
- tier: judge — merge mode: human /prm

## pyautolens-ii-case-studies
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/147
- issued: 2026-11-12
- session: OpenAI Codex desktop
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/pyautolens-ii-case-studies
- repos:
  - autolens_workspace_developer: feature/pyautolens-ii-case-studies
- prompt: active/pyautolens_ii_case_studies.md
- coordination: human approved PyAutoLens/paper_jax/paper.md-only edits alongside magnification-maps-wiring; no library code changes
- next: validate JWST PSF/noise and export calibrated ALMA visibilities, then joint gradient check and bounded pilots
- tier: judge — merge mode: human /prm


## double-source-plane-review
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/640
- issued: 2026-11-12
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/double-source-plane-review
- repos:
  - PyAutoLens: feature/double-source-plane-review
  - autolens_workspace: feature/double-source-plane-review
- prompt: active/double_source_plane_review.md
- tier: judge; review PRs only, no merge
- next: human review of workspace #641 and PyAutoLens #831; no merge authorized
- prs: https://github.com/PyAutoLabs/autolens_workspace/pull/641 ; https://github.com/PyAutoLabs/PyAutoLens/pull/831

- heart-red-override:
  - authorization: I approve the development-only Heart RED override for #640. Commit, push and open both PRs for review, don't merge yet.
  - exact-red-reasons: PyAutoLens: on branch feature/double-source-plane-review (not main); PyAutoLens: 2 uncommitted source change(s); install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate)
  - gates: Fresh checks: syntax; unchanged executable AST and notebook code cells; approved draft parity except image path/trailing whitespace; identical approved images and valid local links; navigator/banner, search-memory, size and whitespace checks; focused Sphinx build with warnings treated as errors. No numerical/API changes. Full numerical/smoke suites were not rerun for this prose/assets-only delta; preceding stellar + dark matter PRs passed all 12 CI jobs on the same base, which is prior evidence rather than fresh testing.
