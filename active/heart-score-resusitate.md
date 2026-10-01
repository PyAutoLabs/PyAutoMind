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
