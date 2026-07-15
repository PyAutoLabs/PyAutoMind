# Redesign the env-profile + validation-gate system so this class of bug cannot happen

Type: research
Target: workspaces
Repos:
- autofit_workspace_test
- autolens_workspace_test
- autogalaxy_workspace_test
- PyAutoBuild
- PyAutoHeart
- PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Model: Fable

## What this is

A **design** task, not a fix task. On 2026-07-15 a single missing line in one YAML file held
`nightly-release` red for five nights. Fixing it was ten minutes. Understanding *why the system
let it happen, stay hidden, and be misdiagnosed twice* took the rest of the day, and turned up a
family of related traps rather than one bug.

Your job is to sweep that whole surface — the env profiles, the validation gates, the runners,
and the `use_jax` contract underneath them — and design something **structurally less able to
produce these failures**. Not a patch. Not a lint rule bolted on the side. A cleaner system.

**Take the time this needs.** Read the code, resolve configs, run scripts, run the test suites,
run things twice with different env to compare. If a claim in this document is load-bearing for
your design, *re-derive it yourself* — see "Trust nothing here" below. A design that is right is
worth many hours; a design that is plausible is worth nothing, and this document is itself
evidence of how easy plausible-but-wrong is here.

## What happened (the seed incident)

- `autofit_workspace_test/scripts/searches/MultiStartAdam.py` landed (#43) as a JAX-native search.
- The `mode=release` profile (`config/build/env_vars_release.yaml`) pinned `PYAUTO_TEST_MODE: "0"`
  (real searches, no bypass) **and** `PYAUTO_DISABLE_JAX: "1"` (forces `use_jax=False`).
- `MultiStartAdam` hard-guards on the backend and raised → the `autofit_test/searches` shard failed
  → Stage 3 of `nightly-release` failed. **Five consecutive nights.**
- Nobody noticed for five nights because the only signal was a red nightly.
- Fixed in #44 / PR #45 (add the missing overrides), then superseded by #46 / PR #47 (delete the
  override list entirely — the release default was buying nothing in that repo).

Read these in full; the comments carry the evidence and the dead ends:
- `autofit_workspace_test` **#44** and **PR #45** — the incident and the symptom fix
- `autofit_workspace_test` **#46** and **PR #47** — the structural fix, and why the alternatives lost
- `PyAutoFit` **#1372** — the `use_jax`/`PYAUTO_DISABLE_JAX` three-layer inconsistency, and the
  adversarial review that killed a fix I had already built and was about to ship

## The system as it currently stands

Verify this map; it was assembled quickly and parts of it may be wrong or already stale.

**Two env profiles per workspace**, similar names, different consumers:

| file | profile | consumed by | typical defaults |
|---|---|---|---|
| `config/build/env_vars.yaml` | `smoke` | Heart `workspace-validation.yml` **mode=smoke** (all scripts, weekly Mon 03:00 UTC) **and** the per-PR runner | `TEST_MODE: "2"` (bypass sampler), `DISABLE_JAX: "1"` |
| `config/build/env_vars_release.yaml` | `release` | Heart `workspace-validation.yml` **mode=release** (all scripts, wheels, release fidelity) | `TEST_MODE: "0"`, `DISABLE_JAX` varies per repo |

**"Smoke" means two different things**, which is its own trap:
1. the **per-PR gate** — `.github/workflows/smoke_tests.yml` → `.github/scripts/run_smoke.py`,
   running the *curated* `smoke_tests.txt` list (11 of 42 scripts in autofit_workspace_test);
2. the **`smoke` env profile** — `env_vars.yaml`, above.

They are not the same mechanism and do not cover the same scripts.

**Two independent implementations of the same env resolution:**
- `PyAutoBuild/autobuild/env_config.py::build_env_for_script`
- `autofit_workspace_test/.github/scripts/run_smoke.py::build_env`

They currently agree (defaults → per-pattern `unset:`/`set:`). Nothing enforces that they keep
agreeing.

**Pattern matching** (both copies): a pattern containing `/` is a **substring match against the
full path including extension**; otherwise it matches the file stem exactly. So
`searches/Nautilus` silently also matches `Nautilus_jax.py`.

**The `use_jax` contract, across three layers:**

| layer | `use_jax` default | reads `PYAUTO_DISABLE_JAX`? |
|---|---|---|
| `af.Analysis` | `False` | yes (`analysis.py`, in `__init__`) |
| `ag.*` (`AnalysisDataset`, `AnalysisImaging`, `AnalysisInterferometer`, `ellipse`) | **`True`** | no |
| `al.AnalysisDataset`, `al.point` | **`True`** | **yes — duplicating af, and *before* `super().__init__()`** |

`PYAUTO_DISABLE_JAX` is read in exactly two places across all five libraries (`af.Analysis` and
`al.AnalysisDataset`). It does **not** affect `SimulatorImaging`.

