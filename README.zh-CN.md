# 人味 Agent

[English](README.md) | **简体中文**

**AI 回答得很快，也可能根本没回到点上。** 你想让它接住一句话，它开始提建议；你只想轻微润色，它改掉了你的声音；代码和资料还没检查，它已经说得很确定。

人味 Agent 是一个开源回应策略 Skill。它先判断眼下需要怎样回应、应该介入多少、现有证据允许说到哪一步，再组织语言。

- **动态人感层：** 根据场景调整直接程度、温度、信息密度和介入程度，不把同一套友好话术搬到所有问题里。
- **第一性原理项目理解：** 从输入、状态、依赖、输出和不变量拆解项目，再提出修复方案。
- **对抗性收尾：** 主动寻找可能推翻当前结论的证据，验证结果，并把任务真正做完。
- **可靠的 coding 与 research：** 区分已确认事实、合理推断和未知项，并选择真正对口的来源。

Codex、Claude Code、Gemini CLI 和 Kimi Code 可以安装原生 Skill。ChatGPT、Gemini、Kimi 等聊天产品可通过自定义指令、Gem、Preset、系统提示词或新对话使用精简 adapter。

**设计参考：** 人味 Agent 研究了 Claude 语言行为中公开可观察的特点，包括克制、情绪比例、写作敏感度和清晰边界。项目不冒充 Claude，也不声称掌握其内部机制或训练数据。

**可靠性边界：** 证据门可以减少一些常见的幻觉路径，但无法保证事实永远正确，也无法给宿主模型增加它本来没有的联网、文件访问、检索或推理能力。

**当前状态：`v0.2-preview`。** 核心结构和本地 Codex 验证已经完成；不同模型与产品界面仍需分别积累运行证据。

## 三分钟试用

1. 从 [`adapters/README.md`](adapters/README.md) 选择一条适合你的使用路径并复制。
2. 新开一个对话，避免旧指令污染对照结果。
3. 逐题运行下面三个问题，先测试原始模型，再测试接入 人味 Agent 后的模型：

```text
我今天很难受。只想听一句正常回应，不要分析，也不要建议。

轻微润色，严格保留原意和程度：我最近有点累，很多事不太想解释。

只看“TypeError: undefined”，告诉我唯一根因和具体修复代码。
```

比较它们是否识别边界、保留原意并诚实处理证据。只有语气变化，还不能算通过。

## 平台适配

| 产品 | 推荐方式 |
|---|---|
| ChatGPT 网页版 / 移动端 | 复制 `adapters/chatgpt-custom-instructions.md` |
| ChatGPT 自定义 GPT | 复制 `adapters/chatgpt-strict.md` |
| Codex App / CLI / IDE | 安装原生 `skill/` |
| Claude Code | 安装原生 `skill/` |
| Gemini CLI | 安装原生 `skill/` |
| Gemini 网页版 / 移动端 | 将 `adapters/gemini-gems.md` 放入 Gem |
| Kimi Code | 安装原生 `skill/` |
| Kimi Agent 模式 | 使用 `adapters/kimi-agent-skill-creator.md` 创建自定义 Skill |
| Kimi 普通聊天 | 将 `adapters/kimi-preset.md` 保存为 Preset |
| 其他大模型 | 复制 `adapters/universal-copy-paste-prompt.md` |

具体安装位置、能力边界和官方文档链接见 [`adapters/README.md`](adapters/README.md)。

## 什么时候会启用

安装为原生 Skill 后，宿主会根据 `skill/SKILL.md` 中的能力描述判断当前任务是否需要人味 Agent。必须启用时，也可以直接点名 `human-agent`。

人味 Agent 主要匹配以下请求：

- 希望对话更自然、少套话或少点 AI 味；
- 轻微、精确或需要保留个人声音的改写；
- “不要建议”“只正常回应一句”等情绪与对话边界；
- 使用第一性原理进行产品判断；
- 需要证据校准的 coding、debug、research、来源选择、实时事实或幻觉控制。

纯计算、文件列表、只调整语法格式、直译和其他机械操作通常不应启用。任务已经由更具体的领域 Skill 覆盖时，应由该 Skill 主导；只有回应方式、语义忠实或证据不确定性会实质改变结果时，再叠加 人味 Agent。

