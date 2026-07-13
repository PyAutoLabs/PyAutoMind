## howtofit-bootstrap
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/38
- completed: 2026-04-22
- sub-prs:
  - sub-1 (HowToFit scaffold): https://github.com/PyAutoLabs/HowToFit/pull/1
  - sub-2 (remove howtofit/ from autofit_workspace + cross-refs): https://github.com/PyAutoLabs/autofit_workspace/pull/39
  - sub-3 (update PyAutoFit library URLs + docs/howtofit/): https://github.com/PyAutoLabs/PyAutoFit/pull/1231 (shipped as howtofit-docs-update)
  - sub-4 (register howtofit target in PyAutoBuild): https://github.com/PyAutoLabs/PyAutoBuild/pull/55 (shipped as howtofit-register)
- note: Umbrella task for the HowToFit extraction. Moved HowToFit from `autofit_workspace/scripts/howtofit/` into a standalone `PyAutoLabs/HowToFit` repository with its own CI, seeded by the existing chapter scripts/notebooks/config/dataset. All four sub-tasks merged on 2026-04-22. HowToFit is now built and released by the same PyAutoBuild pipeline as HowToGalaxy and HowToLens.
