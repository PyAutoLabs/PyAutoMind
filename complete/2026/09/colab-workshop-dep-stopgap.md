## colab-workshop-dep-stopgap
- issue: n/a — workshop stopgap filed directly as PRs; tracked by PyAutoNerves#167
- completed: 2026-09-15
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/63
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/77
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/85
- summary: |
    Workshop-day (2026-09-15) stopgap: a Colab-only second `pip install --no-deps
    corner optax xxhash blackjax` cell added to all 100 notebooks carrying a setup
    cell (HowToFit 18, HowToGalaxy 32, HowToLens 50), because autofit imports these
    lazily and the released autonerves bootstrap did not install them. HowToFit #64
    (separate session) repointed the README badges at main so attendees reached it.
    All three PRs merged 2026-09-15; the workshop ran on them. The real fix is
    PyAutoNerves#168 (_SHARED_EXTRAS audit), merged on main and awaiting an
    autonerves PyPI release. The stopgap is being REVERTED by task
    `blackjax-reqs-stopgap-revert` (HowToFit#65; PRs HowToFit#66, HowToGalaxy#78,
    HowToLens#86), merge-gated on that release. Lesson: a stopgap in generated
    notebooks/ only reaches readers if the badges point where it landed; the durable
    lever was always the bootstrap list.
