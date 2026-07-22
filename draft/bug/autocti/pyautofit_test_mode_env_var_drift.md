# Bug: PYAUTOFIT_TEST_MODE is a dead env var — aggregator test-mode fixture is a silent no-op

Type: bug
Target: PyAutoCTI
Repos:
- PyAutoCTI
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

The canonical test-mode knob is **`PYAUTO_TEST_MODE`** (authoritatively read in
`PyAutoNerves/autonerves/test_mode.py:14` via `os.environ.get("PYAUTO_TEST_MODE", "0")`,
alongside `PYAUTO_TEST_MODE_SAMPLES`). **Nothing anywhere reads
`PYAUTOFIT_TEST_MODE`** — verified by grep across every library and workspace repo.

Two shippable sites:

1. **BUG — `PyAutoCTI/test_autocti/aggregator/conftest.py:15,17`.** An
   `@pytest.fixture(autouse=True) set_test_mode` sets and deletes
   `os.environ["PYAUTOFIT_TEST_MODE"]`. Because nothing reads that name, the
   whole aggregator test module *intends* to run in test mode but never enters
   it — a silent no-op. Fix: rename to `PYAUTO_TEST_MODE`. Note this may surface
   previously-masked behaviour in those tests (test mode changes output paths and
   bypasses sampling), so run the aggregator suite after the change.

2. **Misleading prose — `PyAutoFit/autofit/non_linear/analysis/visualize.py`**,
   `Visualizer.should_visualize` docstring point 5 says "If PyAutoFit test mode is
   on visualization is disabled". Naming the product rather than the variable is
   what leads readers to invent `PYAUTOFIT_TEST_MODE`. Fix: name
   `PYAUTO_TEST_MODE` explicitly.

Out of scope (local-only, no PR): two **gitignored** `.claude/settings.local.json`
allowlists (`euclid_strong_lens_modeling_pipeline`, `autogalaxy_workspace`) also
use the dead name, so those allowlisted commands run *without* test mode. Fix
locally, not in a PR.

Prior art / why this persisted: `autocti_workspace_test/AGENTS.md:42` and
`autocti_assistant/skills/ac_fit_cti_model.md:126` **already document** that
`PYAUTOFIT_TEST_MODE` does not exist. The trap was documented instead of deleted
— exactly the failure mode "delete the trap, don't document it" warns about. This
task deletes it.
