## colab-maturity
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/124 (left open as phase tracker for colab-link-rot)
- completed: 2026-07-09
- library-pr: PyAutoConf#120 + PyAutoBuild#125 + PyAutoHeart#44 (all merged 2026-07-09)
- note: Colab maturity phase 1. setup_colab rewritten around a _PROJECTS registry (6 notebook repos, for_autofit/for_howto* added, GPU-detect + import-time-env-mutation fixes, --depth 1 tag-pinned clones, first 15 unit tests); build_util.inject_colab_setup() injects the setup cell into every generated notebook (coverage 9/489 -> all at next release, hand-written setups skipped, unknown project raises); url_check.sh forbids blob/main + workspace chapter_* Colab URL forms (Monday sweep intentionally red until phase 2). Census in issued/colab_maturity.md.

## Original prompt

# Colab infrastructure: census follow-up — polish, mature, maintainable

Status: prompt

## Original request (verbatim)

> We have most of the infrastructure in place to make workspace exampels and
> tutorials run in Google colab, such that users can mess around with
> everything without installation. This includes docs pointing to them, links
> on our README.md, etc. But, the infrastructure could be developed in a more
> mature and robust way, including better on going maintenance during release
> and whatnot. Given we only have Fable access until Sunday, can you do a
> census of the Google Colab setup for all projects and do the work to make it
> more polished, mature and maintainable?

## Census findings (2026-07-09)

The Colab stack today:

1. `PyAutoConf/autoconf/setup_colab.py` — runtime bootstrap (`for_autolens`,
   `for_autogalaxy` only). Installs the stack `--no-deps`, clones the
   workspace `main` HEAD, pushes config paths.
2. Hand-written Colab setup cells in exactly **9 / 489** notebooks (6
   autolens + 3 autogalaxy `start_here` scripts). autofit_workspace, HowToFit,
   HowToGalaxy, HowToLens: zero.
3. `PyAutoBuild/autobuild/bump_colab_urls.sh` — release-time tag bumper,
   tested, wired into `release.yml` (`release_workspaces` +
   `bump_library_colab_urls`), rehearsal-aware. Only bumps canonical
   date-tagged `PyAutoLabs/<repo>` URLs.
4. PyAutoHeart central `url-check.yml` (Monday cron) — offline forbidden
   patterns (`url_check.sh`) + live Colab→raw 404 audit
   (`url_check_live.py`) with per-repo `.url_check_allowlist.txt`.
5. Entry links in the 3 library READMEs/docs, 3 workspace READMEs, and HowTo
   chapter pages, pinned to the current tag.

### Defects / gaps

- **Coverage**: docs link 100+ notebooks to Colab (all HowTo chapters in
  PyAutoLens/PyAutoGalaxy docs, PyAutoFit README badge →
  `overview_1_the_basics.ipynb`) but only the 9 start_here notebooks have a
  setup cell — everything else dies on `ModuleNotFoundError`. No
  `for_autofit` or HowTo* helpers exist. `generate.py` does plain py→ipynb,
  no injection.
- **Link rot, allowlisted instead of fixed**:
  - HowToLens chapter READMEs (scripts/ + notebooks/): 71 unpinned
    `blob/main` Colab URLs — the bumper never touches them.
  - HowToGalaxy chapter READMEs: 28 URLs point at the **wrong repo**
    (`autogalaxy_workspace/.../chapter_*` instead of `HowToGalaxy/...`) —
    dead, yet re-bumped every release.
  - Dead filenames: `tutorial_11_adapt_regularization.py.ipynb` (actual:
    `tutorial_11_adaptive_regularization.ipynb`), `tutorial_3_pixelizations`
    (actual: `tutorial_1_pixelizations`), `tutorial_6_modeling` (actual:
    `tutorial_6_lens_modeling`), removed `chapter_optional` tutorials still
    linked from PyAutoLens/PyAutoGalaxy docs.
  - `euclid_strong_lens_modeling_pipeline/README.md` has a forbidden
    `Jammy2211` Colab URL.
  - Allowlist colab entries are themselves stale (frozen at `2026.5.14.2`
    forms that no longer match the files).
- **`setup_colab.py` defects**: `no_gpu` unbound if JAX returns no devices,
  and only the last device's status counts; module-level
  `os.environ['XLA_FLAGS']` mutation on import; duplicated package lists;
  clones workspace `main` HEAD (version skew vs pip-installed release and the
  tagged notebook), no `--depth 1`; no tests in `test_autoconf/`.
- **Guard gaps**: `url_check.sh` doesn't forbid unpinned `blob/main` Colab
  URLs; nothing asserts a Colab-linked notebook can bootstrap itself.

## The work

1. **PyAutoConf** — generalize `setup_colab` into a single parameterized
   registry covering autofit / autogalaxy / autolens / HowToFit / HowToGalaxy
   / HowToLens; fix the `no_gpu` bug; move the env mutation inside the setup
   function; one shared package table; clone the tag matching the installed
   release (`--branch <version> --depth 1`, fallback `main`); unit tests.
2. **PyAutoBuild** — inject a standard Colab setup cell (markdown + code) into
   every generated notebook at `generate.py` / `build_util.py_to_notebook`
   time, parameterized per project; handle the 9 scripts with hand-written
   sections (strip or skip); tests; document the end-to-end Colab
   architecture in `docs/internals.md`.
3. **Workspaces + HowTo repos (6)** — remove/align hand-written setup
   sections, regenerate notebooks, fix chapter README URLs (right repo,
   tag-pinned, real filenames).
4. **Library docs (PyAutoFit / PyAutoGalaxy / PyAutoLens)** — fix dead Colab
   links (renamed/removed tutorials), then purge the now-fixed colab entries
   from every `.url_check_allowlist.txt`.
5. **PyAutoHeart** — extend `url_check.sh` forbidden patterns: unpinned
   `blob/main` (and non-date-tag) Colab URLs to the 6 notebook repos, so the
   bumper's blind spot can't recur. Keep the live sweep as the existence
   check.
6. **euclid_strong_lens_modeling_pipeline** — fix the `Jammy2211` Colab URL.

Release maintenance (bumper) already works; after this the only per-release
moving part remains the URL tag bump, and setup-cell coverage is guaranteed
by construction at generation time.
