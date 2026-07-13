# Remove the NSS nested sampler from PyAutoFit and retire its infrastructure

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoLens
- autolens_profiling
- PyAutoBuild
- PyAutoHeart
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Refactor: remove the NSS nested sampler from PyAutoFit and retire all its supporting infrastructure across the organism. Delete the autofit/non_linear/search/nest/nss module, the af.NSS export, the [nss] git+ direct-URL extra in pyproject.toml, and its tests. Strip the NSS handling out of PyAutoBuild's release.yml (the git+ footgun guard, the separate unittest_nss job, the nss test-dir ignore) and remove the NSS references from PyAutoHeart (the nss install smoke CI fixture and release_validation docs). Sweep the autofit/autolens workspace examples and tutorials, retire the autolens_profiling NSS runs, and close out the PyAutoMind nss_first_class_sampler epic and its issued prompts. NSS performance never warranted this infrastructure cost and it can return as a genuine pip install later; we no longer support it.

<!-- formalised by the Intake (Conception) Agent on 2026-07-11 from user-intake -->
