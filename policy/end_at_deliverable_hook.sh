#!/usr/bin/env bash
# GENERATED — canonical source: PyAutoMind/policy/end_at_deliverable_hook.sh
# Installed into every checked-out repo as .claude/hooks/end-at-deliverable.sh by
# `python3 PyAutoMind/scripts/repos_sync.py --write`, and drift-checked by
# `--check`. Edit the canonical file, never a copy.
#
# ---------------------------------------------------------------------------
# Sessions end at their deliverable (PyAutoMind/policy/end_at_deliverable.md).
#
# A PreToolUse guard on the tools that outlive the turn. It exists because the
# prose rule was already written and was still broken twice: five batch members
# armed hourly check-ins on 2026-08-31 (fixed for batch members only), and on
# 2026-09-02/03 a mobile `/prm` re-armed a 60-minute `send_later` hourly from
# 02:39 to 12:11 UTC with no task active, leaving twenty fired one-shots and a
# drained usage window. A rule a session can talk itself past is not a rule, so
# this one is enforced by the harness.
#
# Registered under `hooks.PreToolUse` with the matcher
#   ^(send_later|subscribe_pr_activity|ScheduleWakeup|CronCreate|RemoteTrigger|Monitor|Bash|mcp__.*(send_later|subscribe_pr_activity).*)$
#
# Allowed through:
#   * `RemoteTrigger` with action list / get / list_runs / get_run_log — reading
#     what already exists never outlives the turn;
#   * `Monitor` running exactly the shift cockpit's stream
#     (`<abs>/PyAutoBrain/bin/pyauto-brain batch watch --stream --record
#     <abs>/PyAutoMind/batches/<slot>.md [--from N] [--for M] [--home DIR]`),
#     only from 30 min before that record's `dispatched:` to 45 min after its
#     `review-at:` (the carve-out in shift_cockpit_watch.md, human ruling
#     2026-11-16, PyAutoBrain#646);
#   * any other `Monitor` that names neither GitHub nor the watcher — a local
#     tail of a pilot run's log stays allowed;
#   * every foreground `Bash` call, and every background one that is not a loop
#     on GitHub — a one-shot `gh pr checks 12` is how a session reads CI;
#   * anything at all when PYAUTO_ALLOW_TIMERS=1 — the human-authorised escape
#     for a routine the human actually asked for.
#
# Refused, beyond the timer tools: a `Monitor` that names GitHub (`gh`, a
# fetching `git`, github.com, `claude agents`, `ci_verdict`) or opens a
# WebSocket; a `Monitor` that names `batch watch` or `orchestrator_watch` in any
# but the canonical form (a piped or wrapped stream is never let through); the
# stream outside its window or on a record it cannot read; and a background
# `Bash` loop (`while`/`until`/`watch`/`sleep`) that names GitHub. Known gap:
# the check is textual, so `gh` called from inside a local script passes it, as
# with scheduler_action_guard.py; the prose rule covers that case.
#
# Everything else exits 2 (the harness treats stderr as the reason and blocks
# the call). An unreadable payload also exits 2: this fails closed, because the
# failure it guards against is silent and costs a night of usage.
set -uo pipefail

# Human-authorised routine: the one way past this guard, and it has to be set
# deliberately in the environment.
[ "${PYAUTO_ALLOW_TIMERS:-}" = "1" ] && exit 0

payload="$(cat)"

# python3 rather than jq: python3 is present everywhere this hook is installed
# (it is what the SessionStart hook guarantees), jq is not. The payload rides in
# the environment rather than on stdin so the heredoc keeps its own stdin.
PYAUTO_HOOK_PAYLOAD="$payload" python3 <<'PY'
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

# Read-only RemoteTrigger actions: they inspect what exists and schedule nothing.
READ_ONLY_REMOTE_TRIGGER = {"list", "get", "list_runs", "get_run_log"}

REASON = (
    "policy end_at_deliverable: sessions end at their deliverable "
    "— {tool} would outlive the turn.\n"
    "Report and stop; the human re-runs /prm. Set PYAUTO_ALLOW_TIMERS=1 only "
    "for a routine the human asked for.\n"
)

# A watch on GitHub (CI, a review, a merge, a PR, an issue) or a remote feed.
WATCH_REASON = (
    "policy end_at_deliverable: sessions end at their deliverable "
    "— {what} would watch GitHub past the turn.\n"
    "Do not wait for CI in the session: read it once in the foreground "
    "(`gh pr checks <n>` or `ci_verdict.py`), report the verdict and hand "
    "back; the human re-runs /prm when it is green.\n"
    "The only watch a session may hold is the shift cockpit's stream, inside "
    "its window. PYAUTO_ALLOW_TIMERS=1 only for a routine the human asked "
    "for.\n"
)

