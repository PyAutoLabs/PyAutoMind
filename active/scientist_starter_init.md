# Initialize an isolated Scientist configuration

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/63
Epic: scientist-adoption-pilot
Difficulty: medium
Consequence: judge
Parent: scientist_minimal_starter.md

## Original request

do nexttask

## Plan

Next bounded bootstrap slice in @PyAutoScientist. Add an offline dry-run-by-default starter command that validates an existing canonical Mind repository ID, name and Pages URL, then creates an empty instance profile/project config and fresh-chat continuation guide in a new user-owned directory. Refuse any existing destination, including symlinks; never overwrite records or copy live state. Explicit --apply writes only this directory. No remote, provisioning, organ activation or harness installation. Tier judge; human /prm.

## Detailed implementation

Add scripts/starter.py with argument parsing, validation reused from instance_profile.py, deterministic file plan and exclusive destination creation. Output instance.json, projects.json, and SETUP.md describing exact resume/validate commands and remaining Mind/template/harness setup. Use an existing canonical repos.yaml supplied by the user without copying or rewriting it. Tests cover dry run, unknown identity, invalid URL, existing/symlink destination, repeat invocation preserving records and real renderer consumption. Update STARTER.md to distinguish initialization from full installation.

Audit: current Mind spawn generates a full template family; Brain installer modifies harness-wide settings. This task does not duplicate either or claim minimal harness readiness. Remaining parent work: adopt empty Mind/optional Memory templates, audit one harness, project connection and fresh-chat end-to-end proof.

Branch survey: Scientist main clean at 002d305; no active claims. Unregistered DNA worktree left untouched. Branch feature/scientist-starter-init, worktree .worktrees/scientist-starter-init.
