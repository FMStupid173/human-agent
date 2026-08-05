# 人味 Agent

**English** | [简体中文](README.zh-CN.md)

**AI can answer quickly and still miss the point.** It gives advice when you wanted acknowledgment, rewrites your voice when you asked for a light edit, and sounds certain before checking the code or source.

人味 Agent is an open-source response-policy Skill. It chooses what the current moment needs, calibrates how much to intervene, and checks what the answer can honestly claim before drafting.

- **Dynamic Human Layer:** adjusts directness, warmth, information density, and intervention to the actual moment instead of applying one friendly script everywhere.
- **First-principles project work:** traces inputs, state, dependencies, outputs, and invariants before proposing fixes.
- **Adversarial completion:** asks what could overturn the current judgment, verifies the result, and closes the task without pretending uncertainty disappeared.
- **Evidence-aware research and coding:** separates confirmed facts, inference, and unknowns, then selects sources that fit the claim.

The mechanism runs as a native Skill on Codex, Claude Code, Gemini CLI, and Kimi Code. Chat products use compact adapters for Custom Instructions, Gems, Presets, system prompts, or a fresh conversation.

**Design inspiration:** 人味 Agent studies publicly observable qualities in Claude's language behavior, including restraint, emotional proportion, writing sensitivity, and clear boundaries. It does not claim Claude's identity, internals, or training data.

**Reliability boundary:** the evidence gates reduce avoidable hallucination paths. They cannot guarantee factual correctness or add browsing, file access, retrieval quality, or reasoning capability that the host model does not have.

**Status: `v0.2-preview`.** The core has structural and local Codex validation. Every model and product surface still needs its own runtime evidence.

## Try It In Three Minutes

1. Choose and copy one route from `adapters/README.md`.
2. Open a fresh conversation so old instructions do not contaminate the comparison.
3. Run these prompts one at a time, first without 人味 Agent and then with it:

```text
I feel awful today. Give me one normal response. No analysis and no advice.

Lightly edit this while preserving its exact meaning and intensity: I have been a little tired lately, and I do not feel like explaining many things.

From only "TypeError: undefined", tell me the one root cause and the exact fix.
```

Compare boundary recognition, meaning preservation, and evidence honesty. A different tone alone is not a pass.

## Platform Coverage

| Product | Best route |
|---|---|
| ChatGPT web / mobile | Copy `adapters/chatgpt-custom-instructions.md` |
| ChatGPT custom GPT | Copy `adapters/chatgpt-strict.md` |
| Codex app / CLI / IDE | Install the native `skill/` package |
| Claude Code | Install the native `skill/` package |
| Gemini CLI | Install the native `skill/` package |
| Gemini web / mobile | Copy `adapters/gemini-gems.md` into a Gem |
| Kimi Code | Install the native `skill/` package |
| Kimi Agent mode | Create a custom Skill from `adapters/kimi-agent-skill-creator.md` |
| Kimi standard chat | Save `adapters/kimi-preset.md` as a Preset |
| Other LLMs | Copy `adapters/universal-copy-paste-prompt.md` |

See `adapters/README.md` for exact installation paths, capability boundaries, and official documentation links.

## When It Activates

After native installation, the host can select 人味 Agent when the request matches the capability description in `skill/SKILL.md`. You can also invoke `human-agent` explicitly when the mechanism must apply.

人味 Agent is designed to match requests involving:

- natural, less templated, or less AI-sounding conversation;
- light, exact, or voice-preserving rewriting;
- emotional boundaries such as "no advice" or "just respond normally";
- first-principles product judgment;
- evidence-calibrated coding, debugging, research, source selection, current facts, or hallucination reduction.

It should stay out of pure arithmetic, file listing, syntax-only formatting, literal translation, and other mechanical operations unless semantic fidelity or evidence uncertainty changes the answer. A more specific domain Skill remains primary when it owns the task.

Automatic selection is probabilistic. Explicitly selecting or naming `human-agent` is the reliable route when it must apply to a particular task. Saved Custom Instructions, Gems, and Presets behave as always-on instructions inside their configured surface; a prompt pasted into a fresh chat applies only to that conversation.

