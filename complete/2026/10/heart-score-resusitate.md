# Heart Score and Resusitate sections

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/255
- pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/256
- merged: 2026-10-01
- merge-commit: 6463c80050c82a73919bb01cca55edd534be3718

## Shipped

Replaced the large verdict box with Score and Resusitate sections matching Observed checks. Score retains the numeric score, small readiness text, expandable penalties, provenance and reason counts. Repair labels reveal their full prompts; right-aligned clipboard icons copy the original payloads. Evidence gaps remains below.

No readiness computation or CLI/Markdown/JSON change. No remaining scope or downstream workspace changes.

## Validation and merge evidence

Actions run 36837833217 on 4e879031cabacd0b2955e7b1dbe020ea714b7083: Python 3.12 and 3.13 jobs completed successfully, including pytest and tenant firewall. One PR workflow run is expected for this repo. GitHub merge state CLEAN; all claimed branch commits proven included in fetched origin/main (0 unmerged commits; repository not shallow).

Local suite: 1105 passed in 67.31s. Tenant firewall, HTML rendering, in-session diff review and diff --check passed. Browser verification unavailable because sandbox socket restrictions prevented Chromium startup. Preview and test logs preserved under PyAutoMind/tmp/heart-score-resusitate/.

Human `$prm also rebuild it` authorized merge, close-out and the web-dashboard rebuild. The previously recorded Heart RED development override remains scoped to development: `release validation FAILED (stage integrate)` is not repaired by this presentation change. No package release performed.

## Web rebuild

Manually dispatched Heart Health on merged head 6463c80: https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/36838075304. Both Cloud health checks + dashboard and Publish the board to GitHub Pages completed successfully during close-out.

## Original prompt

# Heart Score and Resusitate sections

Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/255
Issued: 2026-10-01
Type: feature
Target: @PyAutoHeart

## Original request

its good! The Stale: score 65 box seems uncessary now. I think we have a new header with the same size and font as Observed checks, called "Score", Which gives the score and then has the Why this score: 65/100
Start at 100; subtract these capped penalties, with a floor of 0. The verdict is determined by the reasons, not the score.
Missing workspace test report: −10 (1 × 10, cap 10)
Missing install verification: −10 (1 × 10, cap 10)
Missing release validation: −15 (1 × 15, cap 15)  
0 release blockers · 0 warnings · 3 evidence gaps stuff.    I think we then have a header called "Resusitate" Which has the Fix Heart systematically and Refresh all missing evidence boxes, then we have Evidence gaps as it is. I think the clickable prompt button for "Fix Heart Systematically" and "Refresh all missing evidence" can be to the right as an icon of these, like it is for the main dashboard

## Approved plan

- Keep the Observed checks grid first.
- Replace the large verdict/score box with an h2 Score section containing the score, small readiness verdict, existing expandable penalty explanation and reason counts.
- Add an h2 Resusitate section with labeled repair rows and accessible right-aligned clipboard icons; preserve view/select prompt disclosures and clipboard failure feedback.
- Keep Evidence gaps and the existing warning/blocker content below the repair section.

## Detailed implementation

- Edit heart/dashboard.py: _render_html section structure and metadata placement; _html_actions repair rows with _copy_btn(icon=True); responsive CSS. Retain _html_score data and computation, snapshot provenance and freshness notice.
- Update existing dashboard HTML tests for hierarchy, icon semantics, copy payloads and fallback disclosures. Use synthetic fixture data. Validate targeted tests, full Heart suite, and tenant-firewall check; browser-check if available.
- No readiness, CLI, Markdown or JSON contract change. One organ repo; no downstream scientific smoke required.
- Branch: feature/heart-score-resusitate. Heart canonical checkout clean on main; no conflicting claim. Implementation through start_library / ship_library.

## Approval

User replied "I approve" on 2026-10-01 to the above layout and the development-only override for Heart RED `release validation FAILED (stage integrate)`. Scope: this task's implementation and development shipping; no merge or release.

## Implementation handoff

PR: https://github.com/PyAutoLabs/PyAutoHeart/pull/256 (pending-release). Commit: `4e87903` on `feature/heart-score-resusitate` in `/home/jammy/Code/PyAutoLabs/.worktrees/heart-score-resusitate/PyAutoHeart`.

Implemented Score and Resusitate sections, small readiness text, icon copy rows with view/select disclosure, existing evidence sections retained. Full suite: **1105 passed in 67.31s**; tenant firewall OK; HTML preview generated; diff review passed. Browser startup blocked by sandbox socket permission; preview and full-tests.log are in task root.

Both Python CI jobs in progress at the single post-push check. User approval covers this task and the known RED development override; merge/deployment remain pending explicit instruction. Next: `/prm` once CI is green, then publish via Heart Health when authorized.
