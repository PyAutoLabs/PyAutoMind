## mass-field-reduce
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/76 (closed completed 2026-09-19)
- completed: 2026-09-19
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/77 (merge 0d284fa7)
- pending-release: PyAutoReduce@https://github.com/PyAutoLabs/PyAutoReduce/pull/77
- epic: mass-field (consumer sweep)
- summary: Migrated the B1938 and SLACS1430 PyAutoReduce prototypes to a top-level MassField and `fields=` collection. The SLACS posterior summary now reads from `fields.shear`. Both scripts compiled; a live model/tracer witness passed; `pytest test_autoreduce -q` passed with 299 tests and 3 skips. Python 3.12 and 3.13 GitHub tests passed. The PR merged on 2026-09-19; publication remains pending.
