## pyautoscientist-3b-config
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/53 (closed)
- completed: 2026-07-10
- prs: PyAutoHeart#54 + PyAutoBuild#133 + PyAutoMind#49 (all merged 2026-07-10)
- summary: config extraction 4a — Heart version_skew map → config/repos.yaml `version_skew:` block (incl. unpolled assistant; WORKSPACE_LIBRARY → strict workspace_library()); readiness load_library_names strict no-fallback + DEFAULT_LIBRARIES deleted; dashboard derives from the same file; Build run_all WORKSPACES + slow_skip defaults → autobuild/config/workspaces.yaml. Suites 244/78 green, behaviour identical. FIREWALL_ALLOWLIST shrunk 42→16 tokens across 5 files (slow_skip row deleted). 4b remainder recorded in issued/pyautoscientist_3b_config_extraction.md: Brain constant tables + Heart url_check_live rules — Opus-executable, seam test per move (Brain suite is thin).
