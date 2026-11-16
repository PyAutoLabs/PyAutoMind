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
from datetime import datetime, timedelta, timezone
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
    "RemoteTrigger", "mcp__anything__send_later__x", "Monitor", "Bash",
])
def test_the_registered_matcher_selects_every_timer_tool(tool):
    import re
    assert re.match(repos_sync.DELIVERABLE_HOOK_MATCHER, tool), tool


@pytest.mark.parametrize("tool", ["Read", "Edit", "Task", "BashOutput", "mcp__github__x"])
def test_the_matcher_leaves_ordinary_tools_alone(tool):
    """An over-broad matcher would run this hook on every call in the session."""
    import re
    assert not re.match(repos_sync.DELIVERABLE_HOOK_MATCHER, tool), tool


# --------------------------------------------------------------------------
# Codex PreToolUse wire shape
# --------------------------------------------------------------------------

def codex_payload(tool, tool_input):
    return {
        "session_id": "codex-session",
        "turn_id": "turn-1",
        "cwd": str(MIND),
        "hook_event_name": "PreToolUse",
        "tool_name": tool,
        "tool_use_id": "call-1",
        "tool_input": tool_input,
    }


def test_codex_payload_denies_a_timer():
    result = run(codex_payload("send_later", {"minutes": 60}))
    assert result.returncode == 2
    assert REASON in result.stderr


def test_codex_payload_allows_a_read_only_remote_trigger():
    result = run(codex_payload("RemoteTrigger", {"action": "list"}))
    assert result.returncode == 0
    assert result.stderr == ""


def test_codex_malformed_payload_is_still_fail_closed():
    result = run('{"turn_id":"turn-1","tool_input":{}}')
    assert result.returncode == 2
    assert REASON in result.stderr



# --------------------------------------------------------------------------
# The shift-cockpit carve-out (2026-11-16, PyAutoBrain#646): Monitor and
# background Bash. The one watch allowed is the cockpit's stream inside its
# window; any watch on GitHub is refused; local tails and one-shot reads pass.
# --------------------------------------------------------------------------

WATCH = "would watch GitHub past the turn"
STREAM = "The only watch a session may hold is the shift cockpit's stream"
# Fictional shift times, set relative to the real clock so the hook runs
# unpatched: the record's window is [dispatched - 30 min, review-at + 45 min].
SHIFT_LENGTH = timedelta(hours=2)


def stamp(moment):
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fixture_shift(tmp_path, *, dispatched=None, review_at=None, body=None):
    """A fictional workspace: the Brain CLI and one Mind shift record.

    Returns the canonical stream command for that record. Times default to a
    shift that is open now (dispatched an hour ago, review-at in an hour).
    """
    now = datetime.now(timezone.utc)
    dispatched = dispatched or now - timedelta(hours=1)
    review_at = review_at or dispatched + SHIFT_LENGTH
    cli = tmp_path / "ws" / "PyAutoBrain" / "bin" / "pyauto-brain"
    cli.parent.mkdir(parents=True)
    cli.write_text("#!/bin/sh\n")
    record = tmp_path / "ws" / "PyAutoMind" / "batches" / "2026-11-16-pm.md"
    record.parent.mkdir(parents=True)
    if body is None:
        body = (
            "# Batch 2026-11-16-pm\n"
            f"- dispatched: {stamp(dispatched)}      # fictional\n"
            f"- review-at: {stamp(review_at)}\n"
            "- brief:\n"
        )
    record.write_text(body)
    return f"{cli} batch watch --stream --record {record}"


def monitor(command=None, **extra):
    tool_input = {"description": "shift events", "timeout_ms": 1800000, **extra}
    if command is not None:
        tool_input["command"] = command
    return run({"tool_name": "Monitor", "tool_input": tool_input})


def bash(command, background):
    tool_input = {"command": command, "description": "x"}
    if background is not None:
        tool_input["run_in_background"] = background
    return run({"tool_name": "Bash", "tool_input": tool_input})


def allowed(result):
    return result.returncode == 0 and result.stderr == ""


# -- the stream: allowed only inside its window ------------------------------

def test_the_stream_is_allowed_mid_shift(tmp_path):
    assert allowed(monitor(fixture_shift(tmp_path)))


@pytest.mark.parametrize("flags", [
    " --from 42", " --for 28", " --from 0 --for 28",
    " --from 42 --for 28 --home /home/someone/.orchestrator",
])
def test_the_stream_with_its_canonical_flags_is_allowed(tmp_path, flags):
    assert allowed(monitor(fixture_shift(tmp_path) + flags))


