# Assistant activate.sh: pin JAX to CPU on GPU-less jobs; autolens keeps TMPDIR off /tmp

Targets: @autolens_assistant @autogalaxy_assistant
Type: bug
Filed: 2026-11-13
Issued: 2026-11-13
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/185
Consequence: judge

Verbatim user request (2026-11-13): "do all four" — item 4: add the JAX_PLATFORMS line to the projects and the template (plus the autolens template's missing TMPDIR block found on the way).

Tier: judge — merge mode: human /prm
