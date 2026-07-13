## pyautoscientist-4b
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/75 (closed)
- completed: 2026-07-10
- prs: PyAutoBrain#76 + PyAutoHeart#55 + PyAutoMind#50 (all merged 2026-07-10)
- summary: config extraction COMPLETE — Brain identity sets derive from repos.yaml categories at runtime (strict supersets: reduce/developer/euclid targets now resolve); vocabulary → PyAutoBrain/config/policy.yaml (aliases, memory_wikis, target_signals, default wikis, test_witness, release policy + nightly tag_repo); Heart url_check_live 31 fixup rules → config/url_fixups.yaml (ast-extracted, byte-identical verified). Seam tests 12→22; feature/intake decisions diffed identical pre/post; allowlist: sizing 8→1, refactor+activity_gate rows DELETED, url_check_live 11→3. Remaining allowlist = docstring examples + test fixtures + workspace-root defaults only.
