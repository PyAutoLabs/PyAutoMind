# Expose convolve_over_sample_size as a visible input (default 1) across workspace scripts

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

The final form of option (c) from the phase-4 fork (PyAutoLabs/PyAutoArray#362,
user decision 2026-07-08): **workspace scripts keep PSF convolution at sub
size 1 so they run fast**, but the setting becomes an explicit, documented
input in the script code — users see the knob and know raising it is an
option, without any runtime or dataset change.

## Scope

1. **Simulator scripts** (`scripts/imaging/simulator.py` + the feature
   simulators that copy its pattern): an explicit variable near the PSF
   construction —

   ```python
   # PSF convolution is performed at the image resolution (sub size 1), which is
   # fastest. Supplying the PSF at a multiple of the image resolution and raising
   # this improves blurring fidelity for undersampled PSFs — see the
   # `__Oversampled PSF__` section below and `guides/advanced/over_sampling.py`.
   psf_convolve_over_sample_size = 1
   ```

   passed to `Convolver.from_gaussian(convolve_over_sample_size=...)`.
   Prose is tutorial-register (judgment-tier per the workspace prose split):
   what it does, why 1 is the default (speed), when to raise it.
2. **Loader / modeling scripts**: the flagship chain (`start_here.py`, the
   core `imaging/modeling.py` / `fit.py` / `likelihood_function.py`
   examples) gains the same visible variable passed as
   `convolve_over_sample_size_lp` / `convolve_over_sample_size_pixelization`
   to `Imaging`, with one short comment pointing at the guide. The wider
   ~76-script start-here chain gets the *kwarg-with-one-line-comment*
   pattern only — no prose duplication. Survey and propose the exact script
   list before editing (checkpoint per supervised contract).
3. **No behaviour change anywhere**: every value stays 1 (the s=1 path is
   byte-identical), datasets do not regenerate, no re-baselining. The diff
   is inputs + prose only.
4. Navigator catalogue regen; notebook regeneration follows via the normal
   build.
5. `autogalaxy_workspace` parity is a follow-up, not this prompt.

## Relationship to the full-adoption prompt

`oversampled_psf_dataset_adoption.md` (option a) builds on this: once the
input is exposed everywhere, full adoption is "flip the exposed values to 2
and save the fine psf.fits" plus its re-baselining survey. This prompt goes
first.
