# HowTo* validation must run scripts/simulator/ before the chapters

Type: bug
Target: workspaces
Repos:
- HowToLens
- HowToGalaxy
- HowToFit
- PyAutoBuild
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

The HowTo* smoke surface passed for months only because releases had
force-committed simulated datasets into the repos (`pre build` commits
2026-05-01/14/29 in HowToLens); PyAutoBuild#151 purged them (2026-07-13,
correctly). The tutorials load data via `Imaging.from_fits` from paths like
`dataset/imaging/simple__no_lens_light/` and **never simulate for
themselves** — a `scripts/simulator/` directory exists in each HowTo repo but
nothing in the validation path runs it before the chapters. Result: the
2026-07-15 `workspace-validation.yml mode=smoke` run failed ~30 HowTo*
scripts/notebooks with `FileNotFoundError: dataset/.../data.fits`
(run 29418019889). This is a **pre-existing falsehood newly revealed, not a
regression** — see `PyAutoHeart/docs/readiness_evidence_audit.md` §3
(campaign PyAutoBuild#155 Phase 2, issue PyAutoHeart#83).

Fix direction (design first — the open decision is WHERE the stage runs):
- (a) the validation runner (PyAutoBuild `run_all` / `workspace-validation.yml`)
  executes each HowTo repo's `scripts/simulator/*` before its chapters, or
- (b) a per-repo bootstrap (conftest-style / should_simulate-on-missing in the
  tutorials' load path).
Do NOT restore committed datasets (that re-opens #126), and do not mark the
failing tutorials no_run (that hides the surface the gate exists to validate).
Whichever side wins, the validation report should record the choice so the
smoke surface's denominator is comparable across runs (audit §5.3).

<!-- filed 2026-07-16 from the Phase 2 evidence-chain audit (finding 3 remediation); satellite of the build-chain umbrella -->
