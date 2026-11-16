Shipped 2026-11-12 in PyAutoLabs/euclid_strong_lens_modeling_pipeline#125 (merge `784d55e`); issue #124 closed.

- **Cause.** PyAutoArray #687/#688 made the imaging simulator draw Poisson noise only when it is used. The control test `test_the_library_really_does_raise_without_the_clip` asserted the old `lam < 0` crash, so it went red on `main` and on PR #123.
- **Fix.** The control is replaced by `test_the_library_no_longer_raises_without_the_clip`. With noise off, the round-off negative now passes through unchanged. The pipeline's own clip in `scripts/simulator.py` stays for older stacks, and the module docstring says why.
- **Evidence.** Locally, `pytest -m "not slow"` gives 425 passed. In CI on #125, the unit and slow legs pass on Python 3.12 and 3.13. The smoke leg was skipped, because only a test file changed.
- **Follow-ups.** A cosmetic `NameError: warnings` appears in the "Record cache state" step of PyAutoHeart's `smoke-tests.yml`. Separately, CI now fails on JAX 0.12.0.1, which is outside PyAutoNerves' supported range `<0.12.0`; this blocks euclid#123 and is a separate bug.

## Original prompt

# Obsolete control test after PyAutoArray fixed the simulator round-off crash

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-11-12
Consequence: judge

## Report (human, 2026-11-12: "fix it with /bug then prm")

CI on `main` and on PR #123 is red. Both unit legs fail on one test:

    tests/test_simulator_round_off_clip.py::test_the_library_really_does_raise_without_the_clip
    Failed: DID NOT RAISE ValueError   (1 failed, 424 passed)

`main` reproduces it locally at fbfd7a3. The last green Tests run on main was 2026-11-10.

## Cause

`scripts/simulator.py::simulated_image_from` clips PSF-convolution round-off negatives (about -1e-18)
before the simulator draws Poisson noise. The workaround exists because PyAutoArray's imaging
simulator drew Poisson noise before checking `add_poisson_noise_to_data`, so
`np.random.poisson` raised `lam < 0` even with noise off.

PyAutoArray #687 / #688 ("draw Poisson noise only when used and clip round-off negatives",
merged after 2026-11-10) fixed that upstream. The control test asserts that the library still
raises without the pipeline's clip. That is now false, so the control is obsolete. Nothing is
wrong with the pipeline.

## Fix locus

The test, in this repository. No library change is needed: the library fix is correct.

- Replace the control with a test that pins the new library behaviour: the unguarded path no
  longer raises on round-off negatives (PyAutoArray >= #687).
- Keep the pipeline clip for older stacks (the RAL stack may lag `main`), and say so in the
  docstrings. Its own tests (no raise; real negatives not zeroed; clean images bit-identical)
  stay.

## Also seen, out of scope

A cosmetic `NameError: name 'warnings' is not defined` appears in the "Record cache state" step
of PyAutoHeart's reusable `smoke-tests.yml`. That step still succeeds. File it separately against
PyAutoHeart.