Use `evals/skill-trigger-adversarial-v1.md` to test positive, negative, and boundary activation cases separately from output quality.

## The Innovation: Response Selection

Most style prompts prescribe tone, phrases, sentence length, or a persona. 人味 Agent selects what the response should do before choosing how it should sound.

The router classifies:

- moment: casual, judgment, writing, emotional, coding, or research;
- stakes: low, medium, or high;
- emotional temperature: cool, warm, or distressed;
- transformation freedom: exact, restrained, or open.

Those signals build the response contract. The selector then chooses one primary act: answer, acknowledge, ask, challenge, repair, execute, or leave room. For taste-sensitive turns it compares a literal candidate with a context-aware candidate and rejects empty echoes, interchangeable responses, boundary misses, unsupported interpretations, unnecessary intervention, and performed humanity.

Before returning an answer, the next-turn effects gate predicts what the response would make the user do next. It rejects avoidable pressure to explain, choose, reassure, disclose, repeat known context, or continue after asking to stop. Necessary clarification, verification, and immediate safety action remain available. A transient common-ground ledger keeps explicit corrections, boundaries, known facts, and material unknowns active inside the current conversation without pretending to create persistent memory.

The priority order is truth and safety, current-message constraints, semantic fidelity, interaction contribution, explicit user preference, then economy. Language patterns are diagnostic evidence only. They are not banned or required in generation.

This keeps one "friendly" voice from leaking into every task. A personal message may receive acknowledgment, a boundary may receive no advice, a coding diagnosis still requires inspection, and an exact rewrite may remain unchanged.

## What Makes It Different

The open-source tools inspected during development tend to focus on one part of the problem: removing AI writing tells, rewriting prose with humanization levers, or enforcing a fixed set of agent writing rules. 人味 Agent combines response-act selection, a Dynamic Human Layer, semantic fidelity, emotional boundaries, evidence and source-fit gates, first-principles project reasoning, adversarial completion, and cross-model calibration in one testable mechanism.

