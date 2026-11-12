#!/usr/bin/env bash
# prompt_sync.sh — keep PyAutoMind in sync with origin during task lifecycle.
#
# Sourced by skills that mutate PyAutoMind registry files (active.md,
# planned.md, queue.md, the complete/ records, ...) so we never accumulate local-only
# changes that drift from origin.
#
#   source PyAutoMind/scripts/prompt_sync.sh
#   prompt_sync_new_prompts                       # commit + push new prompt files
#   prompt_sync_push "prompt: <subject>" <path>...  # commit + push ONLY these paths
#
# Paths are relative to the Mind repo root (absolute paths inside it also work);
# a directory covers everything under it. A rename (`git mv`) needs BOTH sides.
# prompt_sync_push refuses, committing nothing, when no paths are given, when
# the tree has changes outside them (staged, unstaged or untracked), when a
# changed file holds conflict markers, or when a changed state.json does not
# parse. In a shared checkout another session's edits are never swept up.
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

# Push the checkout's CURRENT branch — never a hardcoded `main`.
#
# Both helpers below used to end in `git push origin main` regardless of what
# was checked out. `create_issue` step 6 and `start_dev` step 7 both instruct an
# agent to call them, so a branch-scoped session (a cloud session with a
# designated branch, or any PR-based flow) that followed the documented steps
# verbatim pushed Mind straight to `main`, bypassing review entirely.
#
# Pushing HEAD leaves the single-branch laptop flow byte-identical — there the
# current branch IS `main` — while making a branch-scoped checkout do the right
# thing instead of the dangerous thing.
_prompt_sync_push_current() {
  local branch
  branch=$(git -C "$PROMPT_REPO" rev-parse --abbrev-ref HEAD 2>/dev/null)
  if [ -z "$branch" ] || [ "$branch" = "HEAD" ]; then
    echo "prompt_sync: refusing to push from a detached HEAD in $PROMPT_REPO" >&2
    echo "  check out a branch first." >&2
    return 1
  fi
  git -C "$PROMPT_REPO" push -u origin "$branch"
}

# Commit and push any new untracked .md files at the repo root or under
# category dirs as one "sync new task ideas" commit. Each new file is listed
# individually in the commit body so the history shows which prompts arrived.
# Excludes active/ and complete/ (lifecycle dirs the skills move files into via
# prompt_sync_push, issue #71) and tmp/ (scratch). New draft prompts under
# draft/ are swept normally.
#
# Contract: new untracked prompt files ONLY. The commit names exactly those
# files (`git commit -- <files>`), so anything else already staged in a shared
# checkout stays staged and uncommitted.
prompt_sync_new_prompts() {
  _prompt_sync_require_repo || return 1
  local -a files=()
  local f
  while IFS= read -r -d '' f; do
    case "$f" in
      active/*|complete/*|tmp/*) continue ;;
    esac
    files+=("$f")
  done < <(git -C "$PROMPT_REPO" ls-files -z --others --exclude-standard \
             -- '*.md' '*/*.md')
  [ "${#files[@]}" -eq 0 ] && return 0

  echo "Found new prompt files to sync:"
  printf '  - %s\n' "${files[@]}"

  local body
  body=$(printf -- '- %s\n' "${files[@]}")

  git -C "$PROMPT_REPO" add -- "${files[@]}" || return 1
  git -C "$PROMPT_REPO" commit \
    -m "$(printf 'prompt: sync new task ideas\n\n%s\n' "$body")" \
    -- "${files[@]}" || return 1
  _prompt_sync_push_current
}

# Print the one-line refusal reason; each caller then returns 1 itself.
_prompt_sync_refuse() {
  echo "prompt_sync_push: refusing, nothing committed: $*" >&2
}

# True when repo-relative path $1 is one of, or under one of, the given paths.
_prompt_sync_in_scope() {
  local path="$1" given
  shift
  for given in "$@"; do
    if [ "$path" = "$given" ] || [ "${path#"$given"/}" != "$path" ]; then
      return 0
    fi
  done
  return 1
}

