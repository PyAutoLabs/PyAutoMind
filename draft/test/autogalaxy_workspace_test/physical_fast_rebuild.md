# autogalaxy_workspace_test physical + fast rebuild (rehearsal repo)

Type: test
Target: autogalaxy_workspace_test
Repos:
- autogalaxy_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 5

autogalaxy_workspace_test physical + fast rebuild (the rehearsal repo before autolens).

Two coupled changes across the repo's 39 smoke-gate scripts (64 scripts total), done as ONE
wave because both force regenerating every pinned likelihood literal:

1) PHYSICAL REALISM: every script uses physical, realistic galaxy models with
simulator↔model consistency and high-likelihood solutions. Where the simulator and the
fitted model mismatch, fix it. Sensible physical inputs throughout (intensities,
background sky, sizes resolvable at the chosen pixel scale). Rationale: when a user
inspects a _test failure, a physical setup is interpretable.

2) SPEED: make the scripts as fast as possible without losing coverage. The ~50s class is
`ENV: jax full_datasets` scripts (compile ~12-18s + full-resolution vmap + ~5-7s import
floor; `config/build/profile_smoke.yaml:22-43` records mge_group.py at 54-63s). Ranked
levers from the 2026-08-31 survey: coarser simulated datasets (e.g. 180x180@0.2" mask 3.5"
-> ~100x100@0.3", shrinking both compile graphs and execution quadratically — 0.3" still
resolves the structure); over-sampling reduction (over_sample_size_lp=4 + radial [4,2,2]
-> [2,2,1]/uniform 2); fewer MGE gaussians / smaller vmap batch sizes (20+30-gaussian
bases dominate graph size). TEST_MODE=2 already bypasses samplers on the smoke gate, so
search settings are not the lever; keep n_like_max philosophy for the weekly/release
channels — better-conditioned physical models are how those get faster.

Constraints: regenerate every pinned `fitness._vmap` literal once, at the end, from the
new sims (pins are deliberately absolute — `scripts/CLAUDE.md`); keep the
`--xla_cpu_multi_thread_eigen=false` workaround and do NOT shrink the
`multi_dataset/jax_likelihood/*` scripts in ways that stop reproducing the Eigen-pool bug
class (jax-compile-stall epic); library unit tests + developer/profiling workspaces are
the independent validation that likelihood-value changes stayed local. Record before/after
per-script seconds against the phase-4 legacy snapshot. Patterns proven here are the
template phase 6 applies to autolens_workspace_test.