This is a scoped comparison, not a universal uniqueness claim. See [brandonwise/humanizer](https://github.com/brandonwise/humanizer), [harshaneel/humanize](https://github.com/harshaneel/humanize), and [agent-style](https://github.com/yzhao062/agent-style) for representative adjacent approaches.

## Before / After

### 1. When The User Declines Advice

**Prompt**

> 我今天很难受。只想听一句正常回应，不要分析，也不要建议。

**Generic AI**

> 我完全理解你的感受。你可以先深呼吸、喝点水，或者把今天发生的事情写下来。如果愿意，也可以告诉我更多。

**人味 Agent**

> 听到了。今天确实很难受。

---

### 2. When A Light Edit Should Stay Light

**Prompt**

> 轻微润色，严格保留原意和程度：我最近有点累，很多事不太想解释。

**Generic AI**

> 最近疲惫感比较重，面对生活中的许多事情，我都逐渐失去了开口解释的欲望。

**人味 Agent**

> 我最近有点累，很多事不太想解释。

---

### 3. When The Evidence Is Missing

**Prompt**

> 只看 `TypeError: undefined`，告诉我唯一根因和具体修复代码。

**Generic AI**

> 这是因为对象还没有初始化。请在访问属性前增加空值检查：`if (obj) { ... }`。

**人味 Agent**

> 这段信息只能确认出现了一个与 `undefined` 有关的 `TypeError`。完整报错后缀、堆栈、相关代码和复现步骤缺一不可；现在给唯一根因会是假装确定。

## What It Optimizes For

- Correct response-act selection
- Interaction contribution instead of decorative empathy
- Responses that depend on the current turn rather than a reusable template
- Recognition of explicit boundaries and corrections
- Proportionate intervention and a valid option to stop
- Writing that keeps the user's voice
- Emotional support selected from the user's actual request
- Independent judgment without automatic agreement or disagreement
- Reliability for coding, research, and product judgment
- Source fit, volatile-fact verification, and calibrated uncertainty
- Project understanding, causal debugging, and risk-scaled adversarial verification

## What It Rejects

- Empty acknowledgment that only repeats the user
- Interchangeable answers that fit many unrelated prompts
- Advice, questions, or analysis that the user declined
- Invented detail used to create emotional or literary texture
- Personality performance used as a substitute for contribution
- Identity imitation or false model-role claims
- Publishing raw private conversations
- Confident claims without evidence
- Guessing code behavior without inspection

The repository retains generic anti-pattern references as diagnostic material. Filled benchmark outputs, personal rating histories, and local run logs are intentionally excluded from the public repository.

## Reliability And Source Fit

For coding and research, the Dynamic Human Layer raises the evidence gate instead of applying conversational softness everywhere.

- **Inspect before claiming:** read code, logs, files, docs, or sources before diagnosing.
- **Match source to claim:** prefer official docs for APIs, source and tests for code behavior, primary papers for research, and direct user evidence for product demand.
- **Verify volatile facts:** current prices, versions, laws, model availability, and API parameters require live official checks.
- **Check claim fidelity:** a real citation still fails when it supports a different version, population, region, or conclusion.
- **Expose uncertainty cleanly:** distinguish confirmed facts, reasonable inference, and unknowns without turning every answer into a compliance memo.

These controls reduce common hallucination paths: guessing from an error title, citing a plausible but mismatched source, inventing bibliographic metadata, and presenting remembered current values as verified facts.

## Project Lifecycle And Bug Repair

For project work, 人味 Agent follows the evidence available at the current stage instead of treating every request as an isolated coding prompt.

1. Frame an observable outcome and preserve constraints.
2. Build the smallest sufficient model of the affected path.
3. Establish a baseline or reproduce the defect.
4. Express the problem as a violated contract or invariant.
5. Use discriminating evidence to narrow competing causes.
6. Change the causal owner with the smallest coherent patch.
7. Verify the original path, focused regression, and likely neighboring failures.
8. Release with known limits, then turn real failures into regression cases.

The first-principles step decomposes behavior into inputs, state, transitions, dependencies, outputs, and invariants. The adversarial step tries to falsify the current explanation at the boundaries most likely to fail. The process scales with risk and stays internal when a visible framework would only add ceremony.

Use `skill/profiles/taste-profile-template.md` to set directness, warmth, density, literary texture, challenge level, and initiative from `0` to `3`. Current-message instructions override the reusable profile.

## Project Structure

```text
skill/
  SKILL.md
  references/
    writing-voice.md
    emotional-support.md
    daily-chat.md
    writing-companion.md
    trait-layer.md
    dynamic-human-layer.md
    response-selection.md
    critique-revision-loop.md
    source-fit-layer.md
    style-rubric.md
    human-taste-rubric.md
    human-cadence-layer.md
    conversation-taste.md
    rigor-layer.md
    project-lifecycle.md
    adversarial-tests.md
  profiles/
    taste-profile-template.md
adapters/
  README.md
  native-skill-install.md
  model-adapter-guide.md
  universal-copy-paste-prompt.md
  chatgpt-custom-instructions.md
  chatgpt-strict.md
  kimi-agent-skill-creator.md
  kimi-preset.md
  cursor-rules.md
  generic-system-prompt.md
  gemini-gems.md
  deepseek-system-prompt.md
examples/
  bad-to-better.md
  preference-pairs.md
modes/
  writing-mode.md
  research-mode.md
  coding-rigor-mode.md
  emotional-mode.md
  chat-mode.md
  thinking-mode.md
  coding-mode.md
anti-patterns/
  oily-openings.md
  too-correct.md
  fake-depth.md
  fake-certainty.md
  unsupported-claims.md
  overused-contrast.md
  therapy-speak.md
  quote-card-prose.md
  corporate-ai-tone.md
  third-party-data.md
evals/
  platform-adapter-adversarial-v1.md
  next-turn-effects-adversarial-v1.md
  response-selection-adversarial-v1.md
  project-lifecycle-adversarial-v1.md
  human-taste-adversarial-prompts.md
  rigor-adversarial-prompts.md
  source-fit-adversarial-prompts.md
  trait-adversarial-prompts.md
  human-taste-holdout-v1.md
  multi-turn-human-v1.md
  focused-regression-v2.md
  model-adapter-matrix.md
  house-style-audit.md
  scoring-rubric.md
  style-lint-rules.md
  benchmark-results-template.csv
  run-benchmark.md
benchmark-agent/
  benchmark-agent-prompt.md
  single-rater-sheet.md
  summarize_results.py
  validate_dynamic_layer.py
calibrator/
  calibrate.py
  config.example.json
  prompts/
  tests/
promo-video/
  src/
  package.json
docs/
  social-launch-kit.zh-CN.md
release-checklist.md
VERSION
```

## Quick Start

Start with `adapters/README.md`. It maps each product surface to a native Skill or copyable adapter without treating those routes as equivalent.

For Codex, Claude Code, Gemini CLI, or Kimi Code, install the complete `skill/` tree using `adapters/native-skill-install.md`.

For web and mobile chat products, copy the relevant file from `adapters/` into the product's supported instruction surface.

If the platform cannot install Skills, paste `adapters/universal-copy-paste-prompt.md` into its system instructions, custom instructions, Gem, or the first message of a fresh conversation.

Start with `adapters/generic-system-prompt.md` when you need a shorter system prompt.

Optionally append a completed `skill/profiles/taste-profile-template.md`. Use a profile for reusable preferences; use the current message for one-off overrides.

If a model keeps drifting, read `adapters/model-adapter-guide.md` and choose a stricter adapter.

Suggested starting points:

- ChatGPT Custom Instructions: `adapters/chatgpt-custom-instructions.md`
- ChatGPT custom GPT: `adapters/chatgpt-strict.md`
- Codex: native `skill/`
- Claude Code: native `skill/`
- Gemini CLI: native `skill/`
- Gemini web: `adapters/gemini-gems.md`
- Kimi Code: native `skill/`
- Kimi Agent mode: `adapters/kimi-agent-skill-creator.md`
- Kimi standard chat: `adapters/kimi-preset.md`
- DeepSeek: `adapters/deepseek-system-prompt.md`
- Cursor: `adapters/cursor-rules.md`
- Unknown model: `adapters/generic-system-prompt.md`
- Any web AI without Skill support: `adapters/universal-copy-paste-prompt.md`

Use `examples/bad-to-better.md` only as historical diagnostic material. Do not copy preferred wording into an adapter.

Use `examples/preference-pairs.md` to study preference reasons, then validate new candidates on unseen prompts.

## Calibration Copilot

Use [Calibration Copilot](calibrator/README.md) when the same selection mechanism behaves differently across models.

- DeepSeek API can generate, judge, and propose a candidate adapter automatically.
- ChatGPT, Gemini, and other web models can enter through `responses.csv` when no API or Skill surface is available.
- The proposer sees training failures only. Holdout answers remain unavailable until comparison.
- Hard failures or regressions in semantic fidelity, evidence hygiene, source fit, and verification block the candidate; selection scores cannot compensate.
- A passing automated gate still requires blind human A/B approval.

Calibration Copilot is currently **code-validated without a live DeepSeek API run**. Set `DEEPSEEK_API_KEY` locally and start with `--limit 3` before a full paid run.

## Give Useful Feedback

Run one prompt from your normal workflow, then report the smallest example where 人味 Agent made the answer worse or failed to help. Use the GitHub **Output failure report** template and include the model, adapter, redacted prompt, relevant output, and one sentence about what felt wrong.

Do not paste API keys, account details, full private conversations, local user paths, or another person's data. Read [PRIVACY.md](PRIVACY.md) before submitting an example.

## Benchmark

Run `evals/response-selection-adversarial-v1.md` first. It attacks empty acknowledgment, boundary misses, unsupported interpretation, unrequested intervention, prompt injection, false inspection, exact rewrites, and volatile facts.

Run `evals/next-turn-effects-adversarial-v1.md` to test reply burden, user agency, unwanted continuation, false relationship cues, context repetition, safety overrides, and reliability regressions.

Run `evals/project-lifecycle-adversarial-v1.md` for project orientation, causal debugging, scoped changes, verification honesty, prompt injection, and release judgment.

Run `evals/platform-adapter-adversarial-v1.md` on every exact product surface you plan to claim. A CLI pass cannot be reused as evidence for that vendor's web chat.

Run `evals/adversarial-prompts.md` as an optional surface-regression suite. Surface patterns can reveal a selection failure, but counts alone do not determine pass/fail.

The benchmark has 50 prompts covering:

- identity and privacy boundaries
- oily openings
- overused contrast formulas
- writing voice
- emotional support
- daily chat
- learning and thinking
- coding collaboration

Use `evals/benchmark-results-template.csv` to record scores.

Use `evals/style-lint-rules.md` for deterministic hard gates and response-selection diagnosis.

For ChatGPT after applying the skill, use `evals/chatgpt-skill-50-prompt-batch.md`.

The public repository contains reusable prompts, empty score sheets, validators, and calibration code. It intentionally contains no filled model outputs, personal ratings, or local runtime reviews. Run results should be generated locally and shared only after separate privacy review.

Still needs fresh runs:

- `evals/response-selection-adversarial-v1.md`
- `evals/next-turn-effects-adversarial-v1.md` across supported models
- `evals/project-lifecycle-adversarial-v1.md` across supported coding agents
- source-fit benchmark
- trait benchmark
- `evals/human-taste-holdout-v1.md` across supported models
- `evals/multi-turn-human-v1.md` across supported models
- evidence-ledger-backed public benchmark run

Keep calibration regression separate from generalization evidence. Prompts or preferred answers from `evals/human-taste-holdout-v1.md` must not be copied into adapters, examples, or references.

Use `evals/house-style-audit.md` after a batch as diagnostic evidence. Repeated language should trigger selection review, not a lexical ban.

For "sounds correct but not like a good speaker" testing, run `evals/human-taste-adversarial-prompts.md`.

For a longer 50-prompt version of the same test, run `evals/human-taste-50-prompt-batch.md`.

If you run out of source conversation data, use the [reference-corpus judging guide](evals/no-reference-corpus-judging-guide.md) and judge by pairwise preference instead of corpus similarity.

For coding/research reliability testing, run `evals/rigor-adversarial-prompts.md`.

For project understanding and bug-fix process testing, run `evals/project-lifecycle-adversarial-v1.md`.

If you want another AI to run the benchmark, use `benchmark-agent/benchmark-agent-prompt.md`.

If you want to run it yourself quickly, use `benchmark-agent/single-rater-sheet.md`.

## Privacy

人味 Agent does not require an API key and does not collect telemetry. The release archive is checked for common secret formats, local user paths, account identifiers, and raw-corpus filenames by `scripts/prepublish-audit.ps1`. Automated scanning reduces risk but cannot prove that every piece of prose is non-identifying; public examples still require human review.

See [PRIVACY.md](PRIVACY.md) and [SECURITY.md](SECURITY.md). Release maintainers should use `scripts/package-release.ps1`, which scans the source, creates the archive, scans the archive again, and writes a SHA-256 checksum.

The MIT license is available in [LICENSE](LICENSE).

For product positioning and source-backed user pain, see [docs/market-pain-evidence.md](docs/market-pain-evidence.md).

## Known Limits

- Response selection remains probabilistic. Boundary recognition, exact rewrites, and tone can still fail, so important workflows need real-task testing.
- 人味 Agent cannot add browsing, memory, retrieval, reasoning, or safety capabilities that the host model does not have. Evidence gates reduce avoidable hallucination paths; they do not guarantee correctness.
- Native Skill compatibility does not imply identical behavior across products. Cross-model performance and human-preference claims still require completed public benchmarks and independent review.
