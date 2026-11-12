"""Suite-wide: no test reaches GitHub.

`lifecycle.py close` / `shadow-row` look up `gh pr view --json mergedBy` for
the merge-actor evidence. The env var turns that off for this process and every
subprocess a test starts; the tests that exercise the lookup pass a fake `gh`.
"""

import os

os.environ["LIFECYCLE_NO_GH"] = "1"
