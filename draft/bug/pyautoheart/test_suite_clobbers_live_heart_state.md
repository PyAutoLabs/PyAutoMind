# PyAutoHeart's test suite writes into the user's live ~/.pyauto-heart state

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

Running PyAutoHeart's own unit tests overwrites the developer's **live** Heart state.
`tests/test_test_run.py` calls `tr.run(results_dir=tmp_path)` (lines 48, 61, 69, 101, 110) and
never isolates `HEART_STATE_DIR`. `heart/checks/test_run.py:36` resolves `HEART_STATE_DIR` at
import time (env or `~/.pyauto-heart` default), and `:231` unconditionally does
`state.atomic_write_json(HEART_STATE_DIR / "test_run.json", summary)`. So `tmp_path` isolates the
*input* (`results_dir`) but not the *output*: the summary lands in the real state dir.

**Measured 2026-07-15 (on `main`, not a feature branch).** Running `pytest tests/test_test_run.py`
replaced a 10,234-byte real `test_run.json` with this 251-byte fixture — the last test to run wins:

    {"cloud_url": "U", "failed": 0, "parked_stale": [], "parked_stale_count": 0,
     "passed": 0, "per_project": {}, "ready": true, "run_label": "cloud#9",
     "skipped": 0, "source": "cloud", "timeout": 0, "ts": "2026-06-25T00:00:00Z"}

Proven by pointing `HEART_STATE_DIR` at a sandbox and re-running that file alone: the same stub
appears there. With the variable unset — the normal case for anyone running `pytest` in this repo —
the target is `~/.pyauto-heart/`.

**Impact, measured not reasoned.** Two of the three legs currently holding Heart at YELLOW read
from `test_run`. Re-aggregating with the stub in place:

    before:  yellow score 60  — "workspace validation not passing (3 failed, 2026-07-09T09-48-30Z)"
                              — "58 stale parked script(s)"
    after:   stale  score 70  — "test run stale (20d old)"

Both real reasons **disappear**, replaced by a bogus one. **It is not a fake-GREEN today** — the
fixture's hardcoded `ts` (2026-06-25) reads as 20d old, past `TEST_STALE_DAYS=10`, so the verdict
degrades to STALE and still blocks the GREEN-gated nightly. That is luck, not design: a fixture
with a fresh `ts` would clear the leg outright. Do not treat "it only goes STALE" as the safety
property.

The real damage is **evidence destruction**. The stub wipes the 3 recorded failures and the entire
58-entry `parked_stale` list — which is exactly the hygiene-triage input for the other open YELLOW
leg. On 2026-07-15 this was recoverable only because `~/.pyauto-heart/state.json` still held a
pre-clobber copy of the block (restored from it, back to a byte-identical 10,234 bytes). **Had a
`tick` re-aggregated between the pytest run and the restore, `state.json` would have been
overwritten too and the data would be gone permanently.**

## Fix direction (design first — do not assume)

The obvious `monkeypatch.setenv("HEART_STATE_DIR", tmp_path)` in the test only fixes *this* test
file. Prefer removing the trap over documenting it:

- **Is the write in `tr.run()` the actual defect?** A `run(results_dir=...)` that also performs a
  hidden write to a *global* path is doing two jobs. Consider having `run()` return the summary and
  letting the CLI entrypoint persist it — then the tests cannot pollute anything because there is
  nothing to pollute.
- **Sweep for siblings.** `heart/checks/` resolves `HEART_STATE_DIR` at import in several modules;
  find every check whose test path can reach a module-level-resolved write. `test_run` was found by
  accident, so assume it is not alone. `git status`-style proof: run each test file with
  `HEART_STATE_DIR` sandboxed and list what appears.
- **An autouse fixture** in `tests/conftest.py` pointing `HEART_STATE_DIR` at `tmp_path` for the
  whole suite is a cheap belt-and-braces backstop, but it hides the design smell rather than fixing
  it — decide deliberately whether to do both.

## Constraints

- Heart's state dir is the **input to the release gate**. Anything that can silently rewrite it
  with passing values is a release-safety issue, not a tidiness issue — hence Priority: high.
- Verify any fix by running the full suite with `HEART_STATE_DIR` **unset** against a throwaway
  `HOME`, and diffing the state dir before/after. "No test writes it" must be measured, not argued.

<!-- filed 2026-07-15 from a live incident: triggered while running the suite for PyAutoHeart#76/PR#77 -->
