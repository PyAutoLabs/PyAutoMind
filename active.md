# Active Tasks

## witt-wynne-projection
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/510
- issued: 2026-08-28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/witt-wynne-projection
- repos:
  - autolens_workspace: feature/witt-wynne-projection

## cmap-magma-default
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/509
- prompt: active/cmap_magma_default.md
- issued: 2026-08-28
- status: library-shipped, workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/cmap-magma-default
- classification: combined (library first, then the Euclid pipeline workspace)
- epic: euclid-dr1-prep (phase 0 of 10; gates nothing, gated by nothing)
- repos:
  - PyAutoArray: feature/cmap-magma-default
  - euclid_strong_lens_modeling_pipeline: feature/cmap-magma-default
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/510
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/42
- commit: c8fe47f35e37f4ea8a51303ece0ab5f708def460 (PyAutoArray); c7c3941a3ccd5a1a28c5327cd1ef09be004e8fd0 (euclid pipeline)
- tests: 1337 passed, 0 failed (test_autoarray, 2026-08-28); euclid PR is config+docs only, no scripts changed
- merge-gate: library-first — PyAutoArray#510 must merge before euclid#42
- heart-ack: Heart RED at ship time for an unrelated reason, verbatim: "release validation
  FAILED (stage integrate)". YELLOW, also unrelated, verbatim: "workspace validation not
  passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py,
  autolens_test scripts/imaging/rectangular_mge_rtu.py)"; "manifest drift: session-start hooks
  (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml". PR opened under the standing human
  authorisation recorded 2026-08-28 ("open prs under red and merge i acknowledge"); NOT merged.
