#!/usr/bin/env bash
# PyAutoMind registry status.
#
# Prints prompt inventory grouped by category, plus the current state of
# active.md / planned.md / complete.md.
#
# Usage:
#   bash PyAutoMind/scripts/status.sh [--full | --repos]
#
# Without args: counts + active task list + last 5 completed.
# With --full:  also lists every prompt under every category.
# With --repos: delegate to pyauto-status (cross-repo git sync dashboard).

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ "${1:-}" = "--repos" ]; then
  # shellcheck source=./pyauto_status.sh
  source "$ROOT/scripts/pyauto_status.sh"
  pyauto-status
  exit 0
fi

bold() { printf "\033[1m%s\033[0m\n" "$1"; }
dim()  { printf "\033[2m%s\033[0m\n" "$1"; }

# ---------- Counts per category ----------
#
# Prompt files run through three lifecycle states (issue #71):
#   draft/<work-type>/<target>/   not started (intaken, pre start_dev)
#   active/                        issued, in flight
#   complete/<YYYY>/<MM>/          shipped
# Draft prompts are organised by WORK TYPE (feature/, bug/, …) under draft/.
# Meta folders (z_features/, z_vault/, autoprompt/) keep their own names.
# See README "Prompt taxonomy".

WORK_TYPES=(feature bug refactor docs test release maintenance research experiment triage)
LIFECYCLE_DIRS=(active complete z_features z_vault autoprompt)

bold "== Draft prompts (by work type) =="
printf "%-35s %s\n" "category" "count"
printf "%-35s %s\n" "----------------------------------" "-----"

for dir in "${WORK_TYPES[@]}"; do
  if [ -d "$ROOT/draft/$dir" ]; then
    count=$(find "$ROOT/draft/$dir" -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    printf "%-35s %s\n" "draft/$dir/" "$count"
  fi
done

echo ""
bold "== Lifecycle / meta =="
for dir in "${LIFECYCLE_DIRS[@]}"; do
  if [ -d "$ROOT/$dir" ]; then
    count=$(find "$ROOT/$dir" -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    printf "%-35s %s\n" "$dir/" "$count"
  fi
done

echo ""

# ---------- Registry state files ----------

count_h2() {
  if [ -f "$1" ]; then
    awk '/^## /{n++} END{print n+0}' "$1"
  else
    echo 0
  fi
}
active_count=$(count_h2 "$ROOT/active.md")
planned_count=$(count_h2 "$ROOT/planned.md")
# complete/ records are the source of truth once split (issue #71); fall back to
# the legacy complete.md ledger until it is retired.
complete_count=$(find "$ROOT/complete" -type f -name "*.md" \
  ! -name AGENTS.md ! -name index.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$complete_count" -eq 0 ]; then
  complete_count=$(count_h2 "$ROOT/complete.md")
fi

bold "== Registry =="
printf "active.md     %s task(s) in flight\n"  "$active_count"
printf "planned.md    %s task(s) queued\n"     "$planned_count"
printf "complete.md   %s task(s) recorded\n"   "$complete_count"

echo ""

# ---------- Active task list ----------

if [ "$active_count" -gt 0 ]; then
  bold "== Active tasks =="
  awk '
    /^## / { name=$0; sub(/^## /, "", name); print " - " name; in_task=1; next }
    in_task && /^- (issue|status|location|worktree):/ {
      sub(/^- /, "    ")
      print
    }
    /^### / || /^---/ { in_task=0 }
  ' "$ROOT/active.md"
  echo ""
fi

# ---------- Recently completed (last 5) ----------

if [ "$complete_count" -gt 0 ]; then
  bold "== Recently completed (last 5) =="
  awk '
    /^## / {
      if (count >= 5) exit
      name=$0; sub(/^## /, "", name)
      printf " - %s\n", name
      count++
    }
  ' "$ROOT/complete.md"
  echo ""
fi

# ---------- Full mode ----------

if [ "${1:-}" = "--full" ]; then
  bold "== Full prompt list =="
  for dir in "${WORK_TYPES[@]/#/draft/}" "${LIFECYCLE_DIRS[@]}"; do
    [ -d "$ROOT/$dir" ] || continue
    files=$(find "$ROOT/$dir" -type f -name "*.md" 2>/dev/null | sort)
    [ -z "$files" ] && continue
    bold "$dir/"
    while IFS= read -r f; do
      rel="${f#$ROOT/}"
      printf "  %s\n" "$rel"
    done <<< "$files"
    echo ""
  done
fi

dim "Run 'bash $ROOT/scripts/status.sh --full' for the full prompt list."
