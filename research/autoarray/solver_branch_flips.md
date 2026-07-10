# Root-cause the measure-thin solver branch flips in pixelized likelihoods

Type: research
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Original request (verbatim): "do these two: kernel-forward chunking, the
branch-flip investigation" (2026-07-10, follow-up to
PyAutoArray#373 / PR#374, human-directed after merge).

## Background (evidence on PyAutoArray#373, probes of 2026-07-10)

Pixelized-source likelihoods contain deterministic, measure-thin branch flips:

- Width **< 1e-15 in the parameter** (single float inputs — both ±1e-15
  neighbours of a bad input are clean).
- ΔLL ≈ **1.577e-3** on the interferometer sparse 8×8 config; up to **~14**
  on imaging 28×28 — the SAME ΔLL for flips in two orthogonal parameter
  directions on a given config (one binary switch per config).
- Present under `reg.Constant` AND `reg.Adapt`; observed with the kernel-CDF
  mesh (which made mass/shear FD certifiable and hence exposed them) but
  suspected mesh-independent. RectangularUniform showed none on a 25-point
  scan (could be luck or a better-conditioned system).
- The surface is otherwise exactly linear over ±2e-8 windows (resid ≤ 5e-13).
- Reproducible across processes at the same float input (deterministic).
- Density on the probed configs: ~1 hit per ~25 sampled floats in a 4e-8
  window — frequent enough to poison single-step FD (the jax_grad harness
  grew an FD-step-sweep in response) and to perturb any sampler evaluating
  at a bad float.

**Prime suspect**: positive-only solver (PDIP/fnnls) iteration/tie-break
knife-edges near a degenerate active-set vertex — solution differs by
~tolerance scale between branches. Related: the nnls_solver_tol knob
(Settings, default off; PyAutoArray PR#371 / nnls ledger).

## Task

1. **Reproduce at the known bad input**: interferometer sparse config from
   `jax_grad/interferometer.py` variant D, gamma_2 = base − 1e-8 (probe
   script pattern is on #373). Confirm determinism on current main.
2. **Instrument the solve**: diff solver internals between the bad float and
   an adjacent clean one — iteration count, active set / clamped pixel set,
   solution vector, residual. Identify WHERE the branch splits (PDIP
   iteration count? active-set pivot? a `jnp.where` threshold? reduction
   order?).
3. **Test the mechanism**: does `nnls_solver_tol` (tighter/looser) move or
   remove the flips? Does the unconstrained (non-positive-only) solve show
   any? Does flip magnitude track solver tolerance?
4. **Deliverable**: mechanism + recommendation on the issue — options include
   a tolerance/tie-break fix, a documented accuracy floor for pixelized LL
   (relevant to evidence estimates and samplers), or "won't fix, documented".
   A fix, if small and clearly safe, may ship behind the normal gates;
   otherwise file it as its own follow-up.

## Constraints

- Investigation is read-only on main (keck-ao pattern: no worktree claim
  until/unless a fix ships); probes live in scratch, findings on the issue.
- Do not modify the jax_grad certification semantics — the step-sweep stands
  regardless of the outcome here.

<!-- formalised 2026-07-10 from #373 follow-up list, human-directed -->
