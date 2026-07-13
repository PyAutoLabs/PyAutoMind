## simulator-use-jax-pr4-xp-mismatch
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/334 (CLOSED — final PR of Phase 2)
- completed: 2026-05-24
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/337
- notes: Final PR (4 of 4) of simulator_use_jax.md. AbstractMaker.__init__ now raises ValueError when xp=np is passed with a jnp-backed grid (grid.use_jax=True). Helps users discover the `@jax.jit + xp=jnp` pairing rule the first time they break it — pointer to lens_calc.py workspace guide in the error message. No breaking changes: existing PyAutoArray/Lens/Galaxy tests pass (837/317/918). Worktree removed, branch deleted. **Phase 2 of jax_user_intro DONE.** Library deliverables: PointSolver(use_jax) + autolens.jax.register_tracer_classes (PR 1), SimulatorImaging(use_jax) (PR 2), SimulatorInterferometer(use_jax) (PR 3), xp/grid mismatch ValueError (PR 4). Issue #334 closed.