# Commit ONLY the given paths, then push the current branch. Used by skills at
# task milestones (issue filed, repos registered, task shipped, etc.):
#
#   prompt_sync_push "prompt: <subject>" active.md active/<file>.md
#
# Refuses (returns 1, commits nothing, one-line reason on stderr) when:
#   - no paths are given;
#   - `git status --porcelain` shows any change outside the paths: staged,
#     unstaged or untracked-not-ignored, including the source side of a staged
#     rename (or an unmerged path anywhere);
#   - a changed file in the paths holds conflict markers: a line starting
#     `<<<<<<< ` AND a line starting `>>>>>>> `. A lone `=======` never counts,
#     because Markdown setext headings underline with it;
#   - a changed `state.json` does not parse as JSON.
# Still a no-op (returns 0, no commit, no push) when nothing in the paths changed.
prompt_sync_push() {
  _prompt_sync_require_repo || return 1
  if [ "$#" -lt 2 ]; then
    _prompt_sync_refuse "no paths given (usage: prompt_sync_push <message> <path> [path...])"
    return 1
  fi
  local subject="$1"
  shift

  local repo_root
  repo_root=$(git -C "$PROMPT_REPO" rev-parse --show-toplevel) || return 1

  # Normalise each path to repo-relative form.
  local -a paths=()
  local p
  for p in "$@"; do
    case "$p" in
      "$repo_root"/*) p="${p#"$repo_root"/}" ;;
      "$PROMPT_REPO"/*) p="${p#"$PROMPT_REPO"/}" ;;
    esac
    while [ "${p#./}" != "$p" ]; do p="${p#./}"; done
    while [ "${p%/}" != "$p" ]; do p="${p%/}"; done
    case "$p" in
      ""|.|/*|..|../*|*/..|*/../*)
        _prompt_sync_refuse "path '$1' is not a file or directory inside the Mind repo"
        return 1 ;;
    esac
    paths+=("$p")
    shift
  done

  # Every change in the tree must sit inside the given paths. Porcelain v1 -z:
  # "XY path\0", and a rename/copy is followed by "origpath\0".
  local entry xy path orig
  local -a changed=() outside=()
  while IFS= read -r -d '' entry; do
    xy="${entry:0:2}"
    path="${entry:3}"
    orig=""
    case "$xy" in
      R*|C*) IFS= read -r -d '' orig ;;
    esac
    case "$xy" in
      DD|AU|UD|UA|DU|AA|UU)
        _prompt_sync_refuse "unmerged path '$path'; finish the merge or rebase first"
        return 1 ;;
    esac
    if _prompt_sync_in_scope "$path" "${paths[@]}"; then
      changed+=("$path")
    else
      outside+=("$path")
    fi
    if [ -n "$orig" ] && [ "${xy:0:1}" = "R" ] \
        && ! _prompt_sync_in_scope "$orig" "${paths[@]}"; then
      outside+=("$orig (rename source of $path)")
    fi
  done < <(git -C "$PROMPT_REPO" status --porcelain -z --untracked-files=all)

  if [ "${#outside[@]}" -gt 0 ]; then
    _prompt_sync_refuse "${#outside[@]} change(s) outside the given paths, e.g. '${outside[0]}'; pass them or leave them to their owner"
    return 1
  fi
  [ "${#changed[@]}" -eq 0 ] && return 0

  # Content checks on what is about to be staged (the worktree copy: `git add`
  # makes the index match it for every changed path).
  local f
  for f in "${changed[@]}"; do
    [ -f "$repo_root/$f" ] || continue
    if grep -q '^<<<<<<< ' "$repo_root/$f" && grep -q '^>>>>>>> ' "$repo_root/$f"; then
      _prompt_sync_refuse "conflict markers in '$f'"
      return 1
    fi
    if [ "${f##*/}" = "state.json" ] \
        && ! python3 -c 'import json, sys; json.load(open(sys.argv[1]))' \
             "$repo_root/$f" >/dev/null 2>&1; then
      _prompt_sync_refuse "'$f' does not parse as JSON"
      return 1
    fi
  done

  # Stage only the given paths. A path already gone from both worktree and
  # index (the source of a `git mv`) is staged already; `git add` would reject it.
  local -a to_add=()
  for p in "${paths[@]}"; do
    if [ -e "$repo_root/$p" ] \
        || [ -n "$(git -C "$PROMPT_REPO" ls-files -- "$p")" ]; then
      to_add+=("$p")
    fi
  done
  if [ "${#to_add[@]}" -gt 0 ]; then
    git -C "$PROMPT_REPO" add -- "${to_add[@]}" || return 1
  fi

  # Still a no-op when nothing is staged — the early return must come BEFORE the
  # push, or a caller with no changes would push anyway.
  if git -C "$PROMPT_REPO" diff --cached --quiet; then
    return 0
  fi

  # Belt and braces against a concurrent writer between the check and the
  # commit: the index must hold nothing outside the paths (both rename sides).
  local -a staged=()
  while IFS= read -r -d '' f; do
    if ! _prompt_sync_in_scope "$f" "${paths[@]}"; then
      _prompt_sync_refuse "'$f' was staged outside the given paths"
      return 1
    fi
    staged+=("$f")
  done < <(git -C "$PROMPT_REPO" diff --cached --name-only --no-renames -z)

  # Commit with an explicit pathspec (`--only`), so anything staged after the
  # check above stays staged and never rides along in this commit.
  git -C "$PROMPT_REPO" commit -m "$subject" -- "${staged[@]}" || return 1
  _prompt_sync_push_current
}
