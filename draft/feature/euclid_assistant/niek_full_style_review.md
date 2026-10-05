# Full Euclid style coverage and Niek manuscript review

Type: feature
Consequence: judge
Lane: local-dev

## Original request (verbatim)

In collaborator/niekpaper we have a paper which I want to apply the full Eulcid style guide type setting scan that lens/euclid_assistant does. I want you to reread through the cirtiera and docs to double check the project has them all built (e.g. we last did this with Fable but lets keep building on and improving the assistant). I want you to then apply it all to the niek paper. I want you to do then do a opus 5.5 review. and putting all missed content in the assistant. And then package it up as a zip for me to send back to the author

## Scope and plan awaiting approval

Target @euclid_assistant. Input is collaborator/niekpaper.zip (67 entries, paper/main.tex); preserve the original archive. Assistant checkout is clean main at 3a6f1ff; no existing task found in active/planned registries. Proposed branch: feature/niek-euclid-style-review. No manuscript or assistant source edits before approval and worktree setup.

1. Reread the full local Style Guide V4.0, PDD, template/macro assets, and relevant wiki pages. Build an item-level coverage record distinguishing implemented, manual, missing, and inapplicable criteria, with exact provenance. Correct stale workflow documentation; never infer full coverage from rule counts.
2. Improve rules/euclid_rules.yaml, supporting rule catalogues, src/euclid_assistant/lint/{checks,rule_engine,latex_scanner}.py as justified by gaps, matching wiki documentation, and targeted regression tests. Keep judgement-dependent checks manual and explicitly recorded. No invented policy for unavailable EC-PPD.
3. Extract a working manuscript copy, identify active includes and assets versus old drafts, run a baseline audit and LaTeX build, and create a persistent rule-linked changelog. Review prose, maths, units, notation, front matter, citations, figures, tables, links, and acknowledgements against the full checklist. Preserve scientific values/results; defer substantive ambiguities to the author.
4. Apply supported style corrections to active source files. Recompile and inspect rendered pages as well as source. Record every applied/deferred finding as work proceeds.
5. Obtain an independent Opus 5.5 review of the corrected paper and source-to-assistant coverage; verify exact model availability and report any limitation. Feed supported omissions back into assistant rules/docs/tests and the paper, then rerun relevant validation.
6. Run make test, regenerate generated coverage/Vale assets where affected, and compare baseline/final audits and compile logs. Package corrected LaTeX, required assets, compiled PDF if successful, changelog, review report, author questions, and build instructions into collaborator/niekpaper_euclid_reviewed.zip. Validate archive integrity and rebuild from the package. Keep internal sources and unpublished manuscript out of assistant commits.

Assistant improvements proceed through start_workspace/ship_workspace. Tier: judge — merge mode: human /prm. The author ZIP is a local deliverable and is not sent automatically.

## Initial evidence

- Existing generated coverage matrix lists 47 rules; manual bibliography and serial-comma checks remain, and figure bitmap detection is documented as noisy.
- audit-paper.md contains stale claims that CLI/Makefile are absent, despite their implementation.
- Input already loads euclid.sty and uses the A&A longauth class. Old section files also exist in the archive, so the active include graph must define review scope.
- Heart entry verdict is STALE (exit 1); detailed ecosystem warnings remain a shipping consideration.
