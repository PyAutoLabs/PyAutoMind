# Heart `test_html_is_self_contained` fails on main since PyAutoBrain#499 rewrote the "markdown version" link

Type: bug
Target: pyautoheart
Repos:
- PyAutoHeart
- PyAutoBrain
Themes:
- ci
- dashboard
Difficulty: small
Autonomy: safe
Priority: high
Status: draft
Filed: 2026-10-07

## Symptom

`tests/test_dashboard.py::test_html_is_self_contained` (PyAutoHeart `tests/test_dashboard.py:102`) asserts the literal
`<a href="dashboard.md">markdown version</a>` in the rendered HTML. It fails on Heart `main` (3de585f)
against current PyAutoBrain `main` (1100c20) — reproduced locally and on PR PyAutoHeart#292's `pytest (3.12)`/`(3.13)` legs
(run 37683297574, 1 failed / 1228 passed). Heart's own last green `Heart Tests` run on main was 13:18Z 2026-10-07,
before PyAutoBrain#499 merged (18:52Z).

## Cause (verified)

PyAutoBrain#499 "feat: align dashboard Markdown source icons to the right" (`board/_theme.py:1314`,
`if label.lower() != 'markdown version':`) special-cases that anchor label and renders it as an icon, so the literal
anchor Heart's `heart/dashboard.py:2423` emits no longer survives the shared theme pass. Cross-repo break: Heart's
test pins Brain's old markup.

## Fix

Either relax the Heart assertion to the theme's new markup (check for the `dashboard.md` href rather than the
label text), or have Brain's theme keep the label for consumers that assert it. Heart-side relaxation is the smaller
change and matches the theme's intent. Re-run Heart#292 after the fix lands.

## Original request (verbatim)

Observed by the Fable session while shipping search-extensibility B1 (PyAutoHeart#292 red on an unrelated
documentation-only change); no human words yet.
