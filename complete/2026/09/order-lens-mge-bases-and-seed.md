## order-lens-mge-bases-and-seed
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/57
- library-issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/610
- completed: 2026-09-08
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1586
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/611
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/58
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1586
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/611
- heart-ack: 2026-09-08 in-session, the two organism-scope reasons acknowledged earlier this session (autolens workspace validation failures; no release rehearsal)
- Summary: human direction: the two-basis MGE ordering lives in the library. `mge_model_from` gains `order_bases` (default off; consecutive-pair `ell_comps_1 > ell_comps_1` assertions on the returned Basis model) and `ell_comps_limit`; the Euclid pipeline turns it on (`ell_comps_limit=0.5, order_bases=True`, source 0.7, reassignment loops removed), adds `fit(seed=None)` / `--seed`, factors `vis_lp_model_from()`, docs section 7. Key is `ell_comps_1`, not magnitude: phase-4 tiles show the antiparallel cross (equal magnitudes, Δe1 = 1.0 on 102005065); no continuous key is exact everywhere (Δe1 = 0.01 on 102007299).
- Review: Codex gpt-6-astra on both branches. Real: assertions did not enter the PyAutoFit identifier (ordered fit would resume the unordered one) → PyAutoFit#1586 hashes assertions by class + operand paths, assertion-free models unchanged; new params inserted mid-signature broke positional callers → moved to the end + pinned; `Result.model` drops assertions (documented; ideas.md); wording: "forbids the solution" → mode separation vs posterior width; "rotation-invariant reduces to magnitude" was false (cross product is invariant too; both blind on the antiparallel cross).
- Traps: PyAutoFit `add_assertion(name=)` is silently discarded (ideas.md); `test_autogalaxy` config sets `exception_override` so `instance_from_vector` never raises under pytest (call `check_assertions` directly); the pipeline test config likewise; `model.paths` is not vector-aligned (find prior indices by identity).
- Next: RAL stack pulled (PyAutoFit, PyAutoGalaxy), science clone synced, Cortex task `euclid_dr1_prelim/ordered_mge_witness_102005065` (two unseeded runs, own output roots) awaiting the human's submit; then flip the library default once validated; `mge_model_from` ordering for K>2 already covered.
- Session: parallel-claim on euclid_strong_lens_modeling_pipeline with profiling-production-representative (#235); a shared-Mind-index collision twice this session (another session's staged prunes rode along in active.md commits; converged on their push).

## Original prompt

# Order the two lens-light MGE bases in vis_lp and expose a Nautilus seed

Type: feature
Target: workspaces
Repos:
- euclid_strong_lens_modeling_pipeline
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-08
Consequence: review
Witness: two independent unseeded vis_lp runs of the ordered model on tile 102005065 (euclid_dr1_prelim, RAL) give set-A and set-B ell_comps that agree run-to-run to within 0.05 per component with no A<->B swap, log evidence within 1.0 of the unordered baseline 9492.7, and per-set ell_comps marginal widths narrower than the unordered run's (the bimodal mixture collapses); the pipeline's test_mode run and `pytest tests/` pass locally under both `--use_cpu` and the JAX path with the assertion attached.
Review-minutes: 8
Unattended: ready


Apply the recommendation of `docs/mge_label_degeneracy.md` (euclid_strong_lens_modeling_pipeline#54) now that PyAutoFit#1583 (merged 2026-09-08, on library `main`; the RAL stack tracks library mains via HPCPullPyAuto) makes `add_assertion` enforceable on the JAX path.

In `scripts/initial_lens_model.py`:
1. After the model `af.Collection` is composed (after line ~236), attach an ordering assertion between the two lens-light MGE bases so the label symmetry is broken exactly: `|e_A|^2 > |e_B|^2` on the two shared ell_comps prior pairs (set A = `profile_list[0]`, set B = `profile_list[20]`), with a descriptive assertion name. Add a short prose block explaining why (two identical 20-Gaussian bases with iid priors are exchangeable; unseeded Nautilus lands on either labelling; see the note).
2. Expose the Nautilus seed for the vis_lp search as a `seed: Optional[int] = None` argument of `fit()` and a `--seed` CLI option in `start_here.py` (and wherever `fit()`'s arguments are plumbed, e.g. the two-stage batch scripts), default `None` (unseeded, so the witness measures the ordering alone). Document that `seed` is a search identifier field.
3. Do not change the vis_pix stage: it freezes the vis_lp ML instance; the ordering makes the frozen values canonical.
4. Keep `--use_cpu` working: on the NumPy path the assertion is enforced by exception + resample; on the JAX path by the traced penalty.

Constraints: land only between phases (both changes alter the vis_lp identifier and force fresh runs); euclid_dr1_prelim phase 4 (SLURM 342301_[0-9], 342314_3) must be finished or explicitly abandoned first. The science clone at `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim` pulls this change and `hpc/sync push --no-data` carries it to RAL; the witness reruns are a Cortex task on euclid_dr1_prelim, not part of this PR.

Out of scope: the `mge_model_from` ordering option in PyAutoGalaxy (ideas.md).

<!-- filed 2026-09-08 by the mge-label-degeneracy session from the ideas.md bullet tagged "research mge-label-degeneracy · scripts/initial_lens_model.py:162"; that bullet is retired by this prompt -->

## Library prompt (PyAutoGalaxy#610)

# `mge_model_from`: optional ordering of multiple bases and a configurable ell_comps limit

Type: feature
Target: autogalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-08
Consequence: review
Witness: `mge_model_from(total_gaussians=20, gaussian_per_basis=2, order_bases=True)` returns a Basis model carrying exactly one assertion `basis_0.ell_comps_1 > basis_1.ell_comps_1`; `order_bases=False` (the default) carries none and every existing test is byte-for-byte unchanged; `ell_comps_limit=0.5` sets the TruncatedGaussian ell_comps bounds to ±0.5; the Euclid pipeline composes its vis_lp lens light with `ell_comps_limit=0.5, order_bases=True` and no prior reassignment loop.
Review-minutes: 5
Unattended: ready


Human direction 2026-09-08 (verbatim): "I think that the solution should be implemented in the source as an extension to mge_model_from, I think it should be default off for now but used in the euclid pipeline with it on, and we can swap it to default on once its properly tested".

Context: `mge_model_from(gaussian_per_basis=K>1)` builds K bases with identical sigma ladders, iid ell_comps priors and a shared centre, so swapping any two bases' ell_comps is an exact label symmetry of the likelihood (euclid_strong_lens_modeling_pipeline#54, `docs/mge_label_degeneracy.md`). PyAutoFit#1583 (merged 2026-09-08) makes `add_assertion` enforceable on the JAX path, and gathers child-attached assertions, so an assertion on the returned Basis model is enforced on both backends.

Add to `autogalaxy/analysis/model_util.py::mge_model_from`:
1. `order_bases: bool = False` — when True, `gaussian_per_basis > 1` and not `use_spherical`, add to the returned `af.Model(Basis)` one assertion per consecutive pair, `ell_comps_1[j] > ell_comps_1[j+1]`, named `mge_basis_{j}_ell_comps_1_gt_basis_{j+1}`. The key is `ell_comps_1` (cos 2φ component), not the magnitude: on the Euclid phase-4 tiles the two bases often sit at the ±0.5 edge with opposite signs (equal magnitude), where a magnitude key slices both modes. Docstring: what it removes, why e1, the blind band (a small |Δe1| between bases means the ordering did not resolve on that dataset), that it changes the run identifier, that `take_attributes` refuses a target with assertions, and that the default stays off until validated.
2. `ell_comps_limit: float = 1.0` — the TruncatedGaussian ell_comps bounds become ±`ell_comps_limit` (uniform priors keep `ell_comps_uniform_width`). Needed so callers set tighter bounds without replacing the prior objects an assertion references.

Tests in `test_autogalaxy/analysis/test_model_util.py`: default off → no assertions, existing tests unchanged; order_bases with K=2 → one assertion, K=3 → two, spherical → none; an ordered vector satisfies and its swap fails via `assertions_satisfied_from_vector`; `ell_comps_limit=0.5` bounds. No JAX in unit tests.

Follow-up (workspace): euclid_strong_lens_modeling_pipeline#57 composes with `ell_comps_limit=0.5, order_bases=True`.
