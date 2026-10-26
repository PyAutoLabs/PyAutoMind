# Workspace config + docs for corner-plot labels and latent plots (phase 3 of PyAutoFit#1709)

Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/autofit_workspace/issues/177
Type: docs
Target: workspaces
Repos:
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- HowToGalaxy
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: medium
Status: issued
Consequence: glance
Blocked-by: Published PyAutoGalaxy release containing merged #656; profile latent-output examples and executed Markdown validation remain.
Library-completion: complete/2026/10/latent-profile-declarations.md
Release-evidence: PyAutoFit 2026.10.23.1 is published/non-yanked and includes #1709 (verified 2026-10-26).
Filed: 2026-10-21

Remainder of `complete/2026/10/finish-pr-1709-corner-plots.md`. The library defaults cover the missing keys, so nothing breaks meanwhile.

- `config/visualize/plots_search.yaml` `nest:` add `corner_anesthetic_components`, `corner_anesthetic_latent` (false),
  `corner_anesthetic_latent_components`, with the library's comments.
- `config/output.yaml` add `latent_model_parameters: true`.
- `config/notation.yaml` `superscript:` comments: it now applies only to priors directly on an unnamed `Model`;
  named components are labelled by their path (`lens.bulge`, `source.pix.reg`).
- Contributor branches `feature/corner-plot-labels` on autofit/autogalaxy/autolens_workspace, HowToLens and HowToGalaxy may
  already carry these; land theirs if so.
- Release note: corner-plot labels change from class abbreviations to component paths (user-visible).

## Approved continuation — 2026-10-26

User request (verbatim): "ok do that" — approving completion of the remaining development and validation against merged Galaxy code, leaving shipping gated on publication.

Resume the five existing contributor branches. Verify their prose against current output paths, plot-only periodic recentering and actual component labels; make only necessary corrections. Regenerate changed notebooks using Hands, execute the affected curated Markdown examples with real sampling or verified completed real-run caches, inspect the latent output/figures, and refresh focused/smoke/review/PR evidence. Preserve all original claims and human merge authority; do not publish or merge these workspace PRs. Record any genuine execution blockers with evidence rather than calling smoke-generated output scientific validation.


## Pre-release preparation checkpoint — 2026-10-26

Approved intent remains: finish examples, generated Markdown and PR validation against merged local Galaxy; do not release or merge workspaces.

- Normal Fit latent cookbook completed. Galaxy imaging completed on full 100×100 data, 5,458 posterior samples, seven generated figures; visual labels and latent summaries verified.
- Twenty notebooks regenerated from canonical scripts. Fourteen edited Python files preserve executable AST; prose now distinguishes plot-only angle recentering and conditional `files/latent/samples.csv` output. Config review removed a duplicate Fit key and preserved CRLF/effective YAML values. Lens config-comment correction remains outstanding.
- Isolated fresh smoke: Fit 8 scripts + 2 notebooks and Galaxy 14 scripts + 2 notebooks passed. Other three suites not started; older 152-check result is not final continuation evidence. Validation copies and all outputs retained.
- Galaxy interferometer generator unexpectedly exited 143 (SIGTERM) while creating latent samples after sampling. Kernel reports parent exited; no Python traceback. Its 300-minute timeout had not elapsed; sender unknown. Checkpoint retained (`n_like=3350`, `explored=True`). No retry performed.
- Per ship-workspace failed-step rule, requested human approval to retry from checkpoint. Lens imaging was deliberately interrupted afterward with SIGINT (exit130) to leave no unattended render. Its checkpoint is retained; this is an operator stop, not an observed scientific failure. No new PR push, publication, merge or close-out performed.
- Resume: resolve retry decision; correct remaining Lens comments between renders; resume Galaxy interferometer and Lens imaging, then remaining four curated pages; run remaining three smoke suites; complete independent artifact review; update existing five contributor PRs and current-head CI evidence. Keep `release-gate: PyAutoGalaxy`.

Evidence root: `.worktrees/corner-plot-workspace-config/logs/continuation/` — `provenance.json`, `prose-code-proof.json`, `smoke-validation-summary.json`, `smoke-validation-equivalence.json`, `galaxy/imaging-evidence.json`, `galaxy/interferometer-interrupted.json`, renderer logs and `review/preliminary-review.md`. Workspace changes remain local in the existing claimed worktrees.

## Retry approval — 2026-10-26

User: "ok do that" — explicitly approves retrying the interrupted renders, completing remaining validation and updating the five existing PRs. No release or workspace merge authorized. Lens config-comment corrections now preserve parsed values; normal Lens imaging resumed from its checkpoint.
