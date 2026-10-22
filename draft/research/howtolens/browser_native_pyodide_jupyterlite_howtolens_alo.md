# Browser-native (Pyodide / JupyterLite) HowToLens alongside Colab

Type: research
Target: HowToLens
Repos:
- PyAutoArray
- PyAutoFit
- PyAutoLens
- PyAutoNerves
- HowToLens
Difficulty: medium
Autonomy: safe
Priority: medium
Memory: wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/massive-ellipticals.md; reading-queue.md
Status: formalised
Consequence: glance
Witness: a headless Node Pyodide run imports autolens and executes HowToLens chapter_1 tutorial_2_ray_tracing to completion, logging pass/fail and wall time.
Review-minutes: 3
Unattended: ready

# Browser-native (Pyodide / JupyterLite) HowToLens alongside Colab

Research whether HowToLens (and the other HowTo* tutorial series) should be built to run natively in the browser (JupyterLite or custom Pyodide HTML) alongside Google Colab. Prompted by building in-browser runnable Pyodide HTML for a PHY2039 teaching workshop on 22 Oct 2026 when Chirun/Numbas were down.

## Preliminary findings (22 Oct 2026, not yet verified by a spike)

1. JAX/jaxlib has no Pyodide/wasm build, but autonerves.jax_wrapper already falls back to pure NumPy when JAX is absent (the Intel macOS path).
2. Pyodide (latest) ships numpy 2.4.6, scipy 1.18.0, astropy 7.2.0, scikit-image 0.26.0, scikit-learn 1.8.0, h5py 3.13.0, xxhash 3.6.0, SQLAlchemy 2.0.48, matplotlib, pandas, networkx 3.6.1, threadpoolctl. NOT shipped: psutil, numba, jax. The PyAuto packages, nautilus, dynesty and emcee are pure Python (micropip).
3. Blockers:
   - autofit/non_linear/search/updater.py has a top-level `import psutil`, so `import autofit` fails in Pyodide (make it lazy).
   - Pin conflicts: scipy<=1.17.1 vs 1.18, xxhash<=3.4.1 vs 3.6, networkx==3.1. Install with --no-deps, as autonerves/setup_colab.py already does.
   - The Sibson interpolator is numba-only (autoarray/inversion/mesh/interpolator/_sibson_numba.py).
   - timeout_decorator relies on signal (import is fine; use would fail).
4. Performance: single-threaded wasm NumPy, no JAX. Model fits (af.Nautilus appears 26x in HowToLens scripts) are impractical in the browser.
5. Scope guess: HowToLens chapter 1 (tutorials 0-8, no searches) and chapter 3 tutorials 1-6 look feasible; search-based tutorials stay on Colab or show precomputed results.
6. Delivery options: JupyterLite (unchanged .ipynb, static hosting e.g. GitHub Pages) vs hand-built Pyodide HTML pages.

## Proposed first step

Headless Node Pyodide spike: stub psutil, micropip-install the PyAuto stack with --no-deps, run HowToLens chapter_1 tutorial_2_ray_tracing, and record pass/fail plus timings. Then decide whether to extend to the other HowTo* series.

Source: https://pyodide.org/en/latest/usage/packages-in-pyodide.html

<!-- formalised by the Intake (Conception) Agent on 2026-10-22 from file:/tmp/claude-1000/-mnt-c-Users-Jammy-Teaching/9bf25cff-0cd0-4b25-9a01-d8fabed9e3b2/scratchpad/intake.txt -->
