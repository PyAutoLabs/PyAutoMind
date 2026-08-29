# Fix wiki-currency CI drift in the lens and galaxy assistants

Type: maintenance
Target: PyAutoBrain
Repos:
- autogalaxy_assistant
- autolens_assistant
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: medium
Status: issued
Issued: 2026-08-28

# Fix wiki-currency CI drift in the lens and galaxy assistants
Type: maintenance
Difficulty: small
Autonomy: safe
Priority: medium

The `wiki-currency` CI leg is red on main for autolens_assistant and autogalaxy_assistant (Actions runs 33226180760 and 33226182888, 2026-08-28). The symbol audit run with `--scope all` reports 1 missing or broken symbol in each repo, out of 67 files and 141 symbols scanned. autogalaxy_assistant additionally fails its citation-path check: `wiki/core/operations/sandbox.md` cites the galaxy library's `plot/plot_utils.py` module, which no longer exists in the sources checkout. autolens_assistant's `llms-chat.txt` and `chat_pack/01_api_surface.md` are also stale on main.

Task: regenerate the stale generated surfaces and re-cite the dead path so the `wiki-currency` leg goes green again on both repos. Note that PRs #115 and #116 (autolens_assistant) and #19 and #20 (autogalaxy_assistant) were merged over this drift on human acknowledgement, so the red leg predates and survives those merges.

Related: PyAutoBrain#315.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/069a02ef-b14f-4a43-b0c3-92e461ddef66/scratchpad/intake_wiki_currency.md -->