# The cockpit stream asked for in the wrong form, or outside its shift.
STREAM_REASON = (
    "policy end_at_deliverable: sessions end at their deliverable "
    "— {what}.\n"
    "The only watch a session may hold is the shift cockpit's stream, inside "
    "its window: exactly `<abs>/PyAutoBrain/bin/pyauto-brain batch watch "
    "--stream --record <abs>/PyAutoMind/batches/<slot>.md [--from N] "
    "[--for M] [--home DIR]`, from 30 min before the record's dispatched: to "
    "45 min after its review-at:.\n"
    "If the shift is over, report the digest and stop; do not re-arm.\n"
)

STREAM_RE = re.compile(
    r"^(?P<cli>/\S+/PyAutoBrain/bin/pyauto-brain) batch watch --stream"
    r" --record (?P<rec>/\S+/PyAutoMind/batches/[A-Za-z0-9-]+\.md)"
    r"(?: --from \d+)?(?: --for \d+)?(?: --home /\S+)?$"
)
# Anything that reads the watcher's state: only the canonical stream may.
WATCHER_RE = re.compile(r"batch\s+watch|orchestrator_watch")
GITHUB_WATCH_RE = re.compile(
    r"(^|[\s;|&(`$\"'/])(gh\s|git(\s+-C\s+\S+)?\s+(fetch|pull|ls-remote|remote\s+update)\b)"
    r"|github\.com|claude\s+agents\b|ci[_-]verdict"
)
LOOP_RE = re.compile(r"\b(while|until|watch|sleep)\b")
KEY_RE = re.compile(
    r"^- (dispatched|review-at):\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)",
    re.M,
)
BEFORE = timedelta(minutes=30)   # before dispatched:
AFTER = timedelta(minutes=45)    # after review-at: (the late-sweep window, H2)


def block(tool):
    sys.stderr.write(REASON.format(tool=tool))
    raise SystemExit(2)


def refuse(template, what):
    sys.stderr.write(template.format(what=what))
    raise SystemExit(2)


def parse_utc(stamp):
    fmt = "%Y-%m-%dT%H:%M:%SZ" if stamp.count(":") == 2 else "%Y-%m-%dT%H:%MZ"
    return datetime.strptime(stamp, fmt).replace(tzinfo=timezone.utc)


def shift_window(record):
    """The (dispatched, review-at) pair of a shift record: the first of each key."""
    with open(record, encoding="utf-8") as handle:
        text = handle.read()
    keys = {}
    for key, stamp in KEY_RE.findall(text):
        keys.setdefault(key, stamp)
    start, end = parse_utc(keys["dispatched"]), parse_utc(keys["review-at"])
    if end < start:
        raise ValueError("review-at before dispatched")
    return start, end


def check_monitor(tool_input):
    if tool_input.get("ws") is not None:
        refuse(WATCH_REASON, "a WebSocket Monitor")
    cmd = str(tool_input.get("command") or "").strip()
    stream = STREAM_RE.match(cmd)
    if stream:
        try:
            start, end = shift_window(stream["rec"])
        except Exception:
            # Fail closed: a window the hook cannot read is one it cannot clear.
            refuse(STREAM_REASON, "a shift stream on an unreadable shift record")
        now = datetime.now(timezone.utc)
        if not os.path.isfile(stream["cli"]):
            refuse(STREAM_REASON, "a shift stream from a CLI that does not exist")
        if start - BEFORE <= now <= end + AFTER:
            raise SystemExit(0)
        refuse(STREAM_REASON,
               "a shift stream outside its window (the shift has ended or not begun)")
    if WATCHER_RE.search(cmd):
        refuse(STREAM_REASON, "a Monitor on the shift watcher in a non-canonical form")
    if GITHUB_WATCH_RE.search(cmd):
        refuse(WATCH_REASON, "a Monitor on GitHub")
    raise SystemExit(0)  # H3a: a local watch (a pilot run's log) stays allowed


def check_bash(tool_input):
    background = tool_input.get("run_in_background")
    if isinstance(background, str):
        background = background.strip().lower() == "true"
    if background is not True:
        raise SystemExit(0)  # a foreground call ends inside the turn
    cmd = str(tool_input.get("command") or "")
    if GITHUB_WATCH_RE.search(cmd) and LOOP_RE.search(cmd):
        refuse(WATCH_REASON, "a background Bash loop on GitHub")
    raise SystemExit(0)


try:
    event = json.loads(os.environ.get("PYAUTO_HOOK_PAYLOAD", ""))
    if not isinstance(event, dict):
        raise ValueError("PreToolUse payload is not a JSON object")
    tool = event.get("tool_name")
    if not isinstance(tool, str) or not tool:
        raise ValueError("PreToolUse payload carries no tool_name")
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
except Exception:
    # Fail closed. A payload this hook cannot read is a call it cannot clear.
    block("an unreadable tool call")

if "RemoteTrigger" in tool:
    action = tool_input.get("action")
    if isinstance(action, str) and action in READ_ONLY_REMOTE_TRIGGER:
        raise SystemExit(0)

if tool == "Monitor":
    check_monitor(tool_input)

if tool == "Bash":
    check_bash(tool_input)

block(tool)
PY
