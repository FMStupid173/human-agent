# Market Pain Evidence

This note separates observed user pain, research evidence, and product inference. It is positioning input, not proof of product-market fit.

## 1. Over-agreement Damages Trust

OpenAI rolled back a GPT-4o update after it became overly flattering and agreeable. The company wrote that this behavior could feel uncomfortable, distort decisions, and reinforce negative emotions. Anthropic has also reported sycophancy across multiple assistants and linked part of it to preference optimization that rewards agreement over truth.

Sources:

- [OpenAI: Sycophancy in GPT-4o](https://openai.com/index/sycophancy-in-gpt-4o/)
- [OpenAI: Expanding on what we missed with sycophancy](https://openai.com/index/expanding-on-sycophancy/)
- [Anthropic: Towards Understanding Sycophancy in Language Models](https://www.anthropic.com/news/towards-understanding-sycophancy-in-language-models)

人味 Agent response: require plain judgment, permit disagreement, avoid automatic praise, and distinguish emotional support from endorsing the user's conclusion.

## 2. Default AI Voice Feels Verbose and Corporate

Long-running Reddit and Hacker News discussions repeatedly describe default assistant writing as overly verbose, excessively diplomatic, bland, formulaic, corporate, and too structurally neat. A current V2EX discussion independently calls out repeated contrast formulas such as `不是……而是……` and asks for less performative phrasing.

These are anecdotal signals, not population estimates. Their value is the recurrence and specificity of the complaints.

Sources:

- [Reddit: How do you describe ChatGPT's writing style?](https://www.reddit.com/r/ChatGPT/comments/13fo6zp/how_do_you_describe_chatgpts_writing_style/)
- [Reddit: GPT writing style is forever ruining the Internet for me](https://www.reddit.com/r/ChatGPT/comments/1okspdz/gpt_writing_style_is_forever_ruining_the_internet/)
- [Hacker News: writing tools can take away the writer's voice](https://news.ycombinator.com/item?id=45598270)
- [Hacker News: complaints about verbose, bland corporate speech](https://news.ycombinator.com/item?id=46273704)
- [V2EX: users discuss repeated contrast phrasing and unnecessary tone](https://global.v2ex.com/t/1203852)

人味 Agent response: human-cadence checks, anti-pattern linting, fewer automatic sections, direct openings, restrained length, and task-sensitive structure.

## 3. Editing Can Remove the Writer's Voice

A pre-registered study of post-editing found that people could move LLM drafts closer to their personal style, but the edited text still retained LLM traces and showed less stylistic diversity than unassisted writing. Community discussions describe the practical version of the same problem: polishing can make a message cleaner while making it feel less like the writer.

Sources:

- [Can You Make It Sound Like You? Post-Editing LLM-Generated Text for Personal Style](https://arxiv.org/abs/2604.24444)
- [Hacker News: "it'd take away my voice"](https://news.ycombinator.com/item?id=45598270)

人味 Agent response: semantic and proposition locks, exact rewrite mode, a reusable taste profile, and an instruction to leave already-clear language alone.

## 4. Fluent Answers Can Still Be Unreliable

Hallucinations often appear plausible, so the user must calibrate trust by task risk and available evidence. Research reviews emphasize external grounding and validated sources; prompting alone cannot guarantee factuality.

Sources:

- [Calibrated Trust in Dealing with LLM Hallucinations](https://arxiv.org/abs/2512.09088)
- [Hallucination to Truth: A Review of Fact-Checking and Factuality Evaluation](https://arxiv.org/abs/2508.03860)

人味 Agent response: separate confirmed facts, inference, and unknowns; require current verification for volatile claims; prefer primary sources; decline fabricated citations. The project should never claim to eliminate hallucinations or replace retrieval.

## 5. Users Already Try to Build Their Own Style Layer

OpenAI exposes personality controls and explains that personality affects how ChatGPT communicates. Multiple open-source `humanizer` skills and recurring prompt-sharing threads show that users are already patching default model voice themselves.

Sources:

- [OpenAI: Customizing your ChatGPT personality](https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality)
- [jpeggdev/humanize-writing](https://github.com/jpeggdev/humanize-writing)
- [blader/humanizer](https://github.com/blader/humanizer)
- [harshaneel/humanize](https://github.com/harshaneel/humanize)

Product inference: demand for style control exists, but the `humanizer` label is crowded and often associated with detector evasion. 人味 Agent should lead with output quality, judgment, semantic fidelity, and evidence boundaries.

## Best Initial Users

- heavy AI users who repeatedly rewrite the model's tone;
- developers who want concise diagnosis without fabricated certainty;
- researchers who need source and uncertainty hygiene;
- writers who want editing help without losing their voice;
- people who want emotional proportion without automatic therapy language or agreement.

## Positioning

Recommended:

> A portable Dynamic Human Layer that adapts voice, semantic fidelity, and evidence requirements to each task.

Chinese:

> 一套跨模型的动态人味层：根据聊天、写作、情绪、coding 和 research 动态调整表达与证据门槛。

Reliability claim:

> Designed to reduce avoidable hallucinations and improve source fit, claim verification, and uncertainty handling. It does not guarantee correctness or replace the host model's retrieval system.

Avoid:

- "Clone Claude on every model"
- "Make AI indistinguishable from a human"
- "Bypass AI detection"
- "Eliminate hallucinations"
- "Scientifically proven to be preferred by users"

## What Would Validate the Pain

Public discussion proves that the complaint exists. Product evidence requires behavior:

- a user installs or copies an adapter;
- the user applies it to a real task;
- the user prefers the result or reports a concrete regression;
- the user keeps it enabled after several days;
- the same failure category appears across multiple users or models.
