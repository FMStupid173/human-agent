# Release Day

## Before Posting

1. Run `powershell -ExecutionPolicy Bypass -File scripts/prepublish-audit.ps1`.
2. Build the archive with `powershell -ExecutionPolicy Bypass -File scripts/package-release.ps1`.
3. Extract the archive into a temporary directory and inspect the top-level file list.
4. Enable GitHub private vulnerability reporting.
5. Open the README in GitHub and test every Quick Start path listed in `adapters/README.md`.
6. Check screenshots for profile names, avatars, browser tabs, local paths, and notifications.

Upload only the versioned archive produced by the packaging script and its `.sha256` file.

Before claiming live provider support, run the Calibration Copilot unit suite and a small API smoke test on that exact provider and model. Without a live run, describe the route as code-validated and awaiting provider evidence.

## V2EX Draft

**Title**

我给 AI 做了一个会按场景调整人味和严谨度的开源 Skill

**Body**

人味 Agent 的核心是 Dynamic Human Layer。它会判断当前属于聊天、写作、情绪、coding 还是 research，再动态调整语气、结构、改写自由度和证据门槛。

聊天时它减少客服腔；写作时保护原意；情绪场景控制建议的分量；coding 和 research 场景要求先检查、选对来源、核验易变事实，并区分已确认、推断和未知。这些规则用于减少可避免的幻觉，不能保证模型永远正确。

公开仓库只提供可复用测试题和空白评分模板，不发布个人测试记录。ChatGPT、Gemini、DeepSeek 和 Codex 的当前表现都需要由使用者在本地验证。项目不要求模型假装成 Claude，也不包含原始聊天记录。

我现在最需要失败样本：请拿一条你平时真的会问的问题跑一次，告诉我回答哪里仍然有 AI 味、哪里变差了。提交前请删掉隐私和账号信息。

## Show HN Draft

**Title**

Show HN: 人味 Agent - a Dynamic Human Layer for adaptive, evidence-aware AI responses

**Body**

人味 Agent is an open-source Dynamic Human Layer for AI assistants. It routes each turn by moment, stakes, emotional temperature, and transformation freedom, then adapts voice, structure, semantic fidelity, and the evidence gate.

For coding and research, it is designed to reduce avoidable hallucinations through inspect-before-claiming, source-fit checks, volatile-fact verification, and explicit separation of confirmed facts, inference, and unknowns. It does not guarantee correctness or replace retrieval.

The shared Skill package is available for Codex, Claude Code, Gemini CLI, and Kimi Code. ChatGPT and Gemini web have copyable instruction adapters; Kimi Agent has a Skill Creator brief, and Kimi standard chat has a Preset. DeepSeek and Cursor also have copyable adapters. These routes are previews and still need current validation on each exact product surface.

I would value one kind of feedback most: run a prompt from your real workflow, then report the smallest redacted example where the adapter made the answer worse.

## Reddit Framing

Lead with the language problem and one before/after pair. Explain the method before linking the repository. Check each community's self-promotion rules and ask moderators when unclear. Do not paste the same promotional text across multiple communities.

## Seven-Day Signal

- 5 successful installs or copies;
- 3 people using it on real tasks;
- 2 concrete failure examples;
- 1 person keeping it enabled after three days.

Stars measure distribution. Repeated use and specific failures are stronger early product evidence.
