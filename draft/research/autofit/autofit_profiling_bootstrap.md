# autofit_profiling: bootstrap the repo + general PyAutoFit profiling epic

Type: research
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_profiling
Themes:
- profiling
- graphical-ep
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Campaign: research/graphical_ep/ep_campaign.md (Phase 6)
Filed: 2026-08-19 (backfilled from git)

## Why

For the IC50 and cosmology use cases the individual Factor fits will end up
fast; the bottleneck becomes PyAutoFit itself — wrapping up a fit on one
factor, writing its output, starting the next, building the cavity
distributions. The 2026-07 scoping baselines already show this shape: EP is
~11× slower than graphical at every N, with per-factor visualisation alone at
~48% of EP runtime and `scipy.stats.truncnorm` prior transforms at 25–38%
(`research/graphical_ep/ep_scoping.md`, `graphical_scoping.md`). Slowdowns in
`non_linear/` (priors, paths, output) accumulate per factor fit and *become*
the EP bottleneck — so PyAutoFit needs a general profiling assessment, not
just an EP one.

## Deliverable 1 — the `autofit_profiling` repo

A new GitHub repo mirroring `autolens_profiling`'s responsibility, but for
all things PyAutoFit. **Repo creation is human-gated: confirm interactively
with James before creating anything on GitHub.** Seed it by porting the
existing baseline packages from `autofit_workspace_developer/` (`ep/`,
`graphical/`, and the analytic benchmark once
`research/graphical_ep/analytic_gaussian_benchmark.md` ships) so results,
harnesses and hotspot files live in one place with committed history, the way
autolens_profiling does for likelihoods.

## Deliverable 2 — two epics, sequenced (created at start_dev time, one at a
time — never bulk-issued)

1. **General PyAutoFit profiling** (first): a full profiling assessment of a
   single `search.fit` — prior transforms, `non_linear` wrapper overhead
   (paths setup, samples-to-CSV, visualisation, latent samples,
   search-internal cleanup), output I/O — on a fast likelihood so the
   overhead has nowhere to hide. Ranked findings filed as one-PR prompts.
2. **EP-loop profiling** (second, follows on): the EP-specific overhead —
   cavity construction, message updates, `factor_graph.optimise`
   orchestration — building directly on the ranked sub-task list already in
   `ep_scoping.md` (viz suppression, truncnorm fast path, folder-cleanup
   skip, orchestration cProfile, parallel local fits, sampler reuse). Most
   per-fit wins from epic 1 multiply by M·N under EP, which is why epic 1
   lands first.

## Acceptance

- Repo exists with the ported baselines reproducing their committed numbers.
- Epic 1 issue open with a measured, ranked bottleneck table for a single
  search.fit; epic 2 issue opened only after epic 1's top findings ship.
