# inference-setup-browser

Type: feature
Target: pyautoinsight
Repos: PyAutoInsight
Difficulty: large
Consequence: judge
Autonomy: supervised
Priority: high
Filed: 2026-10-08
Epic: inference-setup-redesign (phase 3)

## Authorization

Human: "prm, and continue through all phases autonomously to the end".
The approved five-phase design and original request are preserved in
draft/feature/pyautoinsight/inference_setup_redesign.md. Phase1 merged Insight#14.
Explicit current authorization covers implementation and merge/close-out on
green checks of all remaining approved phases. No compute, science acceptance
or release. Tier: judge — merge mode: human-authorized in-turn merge after
independent CLEAN review, required tests and every CI job pass.

## Plan

Adopt current Pulse setup navigation and shared board components: project → dataset family → model links opening a separate setup tab with deep-link/back behavior. Top page: setup/baseline/max likelihood/parameter count/start/hardware/cost and qualification, sampler disclosures below, then filtered archive/comparisons/config/evidence. Keep all archived and unmapped records reachable. Use project-owned v2 catalogue, pin reader after producer publication; retain no-JS fallback and safe links. Match shared responsive width, hero, top prompt/copy icon and tables; verify browser desktop/mobile. Add a Sampler candidates section rendering curated public-literature records with expected application vs measured status and copyable prompts. Literature data comes from independent primary-source research (phase5); never expose private Memory excerpts. Test DOM navigation, safe rendering, filtering, malformed records, fixture v1/v2 compatibility and copy behavior; full suite/offline checks. Publish and verify Pages with actual producer evidence.

## Survey

@PyAutoInsight: canonical main, no active claim at survey. Isolated worktree under
/home/jammy/Code/PyAutoLabs/.worktrees/inference-setup-browser, branch feature/inference-setup-browser.
Preserve all unrelated canonical untracked data. Source setup through start_workspace.

## Original request

prm, and continue through all phases autonomously to the end
