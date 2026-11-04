# Mind Registry Reconcile red daily: workflow token cannot read a private-repo issue

Type: bug
Target: organs
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Filed: 2026-11-04 (pre-rehearsal /hygiene sweep; Heart ci_status:PyAutoMind red)

The scheduled `Registry Reconcile` workflow in @PyAutoMind has failed every day since at least 2026-10-30 (latest run 41850160786). `python3 scripts/lifecycle.py issues` reports DRIFT:

    active.md: r2-pages-function-access: could not read issue state (unreadable: gh: Not Found (HTTP 404)): https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4

The issue is OPEN and readable with the human's own token; `ECLIPSE_lens_catalogue` is private and the workflow's `GH_TOKEN` cannot see it. Decide between: (a) giving the workflow token read access to the private repos it must reconcile (see policy/github_tokens.md), or (b) making `lifecycle.py issues` classify an unreadable private-repo issue as "unverifiable here" rather than drift. Never drop the row to turn the check green.
