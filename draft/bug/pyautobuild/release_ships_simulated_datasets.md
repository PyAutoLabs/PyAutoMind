# Release pipeline force-commits simulated workspace datasets; add missing should_simulate guards, purge committed sim data, stop the -f leak

Type: bug
Target: PyAutoBuild
Repos:
- PyAutoBuild
- PyAutoHeart
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- HowToLens
- HowToGalaxy
- HowToFit
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

Release pipeline force-commits simulated workspace datasets against .gitignore; the real defect is example scripts that load simulated data WITHOUT the should_simulate() auto-simulate guard. Supersedes the old framing in issued/release_ships_smoke_datasets.md (PyAutoBuild#126, which said "regenerate datasets full-size" — disproven).

CORRECTED DIAGNOSIS (researched 2026-07-13, deeply, with the user):
- Design intent (encoded in each workspace .gitignore): dataset/** is gitignored except a small allowlist of REAL observational data un-ignored via ! lines (autolens: cosmos_web_ring, slacs1430+4105, double_einstein_ring, mass_stellar_dark, extra_and_scaling_galaxies, a few group/cluster/interferometer dirs, los_halos npy). All SIMULATED datasets are meant to be generated at runtime, never committed.
- The self-provision mechanism ALREADY EXISTS: al.util.dataset.should_simulate(dataset_path) (in autoarray util) returns True when data is missing (and, under PYAUTO_SMALL_DATASETS=1, deletes existing data so the simulator re-creates it at 15x15). The standard idiom is: `if al.util.dataset.should_simulate(str(dataset_path)): subprocess.run([sys.executable, "scripts/.../simulator.py"], check=True)` then Imaging.from_fits(...). See scripts/imaging/modeling.py:94-108 for the canonical example.
- Two coupled bugs: (1) pre_build.sh:64 runs `git add -f dataset/` — the -f FORCE-OVERRIDES .gitignore, committing simulated datasets that should be ignored (autolens: 242 tracked files / 8.1MB across 33 dirs are non-allowlisted; many are also degenerate 15x15 because a smoke run PYAUTO_SMALL_DATASETS=1 generated them in the checkout before pre_build). (2) a MINORITY of example scripts load simulated data WITHOUT the should_simulate guard, so they only work because the -f leak committed the data for them.
- autolens_workspace audit (190 from_fits scripts): 29 load only real/allowlisted data (correct, stays committed); 104 load simulated data WITH a should_simulate guard (correct, self-provision); 7 load simulated data with NO guard = THE DEFECT (mostly scripts/imaging/data_preparation/gui/* + manual/* + guides/results/latent_variables.py, loading simple__no_lens_light / extra_galaxies / lens_sersic).
- generate.py does NOT execute simulators (jupytext script->notebook conversion only), so the build isn't shrinking data — it's force-committing whatever a prior smoke run left on disk.

FOUR-LEG FIX (tractable — NOT an epic; no notebook-prose rewrite, no simulator compute):
1. Stop the leak: drop the -f from `git add dataset/` in PyAutoBuild/pre_build.sh so staging honors .gitignore; only allowlisted real data can ever be staged. (Already-tracked real data stays tracked — dropping -f does not untrack it.)
2. Fix the problem set: add the should_simulate()+simulator-subprocess guard to the unguarded scripts (mirroring modeling.py:96-102) so they self-provision like the other 104.
3. Purge: git rm the non-allowlisted committed simulated datasets so the tree matches .gitignore intent. Users/CI/Colab regenerate via the simulators.
4. Guard: a check asserting `git ls-files dataset/` contains nothing outside the .gitignore allowlist (allowlist-based, NOT git check-ignore-based — see caveat), wired as a PyAutoHeart leg or a pre_build assertion, so it can't recur.

CROSS-REPO AUDIT REQUIRED (the autolens numbers above are ONE repo): run the same allowlist-vs-tracked + guarded-vs-unguarded audit across autogalaxy_workspace, autofit_workspace, HowToLens, HowToGalaxy, HowToFit (and sanity-check the *_workspace_test repos). Report per-repo: count of non-allowlisted committed datasets, count of unguarded simulated-data loaders, and total committed-data size. Each repo has its own .gitignore allowlist that is the source of truth.

ADVERSARIAL CAVEATS to verify during execution:
- NOTEBOOK/COLAB CWD RISK: the guard's subprocess uses a RELATIVE path ("scripts/.../simulator.py") that resolves from the workspace root but may break in notebooks (nbconvert CWD = notebook dir). This morning's workspace-validation run had run_notebooks failures — possibly linked. MUST verify the should_simulate subprocess resolves in notebook + Colab execution BEFORE purging data; if not, purging breaks notebooks even with guards (may need a root-anchored path or a setup_notebook chdir).
- ORPHAN DATASETS: some purge candidates have no consumer and no simulator (autolens: interferometer/many_visibilities, simpleold). Classify each purge candidate as {guarded-consumer + simulator exists → purge safe}, {no consumer → dead, purge}, {consumer but no simulator → needs attention, do not blind-purge}.
- .gitignore re-include subtlety: `dataset/**` + `!dataset/X/**` negations may not actually re-include under git's "can't re-include if parent excluded" rule; the allowlisted real data is currently tracked (so shipping is fine), but the leg-4 guard must be allowlist-based, not `git check-ignore`-based (which mis-flags both tracked files and negated paths).

CONSTRAINTS: autolens_workspace is currently claimed by the active lenstool-scaling task (PR#267) — its leg-2/leg-3 work must coordinate or wait. Difficulty: medium. Autonomy: supervised. This is workspace + PyAutoBuild-pipeline + a PyAutoHeart guard leg (library-first: pipeline + guard, then per-workspace). Retire/supersede issued/release_ships_smoke_datasets.md and update PyAutoBuild#126 to the corrected diagnosis.

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/1d6139c3-b7f4-46d0-805e-f13b5bf2a8ea/scratchpad/intake_smoke_datasets.md -->
