## howto-paired-review
- issue: https://github.com/PyAutoLabs/HowToLens/issues/103
- completed: 2026-10-31
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/104
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/93
- summary: Human-reviewed HowToLens Tutorials 0–2 and HowToGalaxy Tutorials 0–1, including canonical scripts, generated notebooks and catalogues. Tutorials 3–5 were deliberately left untouched for the human's larger rewrite.

### Accepted changes
Corrected grid rotation and elliptical/circularised radius conventions, Sérsic intensity normalization, radial sampling, plotting API usage and unit explanations. Lens Tutorial 2 now shows both the schematic and COSMOS-Web Ring image, uses introductory lensed-image terminology, and adds a central source-plane zoom followed by grouped coloured mappings. Reduced-deflection discussion is deferred to Tutorial 3.

### Validation and authorization
Human authorized fixes, Heart RED override and /prm in the same live invocation. Exact readiness reason: `release validation FAILED (stage integrate)`. No release or failed-check bypass.
Local Galaxy suite: 32 passed. Local Lens suite: 49 passed plus the corrected Tutorial 2 focused retest; final-commit GitHub smoke passed on Python 3.12 and 3.13 in both repositories. Each PR passed all 3 workflow runs and all 8 jobs. Five notebooks structurally valid and code-equivalent to source excluding setup injection; catalogues and path/banner checks passed. Actual PyAutoLens mappings and zoom rendered and visually inspected.

### Follow-up
The continuing paired-review prompt remains active in intent under draft/docs/howtolens/tutorial_correctness_and_howtogalaxy_parity.md. The user will revise Tutorials 3–5 before the next five-block editorial review; no Tutorial 3 proposal was applied. See draft/docs/howtolens/paired_tutorial_review_resume.md for current entry point.

### Evidence
Issue #103 and both PRs retain validation details. Local logs and CI snapshots: /home/jammy/Code/PyAutoLabs/scratch/ship/. Human review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/howto_paired_review_ship_2026-10-31/. Actual figures: /mnt/c/Users/Jammy/Workspace/Science/scratch/howtolens_mappings_2026-10-31/.

Merge receipts: HowToLens e986a4ae89c840fe2ef2f7f01c4dd07c75147247; HowToGalaxy ead53e6d736dcf302b93d1d5b54486dd81f80352. Both task branches are ancestors of origin/main.

## Original prompt

# Ship paired introductory tutorial review

Issued: 2026-10-31
Issue: https://github.com/PyAutoLabs/HowToLens/issues/103
Type: docs
Primary target: @HowToLens
Also: @HowToGalaxy

Ship the accepted source review of HowToLens Tutorials 0–2 and HowToGalaxy Tutorials 0–1, with generated notebooks and catalogues. Tutorials 3–5 are outside this phase; the human will rewrite them before continuing the review.

Human: “I approve you to prm and override heart RED”.
Exact Heart RED reason: `release validation FAILED (stage integrate)`.
No failed-test/CI bypass, force merge, release or release rehearsal is authorized.

Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howto-paired-review
Both branches: feature/howto-paired-review

Source syntax/diff checks and notebook structural validation passed. Runtime environments are being prepared using Heart's isolated-environment functions and CI install recipes. Runtime results and PR links will be added before shipping.

Continuing review and earlier decisions: draft/docs/howtolens/paired_tutorial_review_resume.md and draft/docs/howtolens/tutorial_correctness_and_howtogalaxy_parity.md.

## Validation outcome

## Shipping validation — blocked by script failures

Human authorization: “I approve you to prm and override heart RED”.
Exact Heart reason: `release validation FAILED (stage integrate)`. The override does not waive failed script checks.

| Repository | Passed | Failed |
|---|---:|---:|
| HowToLens | 48 | 2 |
| HowToGalaxy | 31 | 1 |

Five notebooks generated with PyAutoHands and structurally validated; notebook code matches source apart from standard setup injection. Both catalogues regenerated; both navigator path/banner checks passed.

