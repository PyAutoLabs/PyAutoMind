#!/usr/bin/env bash
# prompt_sync.sh — keep PyAutoMind in sync with origin during task lifecycle.
#
# Sourced by skills that mutate PyAutoMind registry files (active.md,
# planned.md, queue.md, the complete/ records, ...) so we never accumulate local-only
# changes that drift from origin.
#
#   source PyAutoMind/scripts/prompt_sync.sh
#   prompt_sync_new_prompts                    # scan + commit + push new prompts
#   prompt_sync_push "prompt: <subject>"       # commit + push current state
#
# Both functions are no-ops when there is nothing to do, and safe to call
# multiple times in the same session.
#
# Replaces a now-removed admin_sync.sh helper that formerly operated on
# admin_jammy/prompt/. PyAutoMind is now the home of prompts and registry.

# An explicitly set PROMPT_REPO is always honoured as-is (a missing path then
# surfaces as a normal error rather than being silently redirected). Only when
# PROMPT_REPO is unset do we apply the default and the rename fallback below.
if [ -z "${PROMPT_REPO:-}" ]; then
  # Self-locating default: this script lives at <Mind checkout>/scripts/, so
  # its parent-of-parent IS the Mind repo — correct in the live workspace and
  # in any fork, whatever the workspace root is named.
  PROMPT_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

  # Backwards compatibility: before the PyAutoPrompt -> PyAutoMind rename the
  # repo lived at PyAutoLabs/PyAutoPrompt. If the resolved default is somehow
  # absent but a sibling PyAutoPrompt checkout exists, fall back to it so
  # sourcing still works.
  if [ ! -d "$PROMPT_REPO" ] && [ -d "$(dirname "$PROMPT_REPO")/PyAutoPrompt" ]; then
    PROMPT_REPO="$(dirname "$PROMPT_REPO")/PyAutoPrompt"
  fi
fi

# Fail loudly if PROMPT_REPO is not an actual git checkout. Without this the
# sync functions below silently no-op (git -C <missing> errors are swallowed and
# they return 0), so a missing or mis-set path would look like "nothing to sync"
# instead of a misconfiguration. Returns non-zero (we are sourced, never exit).
_prompt_sync_require_repo() {
  if ! git -C "$PROMPT_REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "prompt_sync: PROMPT_REPO is not a git checkout: $PROMPT_REPO" >&2
    echo "  set PROMPT_REPO to your PyAutoMind checkout, or clone it first." >&2
    return 1
  fi
}

# Commit and push any new untracked .md files at the repo root or under
# category dirs as one "sync new task ideas" commit. Each new file is listed
# individually in the commit body so the history shows which prompts arrived.
# Excludes active/ and complete/ (lifecycle dirs the skills move files into via
# prompt_sync_push, issue #71) and tmp/ (scratch). New draft prompts under
# draft/ are swept normally.
prompt_sync_new_prompts() {
  _prompt_sync_require_repo || return 1
  local untracked
  untracked=$(git -C "$PROMPT_REPO" ls-files --others --exclude-standard \
    -- '*.md' '*/*.md' \
    | grep -v '^active/' \
    | grep -v '^complete/' \
    | grep -v '^tmp/' \
    || true)
  [ -z "$untracked" ] && return 0

  echo "Found new prompt files to sync:"
  echo "$untracked" | sed 's/^/  - /'

  local body
  body=$(echo "$untracked" | sed 's/^/- /')

  ( cd "$PROMPT_REPO" && git add -- $untracked && \
    git commit -m "$(printf 'prompt: sync new task ideas\n\n%s\n' "$body")" && \
    git push origin main )
}

# Stage any modifications under the repo, commit with the given subject,
# and push. Used by skills at task milestones (issue filed, repos
# registered, task shipped, etc.). No-op if nothing is staged.
prompt_sync_push() {
  _prompt_sync_require_repo || return 1
  local subject="${1:-prompt: sync PyAutoMind}"
  ( cd "$PROMPT_REPO" && \
    git add -A && \
    if git diff --cached --quiet; then return 0; fi && \
    git commit -m "$subject" && \
    git push origin main )
}
