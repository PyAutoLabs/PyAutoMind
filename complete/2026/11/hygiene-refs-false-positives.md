`pyauto-brain hygiene refs` reported 16 false positives out of 19 in the 2026-11-04 sweep. Fixed in PyAutoBrain#584
(merged 2026-11-04): a reference dead in its own repo is retried in the HowTo course's companion workspace (derived by
the HowTo<Name> -> auto<name>_workspace convention, so the tenant firewall stays clean) and in any sibling named on the
same line; `files`, `cache`, `cache_root`, `work` join RUNTIME_DIRECTORIES; `notebooks` is unresolvable where the
checkout does not commit it. A path dead everywhere is still a finding. Live scan 16 → 0; 88 hygiene tests pass.

## Original prompt

# hygiene refs: 16/19 findings are false positives (sibling-repo and runtime paths)

Type: bug
Target: PyAutoBrain (hygiene refs scanner)
Consequence: glance

Found 2026-11-04 during workspace-hygiene-sweep-1104 (autolens_workspace#620). `pyauto-brain hygiene refs`
reported 19 dead references; only 3 were real. The other 16 resolve fine but against a *different root*:

- Sibling-repo paths named in prose: HowToLens/HowToGalaxy say "the workspace's `scripts/interferometer/modeling.py`"
  (resolves in autolens_workspace / autogalaxy_workspace); autocti_workspace README names
  `autocti_assistant`'s `colab/contexts.yaml`.
- Runtime/output folders that exist only after a run: `files/search_internal` (guides/plot/searches.py in
  autolens + autogalaxy workspaces), autoreduce `work/injected/`, `cache_root/crds/`, README `cache`, `notebooks`
  (generated at release time).

Fix idea: resolve a ref also against the paired workspace (HowToLens→autolens_workspace, HowToGalaxy→
autogalaxy_workspace) and any repo named in the same sentence; keep an allowlist of runtime folders
(`files/`, `output/`, `cache*/`, `work/`) and per-repo generated dirs. Also: the scanner resolved the canonical
checkout from inside a task worktree because the bundle's PyAutoBrain is a symlink — needed `PYAUTO_ROOT=$PWD`.
Done when the canonical scan of the same tree reports only genuine dead refs.