### HowToLens: tutorial_0_visualization.py
```text
Traceback (most recent call last):
  File "/home/jammy/Code/PyAutoLabs/organs/PyAutoHands/autohands/smoke_dependencies.py", line 101, in <module>
    main()
  File "/home/jammy/Code/PyAutoLabs/organs/PyAutoHands/autohands/smoke_dependencies.py", line 97, in main
    runpy.run_path(str(path), run_name='__main__')
  File "<frozen runpy>", line 287, in run_path
  File "<frozen runpy>", line 98, in _run_module_code
  File "<frozen runpy>", line 88, in _run_code
  File "/home/jammy/Code/PyAutoLabs/.worktrees/howto-paired-review/HowToLens/scripts/chapter_1_introduction/tutorial_0_visualization.py", line 121, in <module>
    aplt.plot_array(
TypeError: plot_array() got an unexpected keyword argument 'figsize'
```

### HowToLens: tutorial_2_ray_tracing.py
```text
Traceback (most recent call last):
  File "/home/jammy/Code/PyAutoLabs/organs/PyAutoHands/autohands/smoke_dependencies.py", line 101, in <module>
    main()
  File "/home/jammy/Code/PyAutoLabs/organs/PyAutoHands/autohands/smoke_dependencies.py", line 97, in main
    runpy.run_path(str(path), run_name='__main__')
  File "<frozen runpy>", line 287, in run_path
  File "<frozen runpy>", line 98, in _run_module_code
  File "<frozen runpy>", line 88, in _run_code
  File "/home/jammy/Code/PyAutoLabs/.worktrees/howto-paired-review/HowToLens/scripts/chapter_1_introduction/tutorial_2_ray_tracing.py", line 454, in <module>
    aplt.plot_grid(
TypeError: plot_grid() got an unexpected keyword argument 'extent'
```

### HowToGalaxy: tutorial_0_visualization.py
```text
Traceback (most recent call last):
  File "/home/jammy/Code/PyAutoLabs/organs/PyAutoHands/autohands/smoke_dependencies.py", line 101, in <module>
    main()
  File "/home/jammy/Code/PyAutoLabs/organs/PyAutoHands/autohands/smoke_dependencies.py", line 97, in main
    runpy.run_path(str(path), run_name='__main__')
  File "<frozen runpy>", line 287, in run_path
  File "<frozen runpy>", line 98, in _run_module_code
  File "<frozen runpy>", line 88, in _run_code
  File "/home/jammy/Code/PyAutoLabs/.worktrees/howto-paired-review/HowToGalaxy/scripts/chapter_1_introduction/tutorial_0_visualization.py", line 120, in <module>
    aplt.plot_array(
TypeError: plot_array() got an unexpected keyword argument 'figsize'
```


Diagnosis: public autolens.plot/autogalaxy.plot wrappers do not expose the underlying autoarray.plot figsize/extent/indexes options. Tutorial 0 can size an explicit Matplotlib axes; Tutorial 2 can call autoarray.plot.plot_grid for extent/index groups. No library change is required. Corrections are not applied during the failed ship run.

No tutorial commit, push, PR or merge. Both worktrees remain intact. Tutorials 3–5 remain untouched.

## Authorized corrections — 2026-10-31

Human: “Fix those plotting errors, rerun the tests and then prm everything. I approve the fixes and the Heart RED override.”

Both Tutorial 0 scripts now size a Matplotlib figure explicitly and pass `ax` to `aplt.plot_array`. HowToLens Tutorial 2 imports `autoarray.plot as aaplt` for extent/indexes-enabled grid plots. Smoke profile preserves that lesson's 101x101 teaching grid; the full-grid mapping retest passed. The actual runtime mapping/zoom figures were rendered and visually inspected. Generated notebooks are structurally valid and code-equivalent to source (excluding standard setup injection). Full suite reruns are finishing before PR-open.

PRs: https://github.com/PyAutoLabs/HowToLens/pull/104 (14b6a08) and https://github.com/PyAutoLabs/HowToGalaxy/pull/93 (489d7ae). Local corrected-script evidence passed; final-head CI pending.
