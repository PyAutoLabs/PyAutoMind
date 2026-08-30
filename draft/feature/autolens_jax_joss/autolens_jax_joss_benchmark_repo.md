# autolens_jax_joss benchmark repo + real-data start_here pairing

Type: feature
Target: autolens_workspace
Repos:
- autolens_jax_joss (new repo)
- autolens_workspace
Themes:
- profiling
- notebooks
- hpc-gpu
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-07-16 (backfilled from git)

Create a repo autolens_jax_joss which provides examples to run each JAX benchmark from the PyAutoLens-JAX paper draft and reports the run time and info. These benchmarks currently do not exist.

Single-dataset and single-regime benchmarks (establish GPU acceleration and autodiff across lensing scales and data types):

- Galaxy-scale CCD imaging: Model JWST COSMOS-Web Ring F150W imaging, including lens-light subtraction and a pixelized source reconstruction, in approximately five minutes.
- Interferometry: Model a real ALMA strong-lensing dataset containing more than one million interferometer visibilities in approximately five minutes.
- Point-source lensing: Model a real multiply imaged quasar or supernova using point-source observables, including image positions and, where available, time delays or flux information, in under five minutes.
- Group-scale strong lensing: Model a real group-scale lens containing multiple deflecting galaxies in under five minutes, demonstrating that PyAutoLens-JAX is not restricted to isolated galaxy-scale lenses.
- Cluster-scale strong lensing: Model a real cluster lens with multiple mass components, multiple images, and potentially multiple source planes in under five minutes.
- Weak lensing: Fit a weak-lensing shear catalogue using a differentiable JAX likelihood in under five minutes, demonstrating that PyAutoLens-JAX is not restricted to strong-lensing data.

Joint and multi-dataset benchmarks (different datasets, lensing regimes, and physical scales combined in a single differentiable, GPU-accelerated probabilistic model):

- Multi-band imaging: Jointly model the four available JWST COSMOS-Web Ring bands, constraining a common lens mass model while fitting the wavelength-dependent lens and source emission in each dataset.
- Joint strong and weak lensing: Constrain a single group- or cluster-scale mass model using both strong-lensing and weak-lensing observables.
- Imaging and point-source lensing: Jointly model extended arcs and point-source constraints from a lensed quasar or supernova within the same lens model.
- Imaging and interferometry: Jointly fit optical or infrared imaging and radio or submillimetre interferometer visibilities, constraining a common mass model using complementary observations of the lensed source.

Pairing requirement: pair each benchmark to the start_here.py file in each autolens_workspace package. For example the JWST COSMOS-Web Ring F150W example, which is made fast, is paired to autolens_workspace/scripts/imaging/start_here.py. All 6 single-dataset start_here.py examples should use real data, and each JOSS example should use the same real data.

The four multi examples pair to examples in autolens_workspace/scripts/multi or scripts/weak/features/strong_lensing. A new multi script will likely be needed for the imaging + point-source lensing joint-modelling benchmark.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b23fc486-a111-4a87-a6c8-b4ca86dd0749/scratchpad/intake_autolens_jax_joss.md -->

---

## PARKED 2026-07-28 — resume state (moved out of `active.md`)

Parked by user request during a `/repo_cleanup` sweep ("we will come back to JOSS
benchmarks later"). The `active.md` registry entry was removed; this section is
the authoritative resume context. Issue: <https://github.com/PyAutoLabs/autolens_workspace/issues/281>

**Status at park:** `#282 MERGED+cleaned`; 8/8 runnable A100 rows committed
(`autolens_jax_joss@64204f6`).

**Worktree:** `~/Code/PyAutoLabs-wt/jax-joss-benchmarks` **no longer exists on
disk** — recreate it (`start_workspace`) before resuming. Autonomy: supervised.
New repo `autolens_jax_joss` (PyAutoLabs, public) was born alongside this task.
Datasets SDP.81 / RXJ1131 / A2744 are user-approved. 5-phase epic, one-shot
attempt per user.

**SDP.81 prep** = detached RAL job `330608`. (Job `330605` diagnosed: an empty
leftover `extracted/` skipped the untar — fixed via a `test -d` guard; `casatools`
import needs `~/.casa/data` — also fixed. The 42GB tarball is CACHED, so no
re-download.) Pipeline: 45GB ALMA Band6 download -> casatools venv -> 3-level
export -> installs `dataset/interferometer/{sdp81,sdp81_mid,sdp81_full}` under
`/mnt/ral/jnightin/autolens_jax_joss`.

**RESUME (short session):**

1. Check `/mnt/ral/jnightin/sdp81_prep_330608.log` — expect `SDP81 PREP ALL DONE`
   plus per-level visibility counts. Failure modes: casatools pip wheel on py3.12
   (fallback = monolithic CASA tarball), datacolumn, `MS_LIST` empty (check the
   find patterns).
2. `sbatch` the interferometry benchmarks on A100: `benchmarks/interferometer.py`
   at `--nvis` default/mid/full, plus `benchmarks/imaging_and_interferometer.py`
   (pattern: `/mnt/ral/jnightin/autolens_jax_joss/run_rest.sbatch`).
3. `scp results/*.json` back, regenerate `RESULTS.md`, commit — **guard: commit
   explicit file paths only**.
4. Copy the small `sdp81/` product locally and rewrite
   `scripts/interferometer/start_here.py` on a NEW branch (`start_workspace`;
   #282 is merged) using it. Decide hosting: commit few-MB FITS to the workspace
   with a `.gitignore` allowlist + `git add -f`, or Zenodo + `SDP81_URL`.
5. Final issue #281 update.

**Also pending:** cluster-tuning prompt
`draft/feature/autolens_workspace/joss_cluster_benchmark_tuning.md`; weak JAX-viz
`PyAutoLens#614`.
