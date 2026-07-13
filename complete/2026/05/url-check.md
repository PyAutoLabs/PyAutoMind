## url-check
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/508
- completed: 2026-05-15
- tool-pr: https://github.com/Jammy2211/admin_jammy/pull/21
- library-prs:
  - https://github.com/PyAutoLabs/PyAutoConf/pull/105
  - https://github.com/PyAutoLabs/PyAutoFit/pull/1265
  - https://github.com/PyAutoLabs/PyAutoArray/pull/309
  - https://github.com/PyAutoLabs/PyAutoGalaxy/pull/413
  - https://github.com/PyAutoLabs/PyAutoLens/pull/509
- workspace-prs:
  - https://github.com/PyAutoLabs/HowToFit/pull/7
  - https://github.com/PyAutoLabs/HowToGalaxy/pull/7
  - https://github.com/PyAutoLabs/HowToLens/pull/10
  - https://github.com/PyAutoLabs/autofit_workspace/pull/57
  - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/70
  - https://github.com/PyAutoLabs/autolens_workspace/pull/152
- notes: Cross-repo doc URL audit + cleanup driven by new admin_jammy/software/url_check/ tool. Audit before fixes 304 broken URLs across 12 PyAuto repos; after both waves 104 broken (200 fixed end-to-end). Remaining 104 are mostly external paywalled/dead links + ~10 internal readthedocs renames needing editorial decisions. Tool patterns hhttps typo, Jammy2211/rhayes777 → PyAutoLabs (libs+workspaces), /blob/release/ → /blob/main/, joshspeagle/nautilus → johannesulf/nautilus, rhayes777/PyAutoBuild → PyAutoLabs/PyAutoBuild, bokeh+numfocus CoC URLs, sphinx /en/main → /en/master, pyautofit.readthedocs.io page renames, workspace notebook reorganisations (overview/{simple,complex}/{fit,result} flattened; modeling/imaging/features/<x>.ipynb → imaging/features/<x>/modeling.ipynb), Colab badge target fixes. Special-cases Colab URLs via raw.githubusercontent.com check (Colab returns 200 even for dead refs). Surface one bug worth remembering Path(__file__).resolve() through admin_jammy's worktree symlink lands at canonical root — pass --root explicitly when fixing from a worktree (memory feedback_path_file_resolve_symlink).

## Original prompt

URL links to Google colabs are not correct, linking to broken colabs which dont run, for example
in the PyAutoLens docs:

https://pyautolens.readthedocs.io/en/latest/overview/overview_2_new_user_guide.html

Here:

CDD Imaging: For image data from telescopes like Hubble and James Webb, go to imaging/start_here.ipynb.


Can you scan all repos for all URLs and check they work, in particular making sure the google colab pages
that come up actrually run?