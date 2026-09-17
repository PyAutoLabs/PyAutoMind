# Check F audits the released Colab bootstrap in a TestPyPI rehearsal, not the candidate

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoNerves
Difficulty: moderate
Autonomy: supervised
Priority: high
Status: formalised
Consequence: block
Witness: with `TARGET_VERSION` set, the check F driver's `colab_gate verify` line reports `installed PyAuto stack - autonerves=<TARGET_VERSION>, autofit=<TARGET_VERSION>, autoarray=<TARGET_VERSION>, autogalaxy=<TARGET_VERSION>, autolens=<TARGET_VERSION>`, asserted by a test that reads the gate's verify report JSON rather than a log grep; the negative control is that with no `TARGET_VERSION` (the continuous PyPI-index tick) the audited stack is still the latest released one, unchanged. Red first: today's rehearsal log shows `autonerves=2026.9.15.1` with `TARGET_VERSION=2026.9.17.1.dev77201`.
Review-minutes: 30
Unattended: ready
Filed: 2026-09-17
Issued: 2026-09-17

## Finding

PyAutoHeart is RED with two reasons that share one root cause, `install
verification FAILED (testpypi; checks F)` and `release validation FAILED (stage
integrate)`. In run 35195111347 all 707 workspace scripts passed and only check
F, the Colab gate, failed.

In a TestPyPI rehearsal (`TARGET_VERSION` set, here `2026.9.17.1.dev77201`) the
seed step does the right thing. `verify_install.sh` line 775 onwards builds
`f_targets` pinning all five PyAuto packages to the candidate version, with a
comment explaining exactly why an unpinned resolve would produce an incoherent
dev/released mix.

The driver then undoes it. `/tmp/F_driver_setup.py`, written at
`verify_install.sh` line 824 as "the injected setup cell, verbatim", runs

    pip install autonerves --no-deps

with no version pin (line 832), which resolves to the latest final release on
PyPI, `autonerves-2026.9.15.1`. That released `autonerves.setup_colab.setup()`
(line 859) then runs its own unpinned `pip install autolens autogalaxy autofit
autoarray autonerves ... --no-deps` (`setup_colab.py` line 309), and the whole
candidate stack is downgraded underneath the gate:

    Successfully installed anesthetic-2.8.14 autoarray-2026.9.15.1 autofit-2026.9.15.1 autogalaxy-2026.9.15.1 autolens-2026.9.15.1 ... nautilus-sampler-1.0.4
    colab_gate verify: installed PyAuto stack - autonerves=2026.9.15.1 ...

So the rehearsal gate audits the RELEASED bootstrap, never the candidate.

## Why it is failing right now

Released autonerves 2026.9.15.1 (tag at 5130298) predates PyAutoNerves #168
(5b3636d, corner/optax/xxhash/blackjax) and #169 (8eca4b3, jax_zero_contour,
zeus-mcmc), both merged to main on 2026-09-15. Check F therefore fails on
blackjax (`autofit/non_linear/search/mcmc/blackjax/nuts/search.py:260`), corner
(`autofit/non_linear/plot/samples_plotters.py:95`), jax_zero_contour
(`autogalaxy/operate/lens_calc.py:1452`) and three more (optax, xxhash, zeus).
PyPI autonerves is still 2026.9.15.1 as of 2026-09-17.

## Consequence

Chicken and egg. The nightly rehearsals on 2026-09-16 and 2026-09-17
(PyAutoHands runs 35068075515 and 35193720454) were rehearsal-only with the
`release` job skipped because Heart is RED. Heart is RED because the bootstrap
fix is unreleased. The rehearsal gate cannot observe the fix even when the
candidate carries it. Any future bootstrap regression will pin Heart RED the
same way until a human overrides the gate, which is exactly the outcome the
gate exists to avoid.

## Design intent

Keep the two modes distinct. The continuous PyPI-index tick (no
`TARGET_VERSION`) SHOULD keep auditing what a reader gets today, the released
bootstrap. That verdict is truthful and must not change. The release-integrate
rehearsal (`TARGET_VERSION` set) must instead audit the CANDIDATE: after the
verbatim setup cell has run, re-pin autonerves and autofit, autoarray,
autogalaxy, autolens to `==$TARGET_VERSION` from the rehearsal index
(`PIP_INDEX_ARGS`) with `--no-deps`, reload `autonerves.setup_colab`, and re-run
its package install so that the `_SHARED_EXTRAS` of the candidate is what gets
audited.

Note that an unpinned `pip install autonerves` can never pick a `.devN`
pre-release, so switching the index alone is not enough; an explicit `==` pin
(or `--pre`) is required.

## Fix options (implementer's choice, both named)

1. A small PyAutoNerves seam: an environment variable honoured by
   `setup_colab.setup()` supplying index arguments and a version pin, so the
   bootstrap installs the candidate when a rehearsal asks it to. Cleaner, but
   the seam itself only takes effect once released.
2. Heart-only: generalise the existing `COLAB_GATE_AUTONERVES_SRC` overlay
   (`verify_install.sh` lines 729 and 842, currently dev/witness only and
   documented "Never set in CI", and currently re-pinning autonerves alone) into
   a rehearsal-mode re-pin that covers all five packages and re-runs the
   package install. Lands entirely inside Heart, so it works on the next run.

The overlay mechanism is proven to work; what is missing is that it only re-pins
autonerves, not the four libraries the setup cell downgrades, and that nothing
sets it in rehearsal mode.

Out of scope: the IMMEDIATE unblock is a human-authorised release carrying
PyAutoNerves main (the #168 and #169 bootstrap fixes). That is a release
decision, not this prompt's work, which is about the rehearsal gate being
unable to see a fix the candidate already carries.

Related: PyAutoHeart#228, PyAutoNerves#168, PyAutoNerves#169,
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/35195111347
