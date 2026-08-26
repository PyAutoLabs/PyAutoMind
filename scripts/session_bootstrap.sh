#!/usr/bin/env bash
# scripts/session_bootstrap.sh — make a remote session's environment correct,
# from anywhere, without depending on the SessionStart hook having fired.
#
# WHY THIS EXISTS
#
# `policy/session_start_hook.sh` is the right mechanism and does the real work.
# But Claude Code registers project hooks from the session's *project
# directory*, and a session scoped to several organs clones them side by side
# under that directory — so the project directory is their parent, which is not
# a repo, has no `.claude/`, and registers no hook at all. Every multi-repo
# remote session therefore came up on the container's Python 3.11: one minor
# below the floor this organism set for itself and below every CI leg, with
# mypy and flake8 reading the interpreter and judging code against 3.11 rules.
# Local-green/CI-red, over and over, for an environment reason no one could see
# from inside the session.
#
# The hook now installs a workspace-root fan-out when it detects that layout,
# which fixes the *next* session in a container. This script is the other half:
# the door anything can knock on to fix the session it is already in. It is
# idempotent and ~0.2s warm, so calling it defensively costs nothing.
#
#   bash PyAutoMind/scripts/session_bootstrap.sh          # ensure, quietly
#   bash PyAutoMind/scripts/session_bootstrap.sh --check  # report, change nothing
#
# `bin/pyauto-brain` calls it before dispatch, so every `/verb` is covered.
# Exits 0 whenever the session is usable — this is a bootstrap, never a gate.

set -u

MIND_DIR="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
HOOK="$MIND_DIR/policy/session_start_hook.sh"
VENV="${PYAUTO_SESSION_VENV:-$HOME/.pyauto/session-py312}"

say() { printf '[bootstrap] %s\n' "$*" >&2; }

py312_ready() {
    [ -x "$VENV/bin/python" ] \
        && "$VENV/bin/python" -c 'import sys; raise SystemExit(sys.version_info[:2] != (3, 12))' >/dev/null 2>&1 \
        && "$VENV/bin/python" -c 'import pytest, yaml, xdist' >/dev/null 2>&1
}

# Which interpreter will this tool actually run on?
#
# Not "what does its shebang say". The hook's own shims are `#!/bin/sh` plus
# `exec "<venv>/bin/<tool>"` wrappers — deliberately, because a symlink loses
# the venv — so sniffing `pytest`'s shebang answered `/bin/sh`, which is not an
# interpreter that can be asked a version. The probe then reported "interpreter
# undetermined" and, worse, SKIPPED the import check below: the check added
# precisely because a 3.12 pytest that cannot import PyYAML fails collection in
# a way that reads like broken source. So the two halves of the same fix
# cancelled — the wrapper that keeps the venv made the check that verifies the
# venv unreachable, and the session reported healthy either way.
#
# Follow the exec target, then sniff that.
resolve_interpreter() {
    local path="$1" hops=0 shebang target
    while [ -n "$path" ] && [ "$hops" -lt 10 ]; do
        shebang="$(head -c 256 "$path" 2>/dev/null | sed -n '1s|^#!\([^ ]*\).*|\1|p')"
        case "$shebang" in
            */sh|*/bash)
                target="$(sed -n 's|^exec "\([^"]*\)".*|\1|p' "$path" 2>/dev/null | head -1)"
                if [ -n "$target" ] && [ -x "$target" ] && [ "$target" != "$path" ]; then
                    path="$target"; hops=$((hops + 1)); continue
                fi
                ;;
        esac
        printf '%s' "$shebang"
        return 0
    done
}

# A repo declares deps beyond the base set in .claude/session-python.txt; the
# hook installs them and stamps a marker keyed to the file's checksum. Report
# per repo, because the failure they cause names a missing module or a missing
# binary and never says "environment" — and because a session that bootstrapped
# through this script runs one repo's hook unless it fans out (see below).
extras_state() {
    local extras repo marker root rc=0
    root="$(dirname "$MIND_DIR")"
    for extras in "$root"/*/.claude/session-python.txt; do
        [ -r "$extras" ] || continue
        repo="$(basename "$(dirname "$(dirname "$extras")")")"
        marker="$VENV/.extras-$(cksum <"$extras" | tr -d ' /')"
        if [ -e "$marker" ]; then
            say "$repo extras: installed"
        else
            say "$repo extras: declared but NOT installed — run this script with no arguments"
            rc=1
        fi
    done
    return "$rc"
}

shallow_repos() {
    local root repo out=""
    root="$(dirname "$MIND_DIR")"
    for repo in "$root"/*/; do
        [ -e "${repo}.git/shallow" ] && out="$out $(basename "$repo")"
    done
    printf '%s' "${out# }"
}

if [ "${1:-}" = "--check" ]; then
    rc=0
    if py312_ready; then
        say "python 3.12: OK ($VENV)"
    else
        say "python 3.12: MISSING — run this script with no arguments"; rc=1
    fi
    if [ -n "$(shallow_repos)" ]; then
        say "shallow clones: $(shallow_repos) — ancestry checks are unreliable"; rc=1
    else
        say "clones: full history"
    fi
    extras_state || rc=1
    # Check the OUTCOME, not the mechanism. The venv on PATH is one way to get
    # there; the hook also repoints /usr/local/bin/python{,3} and rebuilds the
    # uv tools on 3.12, and a session fixed that way is correct even though the
    # venv is not first on PATH. Asserting the mechanism reported a healthy
    # session as broken.
    # A tool's own --version says nothing about the interpreter it runs on, and
    # the interpreter is the whole question: mypy and flake8 read
    # sys.version_info and judge code against THAT version's rules. A 3.11 mypy
    # is why a session could be locally clean and red in CI. So resolve each
    # tool's shebang and ask the interpreter it names.
    for tool in python3 pytest mypy ruff flake8 black; do
        path="$(command -v "$tool" 2>/dev/null)" || true
        if [ -z "$path" ]; then
            say "$tool: not installed"; continue
        fi
        if [ "$tool" = "python3" ]; then
            interp="$path"
        else
            interp="$(resolve_interpreter "$path")"
        fi
        real=""
        [ -n "$interp" ] && [ -x "$interp" ] && real="$("$interp" -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null)"
        if [ -z "$real" ]; then
            # A compiled tool (ruff) has no interpreter to disagree with CI
            # about; say so rather than leaving a blank that reads like a fault.
            if [ "$(head -c 2 "$path" 2>/dev/null)" = "#!" ]; then
                say "$tool: $path (interpreter undetermined)"
            else
                say "$tool: $path (native binary — no interpreter)"
            fi
        elif [ "$real" = "3.12" ]; then
            # The right VERSION is not the same as a usable tool. uv installs
            # each tool in its own isolated environment, so a 3.12 pytest can
            # still be unable to import PyYAML — and then the suite exits on
            # collection ImportErrors that read like broken source rather than
            # like a broken environment. Only the two tools that must import
            # this workspace's code are checked; a linter needs no deps.
            case "$tool" in
                python3|pytest)
                    if missing="$("$interp" -c 'import importlib,sys; sys.stdout.write(" ".join(m for m in ("pytest","yaml","xdist") if not importlib.util.find_spec(m)))' 2>/dev/null)" \
                       && [ -n "$missing" ]; then
                        say "$tool: 3.12 but cannot import: $missing ($path) — it will fail collection, not the code"; rc=1
                        continue
                    fi
                    ;;
            esac
            say "$tool: 3.12 OK ($path)"
        else
            say "$tool: running on $real, not 3.12 ($path) — its results will disagree with CI"; rc=1
        fi
    done
    exit "$rc"
