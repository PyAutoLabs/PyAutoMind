# Colab bootstrap installs no lazily-imported dependency — `corner` kills every MCMC fit mid-run

Type: bug
Target: PyAutoNerves
Repos:
- PyAutoNerves
Themes:
- colab
- dependencies
- tutorials
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Witness: on a Colab runtime bootstrapped with `setup_colab.setup("howtofit")`, `HowToFit/scripts/chapter_1_introduction/tutorial_5_results_and_samples.py` runs to completion and writes its corner plot instead of raising `ModuleNotFoundError: No module named 'corner'` at the end-of-fit results update.
Filed: 2026-09-15
Issued: 2026-09-15

## Original request (verbatim)

> tutorial 5 still gives this
>
>     2026-09-15 06:59:25,441 - autofit.non_linear.search.updater - INFO - Creating latent samples by drawing 100 from the PDF.
>     ---------------------------------------------------------------------------
>     ModuleNotFoundError                       Traceback (most recent call last)
>     /tmp/ipykernel_3678/3237708700.py in <cell line: 0>()
>         111 )
>         112
>     --> 113 result = search.fit(model=model, analysis=analysis)
>
>     8 frames
>     /usr/local/lib/python3.13/dist-packages/autofit/non_linear/plot/samples_plotters.py in corner_cornerpy(samples, path, filename, format, **kwargs)
>          93     pylab.rcParams.update(params)
>          94
>     ---> 95     import corner
>          96     from corner.core import hist2d as corner_hist2d
>          97
>
>     ModuleNotFoundError: No module named 'corner'
>
> is there a way to fix it without a whole release?

Reported against HowToFit chapter 1 tutorial 5 on Colab, Python 3.13, autofit
installed from PyPI. The search itself completed (2000 emcee steps, 57 s); the
crash is in the results update that follows it.

## Root cause

`autonerves/setup_colab.py:126` installs the whole stack with `--no-deps`:

    subprocess.check_call([sys.executable, "-m", "pip", "install", *packages, "--no-deps"])

so any dependency Colab does not itself preinstall has to be named by hand in
`_SHARED_EXTRAS` (`:38-47`) or it never lands. `corner==2.2.2` is a **base**
dependency of autofit (`PyAutoFit/pyproject.toml:41`), is absent from
`_SHARED_EXTRAS`, and is absent from Colab.

The reason it went unnoticed for so long is the shape of the import. `corner` is
imported **inside** `corner_cornerpy` (`autofit/non_linear/plot/samples_plotters.py:95`),
not at module scope, so `import autofit` succeeds, the model builds, the search
runs to completion, and the failure only lands in the results update after the
fit. Nothing before that point can see it.

This is the third instance of the same defect. `PyAutoNerves` commit `8336939`
("fix: install emcee and dynesty in the Colab bootstrap", #166) closed it for
two packages; `draft/bug/howtofit/tutorials_6_7_blackjax_never_installed.md`
has it open for a third. The list is being patched one report at a time.

## Every hole in `_SHARED_EXTRAS`, found by auditing the whole list

Lazily-imported dependencies absent from the list:

| Package | Declared in autofit as | Imported at | Reaches the user via |
|---|---|---|---|
| `corner` | base, `corner==2.2.2` | `plot/samples_plotters.py:95` | every MCMC / nested search's corner plot — **the reported failure** |
| `optax` | base, `optax>=0.2.5` (marker-gated) | `search/mle/multi_start_gradient/search.py:898` | `MultiStartAdam` / `MultiStartProdigy` — HowToFit tutorials 6, 7 |
| `xxhash` | base, `xxhash<=3.4.1` | `graphical/factor_graphs/factor.py:361` | graphical / EP factor hashing — HowToFit chapter_advanced |
| `blackjax` | optional extra, `blackjax>=1.6.2` | `BlackJAXNUTS` | HowToFit tutorials 6, 7 — see the sibling prompt below |

Specifiers in the list that have **drifted** from the file they claim to track
(the comment above `_SHARED_EXTRAS` says outright "their specifiers track that
file"):

| Package | `_SHARED_EXTRAS` says | autofit declares | Effect under `--no-deps` |
|---|---|---|---|
| `anesthetic` | `==2.8.14` | `>=2.9.0` (base) | pins *below* autofit's own floor |
| `nautilus-sampler` | `==1.0.4` | `==1.0.5` (optional) | separate open prompt |

`optax`'s marker in autofit (`sys_platform != "darwin" or platform_machine == "arm64"`)
exists because Intel macOS has no jax wheels. Colab is always linux, so the entry
here is unmarked.

`xxhash<=3.4.1` is an upper bound: if Colab ships a newer xxhash, adding this
entry **downgrades** it. That matches autofit's own declared constraint, so it is
the intended behaviour, but it should be a conscious choice rather than a
side-effect. The `>=`-style entries are no-ops when Colab already satisfies them.

## Why no gate sees any of this

Workspace smoke runs at `PYAUTO_TEST_MODE=2`, which bypasses the sampler, so the
searches are never constructed and the lazy imports are never executed. The
scripts pass green while being unrunnable by a reader on Colab. PyAutoHeart's
`verify_install` check F simulates the Colab bootstrap and is the only gate in
the right place to catch this.

## Sibling prompts covering the same ten lines

- `draft/bug/howtofit/tutorials_6_7_blackjax_never_installed.md` (Priority: high,
  filed 2026-09-15) — its fix step 1 is `blackjax>=1.6.2` into `_SHARED_EXTRAS`,
  step 3 is the nautilus pin.
- `draft/bug/autonerves/nautilus_sampler_pin_drifts_from_pyautofit.md` — the
  nautilus drift, and it already asks whether "the other `_SHARED_EXTRAS` pins
  deserve the same treatment" and recommends deriving the expected specifier from
  PyAutoFit's `pyproject.toml` rather than restating literals.

Each of these needs its own autonerves PyPI release to reach a single user.
Landing them separately means three releases to close one defect. The plan
should decide whether this prompt absorbs the `_SHARED_EXTRAS` legs of both
(leaving the blackjax prompt its `HowToFit/requirements.txt` leg, which is a
different repo and a different install route).

## Fix

1. Close the holes in `_SHARED_EXTRAS`, specifiers tracking
   `PyAutoFit/pyproject.toml` as the existing entries claim to.
2. Correct the two drifted specifiers.
3. Extend the comment above the list to name the lazy-import trap explicitly —
   a dependency imported inside a function survives `import autofit` and only
   detonates mid-run, which is why these are missed.
4. Regression test asserting each package lands in the install list. The existing
   #166 test matches on requirement *name* with the specifier split off, which is
   why it cannot see a drifted pin; a specifier-aware check that reads
   PyAutoFit's `pyproject.toml` rather than restating literals would close both
   classes at once.

## Out of scope (decided with the user, 2026-09-15)

- Do **not** change what PyAutoHands injects as the notebook setup cell.
- Do **not** regenerate or push notebooks in any of the six notebook repos. The
  setup cell runs `pip install autonerves --no-deps` **unpinned at run time**, so
  a released autonerves fixes every published notebook retroactively, including
  already-tagged ones. Notebook regeneration carries nothing.
- Do **not** refactor `_SHARED_EXTRAS` into a fully metadata-derived install list
  (offered and declined). If it is worth doing, file it as its own prompt.

## Shipping

Merging changes nothing on its own — an **autonerves PyPI release** is what ships
this. Latest on PyPI is `2026.9.15.1`, released 2026-09-15. Confirm the overnight
release run has settled before cutting one.
