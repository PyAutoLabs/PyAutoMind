# HowToLens smoke (3.13) red: `tutorial_searches.py` cannot import `zeus`

Type: bug
Target: HowToLens
Repos:
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Filed: 2026-10-22
Blocks: HowToLens#99 (point-plots-yaml-keys, which changes only `config/visualize/plots.yaml`)

## Original request (verbatim)

"doing it in anothr chat just wrap up the prs" (the /prm wrap-up hit this red leg; the human chose a re-run, which failed the same way)

## Evidence

- PR HowToLens#99, head f44030be, run 39754010580. The `smoke / smoke (3.13)` job failed on the first attempt and again on a `--failed` re-run (2026-10-22 20:04Z):
  `scripts/chapter_optional/tutorial_searches.py ... FAIL RuntimeError: ...: Zeus requires importable module zeus: No module named 'zeus'`
- The `smoke (3.12)` leg passes. Its install log shows `zeus-mcmc==2.5.4` being collected (from autogalaxy dev). PyAutoFit `pyproject.toml:88` pins `zeus-mcmc==2.5.4`.
- The 3.13 leg restores a cached environment (key `pyauto-jax-Linux-py3.13-jaxlib0.11.2-e1-…`). The cached env, or the 3.13 install path, appears to lack zeus.
- HowToLens main smoke was last green 2026-10-18. No HowToLens main run since, so main is probably red too.

## Ask

Find why zeus is not importable on the 3.13 smoke leg. Candidates: a stale or shared cache epoch, an optional-dependency extra not installed on 3.13, or zeus-mcmc failing to import on 3.13. Fix it at the source (cache key or epoch, or the install step). Do not skip the tutorial. Then re-run HowToLens#99's smoke and `/prm` it. Check whether other workspaces with a 3.13 leg share the cache and have the same gap.
