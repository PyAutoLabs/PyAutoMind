## contents-block-bullets
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/138
- completed: 2026-05-08
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_workspace/pull/139 (lead, 199 scripts)
  - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/64 (98 scripts)
  - https://github.com/PyAutoLabs/HowToLens/pull/9 (37 scripts)
  - https://github.com/PyAutoLabs/HowToGalaxy/pull/6 (21 scripts)
  - https://github.com/PyAutoLabs/autofit_workspace/pull/54 (1 script)
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/83 (1 script)
  - https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/36 (1 script)
  - https://github.com/PyAutoLabs/autofit_workspace_test/pull/25 (1 script)
- repos: autolens_workspace, autogalaxy_workspace, autofit_workspace, HowToLens, HowToGalaxy, autolens_workspace_test, autogalaxy_workspace_test, autofit_workspace_test
- notes: |
    359 workspace tutorial scripts had their `__Contents__` blocks
    converted from plain `**Section:**` lines into Markdown list bullets
    (`- **Section:**`). Without bullet markers GitHub and JupyterLab
    collapsed the index into a single paragraph in the generated .ipynb's
    first markdown cell — the fix is text-only inside top-level module
    docstrings.

    HowToFit had nothing to ship — its 14 __Contents__ files were
    already bulleted (someone fixed them earlier, possibly the same
    person who shipped the ic50_workspace exemplar at 4cde480).

    Three rewrite-tool bugs were caught during dry-run before any PR
    opened — worth knowing for the next docstring-mass-rewrite tool:
    1. CRLF normalization (Python's read_text/write_text silently
       strip CRLF, would have produced 10K-line bogus diffs in the
       autofit_workspace files that use CRLF). Use read_bytes /
       write_bytes and detect/preserve the original eol byte-for-byte.
    2. Docstring-close `"""` mis-indented as a bullet continuation
       line. Terminate the contents-block scan at any line starting
       with `"""` or `'''`.
    3. Prose intro between `__Contents__` and the first bullet
       mis-indented as a continuation. Skip prose-intro lines until
       the first `**` or `- **` is found, then process from there.

    Visual confirmation via ipynb-py-convert on
    autolens_workspace/scripts/point_source/simulator.py: first
    markdown cell renders as a proper bulleted list.

    Notebooks were deliberately NOT regenerated in this PR set — the
    next /pre_build will pick them up cleanly.

    Out of scope (per the original prompt): same paragraph-collapse
    risk may bite `__Model__` blocks, `Steps`/`Notes`/`Outputs` blocks
    in workspace simulators. Not addressed without a concrete broken
    example.
