# Make prompt_sync.sh self-locating

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: safe
Priority: low
Status: draft — issue when convenient

`scripts/prompt_sync.sh` hardcodes `PROMPT_REPO="$HOME/Code/PyAutoLabs/PyAutoMind"`
(+ a legacy PyAutoPrompt fallback). It ships verbatim in PyAutoMind-template
(spawn KEEP rule), so any adopter whose workspace root differs breaks on
first use. Make it resolve relative to its own location the way
`repos_sync.py` does (bash equivalent:
`PROMPT_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"`), keeping
an env-var override. Zero behaviour change for the live setup (same
resolved path). Verify: source it from an unusual cwd; run
prompt_sync_new_prompts as a no-op; spawn --check picks the fix up in the
template on next regeneration.
