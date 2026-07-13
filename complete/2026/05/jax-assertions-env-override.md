## jax-assertions-env-override
- completed: 2026-05-07
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/24
- repos: autofit_workspace_test
- notes: |
    Cluster G of the recent release-prep triage.
    scripts/jax_assertions/fitness_dispatch.py crashed with
    `AttributeError: Analysis has no attribute _jitted_fit_from`. User's
    hypothesis (library API drift / rename) was wrong — library is intact.
    Real bug: env_vars.yaml `defaults` set PYAUTO_DISABLE_JAX=1 globally,
    and Analysis.__init__ silently flips both use_jax and
    use_jax_for_visualization to False whenever that env var is set.
    fit_for_visualization then early-returns without caching
    _jitted_fit_from, and the next assertion fails. The four scripts in
    jax_assertions/ exist specifically to assert JAX behavior, so
    disabling JAX makes the assertions vacuous. Fix: add an env_vars.yaml
    override that unsets PYAUTO_DISABLE_JAX for the `jax_assertions/`
    pattern (substring match covers all four current scripts and future
    siblings). Per memory feedback_env_vars_yaml_overrides.md — env-var
    conflicts get fixed in env_vars.yaml, not via os.environ.pop in the
    script. Verified pre-fix repro under PYAUTO_DISABLE_JAX=1 and post-fix
    pass under runner-emulated env (all other defaults applied,
    DISABLE_JAX absent).