def test_the_stream_is_allowed_29_minutes_before_dispatched(tmp_path):
    now = datetime.now(timezone.utc)
    assert allowed(monitor(fixture_shift(tmp_path, dispatched=now + timedelta(minutes=29))))


def test_the_stream_is_allowed_44_minutes_after_review_at(tmp_path):
    now = datetime.now(timezone.utc)
    review_at = now - timedelta(minutes=44)
    cmd = fixture_shift(tmp_path, dispatched=review_at - SHIFT_LENGTH, review_at=review_at)
    assert allowed(monitor(cmd))


def test_the_stream_is_refused_46_minutes_after_review_at(tmp_path):
    """The witness: the same record, the same command, the shift over."""
    now = datetime.now(timezone.utc)
    review_at = now - timedelta(minutes=46)
    cmd = fixture_shift(tmp_path, dispatched=review_at - SHIFT_LENGTH, review_at=review_at)
    result = monitor(cmd)
    assert result.returncode == 2
    assert "outside its window" in result.stderr
    assert STREAM in result.stderr
    assert "do not re-arm" in result.stderr


def test_the_stream_is_refused_31_minutes_before_dispatched(tmp_path):
    now = datetime.now(timezone.utc)
    result = monitor(fixture_shift(tmp_path, dispatched=now + timedelta(minutes=31)))
    assert result.returncode == 2
    assert "outside its window" in result.stderr


def test_minute_precision_record_keys_are_read(tmp_path):
    """Real briefs write `2026-11-14T19:50Z`, without seconds."""
    now = datetime.now(timezone.utc)
    body = (f"- dispatched: {now - timedelta(hours=1):%Y-%m-%dT%H:%MZ}\n"
            f"- review-at: {now + timedelta(hours=1):%Y-%m-%dT%H:%MZ}\n")
    assert allowed(monitor(fixture_shift(tmp_path, body=body)))


@pytest.mark.parametrize("body", [
    "# a record with no brief keys\n",
    "- dispatched: 2026-11-16T10:00Z\n",                      # no review-at
    "- dispatched: soon\n- review-at: later\n",
    "- dispatched: 2026-11-16T12:00Z\n- review-at: 2026-11-16T10:00Z\n",  # inverted
])
def test_the_stream_on_an_unreadable_record_fails_closed(tmp_path, body):
    result = monitor(fixture_shift(tmp_path, body=body))
    assert result.returncode == 2
    assert "unreadable shift record" in result.stderr


def test_the_stream_on_a_missing_record_fails_closed(tmp_path):
    cmd = fixture_shift(tmp_path).replace("2026-11-16-pm.md", "2026-11-17-am.md")
    assert monitor(cmd).returncode == 2


def test_the_stream_from_a_cli_that_does_not_exist_is_refused(tmp_path):
    cmd = fixture_shift(tmp_path).replace("/ws/PyAutoBrain/", "/elsewhere/PyAutoBrain/")
    assert monitor(cmd).returncode == 2


@pytest.mark.parametrize("wrap", [
    "{cmd} | grep --line-buffered NEEDS",        # piped
    "{cmd}; gh pr checks 12",                     # chained to GitHub
    "{cmd} && sleep 60",
    "cd /tmp && {cmd}",                           # something before it
    "{cmd} --watch-ci",                           # an unknown flag
    "bash -c '{cmd}'",                            # wrapped
])
def test_a_wrapped_or_piped_stream_is_refused(tmp_path, wrap):
    result = monitor(wrap.format(cmd=fixture_shift(tmp_path)))
    assert result.returncode == 2, result


def test_a_stream_from_a_relative_path_is_refused(tmp_path):
    fixture_shift(tmp_path)
    cmd = ("PyAutoBrain/bin/pyauto-brain batch watch --stream "
           "--record PyAutoMind/batches/2026-11-16-pm.md")
    result = monitor(cmd)
    assert result.returncode == 2
    assert "non-canonical form" in result.stderr


def test_the_raw_watcher_script_under_monitor_is_refused():
    assert monitor("python3 /x/PyAutoBrain/bin/orchestrator_watch.py --once").returncode == 2


# -- any other Monitor on GitHub is refused (H3a) ----------------------------

