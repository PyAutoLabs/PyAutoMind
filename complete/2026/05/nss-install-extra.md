## nss-install-extra
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1276
- completed: 2026-05-16
- library-prs:
  - PyAutoFit: https://github.com/PyAutoLabs/PyAutoFit/pull/1277
- notes: |
    Phase 4 of nss_first_class_sampler. `pip install autofit[nss]` is now the
    single safe install command for af.NSS — replaces the multi-step install
    saga documented in FINDINGS_v3.md.

    Approach: Option C from the prompt (pyproject.toml extra with pinned
    git+ URLs). Original prompt recommended Option A (full vendoring of
    ~1300 LOC) — investigation revealed modern pip 23+ handles URL-direct
    deps cleanly, so the lighter Option C path was feasible without
    ongoing re-vendor maintenance burden.

    Critical pin: handley-lab/blackjax at SHA `ef45acd2f` (the May 2026
    "Merge PR #60 — double_compile" commit). HEAD added `numpy>=1.25`
    which conflicts with autofit's `anesthetic==2.8.14` (numpy<2.0).
    Bump only when the anesthetic numpy cap moves (likely with Python 3.13
    anesthetic>=2.9 takeover).

    Validation: pytest test_autofit 1258 passed/1 skipped; fresh-venv
    `pip install -e PyAutoFit[nss]` completes in ~3 min on Python 3.12 with
    no resolver conflict; `af.NSS()` + `blackjax.ns.adaptive.init` smoke
    pass. New CI workflow runs the fresh-venv install + import smoke on
    every PR + Sunday 03:00 UTC cron — catches upstream drift past the
    pinned SHAs.

    Updated af.NSS ImportError text to reference `pip install autofit[nss]`
    instead of the manual `git+https://...` recipe. Phase 1's NSS unit
    test's `pytest.raises(match=...)` regex still matches the new text.

    Roadmap status: Phases 0-4 shipped. Only Phase 5 remains (workspace
    tutorial scripts — autolens_workspace/searches/nss.py +
    autogalaxy/autofit cookbook entries).
