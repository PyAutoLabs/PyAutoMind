# Nightly run of one HowTo tutorial per chapter at real settings

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- HowToFit
- HowToGalaxy
- HowToLens
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Blocked-by: PyAutoFit#1454 (HowToFit tutorial_5_expectation_propagation cannot complete at real sampling)

Filed: 2026-09-15

Origin: follow-up offered while shipping the Colab gate (PyAutoHeart#227 / #228) and
accepted by the user on 2026-09-15 ("do 1 and 2, and the follow up, and then prm").

## Why

The Colab gate (PyAutoHeart#228) proves the `--no-deps` Colab bootstrap can import
everything the libraries import. It deliberately does NOT run notebooks end to end:
that tests a different bug class — script correctness at real sampling — which today
has no gate at all. Workspace smoke runs every HowTo script at `PYAUTO_TEST_MODE=2`
(sampler bypassed), and the HowTo repos have no `profile_release.yaml`, so they are
outside the release-fidelity matrix by design (`PyAutoHeart/docs/release_validation.md`).
HowToFit `config/build/no_run.yaml` records the consequence: tutorial 5 "passes" in
CI while never completing a single EP update at real settings (PyAutoFit#1454).

## Scope to decide

- One representative tutorial per chapter (HowToFit 18, HowToGalaxy 32, HowToLens 50
  notebooks in total) at `PYAUTO_TEST_MODE=0` or `1`, nightly, not per release —
  rung 3 of the ladder scoped in `active/colab_notebook_release_gate.md`. Tens of
  minutes per chapter; price it before choosing 0 vs 1.
- Where: a Heart deep check (never the <30 s tick) or a workflow in each HowTo repo
  reusing `PyAutoHands/autohands/run_all.py --run-type release` — which would need a
  `profile_release.yaml` per HowTo repo, since fidelity comes from the env profile.
- Verdict: reporting-only at first (a `no_run.yaml`-style census on the Heart board),
  promoted to a readiness input once it has a week of green.
- Representative choice: prefer the tutorial that constructs the most search types;
  tutorial 5 of HowToFit chapter 1 is excluded until PyAutoFit#1454 is fixed.