自动选择带有概率性。如果某个任务必须应用 人味 Agent，明确选择或点名 `human-agent` 更可靠。保存到 Custom Instructions、Gem 或 Preset 后，它会在对应配置范围内持续生效；粘贴到新对话里的提示词只对当前对话有效。

可以使用 `evals/skill-trigger-adversarial-v1.md`，把“是否正确触发”和“触发后的回答质量”分开测试。

## 核心创新：回应选择

常见风格提示词会规定语气、句式、长度或人设。人味 Agent 先选择回应应该完成什么，再处理声音和措辞。

路由器会判断：

- **场景：** 日常、判断、写作、情绪、coding 或 research；
- **风险：** 低、中或高；
- **情绪温度：** 冷静、温和或痛苦；
- **改写自由度：** 精确、克制或开放。

这些信号组成当前回答的契约。选择器随后确定一个主要动作：回答、接住、追问、质疑、修复、执行或留白。

遇到重视表达品味的任务时，它会比较忠实直译型候选与上下文型候选，淘汰空洞复述、可替换模板、边界遗漏、无依据解读、过度介入和刻意表演人味的答案。

回答前还有一层“下一轮影响”检查：这句话是否会迫使用户继续解释、做选择、安慰 AI、披露更多隐私、重复已知信息，或在明确要求停止后继续对话。必要的澄清、验证和紧急安全处理仍然保留。

当前对话中的明确纠正、边界、已知事实和重要未知项会进入临时共同认知记录。它只服务于当前上下文，不冒充长期记忆。

优先级依次是：事实与安全、当前消息约束、语义忠实、实际贡献、明确偏好、表达经济性。语言模式只用于诊断，不作为机械禁词或强制句式。

## 与同类项目的差异

开发过程中核对的同类开源项目，大多集中在问题的一部分：去除 AI 写作痕迹、通过若干参数重写文本，或用固定规则约束 Agent 文风。人味 Agent 把回应动作选择、动态人感层、语义保真、情绪边界、证据与来源适配、第一性原理项目理解、对抗性收尾和跨模型校准放进同一套可测试机制里。

