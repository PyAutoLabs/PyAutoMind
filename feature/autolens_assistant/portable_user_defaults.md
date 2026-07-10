# Portable user defaults and environment discovery

Type: feature
Target: autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

**Rescoped by user decision 2026-07-10:** implement the **environment-discovery half now** —
inspect Git/GitHub identity and authentication, available SSH host aliases where practical, and
the existing profile/project configuration *before* asking the user questions, with the
precedence order below. The `~/.config/autolens_assistant/user.yaml` defaults-file half stays
**evidence-gated and deferred** exactly as written: do not add the YAML until real multi-project
usage shows which non-discoverable values recur.

`autolens_assistant` already separates user and environment state across appropriate sources:

- durable scientific context, interaction preference, and HPC access constraints live in
  `@autolens_assistant/wiki/project/profile.md`;
- project-specific HPC routing lives in gitignored `hpc/sync.conf`;
- SSH credentials and aliases live in `~/.ssh/config`;
- GitHub authentication lives in `gh auth`, and Git identity lives in `git config`;
- project identity and provenance live in `project.yaml`.

Do not add another configuration system merely to duplicate these sources. First use the
assistant across multiple real science projects and identify which non-secret values users are
repeatedly asked to provide.

Future feature, if repeated setup proves significant:

- Add lightweight environment discovery for standard tools: inspect Git/GitHub identity and
  authentication, available SSH host aliases where practical, and the assistant's existing
  profile and project configuration before asking the user questions.
- Optionally support machine-local, reusable defaults at a conventional location such as
  `~/.config/autolens_assistant/user.yaml`. Keep this file optional and limited to non-secret
  defaults that cannot be reliably discovered, such as preferred GitHub owner/organisation,
  name/ORCID, default HPC alias and base directory, preferred interaction mode, repository
  visibility, and remote-execution posture.
- Use an explicit precedence order:
  `user's current instruction -> project configuration -> optional user defaults -> detected
  standard-tool state -> ask`.
- Never store GitHub tokens, SSH keys, passwords, MFA material, or other credentials. Standard
  tools remain authoritative for authentication and account selection.
- Handle multiple GitHub accounts, clusters, and project-specific overrides without assuming
  that one global default is always correct.
- Prefer a small setup/preflight workflow over mandatory onboarding. It should explain what was
  detected, what remains unknown, and where each value will be stored.

Before implementation, collect evidence from normal use: which questions recur, whether defaults
are stable across projects and machines, and whether environment discovery alone removes most of
the friction. If repetition remains low, retain the current design and do not implement the YAML.

## Original request

> Have personal user mode set up via a yaml or something? This was initially for HPC settings but
> I am left wondering how useful this idea is, I guess the point is I always link to HPC and GitHub
> and other things using standard accounts so a user used to using autolens asssistant needs the
> same tools

> ok then this sounds like another PyAutoPrompt if one isnt already there

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
