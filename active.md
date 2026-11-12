
## autonomous-orchestrators-p4c
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/574
- issued: 2026-11-04
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: human-ops (pilot run; no worktree — briefs land in PyAutoMind/batches/ by the human)
- prompt: active/autonomous_orchestrators_p4c_pilot_run.md
- epic: autonomous-orchestrators (phase 4c of 4a–4c)
- pre-check: open shadow tick on system python3.10, minimal env — 6 notify proposals, 0 spawns (2026-11-04)
- tier: judge — merge mode: human /prm


## stellar-dark-review
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/638
- issued: 2026-11-12
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/stellar-dark-review
- repos:
  - PyAutoLens: feature/stellar-dark-review
  - autolens_workspace: feature/stellar-dark-review
- prompt: active/stellar_dark_review.md
- tier: judge; review PRs only, no merge
- coordination: same-session approved separate documentation worktree alongside magnification-maps-wiring
- next: human review of workspace #639 and PyAutoLens #830; no merge authorized
- prs: https://github.com/PyAutoLabs/autolens_workspace/pull/639 ; https://github.com/PyAutoLabs/PyAutoLens/pull/830

- heart-red-override:
  - authorization: I approve the development-only Heart RED override for #638. Commit, push and open both PRs for review, don't merge yet.
  - exact-red-reasons: PyAutoLens: on branch feature/stellar-dark-review (not main); PyAutoLens: 2 uncommitted source change(s); install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate)
  - gates: Fresh checks passed: syntax; unchanged executable AST and notebook code cells; approved draft parity apart from image path/trailing whitespace; image identity and local links; navigator/banner lint; search-memory check; size guard; whitespace; focused Sphinx build with warnings treated as errors. No numerical/API changes. Full numerical and smoke suites were not rerun for this prose/assets-only delta. The preceding potential-correction PRs passed all 12 CI jobs on the same base; that is prior evidence, not fresh testing.