fi

[ -x "$HOOK" ] || { say "WARNING: canonical hook missing at $HOOK"; exit 0; }

# The hook is the single implementation; this script only decides when to run it
# and guarantees CLAUDE_CODE_REMOTE is what the hook keys off, since a caller
# reaching us from a non-hook context (a CLI verb, an agent) may not have it.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
    # A local developer box supplies its own interpreter; nothing to do.
    exit 0
fi

CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(dirname "$MIND_DIR")}" "$HOOK" || {
    say "WARNING: bootstrap incomplete; the session may be on the container's python"
    exit 0
}

# Then every OTHER organ's own copy of the hook. A repo's declared deps are read
# from the repo whose hook is RUNNING, and the canonical hook above derives that
# from its own path — PyAutoMind. So a session bootstrapped through this script
# installed PyAutoMind's declared deps and nobody else's, which is the whole
# multi-repo case. Measured: PyAutoHands declares `ipynb-py-convert` + `Pillow`,
# and without them 14 of its 406 tests fail on a missing module or a missing
# binary, in a session whose bootstrap said it had succeeded.
#
# This is what the workspace-root fan-out does where it exists — but it is
# written INTO a container, and every first session in a fresh container is one
# the fan-out has never run in. Each hook is idempotent (~0.2s warm), so doing it
# here unconditionally costs about a second and removes the dependency.
root="$(dirname "$MIND_DIR")"
for repo in "$root"/*/; do
    [ "${repo%/}" = "$MIND_DIR" ] && continue
    hook="${repo}.claude/hooks/session-start.sh"
    [ -x "$hook" ] || continue
    CLAUDE_PROJECT_DIR="${repo%/}" "$hook" || say "WARNING: ${repo%/} hook failed"
done

# Make the fix apply to THIS process tree too, not only to shells the session
# starts after the env file is read. A caller that sources us gets the PATH; a
# caller that runs us gets the message.
# The env-file export only reaches shells the session starts afterwards. When
# there is no env file (a CLI verb, an agent shelling out), say how to fix the
# shell we are in — but only if it actually needs fixing.
if py312_ready && ! python3 -c 'import sys; raise SystemExit(sys.version_info[:2] != (3, 12))' >/dev/null 2>&1; then
    say "this shell still resolves $(command -v python3); run: export PATH=\"$VENV/bin:\$PATH\""
fi
exit 0
