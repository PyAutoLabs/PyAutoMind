# TEST-mode CI over every Euclid example script, on committed simulated datasets, with latent-variable tests

Type: test
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoLens
Themes:
- euclid
- ci-smoke
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Epic: euclid-dr1-prep
Phase: 2
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28

Phase 2 of 10 in the Euclid DR1 preparation epic. **Gate: phase 1** (the script set must
be settled before CI is wrapped around it) — **UNBLOCKED 2026-08-29**: phase 1 shipped
(`complete/2026/08/euclid-pipeline-parity.md`, euclid#43 closed, PR #44 merged). That PR
added no `.github/workflows/`, so this repo still has **no CI at all** — the whole gap is
this phase's.

User request (verbatim):

"""
2) Next, for "euclid_strong_lens_modeling_pipeline", implement CI using TEST mode against all example scripts, which we will use simulated datasets (include a single simulator.py script)
which are added to the GitHub repo to test them. This differs to the normal workspace, which typically do auto-simulate,
the motivation here is that msot people use the repo to fit real data and we dont want auto simulate stuff clouding 
the setup. Also put unit tests on all Analysis latent stuff and some CI on the latent stuff. Look at the results and code 
setup in /mnt/c/Users/Jammy/Science/euclid and make sure this repo has the same latent variables and whatnot.
"""

## The deliberate difference from the other workspaces

Every other PyAuto workspace **auto-simulates**: a script that needs a dataset makes one
on first run. This repo must **not**. Most of its users fit real Euclid data, and
auto-simulate machinery inside the example scripts would clutter that reading. So the
simulated datasets are **committed to the GitHub repo as files**, and the scripts just
load them like any other dataset.

Two consequences to hold onto:
- Keep the datasets small. They are in git forever. Check what the smoke harness needs
  at minimum (`test_mode` fits do not need full-resolution data).
- There is exactly **one** `simulator.py`, and it is a user-facing example (a user
  resimulates their own fitted lens with it — that is phase 5's contract), not a
  fixture generator hidden in a test directory. Phase 2 and phase 5 must land the
  *same* script; coordinate, do not write two.

## Current state (surveyed 2026-08-28)

- `euclid_strong_lens_modeling_pipeline/smoke_tests.txt` lists 6 entries:
  `start_here.py`, `scripts/initial_lens_model.py`, `scripts/full_model.py`,
  `scripts/lens_model_waveband.py`, `scripts/mge_lens_only.py`,
  `scripts/sersic_lens_model.py`. Phase 1 will add scripts; every added script must
  arrive with its smoke entry.
- `tests/` contains exactly one file: `test_compute_latent_variable.py`. That is the
  seed for the latent unit-test work, not the finished article.
- `Science/euclid/scripts/` carries `diagnose_latent.py` and `diagnose_latent_vis_pix.py`
  — read these to learn which latents the real DR1 runs actually produced, and check the
  pipeline repo computes the same set.

## Deliverables

1. **Committed simulated datasets** under the repo's `dataset/` tree, sized for CI, with
   a README naming what each one is and which script consumes it. No auto-simulate
   fallback in any example script.
2. **A single `simulator.py`** that produced them and that a user can point at their own
   fit result (shared with phase 5).
3. **TEST-mode CI** (`PYAUTO_TEST_MODE` / the repo's `test_mode` convention) running
   **every** example script, not a subset. Follow the workspace smoke convention: in-file
   `# ENV:` declarations where a script needs specific env, and the workspace CWD. The
   CI must report *every* failing script, not just the first.
4. **Unit tests on all Analysis latent variables** — every latent the Analysis computes
   gets a direct test with a known-answer assertion, extending
   `tests/test_compute_latent_variable.py`.
5. **CI on the latent outputs** — a run-level check that the latents actually land in the
   output of a TEST-mode fit (a unit test on the compute function does not prove the
   pipeline writes them).
6. **Latent parity with the science tree** — the set of latents produced here matches
   what `Science/euclid` produced for DR1, verified against the reference tile's
   `lens_mass.csv` / `lens_sersic.csv` / `source_sersic.csv` / `magnitudes.csv` columns.

## Acceptance / gate

- CI green with every example script exercised in TEST mode on committed data.
- No script in the repo auto-simulates.
- Every Analysis latent has a unit test, and a TEST-mode run demonstrably emits the full
  latent set.
- The latent column set matches the DR1 reference bundle.
- Strongly preferred (not strictly required) before phase 4 — going into a 10-lens
  science run without CI means debugging science and software at the same time.