## The failure modes to design against

Each of these is observed, not hypothesised.

1. **Silent override.** `Analysis.__init__` downgrades an explicit `use_jax=True` to `False` with
   no signal. Three lines below, the *other* way `use_jax=True` can fail (JAX not installed) warns
   loudly in a box. Only the env-var path is silent.
2. **Vacuous tests.** A script that declares `use_jax=True` and asserts JAX behaviour, but runs on
   numpy, **passes**. `searches/Dynesty_jax` and `searches/Nautilus_jax` did this for their entire
   existence. `MultiStartAdam` failed loudly *only* because it happens to carry its own guard. The
   scripts with a guard scream; the ones without lie.
3. **Hand-maintained "remember to add your script" lists** — `env_vars*.yaml` overrides,
   `no_run.yaml`, `smoke_tests.txt`. Forgetting an entry does not fail loudly; it degrades
   silently. This is the direct cause of the seed incident.
4. **Config drift is untestable at PR time.** `run_smoke.py` hardcodes
   `ENV_VARS_FILE = config/build/env_vars.yaml`; the per-PR gate never reads the release profile.
   A release-profile error can only surface in the nightly — a ~24h feedback loop, and the only
   signal is one red job.
5. **Inconsistent siblings.** `autofit_workspace` pinned `DISABLE_JAX: "0"` ("release fidelity");
   `autofit_workspace_test` pinned `"1"`. Same organisation, same release, opposite stance, no
   stated reason.
6. **Silent over-match.** The substring/extension pattern rule can quietly capture a script you
   did not mean (`Nautilus` → `Nautilus_jax`).
7. **Duplicated resolvers** that can drift apart unnoticed.
8. **Layered duplicate env reads.** `al.AnalysisDataset` re-implements the base class's env check
   and applies it *earlier*, so the base class cannot see that an override happened. This is
   failure mode 1 recurring one layer up — the pattern reproduces itself.

## What was already tried and rejected — do not redo these blind

Re-test them if your design depends on it, but know the evidence:

- **Promote the script into `smoke_tests.txt`** → rejected. Would not have caught it: the per-PR
  gate never reads the release profile (failure mode 4). Also cuts against the standing "smoke
  tests are a small curated subset; don't mass-promote" preference.
