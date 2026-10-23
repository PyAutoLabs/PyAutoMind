## prior-stable-test-ids
- completed: 2026-10-17
- constraint: Human confirmed 2026-10-17 that existing model/search unique IDs and output-folder names must not change; baseline hashes and exact output paths checked across all four branches.
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1701
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1707
- head: c2f9f8bdd43001e94fffe0414cd10a010ac90df7
- validation: Final serial suite: 3702 passed, 120 skipped, 1 xfailed. Four-worker property tests: 170 passed; collection mismatch reproduced before repair. Full parallel execution still blocked by separately filed shared-output races.
- identifier-evidence: Free/fixed/mixed model hashes, search IDs and output paths equal unmodified main 99d714c71; no identifier code changed.
- merge: ed7adfdad04e239f5d3053fb8f9fd559a66e4c51
- authorization: Human /prm in this chat, 2026-10-17.
- merge-proof: Remote PR head is an ancestor of origin/main in unshallowed PyAutoFit; zero unmerged commits. GitHub confirms MERGED.
- ci: All head workflows and jobs completed successfully; Python 3.12, 3.13 and no-JAX test legs passed. Applicable docs and generated-search-docs passed. No review objections.
- freeze: pyauto-heart freeze --show returned not frozen. Readiness remains STALE; no release-readiness claim.
- release-link-repair: GitHub pending-release label verified; restored the missing Mind link during close-out.
- shadow-row: Human confirmed merged-unchanged in this chat on 2026-10-17; stage-1 glance row appended to autonomy_log.md.
- scope: Stable collection IDs shipped. Full parallel execution still depends on the existing draft/bug/autofit/ep_test_suite_is_not_xdist_safe.md; no duplicate task created.

## Original prompt

# xdist collection ids unstable in test_prior_properties

Issued: 2026-10-17
Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: `python -m pytest -n 4 test_autofit/` collects identically on every worker (no 'Different tests were collected' error) and passes; the parametrize ids in `test_autofit/mapper/prior/test_prior_properties.py` contain no memory addresses.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-11

xdist collection ids unstable in test_prior_properties

Type: bug
Witness: `python -m pytest -n 4 test_autofit/` collects identically on every worker (no 'Different tests were collected' error) and passes; the parametrize ids in `test_autofit/mapper/prior/test_prior_properties.py` contain no memory addresses.

PyAutoFit's test suite cannot run under pytest-xdist: `python -m pytest -n auto test_autofit/` fails at collection with 'Different tests were collected between gw0 and gw1' (3 errors, 2 skipped, nothing runs). The parametrize ids in `test_autofit/mapper/prior/test_prior_properties.py` embed object reprs containing memory addresses, e.g. `test__message_power_keeps_the_support[UniformPrior(<autofit.messages.composed_transform.TransformedMessage object at 0x7f27...>)]`, so each xdist worker generates different test ids and xdist refuses to schedule. Reproduced on a clean main (e331e33) on 2026-09-11 while validating PyAutoFit#1609; the suite passes serially (2575 passed, 43 skipped). The remote-session bootstrap and PyAutoFit's AGENTS.md both prescribe `pytest -n auto` for this suite, so today that instruction cannot be followed.

Fix: give those parametrize cases stable ids (an `ids=` callable naming the prior/message type, or `pytest.param(..., id=...)`), or give the message/prior objects an address-free `__repr__`; then confirm `-n auto` collects and passes. Repos: @PyAutoFit

<!-- formalised by the Intake (Conception) Agent on 2026-09-11 from user-intake -->
