# Platform Adapters

人味 Agent has one behavioral core and two delivery routes:

- **Native Skill:** install the complete `skill/` directory. The host discovers `SKILL.md` and loads referenced files when needed.
- **Instruction adapter:** paste a platform-specific prompt into a persistent instruction surface, or use the universal prompt at the start of a fresh chat.

Do not paste `SKILL.md` alone into a native Skill directory. It references files under `references/` and `profiles/`, so copy the complete `skill/` tree.

## Choose A Route

| Product surface | Route | Use |
|---|---|---|
| Codex app, CLI, or IDE | Native Skill | `skill/` via `native-skill-install.md` |
| Claude Code | Native Skill | `skill/` via `native-skill-install.md` |
| Gemini CLI | Native Skill | `skill/` via `native-skill-install.md` |
| Gemini web or mobile | Gem | `gemini-gems.md` |
| Kimi Code CLI | Native Skill | `skill/` via `native-skill-install.md` |
| Kimi Agent mode | Custom Skill | Run `/skill-creator`, then paste `kimi-agent-skill-creator.md` |
| Kimi standard chat | Preset | `kimi-preset.md` |
| ChatGPT web or mobile | Custom Instructions | `chatgpt-custom-instructions.md` |
| ChatGPT custom GPT | GPT Instructions | `chatgpt-strict.md` |
| Any model with a system prompt | Instruction adapter | `generic-system-prompt.md` |
| Any chat with no persistent instruction surface | First-message adapter | `universal-copy-paste-prompt.md` |

ChatGPT Work mode and the ChatGPT desktop app also expose Skills in supported configurations. This repository does not yet ship a ChatGPT plugin, so the public ChatGPT route remains Custom Instructions or a custom GPT.

## What Portability Means

The same mechanism is available across the listed products. Identical outputs are not promised. Base-model behavior, system instructions, context limits, tools, retrieval, and safety policies still differ.

An adapter changes response policy. It cannot add browsing, file access, execution, persistent memory, or better retrieval to a host that lacks those capabilities.

## Validation

Use `../evals/platform-adapter-adversarial-v1.md` after installation or copying. Record the exact product surface and route. A passing run on Gemini CLI does not validate Gemini web, and a Kimi Code run does not validate Kimi chat.

## Official Capability References

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI: ChatGPT Custom Instructions](https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt)
- [Anthropic: Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)
- [Google: Gemini CLI Agent Skills](https://geminicli.com/docs/cli/using-agent-skills/)
- [Google: Create a custom Gem](https://support.google.com/gemini/answer/15235603)
- [Kimi Code: Agent Skills](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)
- [Kimi: Skills in Agent mode](https://www.kimi.com/help/features/use-skills-in-agent)
- [Kimi: Presets](https://www.kimi.com/help/getting-started/quick-phrases)
