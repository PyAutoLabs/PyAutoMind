"""Every Mind job that reads the Claude or App secret declares `mind-main`.

A dispatch runs the workflow file at the ref the caller picks, and old Mind
heads still carry pre-hardening copies (old_branch_workflow_secret_exposure).
The secrets live in the `mind-main` environment, deployable from `main` only,
so a job that reads them must declare it; otherwise it would fail on `main` once
the repo-level copies are gone, or the copies would have to stay where old refs
reach them (policy/github_tokens.md, "Old refs").
"""

import re
from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"
FILES = sorted(WORKFLOWS.glob("*.yml")) if WORKFLOWS.is_dir() else []
_NAMES = r"(CLAUDE_CODE_OAUTH_TOKEN|APP_PRIVATE_KEY)"
#: Any way an expression can reach a guarded secret: dotted or indexed (names
#: are case-insensitive), the whole context serialised, or inherited wholesale.
GUARDED = re.compile(
    rf"secrets\s*\.\s*{_NAMES}\b|secrets\s*\[\s*['\"]{_NAMES}['\"]\s*\]"
    r"|toJSON\(\s*secrets\s*\)|secrets:\s*inherit", re.I)


def _env_name(job):
    env = job.get("environment")
    return env.get("name") if isinstance(env, dict) else env


@pytest.mark.skipif(not FILES, reason="no workflows shipped here")
def test_every_job_reading_a_guarded_secret_declares_mind_main():
    missing = []
    for path in FILES:
        wf = yaml.safe_load(path.read_text())
        if GUARDED.search(yaml.safe_dump(wf.get("env") or {})):
            missing.append(f"{path.name}: workflow-level env")
        for name, job in (wf.get("jobs") or {}).items():
            if GUARDED.search(yaml.safe_dump(job)) and _env_name(job) != "mind-main":
                missing.append(f"{path.name}:{name}")
    assert not missing, f"guarded secret read outside `environment: mind-main`: {missing}"


@pytest.mark.parametrize("expr", [
    "${{ secrets.APP_PRIVATE_KEY }}", "${{ secrets.app_private_key }}",
    "${{ secrets['CLAUDE_CODE_OAUTH_TOKEN'] }}", "${{ toJSON(secrets) }}",
    "secrets: inherit"])
def test_the_scan_sees_every_spelling(expr):
    assert GUARDED.search(expr)


def test_the_scan_ignores_other_secrets():
    assert not GUARDED.search("${{ secrets.PYAUTO_UPDATE_WEBHOOK_URL }}")
