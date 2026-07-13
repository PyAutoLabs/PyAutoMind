## cli-noise-clean
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1209
- completed: 2026-04-13
- library-pr: https://github.com/PyAutoLabs/PyAutoConf/pull/92, https://github.com/PyAutoLabs/PyAutoFit/pull/1210, https://github.com/PyAutoLabs/PyAutoArray/pull/275, https://github.com/PyAutoLabs/PyAutoGalaxy/pull/349, https://github.com/PyAutoLabs/PyAutoLens/pull/437

## Original prompt

When we run unit tests, integration tests, scripts and other things we get noise on the command
line due to libraries versions, badly formatted docstrings and other issues.

Can you do a full run through of different scripts over the projects, find this noise and gradually fix
the issues as they crop up.