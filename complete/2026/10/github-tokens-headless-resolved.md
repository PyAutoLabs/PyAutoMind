- summary: Follow-up to the GitHub token consolidation (complete/2026/10/github-token-consolidation-epic.md). `policy/github_tokens.md` had recorded the headless RAL/Colab PAT as "state unknown". The page now records that no headless token exists or is needed, gives the rule if one ever is (one fine-grained PAT owned by the maintainer, kept in the password manager, recorded on the page), drops that Owed item, and points the autocti proof item at autocti_visualization#7.
- evidence: read-only probe of RAL (`euclid_jump`), 2026-10-23: no `credential.helper`, no `~/.git-credentials`, no `gh`, no token env vars. Its SSH keys are not registered with GitHub (`Permission denied (publickey)`). Every checkout under `/mnt/ral/jnightin` has an anonymous HTTPS remote on a public repo. The probe added github.com to RAL's `known_hosts` (benign). Colab: `autonerves/setup_colab.py` clones only the six public workspace/HowTo repos. Mind suite 704 passed; PR CI `privacy` green (`drift` PR-skipped); witness passed; tiered merge.

## Original prompt

# policy/github_tokens.md: record that RAL and Colab need no headless token

Type: docs
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `grep -n -i "unknown" policy/github_tokens.md` has no hit about the headless PAT; the page's Owed list no longer carries a "Headless RAL/Colab PAT" item; Mind suite green
Review-minutes: 3
Unattended: never
Filed: 2026-10-23
Issued: 2026-10-23

The page (phase 5, complete/2026/10/github-token-p5-policy-page.md) records the
headless RAL/Colab fine-grained PAT as "state unknown since the 2026-10-23
revocation". Checked 2026-10-23 by the session:

- RAL (`euclid_jump`): no `credential.helper`, no `~/.git-credentials`, no `gh`,
  no token env vars; its SSH keys are not registered with GitHub
  (`Permission denied (publickey)`); every checkout under `/mnt/ral/jnightin`
  (`PyAuto/*`, `inference/*`, `profiling/*`) has an anonymous
  `https://github.com/PyAutoLabs/<repo>.git` remote on a public repo; no RAL job
  script pushes or clones. Results come back by the laptop's pull (rsync), not git push.
- Colab: `autonerves/setup_colab.py` clones only the six public workspace / HowTo
  repos, with no token or auth code.

So no headless PAT exists or is needed. Update the "Local" paragraph to say so
(RAL and Colab read public repos anonymously; should one ever need a private repo
or a push, the rule is one fine-grained PAT owned by the maintainer, kept in the
password manager, recorded here), and drop the Owed item.