@pytest.mark.parametrize("cmd", [
    "gh pr checks 12 --watch",
    "gh run watch 123456",
    "while true; do gh api repos/o/r/issues/1/comments; sleep 30; done",
    "until python3 /x/PyAutoBrain/bin/ci_verdict.py --repo o/r --pr 12; do sleep 60; done",
    "while :; do python3 bin/ci-verdict o/r 12; sleep 60; done",
    "while true; do s=$(gh pr view 12 --json state); echo $s; sleep 30; done",
    "while true; do git fetch origin && git log -1 origin/main; sleep 60; done",
    "while true; do git -C /x/repo fetch -q; sleep 60; done",
    "while true; do curl -s https://api.github.com/repos/o/r/pulls/12; sleep 30; done",
    "bash -c \"gh pr checks 12 --watch\"",
    "claude agents --watch",
])
def test_a_monitor_on_github_is_refused_with_the_check_once_instruction(cmd):
    result = monitor(cmd)
    assert result.returncode == 2, result
    assert WATCH in result.stderr
    # The refusal says what to do instead: read CI once and hand back.
    assert "read it once in the foreground" in result.stderr
    assert "hand back" in result.stderr
    assert "/prm" in result.stderr


def test_a_websocket_monitor_is_refused():
    result = monitor(ws={"url": "wss://events.example.com/stream"})
    assert result.returncode == 2
    assert "WebSocket" in result.stderr


# -- local watches stay allowed (H3a) ----------------------------------------

@pytest.mark.parametrize("cmd", [
    "tail -f run.log | grep --line-buffered ERROR",
    "tail -F /home/someone/Science/active/pilot/output/run.log "
    "| grep -E --line-buffered 'elapsed|Traceback|Killed'",
    "inotifywait -m --format '%e %f' /tmp/out",
    "while true; do ls output | wc -l; sleep 5; done",
    "tail -f /x/autolens_workspace/scripts/log.txt",   # the word 'git' nowhere, 'log' is fine
    "tail -f pilot.log | grep --line-buffered 'git status'",
])
def test_a_local_monitor_is_allowed(cmd):
    assert allowed(monitor(cmd))


# -- Bash: one-shot reads pass; background GitHub loops do not (H3b) ---------

@pytest.mark.parametrize("cmd,background", [
    ("gh pr checks 12", None),
    ("gh pr checks 12", False),
    ("gh pr checks 12 --watch", False),     # foreground: it ends inside the turn
    ("python3 /x/PyAutoBrain/bin/ci_verdict.py --repo o/r --pr 12", False),
    ("until gh pr checks 12; do sleep 30; done", False),
    ("pytest tests -q", True),
    ("python3 pilot.py > run.log 2>&1", True),
    ("until grep -q Ready dev.log; do sleep 0.5; done", True),
    ("gh pr view 12 --json state", True),   # background but one-shot
])
def test_bash_that_does_not_loop_on_github_in_the_background_passes(cmd, background):
    assert allowed(bash(cmd, background))


@pytest.mark.parametrize("cmd", [
    "until gh pr checks 12; do sleep 30; done",
    "while true; do gh api repos/o/r/actions/runs; sleep 60; done",
    "gh pr checks 12 --watch",
    "gh run watch 123",
    "until python3 bin/ci_verdict.py --pr 12; do sleep 60; done",
    "while ! git fetch origin; do sleep 30; done",
])
def test_a_background_bash_loop_on_github_is_refused(cmd):
    result = bash(cmd, True)
    assert result.returncode == 2, result
    assert "background Bash loop on GitHub" in result.stderr
    assert "read it once in the foreground" in result.stderr


def test_a_string_run_in_background_is_read_as_the_flag():
    assert bash("until gh pr checks 12; do sleep 30; done", "true").returncode == 2


# -- the escape and the fail-closed paths still hold for the new tools -------

@pytest.mark.parametrize("payload", [
    {"tool_name": "Monitor", "tool_input": {"command": "gh pr checks 12 --watch"}},
    {"tool_name": "Monitor", "tool_input": {"ws": {"url": "wss://x"}}},
    {"tool_name": "Bash", "tool_input": {"command": "until gh pr checks 1; do sleep 9; done",
                                         "run_in_background": True}},
])
def test_the_escape_hatch_covers_the_new_branches(payload):
    assert allowed(run(payload, env={"PYAUTO_ALLOW_TIMERS": "1"}))


def test_a_malformed_monitor_payload_fails_closed():
    result = run('{"tool_name": "Monitor", "tool_input": ')
    assert result.returncode == 2
    assert REASON in result.stderr
