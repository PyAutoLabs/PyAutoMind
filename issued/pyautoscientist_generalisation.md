# Generalise the organism into PyAutoScientist: adoption assessment + unified docs

Type: docs
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoMemory
- PyAutoBuild
- PyAutoHeart
- PyAutoLens
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Make the PyAuto organism adoptable as **PyAutoScientist** — the basis for
other people's AI dev workflows, driving projects completely independent of
PyAutoFit/PyAutoLens — without splitting off from the repos in daily use and
without touching the live setup's behaviour.

The scoping is **done**: see the companion
`pyautoscientist_generalisation_assessment.md` (same folder) for the coupling
audit (§1), the category-contract insight (§2), the adversarial pass (§7) and
the settled adoption model (§8). This prompt is the execution order.

## Settled direction (do not re-litigate at start_dev)

- **Adoption model: config-diff fork (§8).** One upstream — the live organs.
  Adopters fork Brain/Heart/Build, replace only the declared config surfaces,
  write their own Mind/Memory from skeletons, and `git pull` upstream cleanly.
  Never one shared deployment; never a second hand-maintained "generic"
  organism.
- **One live organism.** No genericisation of `skills/*.md` bodies (they are
  production prompts symlinked into `~/.claude`), no `AGENTS.md` rewrites, no
  stability promises on organ `main` branches.
- **Docs model (§4):** one ReadTheDocs project **pyautoscientist**, sourced
  from `PyAutoBrain/docs/` (growth rule: no new organs). The live lensing
  stack stays in the docs as the *labelled worked example* — do not purge it.

## Phase 1 — zero behaviour risk (start here tomorrow)

1. **Licenses.** Add LICENSE to PyAutoBrain, PyAutoMind, PyAutoHeart,
   PyAutoMemory (PyAutoBuild already has one). Match the existing PyAuto
   library licence unless Jammy says otherwise; for PyAutoMemory decide
   structure-vs-content licensing explicitly (ask — human decision).
2. **README rewrites.** Shrink all five organ READMEs to ~20–40 human-written
   lines each: what it is, one table or diagram, link to ORGANISM.md and (once
   live) the RTD. READMEs are human-facing only — agents load AGENTS.md and
   skills — so this cannot regress behaviour. Kill the AI-essay style.
3. **Build repo hygiene.** Gitignore + evacuate `PyAutoBuild/test_results/`
   and `to_do_list/` (committed instance run-state; collides with any fork's
   own runs).
4. **Tenant firewall.** Extend `PyAutoMind/scripts/repos_sync.py --check`
   with a check that no instance fact (repo name, owner, workspace path)
   appears in organ code outside the declared config surfaces (Heart
   `config/repos.yaml`, `pre_build.sh` tables, Brain constant tables in
   `agents/*/_*.py`, generated doc blocks). Seed the allowlist from the
   assessment §1 inventory. This protects the clean-pull property as the
   organs churn, and is drift hygiene for the live system regardless.

## Phase 2 — the PyAutoScientist ReadTheDocs

5. **RTD skeleton** in `PyAutoBrain/docs/` published as `pyautoscientist`:
   concepts (organism, organs, call chain, conductors/faculties, growth
   rule — sourced from ORGANISM.md, not duplicating it), per-organ reference,
   the **category contract** (what each satellite kind — library / workspace /
   workspace_test / howto / assistant — is for and what the organism expects
   of it), and the worked example (the live lensing instance, labelled as
   such). All **new** prose; it documents the skills, it never rewrites them.
6. **Adoption guide** written against the fork model: fork the organs →
   replace the config surfaces → write your body map → `repos_sync --write`
   → go. State the prerequisites plainly (Claude Code + `~/.claude` skills,
   `gh` CLI, worktree layout, GitHub Actions/PyPI) as what PyAutoScientist
   *is*, not apologetically.
7. **CONTRIBUTING + stability disclaimer** in each organ: living reference
   implementation, `main` moves fast, copy/fork-and-pull, no compatibility
   promises. **Hub card** on pyautolabs.github.io linking the RTD.

## Phase 3 — demand-gated

Trigger: a concrete adopter exists **or** a launch is committed (paper /
announcement / deliberate user-acquisition push). If the trigger is a launch,
do not go straight to publishing: recruit 1–3 friendly beta adopters after
Phase 2 and let their friction shape this phase — they are also the paper's
case studies, and they prove the adoption path end-to-end before strangers
try it. A launch additionally needs a turnkey quickstart on top of the items
below (an `init` bootstrap: zero → running organism in ~an hour).

- Config extraction: Heart `version_skew`/`readiness`/URL rules → `config/`;
  Build tables → policy YAML; Brain constant tables → derived from
  `repos.yaml` where identity, policy file where vocabulary.
- `repos_sync --write` stamping the organ config surfaces from the body map
  (turns "edit five mirrors" into "edit one file, regenerate" — also removes
  the live system's own hand-mirroring burden, so it may be pulled forward on
  its own merits).
- Mind/Memory skeletons (`*-template`, generated not hand-maintained) and an
  optional cookiecutter for the satellite pattern.

## Acceptance for phases 1–2

- Zero diffs to skill bodies, AGENTS.md files, hooks, or organ runtime code
  (except the additive firewall check and Build gitignore).
- `repos_sync.py --check` green, including the new firewall check.
- Heart/Build/Brain test suites green; one PR per repo, normal ship gate.
- A stranger reading pyautoscientist RTD can explain the organism and knows
  exactly what forking it entails — without opening a single organ README
  essay.

## Original request (verbatim)

PyAutoBrain, PyAutoMind, PyAutoMemory, PyAutoBuild (soon to be Hands) and PyAutoHeart make up an AI development ecosystem resembling a organism or a PyAutoScientist. some aspects of these repos might be specific to my workflow, how I develop PyAutoLens and over domain specific aspects of what I do. furthermore they are not documented and their GitHub repos Readme.md are long text and very AI written. could you do an assessment of how we generalise these repos so other people can adopt the PyAutoScientist AI agentic dev workflow and maybe put together docs for all repos (but just one readthedocs maybe called PyAutoScientist). Happy for your opinion on if thus can become a standalone open source repo others user can come in and if this can be done without splitting off from the repos I use  also not that the design of domain specific things like PyAutoLens, autolens_workspace, autolens_assistqnt and the test and HowTo things are built into the PyAuto design so even these may need to be Generalised? (e.g. an example PyAutoProject, autoproject_workspace and so on)

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs-PyAutoMind/ebd42158-6295-466c-9407-20d3e6d1a824/scratchpad/intake_raw.txt -->
<!-- scoped 2026-07-09 in-session: assessment complete (see companion assessment note); phases settled; ready for start_dev -->
