#!/usr/bin/env bash
# health.sh — the `health` shell dispatcher.
#
# Front door for the local health/dev shell tools, mirroring the Claude `/health`
# command door. Routes to the implementations defined in the sibling scripts
# (source all four via ~/.bashrc):
#
#   health              cross-repo git-sync dashboard   (health_sync.sh    -> _health_sync)
#   health sync         explicit alias of the above
#   health release      last release-prep run dashboard (health_release.sh -> _health_release)
#   health audit        structural repo-health audit    (health_audit.sh   -> _health_audit)
#   health help         this usage
#
# Distinct from the `pyauto-heart` binary (the Heart organ CLI) — this is the
# local shell convenience layer. Any argument after the subcommand is passed
# through (e.g. `health release <run-dir>`).

health() {
  local sub="${1:-sync}"
  # Consume the subcommand token only if one was actually given, so bare
  # `health` (defaults to sync) and `health <sub> <args…>` both pass the
  # remaining "$@" straight through to the implementation.
  [ "$#" -gt 0 ] && shift
  case "$sub" in
    sync)    _health_sync "$@" ;;
    release) _health_release "$@" ;;
    audit)   _health_audit "$@" ;;
    -h|--help|help)
      cat <<'EOF'
health — local health/dev shell dispatcher (mirrors the Claude /health door).

Usage: health [sync|release|audit]

    health            cross-repo git-sync dashboard (branch, behind/ahead, dirty)
    health sync       same as bare `health`
    health release    last PyAutoBuild release-prep run dashboard
    health audit      structural repo-health audit (non-repo dirs, stashes, dead branches)

Release-run helpers: health-report / health-json / health-triage.
EOF
      ;;
    *)
      echo "health: unknown subcommand '$sub' (try: health help)" >&2
      return 2
      ;;
  esac
}
