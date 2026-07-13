## version-pinning-design-review
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/118 (closed)
- completed: 2026-07-09
- prs: PyAutoConf#119 + PyAutoBuild#121 (merged, gated order) — via child tasks
- notes: |
    Design review of stack-wide exact version pinning. Found: accidental
    2026.6.25.641-.649 series = scheduled release cron publishing
    run_number versions (no yank issue ever tracked); yanked .649 still
    recorded on all mains -> new-user pip path broken. Verdict: keep ==
    sibling pins; replace workspace exact-match with compatibility floor.
    Shipped: R2 floor check (version-check-compat-floor), R3-core
    wheels+tags-only (release-stamping-slim), R4 rehearsal gating (via
    PyAutoHeart#39). Q2: notebook/Colab cadence stays per-release.
    Rehearsal on new pipeline green (2026.7.8.1.dev65201, run 28973384455).
    OPEN human action (on the closed issue): flip vars.RELEASE_MODE=live or
    dispatch rehearsal=false for first real release -> realigns PyPI,
    unbreaks new users; then run workspace floor adoption + Heart
    version_skew rework (prompts filed in feature/).

## Original prompt

# Version-pinning design review: assess the pinned-version scheme against nightly builds

Type: research
Target: PyAutoBuild
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

We have this API which pins version numbers throughout the source code, with the motivation being it stops users from pairing a wrong version of the source code with the workspace. I think this is a good design, albeit it often breaks for users, and it means we have this version number throughout the code and workspace. We also ran into issues with me accidentally releasing some versions which I think are still in the source code — look at the GitHub history to find them, there was an issue about yanking their PyPIs. Can you review and assess if this high level design makes sense or if we can do it better? Also consider how we will basically have nightly build + release reinstated soon.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake -->
