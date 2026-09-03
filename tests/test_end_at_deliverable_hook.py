"""The PreToolUse guard that makes "sessions end at their deliverable" real.

The prose rule existed and was broken twice — five batch members armed hourly
check-ins on 2026-08-31 (fixed for batch members only), then on 2026-09-02/03 a
mobile `/prm` re-armed a 60-minute `send_later` hourly from 02:39 to 12:11 UTC
with no task active. A rule a session can reason past is not a rule, so it is
enforced by the harness, and the enforcement is exercised here as the harness
runs it: the real script, in a subprocess, fed a real PreToolUse payload on
stdin, judged by its exit code.

Conventions, as in the sibling repos_sync tests: fictional fixtures only, and
every leg is driven with input that must trip it.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import repos_sync  # noqa: E402

MIND = Path(__file__).resolve().parents[1]
HOOK = MIND / repos_sync.DELIVERABLE_HOOK_FILE

# The first words of the two-line reason the harness shows the session.
REASON = "policy end_at_deliverable: sessions end at their deliverable"


def run(payload, env=None):
    """Drive the hook exactly as the harness does: JSON on stdin, exit code out.

    `payload` is sent verbatim when it is a string, so a malformed body can be
    tested; a dict is serialised.
    """
    if not isinstance(payload, str):
        payload = json.dumps(payload)
    return subprocess.run(
        [str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
    )


# --------------------------------------------------------------------------
# Blocked: everything that outlives the turn
# --------------------------------------------------------------------------

@pytest.mark.parametrize("tool", [
    "send_later",
    "subscribe_pr_activity",
    "ScheduleWakeup",
    "CronCreate",
    "mcp__scheduler__send_later",
])
def test_a_timer_tool_is_blocked_with_the_policy_reason(tool):
    result = run({"tool_name": tool, "tool_input": {}})
    assert result.returncode == 2, result
    assert REASON in result.stderr
    assert tool in result.stderr
    assert "would outlive the turn" in result.stderr


def test_the_reason_tells_the_session_what_to_do_instead():
    """Blocking without the alternative just produces a second attempt."""
    stderr = run({"tool_name": "send_later", "tool_input": {"minutes": 60}}).stderr
    assert "Report and stop; the human re-runs /prm." in stderr
    assert "PYAUTO_ALLOW_TIMERS=1" in stderr
    assert len(stderr.strip().splitlines()) == 2, stderr


def test_remote_trigger_create_is_blocked():
    """The scheduling half of RemoteTrigger is the half that outlives the turn."""
    result = run({"tool_name": "RemoteTrigger", "tool_input": {"action": "create"}})
    assert result.returncode == 2, result
    assert "RemoteTrigger" in result.stderr


@pytest.mark.parametrize("action", ["update", "run", "create_webhook_trigger"])
def test_the_other_writing_remote_trigger_actions_are_blocked(action):
    assert run(
        {"tool_name": "RemoteTrigger", "tool_input": {"action": action}}
    ).returncode == 2


# --------------------------------------------------------------------------
# Allowed
# --------------------------------------------------------------------------

@pytest.mark.parametrize("action", ["list", "get", "list_runs", "get_run_log"])
def test_read_only_remote_trigger_actions_pass(action):
    """Reading what already exists schedules nothing; blocking it would stop a
    session from even reporting what is armed."""
    result = run({"tool_name": "RemoteTrigger", "tool_input": {"action": action}})
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_the_human_authorised_escape_hatch_lets_a_timer_through():
    result = run({"tool_name": "send_later", "tool_input": {}},
                 env={"PYAUTO_ALLOW_TIMERS": "1"})
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_the_escape_hatch_is_exactly_one_and_not_any_truthy_value():
    """`PYAUTO_ALLOW_TIMERS=yes` from a half-remembered attempt must not open it."""
    assert run({"tool_name": "send_later", "tool_input": {}},
               env={"PYAUTO_ALLOW_TIMERS": "yes"}).returncode == 2
    assert run({"tool_name": "send_later", "tool_input": {}},
               env={"PYAUTO_ALLOW_TIMERS": "0"}).returncode == 2


# --------------------------------------------------------------------------
# Fail closed
# --------------------------------------------------------------------------

@pytest.mark.parametrize("payload", [
    "not json at all",
    "",
    "[]",                              # JSON, but not an object
    '{"tool_input": {}}',              # no tool_name
    '{"tool_name": 7, "tool_input": {}}',
])
def test_an_unreadable_payload_is_blocked(payload):
    """The failure this hook guards is silent and costs a night of usage, so a
    payload it cannot read is a call it cannot clear."""
    result = run(payload)
    assert result.returncode == 2, result
    assert REASON in result.stderr


def test_a_missing_tool_input_is_not_a_crash():
    """A tool called with no input at all is still a blocked timer, not a
    traceback the harness would report as a broken hook."""
    result = run({"tool_name": "CronCreate"})
    assert result.returncode == 2
    assert "Traceback" not in result.stderr


# --------------------------------------------------------------------------
# The matcher that decides which calls reach the hook at all
# --------------------------------------------------------------------------

@pytest.mark.parametrize("tool", [
    "send_later", "subscribe_pr_activity", "ScheduleWakeup", "CronCreate",
    "RemoteTrigger", "mcp__anything__send_later__x",
])
def test_the_registered_matcher_selects_every_timer_tool(tool):
    import re
    assert re.match(repos_sync.DELIVERABLE_HOOK_MATCHER, tool), tool


@pytest.mark.parametrize("tool", ["Bash", "Read", "Edit", "Task", "mcp__github__x"])
def test_the_matcher_leaves_ordinary_tools_alone(tool):
    """An over-broad matcher would run this hook on every call in the session."""
    import re
    assert not re.match(repos_sync.DELIVERABLE_HOOK_MATCHER, tool), tool
