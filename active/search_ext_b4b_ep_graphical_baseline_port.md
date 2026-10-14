# `@autofit_profiling` B4b: port the EP / graphical-model baselines and the analytic benchmark, reproduce the committed numbers

Type: feature
Target: autofit_profiling
Repos:
- autofit_profiling
- PyAutoPulse
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: B4b
Witness: `scripts/gaussian_1d_ep/{ep,graphical}/baseline.py` (names per AGENTS.md layout) regenerate the N3/N10/N30 cells from the seeded simulator and write `results/**/*.json` records (`schema: autofit-profiling-breakdown` or a generalised schema the exporter reads) carrying host, device, backend, precision, PyAutoFit sha and the sanity verdict; the reproduced N3 and N10 wall times are within the epic's `runtime-drift-2x-1ms` policy of the committed `autofit_workspace_developer/{ep,graphical}/profiles/baseline.json` numbers on the same host as B4a (`DESKTOP-H143S82`, WSL2), and every reproduced `truth_log_likelihood_sum` matches the committed value exactly (-128.397 / -472.253 / -1500.56); the N30 cells are ported with their committed `sanity_pass: false` verdict reproduced, not hidden; the analytic benchmark (`autofit_workspace_test/scripts/graphical/analytic_{autofit,ep_minimal,gaussian,gaussian_collapse,gaussian_priors,reference}.py`) gains a profiling cell that records the closed-form vs minimal-EP vs graphical agreement and the banked `sigma_q95 = 12.18` (seed 0, N=5) as a `runtime` + correctness record; `build_catalogue.py --check --validate-with ../PyAutoPulse` passes with the new `setup_id`s on the existing `runtime` and `memory` axes (no registry row, no contract bump); the Pulse `fit` instance re-ingests (receipt + snapshot refreshed on the Pulse branch after Pages is live) and the board shows the EP and graphical cells; `wiki/campaigns/` gains the B4b page with the reproduction table.
Review-minutes: 30
Unattended: needs-slicing
Filed: 2026-10-14
Issued: 2026-10-14

Authority: epic report "#### B4" B4b scope ("port `autofit_workspace_developer/{ep,graphical}` plus the analytic benchmark, reproducing the committed baselines on the release-sweep host pin; its own research-grade reproduction task"), D17; survey `04_inference_profiling_infra.md` §host pin (lines ~160–170); Pulse task `tasks/autofit_profiling_bootstrap.md` lines 83, 107–109, 131; B4a record `complete/2026/10/search-ext-b4a-breakdown-exporter.md`.

**Decision to flag (decide-and-flag):** the release-sweep host pin in the epic is `autolens_profiling/hpc/release_sweep.conf` (`euclid-ral-gpu-2`, an A100 node) and does not fit these CPU Dynesty runs; nothing on the fit side has a pin. B4b pins to the SAME laptop host B4a used (`DESKTOP-H143S82`, WSL2, recorded via `platform.node()` in every record) so Pulse's same-host comparison rule (AGENTS.md:147) pairs the new records with B4a's, and states the pin in `wiki/campaigns/` and the catalogue LIMITATIONS. Cross-machine reproduction on RAL is a later campaign.

Facts from the survey (do not re-derive): `ep/` and `graphical/` share a byte-identical `simulator.py` (`default_rng(seed=dataset_index)`, 30 datasets), `fit.py` (EP: `factor_graph.optimise()` with DynestyStatic + Laplace cavity, max_steps 5; graphical: joint DynestyStatic), `util.py`, `sanity.py` (max-LL rule, 5.0 nats per dataset; EP skips it), `config/`. Committed profiles: `N3/N10/N30_summary.json`, `N10_cprof_summary.json`, `N10_hotspots.txt`, `postfix_*`, aggregated by `aggregate_profiles.py` into `baseline.json`. Baselines: EP 251.9 / 566.9 / 1758.7 s (N30 sanity FAIL); graphical 22.8 / 50.7 / 132.8 s (N30 sanity FAIL). The hotspots files contain machine-specific absolute paths — strip them in the port (AGENTS.md rule). The exporter `scripts/misc/tooling/build_catalogue.py` reads only `results/**/*.json` with `schema == "autofit-profiling-breakdown"`; generalise the reader or add a sibling schema rather than forcing EP rows into the breakdown shape. The analytic parity scripts parked `NEEDS_FIX` (fixes D1–D6 pending) are recorded as parked, not run.

Shape: PR 1 autofit_profiling (port + results + campaign page + exporter generalisation; lint green) → PR 2 PyAutoPulse (fixture refresh, campaign `autofit` next-line, receipt/snapshot after Pages is live, as B4a did). The developer-tier `ep/` and `graphical/` directories are NOT deleted here (a separate Gut-backed glance task after the port merges, as `searches/nss` and `searches_minimal` were). PyAutoFit pinned at main (≥ df6d218f1) for the reproduction; record the sha.
