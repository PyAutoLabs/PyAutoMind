# PyAutoBuild: wire autofit_assistant wiki-currency into release.yml

Type: feature
Target: PyAutoBuild
Difficulty: easy
Autonomy: safe
Priority: normal
Status: formalised

Wire the autofit_assistant wiki-currency check into PyAutoBuild's release workflow, exactly as autolens_assistant is wired today: at stack-release time release.yml invokes the assistant's reusable wiki-currency.yml via workflow_call (passing the new stack_version and assistant_ref: main), and a dependent if: failure() job downloads the wiki-drift-report artifact and opens a "wiki drift" issue against PyAutoLabs/autofit_assistant. PyAutoBuild only orchestrates and reports — it holds no copy of the rules (the workflow in autofit_assistant is the single home of the checks). The assistant's workflow already exists with the workflow_call trigger (autofit_assistant PR #3); this task is the PyAutoBuild side only.

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fe0b3759-ba31-4d76-9ce1-aefd030356bd/scratchpad/raw_build_wiring.md -->