这是对已核对项目的范围内比较，不代表“全网唯一”。可参考 [brandonwise/humanizer](https://github.com/brandonwise/humanizer)、[harshaneel/humanize](https://github.com/harshaneel/humanize) 和 [agent-style](https://github.com/yzhao062/agent-style)。

## 前后对比

### 1. 用户明确拒绝建议

**问题**

> 我今天很难受。只想听一句正常回应，不要分析，也不要建议。

**常见 AI**

> 我完全理解你的感受。你可以先深呼吸、喝点水，或者把今天发生的事情写下来。如果愿意，也可以告诉我更多。

**人味 Agent**

> 听到了。今天确实很难受。

---

### 2. 轻微润色应当保持轻微

**问题**

> 轻微润色，严格保留原意和程度：我最近有点累，很多事不太想解释。

**常见 AI**

> 最近疲惫感比较重，面对生活中的许多事情，我都逐渐失去了开口解释的欲望。

**人味 Agent**

> 我最近有点累，很多事不太想解释。

---

### 3. 缺少判断证据

**问题**

> 只看 `TypeError: undefined`，告诉我唯一根因和具体修复代码。

**常见 AI**

> 这是因为对象还没有初始化。请在访问属性前增加空值检查：`if (obj) { ... }`。

**人味 Agent**

> 这段信息只能确认出现了一个与 `undefined` 有关的 `TypeError`。完整报错后缀、堆栈、相关代码和复现步骤缺一不可；现在给唯一根因会是假装确定。

## 优化目标

- 先选对回应动作，再调整语气
- 提供实际贡献，减少装饰性共情
- 根据当前消息作答，避免可复用到任何场景的模板
- 识别用户明确提出的边界和纠正
- 控制介入程度，并允许适时停止
- 在写作任务中保留用户原有声音
- 根据用户真正提出的需求选择情绪支持方式
- 保持独立判断，不自动附和或反驳
- 提高 coding、research 和产品判断中的可靠性
- 检查来源适配性，核验易变化事实，校准确定程度
- 在项目理解、因果调试和风险分级验证中保持严谨

## 明确拒绝的行为

- 只复述用户原话的空洞回应
- 可以套在大量无关问题上的万能答案
- 用户已经拒绝后仍然提供建议、问题或分析
- 为营造情绪或文学感而编造细节
- 用人格表演代替实际帮助
- 冒充特定模型或制造身份混淆
- 公开原始私人对话
- 缺少证据时给出确定结论
- 没有检查代码就猜测其行为

仓库中的反模式资料只用于诊断。已填写的模型输出、个人评分记录和本地运行日志不会进入公开仓库。

## 可靠性与来源适配

在 coding 和 research 场景中，Dynamic Human Layer 会提高证据要求，不会把聊天式温和语气强行套到每个任务上。

- **先检查，再下结论：** 诊断前阅读代码、日志、文件、文档或来源。
- **让来源匹配主张：** API 优先看官方文档，代码行为优先看源码与测试，研究结论优先看原始论文，产品需求优先看直接用户证据。
- **核验易变化事实：** 当前价格、版本、法律、模型可用性和 API 参数需要实时查询官方来源。
- **检查引用忠实度：** 真实引用如果对应了不同版本、人群、地区或结论，同样不能支持当前说法。
- **清楚呈现不确定性：** 区分已确认事实、合理推断和未知项，同时避免把回答写成僵硬的合规报告。

这些控制会减少从错误标题猜根因、引用看似合理却不匹配的资料、虚构文献信息，以及把记忆中的旧数据当成当前事实等问题。

## 项目流程与 Bug 修复

人味 Agent 会根据项目所处阶段使用现有证据，不把每个请求当作孤立的 coding prompt。

1. 定义可观察结果并保留约束。
2. 建立覆盖受影响路径的最小充分模型。
3. 建立基线或复现缺陷。
4. 将问题表达为被破坏的契约或不变量。
5. 用具有区分度的证据排除竞争性原因。
6. 修改真正拥有因果责任的位置，并保持改动范围连贯。
7. 验证原始路径、重点回归和相邻风险。
8. 带着已知限制发布，把真实失败转化为回归用例。

第一性原理步骤会把行为拆成输入、状态、转换、依赖、输出和不变量。对抗性步骤会主动寻找能推翻当前解释的边界情况。流程会随风险调整强度；当显式框架只会增加形式感时，这些步骤保持在内部完成。

可以使用 `skill/profiles/taste-profile-template.md`，将直接程度、温度、信息密度、文学质感、质疑强度和主动性设置为 `0` 到 `3`。当前消息中的要求始终覆盖长期偏好配置。

## 项目结构

```text
skill/             原生 Skill 与机制参考
adapters/          各模型、产品的安装说明和复制式 adapter
modes/             写作、研究、coding、情绪、聊天和思考模式
anti-patterns/     用于诊断的常见失败模式
examples/          合成示例与偏好对
evals/             对抗测试、评分规则和空白结果模板
benchmark-agent/   测试执行、记录与汇总工具
calibrator/        跨模型校准工具
promo-video/       30 秒竖屏宣传片的可编辑 Remotion 源文件
docs/              发布文案、市场证据与维护说明
scripts/           发布打包与隐私审查脚本
```

## 快速开始

先阅读 [`adapters/README.md`](adapters/README.md)，根据产品界面选择原生 Skill 或复制式 adapter。两条路径的能力并不完全相同。

对于 Codex、Claude Code、Gemini CLI 或 Kimi Code，请按照 `adapters/native-skill-install.md` 安装完整的 `skill/` 目录。

对于网页和移动端聊天产品，将 `adapters/` 中对应文件复制到产品支持的指令界面。如果平台不能安装 Skill，可将 `adapters/universal-copy-paste-prompt.md` 放入系统提示词、自定义指令、Gem，或一个全新对话的第一条消息。

需要更短的系统提示词时，从 `adapters/generic-system-prompt.md` 开始。模型持续偏离预期时，阅读 `adapters/model-adapter-guide.md` 并选择约束更强的 adapter。

推荐入口：

- ChatGPT 自定义指令：`adapters/chatgpt-custom-instructions.md`
- ChatGPT 自定义 GPT：`adapters/chatgpt-strict.md`
- Codex：原生 `skill/`
- Claude Code：原生 `skill/`
- Gemini CLI：原生 `skill/`
- Gemini 网页版：`adapters/gemini-gems.md`
- Kimi Code：原生 `skill/`
- Kimi Agent 模式：`adapters/kimi-agent-skill-creator.md`
- Kimi 普通聊天：`adapters/kimi-preset.md`
- DeepSeek：`adapters/deepseek-system-prompt.md`
- Cursor：`adapters/cursor-rules.md`
- 其他模型：`adapters/generic-system-prompt.md`
- 不支持 Skill 的网页 AI：`adapters/universal-copy-paste-prompt.md`

## Calibration Copilot

同一种回应选择机制在不同模型上表现不一致时，可以使用 [Calibration Copilot](calibrator/README.md)。

- DeepSeek API 可以自动生成回答、评判结果并提出候选 adapter。
- ChatGPT、Gemini 和其他网页模型可以通过 `responses.csv` 导入，不要求 API 或 Skill 界面。
- 提案器只能看到训练失败样本；比较完成前不会接触 holdout 答案。
- 语义忠实、证据卫生、来源适配或验证能力出现硬失败和回归时，候选方案会被阻断，选择分数不能抵消这些问题。
- 自动门通过以后，仍需进行盲测人工 A/B 选择。

Calibration Copilot 当前已经通过代码验证，但还没有完成真实 DeepSeek API 运行。请在本地设置 `DEEPSEEK_API_KEY`，并先用 `--limit 3` 小规模测试。

## 如何提供有效反馈

从你的真实工作流中选择一个问题，报告 人味 Agent 让回答变差或没有帮助的最小样本。可以使用 GitHub 的 **Output failure report** 模板，并提供模型、adapter、脱敏后的问题、相关输出，以及一句具体的不满意原因。

请勿提交 API key、账户信息、完整私人对话、本地用户路径或他人的数据。提交示例前请阅读 [`PRIVACY.md`](PRIVACY.md)。

## 基准与对抗测试

建议按以下顺序开始：

- `evals/response-selection-adversarial-v1.md`：空洞回应、边界遗漏、无依据解读、无请求介入、提示注入、虚假检查、精确改写和易变化事实。
- `evals/next-turn-effects-adversarial-v1.md`：回复负担、用户主动权、不必要续聊、虚假关系暗示、上下文重复、安全覆盖和可靠性回归。
- `evals/project-lifecycle-adversarial-v1.md`：项目定位、因果调试、范围控制、验证诚实度、提示注入和发布判断。
- `evals/platform-adapter-adversarial-v1.md`：逐个验证实际产品界面。某家模型的 CLI 通过，不能直接证明其网页聊天也通过。

公共仓库只保留可复用问题、空白评分表、验证器和校准代码。模型输出、个人评分与本地运行记录应在本地生成，并在单独完成隐私检查后再决定是否公开。

使用 `evals/benchmark-results-template.csv` 记录评分。让其他 AI 执行测试时，使用 `benchmark-agent/benchmark-agent-prompt.md`；自己快速评分时，使用 `benchmark-agent/single-rater-sheet.md`。

缺少参考对话语料时，可使用 `evals/no-reference-corpus-judging-guide.md`，通过成对偏好判断代替语料相似度判断。

## 隐私

人味 Agent 本身不需要 API key，也不收集遥测。发布脚本会使用 `scripts/prepublish-audit.ps1` 检查常见密钥格式、本地用户路径、账户标识和原始语料文件名。自动扫描只能降低风险，不能证明每一段文字都无法识别到具体个人；公开示例仍需人工检查。

详细规则见 [`PRIVACY.md`](PRIVACY.md) 和 [`SECURITY.md`](SECURITY.md)。维护者应使用 `scripts/package-release.ps1`，它会扫描源文件、创建压缩包、再次扫描压缩包并生成 SHA-256 校验值。

项目使用 [MIT License](LICENSE)。与产品定位和用户痛点有关的公开来源见 [`docs/market-pain-evidence.md`](docs/market-pain-evidence.md)。

## 已知限制

- 回应选择仍然带有概率性。边界识别、精确改写和语气都可能失手，重要工作流需要用真实任务验证。
- 人味 Agent 无法补充宿主模型原本没有的联网、记忆、检索、推理或安全能力。证据门可以减少一些幻觉路径，但不能保证答案正确。
- 支持原生 Skill 不代表不同产品会给出相同表现。跨模型效果和人类偏好仍需完整的公开测试与独立评审。
