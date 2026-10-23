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
