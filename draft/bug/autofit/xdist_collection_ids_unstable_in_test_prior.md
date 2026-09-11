# xdist collection ids unstable in test_prior_properties

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

xdist collection ids unstable in test_prior_properties

Type: bug
Witness: `python -m pytest -n 4 test_autofit/` collects identically on every worker (no 'Different tests were collected' error) and passes; the parametrize ids in `test_autofit/mapper/prior/test_prior_properties.py` contain no memory addresses.

PyAutoFit's test suite cannot run under pytest-xdist: `python -m pytest -n auto test_autofit/` fails at collection with 'Different tests were collected between gw0 and gw1' (3 errors, 2 skipped, nothing runs). The parametrize ids in `test_autofit/mapper/prior/test_prior_properties.py` embed object reprs containing memory addresses, e.g. `test__message_power_keeps_the_support[UniformPrior(<autofit.messages.composed_transform.TransformedMessage object at 0x7f27...>)]`, so each xdist worker generates different test ids and xdist refuses to schedule. Reproduced on a clean main (e331e33) on 2026-09-11 while validating PyAutoFit#1609; the suite passes serially (2575 passed, 43 skipped). The remote-session bootstrap and PyAutoFit's AGENTS.md both prescribe `pytest -n auto` for this suite, so today that instruction cannot be followed.

Fix: give those parametrize cases stable ids (an `ids=` callable naming the prior/message type, or `pytest.param(..., id=...)`), or give the message/prior objects an address-free `__repr__`; then confirm `-n auto` collects and passes. Repos: @PyAutoFit

<!-- formalised by the Intake (Conception) Agent on 2026-09-11 from user-intake -->