- **Static config guard** ("every script with `use_jax=True` must resolve `DISABLE_JAX=0` in the
  release profile") → rejected. The naive string-matching rule **false-positives**:
  `autolens_workspace_test/scripts/imaging/simulator_use_jax_parity.py` contains `use_jax=True`
  but constructs `SimulatorImaging`, which does not read the env var — its parity test is valid.
  The correct rule ("constructs an *Analysis* with `use_jax=True`") is brittle to detect statically
  across `AnalysisImaging` / `TwoLatentAnalysis` / custom subclasses.
- **A loud warning in `af.Analysis`** when the env overrides an explicit `use_jax=True` → built,
  tested, and then **killed by adversarial review**. Two reasons, both proven empirically:
  (a) PyAutoLens flips `use_jax` before `super().__init__()`, so the warning never fires for the
  ~54 autolens scripts; (b) `ag.*`/`al.*` default `use_jax=True`, so it fires on *default*
  constructions claiming JAX "was requested" when it was not. Silent where it mattered, noisy
  where it did not. Nothing was pushed.
- **Write the trap down** → rejected, with the strongest evidence of the lot. A memory note
  recording this exact two-profile trap **already existed, written the day before**, and the trap
  was still walked into the next morning. Documentation does not fire at the moment of the
  mistake. Prefer deleting the thing-to-remember.

## Measured facts (re-measure; do not inherit)

Scripts containing `use_jax=True`, resolved through
`autobuild.env_config.build_env_for_script` against each repo's **release** profile, as of
2026-07-15 (before PR #47):

| repo | declares `use_jax=True` | JAX actually ON | resolves JAX **OFF** |
|---|---|---|---|
| autofit_workspace_test | 7 | 6 | 1 |
| autolens_workspace_test | 54 | 50 | 4 |
| autogalaxy_workspace_test | 36 | 34 | 2 |

Of the 7 JAX-OFF, ~2 are false positives (the `simulator_use_jax_parity.py` pair). The remainder
are genuine and untriaged:

- `autofit_workspace_test/scripts/features/latent_nan_robustness.py` *(resolved by PR #47; verified
  it passes with JAX on)*
- `autolens_workspace_test/scripts/imaging/visualization.py`
- `autolens_workspace_test/scripts/latent/latent_nan_robustness.py`
- `autogalaxy_workspace_test/scripts/imaging/visualization.py`
- `autogalaxy_workspace_test/scripts/latent/latent_nan_robustness.py`

`latent_nan_robustness.py` deliberately builds **both** a numpy and a JAX analysis, so only its
JAX half is vacuous — triage it, do not blindly override it.

**Note the undercount.** That survey string-matches `use_jax=True`, but `ag.*`/`al.*` default to
`True`. So in autolens/autogalaxy, scripts that never mention `use_jax` *also* get JAX by default
and are *also* forced to numpy by `DISABLE_JAX: "1"`. Whether `mode=release` validating the numpy
path for most of the autolens/autogalaxy surface is intended is an **open question worth your
attention** — it may be a much larger fidelity gap than the seed incident, or it may be
deliberate. Find out; don't assume either way.

## Trust nothing here

This document was written by the agent that made the mistakes. Several of its conclusions were
wrong today and were caught only by an explicit adversarial pass:

- "`PYAUTO_DISABLE_JAX` has exactly one consumer" — **false**, missed the PyAutoLens one by
  grepping only three of five libraries.
- "`use_jax` defaults to `False`, so truthiness means explicitly requested" — **false** for the
  entire ag/al surface.
- "The fix works, I ran it on a real script" — the script exercised the one path where the
  assumption held.
- "The smoke change lets the per-PR gate catch this" — **false**, asserted without checking
  `smoke_tests.txt`.

Every one had the same shape: **verifying the path already assumed, and calling it proof.** Treat
this document as a lead sheet, not a source of truth. Where it matters, check.

## What to produce

A design document (propose where it lives — `PyAutoMind/research/` or a `docs/` page in the owning
repo), covering:

1. **A verified map** of the current system: profiles, gates, runners, resolvers, consumers, and
   who reads what. Correct this document's map where it is wrong.
2. **A target design** that makes the failure modes above structurally hard. Explicit goals worth
   weighing (argue with them if you disagree — these are hypotheses, not requirements):
   - one concept per name — kill the "smoke means two things" collision;
   - one resolver, one pattern semantics, no duplicate implementations;
   - derive rather than enumerate — a script's env should follow from what it *is*, not from
     remembering to list it;
   - a missing/forgotten entry should fail **loudly** rather than degrade to a vacuous pass;
   - config errors should be catchable **before** the nightly;
   - one place reads `PYAUTO_DISABLE_JAX`, and an overridden explicit request is never invisible;
   - sibling repos should not silently disagree about release fidelity.
3. **A migration path** that is landable incrementally, each step green on its own. This system is
   live and gates real releases; a big-bang rewrite is not acceptable.
4. **What you rejected and why**, with evidence. Include anything from "already tried" you think
   was rejected wrongly — that judgement may well be wrong.
5. **Open decisions for the human**, separated cleanly from what you're confident about. In
   particular: the autolens/autogalaxy `mode=release` numpy question (above), and whether
   `use_jax` needs a sentinel (`Optional[bool] = None`) threaded through af/ag/al so that
   "explicitly requested" becomes knowable at all — a real cross-repo API change.

## Method — and please actually do this

- **Run things.** Resolve every script's env under both profiles in all three test workspaces.
  Execute scripts both ways and diff the outcome. Run `pytest test_autofit/` (~75s). Nothing here
  is expensive; the expensive thing is being wrong.
- **Prove no-ops empirically.** "Provably inert" is the phrase that preceded being wrong today.
  Run it both ways.
- **Pick the falsifying case.** If a change touches a base class, exercise a subclass from *each*
  downstream library — the base-class path is the one that already agrees with you.
- **Grep all five libraries** (`PyAuto{Conf,Fit,Array,Galaxy,Lens}`), and don't filter out tests
  when the question is "how many consumers are there?".
- **Adversarial pass before concluding.** For each load-bearing claim: *what would have to be true
  for this to be false, and have I looked?* Then look. That pass cost ~15 minutes today and caught
  a fix that was about to ship broken.
- **Prefer deleting the trap to documenting it**, and prefer the lean existing lever to new
  machinery. If a proposal's rationale is "and we'll remember to keep this in sync", it is the
  trap wearing a new hat. PR #47 is the shape to aim for: it deleted 31 lines of config and a
  whole bug class by noticing the dangerous setting was buying nothing.

## Constraints

- **Do not** copy autofit_workspace_test's `DISABLE_JAX: "0"` reasoning to
  autolens/autogalaxy_workspace_test without re-deriving it. It holds there only because
  `af.Analysis` defaults `use_jax=False`, making the var inert for non-opt-in scripts. ag/al
  default `True`, so the var is **not** inert there and flipping it is a real behaviour change
  across the whole surface.
- **Do not** grow `smoke_tests.txt` to make a gate feel stronger. It is deliberately small.
- Releases are gated by this system. Nothing lands that cannot be shown green.
- Design first. Plan approval before implementation, per the usual workflow.
