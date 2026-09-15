# Smoke profile cannot see a missing sampler dependency — add an import check over the af.<Search> classes each script constructs

Type: feature
Target: PyAutoHands
Repos:
- PyAutoHands
- PyAutoHeart
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: with blackjax uninstalled in the smoke environment, the smoke run for HowToFit scripts/chapter_1_introduction/tutorial_6_gradients.py FAILS at PYAUTO_TEST_MODE=2 with a message naming BlackJAXNUTS and blackjax, instead of passing; with blackjax installed it passes as before.
Review-minutes: 3
Unattended: ready

Smoke profile cannot see a missing sampler dependency — add an import check over the af.<Search> classes each script constructs

Type: feature
Target: PyAutoHands
Repos:
- PyAutoHands
- PyAutoHeart
Difficulty: small
Priority: medium

CI runs workspace and HowTo smoke tests at PYAUTO_TEST_MODE=2 (config/build/profile_smoke.yaml), which bypasses the sampler entirely: af.BlackJAXNUTS / af.Nautilus / af.Emcee are never constructed, so a search backend that is not installed (blackjax, nautilus-sampler, emcee, dynesty, zeus, corner for the results update) is never imported and the gate stays green while the script is unrunnable by a reader. Seen three times in 2026-09: the HowTo tutorial 5 corner failure, the HowTo tutorials 6 and 7 blackjax failure (issue 65 on the HowTo fit repo), and the Colab bootstrap gaps the autonerves setup_colab audit (its PRs 166 and 168) closed. config/build/no_run.yaml already documents the same blind spot for tutorial_5_expectation_propagation.

Cheap guard, run at smoke settings in the smoke harness (run_smoke.py / build_util): for each smoke-run script, statically collect the af.<Search> constructors it calls (ast walk for Attribute nodes on the af/autofit alias whose name matches a NonLinearSearch subclass) and, in the smoke environment, import the backend module each search needs (a small mapping in one place: BlackJAXNUTS→blackjax, Nautilus→nautilus, Emcee→emcee, DynestyStatic/DynestyDynamic→dynesty, Zeus→zeus, plus corner for any script that calls the corner plotter). A missing module fails the smoke run for that script with a clear message naming the search and the package, before the script itself runs. Optionally the same mapping is asserted against the Colab bootstrap's _SHARED_EXTRAS in its tests, so the two install routes cannot drift apart again.

Witness: with blackjax uninstalled in the smoke environment, the smoke run for HowToFit scripts/chapter_1_introduction/tutorial_6_gradients.py FAILS at PYAUTO_TEST_MODE=2 with a message naming BlackJAXNUTS and blackjax, instead of passing; with blackjax installed it passes as before.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b2124a79-c4f2-4167-9cb9-43b80d08c87c/scratchpad/intake_raw.md -->
