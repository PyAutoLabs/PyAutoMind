# Version-pinning design review: assess the pinned-version scheme against nightly builds

Type: research
Target: PyAutoBuild
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

We have this API which pins version numbers throughout the source code, with the motivation being it stops users from pairing a wrong version of the source code with the workspace. I think this is a good design, albeit it often breaks for users, and it means we have this version number throughout the code and workspace. We also ran into issues with me accidentally releasing some versions which I think are still in the source code — look at the GitHub history to find them, there was an issue about yanking their PyPIs. Can you review and assess if this high level design makes sense or if we can do it better? Also consider how we will basically have nightly build + release reinstated soon.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake -->
