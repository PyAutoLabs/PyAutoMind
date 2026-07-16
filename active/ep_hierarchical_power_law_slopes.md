# EP hierarchical power-law slope recovery — autolens_assistant science project

Type: research
Target: graphical_ep
Repos:
- autolens_assistant
- PyAutoFit
- PyAutoLens
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

## Original request (verbatim)

I want to use the autolens_assistant to perform Expectation Propagation (EP) analysis of a Cosmology science case.

The science case is inferring the Hubble constant from time delay lensed quasars, and a example package already
containing EP scripts and runs, simulators and other key things is at:

/mnt/c/Users/Jammy/Science/concr/scritps/cosmology and /mnt/c/Users/Jammy/Science/concr/simulator/cosmology.py

This is actually quite a mature project, but its a git old so probably has some API drift (e.g. old PyAutoLens)
and generally needs to be brushed up.

There are also EP and other examples in autolens_workspace/scripts/guides/modeling/advanced

Can you therefore make a new science project using the autolens_assistant, which uses the main scripts in thee projects
project to perform the EP fit but also allows for the one by one / graphical fits. However, for now, I want to descope
down from the Hubble coonstant for now, and have the only goal be to simulate N strong lens using the power-law + shear
mass model, where the power-law slopes are drawn from a hierarchical distribution. The example scripts should
then be built around recovering the slopes acurate but, more important the mean and scatter of the slope hierarchical
parameter.

The goal are:

1) Show that we can do this for large samples without EP, using JAX gradient samples (SPECIFY).

2) Show that we can do this with EP, ideally showing it recovers the same values and errors.

3) We are going to scale up to large lens samples, so make sure all of this can run on RAL and its HPC via the HPC link.

4) To test all the graphical EP diagnostics and result analysis code, especially tyhe recent EP updates we did last week.

## Intake corrections & grounding (2026-07-16)

**Corrected source paths** (verified on disk; the request has typos):

- Legacy EP scripts: `/mnt/c/Users/Jammy/Science/concr/scripts/cosmology/`
  — `ep.py`, `graphical.py`, `one_by_one.py`, `simple_plot.py`. These are the
  "main scripts" to port: EP fit, joint graphical fit, and one-by-one fits.
- Legacy simulator: `/mnt/c/Users/Jammy/Science/concr/simulators/cosmology.py`;
  an existing simulated dataset lives at `concr/dataset/cosmology__time_delay`.
- Workspace examples: `autolens_workspace/scripts/guides/modeling/advanced/`
  — `expectation_propagation.py`, `graphical.py`, `hierarchical.py`.
- Expect API drift in the `concr` package (old PyAutoLens); brush up against
  the installed stack, grounding via the PyAuto API gate / `dir()` rather than
  guessing.

**Descoped goal (this task).** No H0 / time delays yet. Simulate N power-law +
shear lenses with slopes drawn from a hierarchical (parent) distribution;
example scripts recover the per-lens slopes and — the primary metric — the
mean and scatter of the parent slope distribution. Keep the project layout
H0-compatible so time-delay cosmography can be re-scoped in later.

**Project home.** New science project stamped from
`autolens_assistant/skills/start-new-project.md` (project skeleton: `scripts/`,
`dataset/`, `results/`, `hpc/`, `wiki/project/profile.md`). Private science
project, same pattern as PJ011646.

**Goal 1 sampler — the `(SPECIFY)` decision, to settle at start_dev.**
Candidates now first-class in PyAutoFit: multi-start JAX gradient optimizers
(`MultiStartAdam` / ADABelief / Lion — promoted across lib + workspaces) for
MAP-style recovery, and gradient-based posterior sampling (blackjax NUTS/HMC)
for errors. The non-EP baseline must produce parent mean+scatter *with
uncertainties*, so a sampling (not just optimization) path is needed for the
comparison in goal 2.

**Goal 4 context.** The "recent EP updates last week" are the diagnostics /
result-analysis work shipped under `ep_framework_review.md` (this folder,
execution-complete 2026-07-08, wrap-up on PyAutoFit#1330). This project is the
end-to-end exercise of that shipped tooling on a realistic lensing case.

**HPC (goal 3).** Run path is RAL via the assistant HPC link:

- Cluster access: SSH alias `euclid_jump` (ProxyJump through `jump_finan`);
  projects under `/mnt/ral/jnightin/<project>`; PyAuto venv at
  `/mnt/ral/jnightin/PyAuto` kept in sync with local `main`s (`HPCPullPyAuto`),
  activated via `activate.sh` (never pip-install PyAuto* into the venv).
- Project machinery: copy the assistant's `hpc/` (batch_cpu/, batch_gpu/,
  `sync`, `template.py`) into the new project per the start-new-project HPC
  step; docs at `autolens_assistant/wiki/core/operations/hpc_infrastructure.md`.
  Pipeline scripts must preserve the `template.py` HPC interface
  (`parse_fit_args`, `--sample`/`--dataset`/`--use_cpu`/`--number_of_cores`).
- Drive runs with `hpc/sync push-submit gpu <script>` (SLURM array, one
  dataset per task, JAX auto-uses the GPU), then `hpc/sync jobs`/`tail`/`pull`.
  The legacy `concr/hpc/` uses the same layout — port its `sync.conf` pattern,
  not its stale scripts.
- RAL `/mnt/ral` is NFS-slow: detach long remote work (nohup+setsid, poll a
  log), never foreground-`timeout` an ssh.
- N-lens array scaling is the design driver: one lens per SLURM array task for
  the one-by-one/EP factor fits; the joint graphical fit needs a single
  larger-memory task.

**Relationship to existing backlog** (this folder):

- `ep_scoping.md` — EP per-fit overhead / scale-up (performance): directly
  relevant once N grows; do not duplicate its profiling work here.
- `graphical_scoping.md` — joint-graph scale-up (performance): the joint-fit
  baseline in goal 1/2 will hit exactly the dimensionality limits it maps.
- `ep_framework_review.md` — execution-complete; its diagnostics are what
  goal 4 validates.

**Sizing.** too-large is right: expect phased delivery at start_dev
(project stamp + simulator port → one-by-one/JAX-gradient baseline → EP fit +
diagnostics → HPC scale-up), one PR per phase.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/32708468-5918-4dbc-a763-583805364341/scratchpad/intake_ep_cosmology.md; header + grounding hand-fixed at review (docs/autolens → research/graphical_ep) -->
