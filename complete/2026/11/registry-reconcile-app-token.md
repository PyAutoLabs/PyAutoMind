`Registry Reconcile` was red daily since ~2026-10-30: `github.token` reads only PyAutoMind, so `lifecycle.py issues`
404'd on private ECLIPSE_lens_catalogue#4. Fixed in PyAutoMind#538 (merged 2026-11-05) per policy/github_tokens.md: the
workflow mints the org App token (owner-wide, issues + pull-requests read) right before the run step; inventory row
added. Option (b) — "unverifiable" classification — rejected as the warn-and-skip the policy forbids. Proof: dispatched
run 42028192888 on main after merge.

## Original prompt

# Mind Registry Reconcile red daily: workflow token cannot read a private-repo issue

Type: bug
Target: pyautomind
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
