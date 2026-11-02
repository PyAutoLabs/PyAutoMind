## likelihood-lifecycle-p4c-runners
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/54
- completed: 2026-11-02
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/55 (4c-0 tooling, 20d297dd)
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/56 (4c-1 imaging mge/delaunay_nn, interferometer ×3, datacube; ba27f95b)
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/57 (4c-3 point ×2, cluster ×2, weak; 4186c045)
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/58 (4c-2 group ×3, multi_galaxy ×3, multi_dataset; a24e993c)
- Every one of the 20 catalogue likelihoods now has a validation runner (one reference instrument, Optimal setups only; human rulings 2026-11-02: workspace pipeline + profiled preset; 4c-0 first then families in parallel). validation_p4 emits 70 submits, all check_submits-clean; 470 tests. No compute.
- Departures recorded on each PR (interferometer/mge closed MGE-style; positive-only solver kept on; search priors on point/cluster/weak; cluster profiled parameterisation; workspace lens-light MGE sizes on group/multi_galaxy; multi_dataset uniform over-sampling).
- Follow-ups: PyAutoLens weak plotter fails under JAX (ArrayImpl has no grid); trim the 5-day containment --time on 4c-1 legs at the compute go.
- Lessons: three families built in parallel each generalised the shared generator their own way; rebasing them onto one another and adopting the first-merged hooks kept one mechanism per concern. Run the exporter after every commit (dashboard freshness records the source revision). After a WSL restart, ssh/git need SSH_AUTH_SOCK pointed at the human-started agent.

## Original prompt

# Likelihood lifecycle phase 4c: Nautilus validation runners for the 19 remaining likelihoods

Type: research
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- profiling
- inference
Difficulty: large
Autonomy: supervised
Priority: high
Status: issued
Consequence: judge
Witness: autolens_inference main carries a runner (a leaf under scripts/<dataset_type>/<variant>/validation/) for each of the 19 likelihoods. Each writes stages.json under results/<dataset_type>/<variant>/<instrument>/validation/ that the exporter resolves to its likelihood and setup_id and pairs with a profiling runtime record. validation_p4.py emits their Optimal-setup legs (one reference instrument each), and every submit passes check_submits. Lint and tests are green. No compute.
Review-minutes: 45
Unattended: never
Epic: likelihood-lifecycle
Phase: 4
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/54
Issued: 2026-11-02

## Likelihoods (reference instrument)

| Group | Likelihoods (instrument) |
|---|---|
| imaging | mge, delaunay_nn (hst) |
| interferometer | rectangular, delaunay, mge (sma) |
| datacube | delaunay (sma) |
| group | rectangular, delaunay, mge (euclid) |
| multi_galaxy | rectangular, delaunay, mge (hst) |
| multi_dataset | delaunay (hst) |
| point source | point_source_source/source_plane, point_source_image/image_plane (simple) |
| cluster | source_plane, image_plane (simple) |
| weak | isothermal (simple) |

## Human rulings (2026-11-02)

- "now do runners and everything for all other dataset types".
- Runner model: "Workspace pipeline + profiled preset". Mirror the autolens_workspace pipeline's stage chain, with the profiled cell's mesh, regularization and size swapped into the stages whose likelihood is the one timed. Where no workspace pipeline exists, build the nearest analogue.
- Execution: "4c-0 first, then families in parallel".
- Already in force: one reference instrument per likelihood; Optimal setups only; day zero may span versions.

## Plan

### 4c-0, shared tooling (one PR)

- **Exporter and catalogue:**
  - resolve the likelihood from the row's own variant (mge, delaunay_nn, point, cluster, weak), not only rectangular/delaunay;
  - extend the setup-id grammar to the `na`, `nufft` and `wtilde` setups;
  - pair no-inversion stages (MGE linear solve, point, cluster, weak) with their own likelihood's profiling record instead of skipping them;
  - fix delaunay_nn filing in validation_layout.
- **Runner:** split `_runner.py` into a shared result core plus per-family stage builders; add mesh options `delaunay_nn` and `rect_35`.
- **Simulators:** port the group, multi_galaxy, cluster and weak simulators byte-equivalently from autolens_profiling.

### Families (three PRs in parallel, after 4c-0)

- **4c-1:** imaging mge and delaunay_nn; interferometer ×3; datacube.
- **4c-2:** group ×3; multi_galaxy ×3; multi_dataset.
- **4c-3:** point ×2; cluster ×2; weak.

Each family adds its Optimal-setup legs to validation_p4.py. Compute runs only on the human's go per batch.

## Context

The survey (2026-11-02) of the exporter contract and the per-likelihood pipelines, datasets and models is quoted in the issue.
