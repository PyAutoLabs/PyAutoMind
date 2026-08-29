# Human review: multi-plane cross-validation (library tests + workspace guide)

Type: human review
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
Themes:
- ci-smoke
- notebooks
Priority: normal
Status: awaiting human review
Filed: 2026-08-29

Shipped by an agent session on 2026-08-29 in two PRs; the human asked to read it before it
counts as done. Nothing is broken — this is a sign-off, not a bug.

## What shipped

- **PyAutoLens#715** (merged `9e89bd7c3`) — `test_autolens/lens/test_multi_plane_cross_validation.py`:
  independent oracles for multi-plane ray tracing (astropy Planck15 distances, the SEF §9.1
  recursion written from the paper, a central-difference ray-traced Jacobian, the McCully+14
  Jacobian recursion), 16 tests + 1 strict xfail. Record:
  `complete/2026/08/multi-plane-cross-validation.md`.
- **autolens_workspace#517** (merged `0480fbea`) — `scripts/guides/advanced/multi_plane.py`
  gained a `__Cross Validation__` section (512 → 1271 lines) with the same oracles as runnable
  guide code, the 1.86-vs-27.9 worked example, a double-Einstein-ring figure, a JAX `jacfwd` arm
  and a live warning on the Richardson-step defect. Notebook regenerated. Record:
  `complete/2026/08/multi-plane-guide-cross-validation.md`.

## What to check (read-and-report)

1. **The formalism as written** — the module docstring (PyAutoLens) and `__The Formalism__` /
   `__Two Convention Traps__` (guide): do the cited equations (SEF 9.6/9.7b; Narayan & Bartelmann
   55/60; McCully+14 recursion) and the two traps read correctly to a lensing expert? The agent
   transcribed them from the papers, not from the code, but no human has yet read them.
2. **The astropy-vs-project β split** — β-dependent assertions run twice (astropy β at 1e-6,
   project β at 1e-10) because the hand-rolled cosmology differs from astropy by ~2e-7. Is that
   the right call, or should the cosmology itself be tightened so one tolerance suffices?
3. **The guide's length and voice** — the section more than doubled the guide. Is the prose in
   register, and is 1271 lines acceptable for a single guide, or should the oracle arms move to
   a companion script?
4. **The ENV trade-off** — the guide is now `ENV: jax full_datasets`, so the nojax CI leg skips
   the whole guide. Acceptable?
5. **The strict xfail** pins the Richardson-step defect
   (`draft/bug/autogalaxy/lenscalc_numpy_hessian_step_is_too_coarse.md`, in progress). Confirm
   you want it to XPASS-and-fail when the fix lands (forcing the pin's removal).

Sign off by retiring this prompt (`scripts/lifecycle.py record …`); anything that does not pass
goes back through `/intake` as an ordinary task.
