Human request (2026-11-16), reworked twice on the human's feedback. Shipped as PyAutoBrain#651 (renderer) and PyAutoMind#578 (re-render), merged 2026-11-16. Brain went in on `ci-verdict` GREEN with Heart green. Mind went in on the human's "looks good": it had no CI on dashboard-only files, and its conflict with the self-healed render was resolved by re-rendering with the merged renderer. Issue PyAutoBrain#650.

**Result:**
- **Autopilot block:** one block sits directly above Start here. It uses the page's own `section_layout` / `details.board-section` and holds Goals, Queue (★ rank, 📋), Questions and Shift.
- **Badge:** LIVE · N in progress during a shift, otherwise N to review, otherwise N queued · M questions.
- **Idle shift:** collapses to one muted line with a "shift issue #N" link.
- **Tile:** an Autopilot tile leads the nav row, matching the other tiles.
- **Removed:** the standalone Questions aside, the top steer box and the separate batch block. No new CSS, and the CSP is unchanged.

**Feedback recorded (memory):** dashboard additions must reuse the existing block style, and previews open in Opera GX.
