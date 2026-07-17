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

## Evidence + decided design (2026-07-17) — corrects two claims above

Measured before designing; **two claims in the original filing were wrong**:

1. **"a `scripts/simulator/` directory exists in each HowTo repo"** — the name
   differs per repo: HowToLens uses `scripts/simulator/` (singular, 5 sims);
   HowToGalaxy and HowToFit use `scripts/simulators/` (plural). (An interim
   "HowToGalaxy/HowToFit have zero simulators" reading was also wrong — a
   truncated `ls | head -6` hid the dir. Third instrument-truncation error of
   this campaign; see PyAutoBrain docs/agent_failure_modes.md F2.)
2. **"nothing in the validation path runs it before the chapters"** — true but
   for a mechanism that rules out the obvious fix. Locally,
   `PyAutoBuild/autobuild/run_all.py::run_workspace` iterates
   `sorted(scripts/*)`, so `chapter_*` runs before `simulator*` (producer
   last). **But in the cloud — the path that actually produced the 30
   failures (run 29418019889) — `workspace-validation.yml` shards ONE JOB PER
   `scripts/<directory>`, each with its own fresh clone.** The simulator
   shard's `dataset/` is discarded at job end and never reaches the chapter
   shards. Ordering cannot fix parallel isolated jobs, so fork (a) "the
   runner runs the sims before the chapters" is **dead**.

**Decided: fork (b), via the idiom the organism already has.**
`aa.util.dataset.should_simulate(dataset_path)` exists and is documented as
"the workspace auto-simulation pattern":

    if aa.util.dataset.should_simulate(dataset_path):
        subprocess.run([sys.executable, "scripts/.../simulator.py"], check=True)

**autolens_workspace calls it in 35 scripts; HowToLens/Galaxy/Fit call it in
ZERO** — the HowTo repos are the outlier, which is exactly why their smoke
surface was the one living on leaked release artifacts. The fix is to adopt
the existing lever, not to build a new runner stage (reach-for-the-lever;
delete-the-trap).

Scope (measured): ~30 tutorials across 3 repos load via `Imaging.from_fits`
and need the 3-line block above ahead of the load, each pointing at its own
repo's simulator path (mind the singular/plural split). This is **teaching
prose — judgment tier, not execution tier** (WORKFLOW.md tutorial split), and
it fixes the Heart `test_run` leg's real failures rather than hiding them.

Deliberately NOT doing: the local `run_all` ordering tweak — it fixes only
the local path and is obviated by fork (b) (a self-simulating script does not
care about directory order). Building it would be machinery the real fix
deletes.

Follow-up worth one line in its own prompt: normalise `simulator/` vs
`simulators/` across the three repos (inconsistent siblings).
