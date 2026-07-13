## slack-release-notes
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/141 (closed)
- completed: 2026-07-10
- library-pr: https://github.com/PyAutoLabs/PyAutoBuild/pull/142 (merged 682c3c9, squash)
- repos: PyAutoBuild
- notes: #pipreleases success post now embeds the full PyAutoLens release notes (which already aggregate upstream Fit/Array/Galaxy via "Upstream Changes") + links to all four GitHub release pages. New autobuild/slack_release_notes.py reads back the published Lens GitHub Release (gh release view), converts GitHub-md->Slack-mrkdwn, falls back to the one-liner if unfetchable; failure post unchanged. announce_release now needs publish_release_notes (kept in always() so failures still page), checks out repo + PAT_PYAUTOLABS as GH_TOKEN for the cross-repo read. --auto safe run: parked at ship gate on unacked Heart YELLOW, then human acked the 5-reason organism-scope set -> PR-open -> merged. Verified end-to-end against the LIVE 2026.7.9.1 release. Notes only appear on the NEXT live release (workflow YAML, not CI-exercisable).
