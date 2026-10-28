
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## rectangular-28sq-profiling-rows
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/468
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/rectangular-28sq-profiling-rows
- repos:
  - autolens_inference: feature/rectangular-28sq-profiling-rows
- released-claims: autolens_profiling (#470 merged a1a4ccf1), PyAutoPulse (#80 merged 5474e3cb) — branches kept in the worktree until close-out
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/49 OPEN 2026-10-27 (size_match 32/0)
- prompt: active/rectangular_28sq_profiling_rows.md
- epic: likelihood-lifecycle
- heart-red-override: authorized by live human 2026-10-26 "I approve of the override" (this task incl. RAL jobs); reasons + gates recorded at ship
- scope-add: HUMAN 2026-10-26 chose "Yes, small Pulse PR first" (option text: "Same RED override extended to it. Ships before the profiling rows.") — PyAutoPulse one-current-per-key adds regime
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/80 MERGED 2026-10-26 5474e3cb via human /prm (regime in @3 one-current key)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/470 MERGED 2026-10-27 a1a4ccf1 via human /prm (rect28 rows, RAL 413044/413046 8/8); task stays open — NEXT autolens_inference size_match leg (branch has no commits yet); witness gap jax_cpu_dense + light_fixed unmeasured

## likelihood-lifecycle-p2b-interferometer
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/469
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2b-interferometer
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2b-interferometer
- prompt: active/likelihood_lifecycle_p2b_interferometer_campaign.md
- epic: likelihood-lifecycle
- heart-red-override: live human 2026-10-26 "Yes, authorise for 2b" (PRs + planned RAL batches)
- batch-go: HUMAN 2026-10-27 "do the next tasks to the point interferometry is hopefully running" = go for batch 0
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/471 OPEN 2026-10-27 (PR A, dff89226; Heart GREEN; judge → human /prm)
- batch0: chained on RAL 2026-10-27 (scratch/p2b_batch0_submit.log; CPU 0-13 + refs 0-1 on ral, A100 0-9%2) from branch head dff89226

## lenstwin-p0-twins-core
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/671
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/803
- issued: 2026-10-28
- session: Claude Code remote (web) session_016nhQ8MoEbXHfUW3wiH58VY
- location: remote session clones /home/user/pyautogalaxy and /home/user/pyautolens on feature/lenstwin-p0-twins-core (from origin/main a108092 / a8eb094); no task worktree
- status: library-shipped, awaiting-merge (0A merged 2026-10-28; 0B red on a pre-existing pytest-9 failure)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/672
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/804
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/672
- epic: lenstwin (phase 0; ledger draft/feature/autolens/lenstwin_epic.md)
- prompt: active/lenstwin_p0_twins_core.md
- repos:
  - PyAutoGalaxy: feature/lenstwin-p0-twins-core
  - PyAutoLens: feature/lenstwin-p0-twins-core
- summary: |
    Phase 0 of lenstwin issued 2026-10-28 via /start_dev → /create_issue: 0A PyAutoGalaxy#671
    (grid-integrated aperture mass for any convergence object; Basis.mass_basis_from) and
    0B PyAutoLens#803 (autolens/twins/: ObservationSetup, ReferenceModel, Twin, SimulatedTwin,
    TransformationRecord, transform.Identity; seeded simulation, observed noise map by default;
    twin.json provenance). Library first: 0A merges before 0B; 0B may develop against the
    same-named PyAutoGalaxy branch. Rulings R1/R2 taken; R3–R8 untouched. Consequence: judge
    (human /prm). Next: /start_library lenstwin-p0-twins-core, 0A first; implementation on the
    execution tier (Opus), plan and judgment in the main session.
    2026-10-28: 0A shipped to PyAutoGalaxy#672 (pending-release; 1390 passed / 7 skipped;
    Heart STALE, environment reasons only). 0B shipped to PyAutoLens#804 (pending-release; 946 passed,
    7 pre-existing point/test_dataset.py failures under pytest 9.2, identical on the clean branch).
    Both PRs stop at PR-open (Consequence: judge); merge order 0A then 0B via human /prm.
    /prm 2026-10-28: PyAutoGalaxy#672 MERGED (b072e4d; Tests + Docs green on b81951a; not frozen).
    PyAutoLens#804 NOT merged: unittest-nojax red with the 7 pre-existing point/test_dataset.py
    failures (pytest 9 nested approx; unpinned pytest; main's last run predates pytest 9.2);
    standing-down comment posted; fix queued as its own task. Re-run /prm once #804 is green.
    2026-10-28 later: the fix exists as 2b063ca on unmerged branch ccr-b1080ef2-0tcwow (no PR);
    cherry-picked onto the 0B branch as 1d430dc and pushed; CI re-running. Re-run /prm when green.
