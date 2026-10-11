# Nerves Markdown icon removal

Epic: scientist-adoption-pilot

Merged https://github.com/PyAutoLabs/PyAutoNerves/pull/201; issue #200 closed. Removed only the dashboard.md HTML utility anchor. Generated Markdown remains available. No packaged source changed or package release required.

Validation: 241 tests; exact-head Actions run 38165996885, all 3 matrix jobs passed. Merge 7f3055b contains head af6eff4. Heart freeze clear. Human /prm authorized merge and close-out.

Local validation evidence archived at `tmp/nerves-markdown-link/`.

Publication: https://github.com/PyAutoLabs/PyAutoNerves/actions/runs/38167286532 succeeded; live HTML verified. Task worktree removed after evidence archival; active claim released.

## Original prompt

# Remove Nerves Markdown utility link

Type: bug
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/200
Consequence: judge
Epic: scientist-adoption-pilot

## Original request

for nerves also remoe the icon linking to the markdown board

## Plan

Remove the dashboard.md utility anchor from @PyAutoNerves scripts/board.py HTML only. Preserve generated Markdown output. Run existing board tests; adjust any obsolete link expectation. Tier: judge — human /prm.
