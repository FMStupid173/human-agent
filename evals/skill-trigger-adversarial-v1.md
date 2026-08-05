# Skill Trigger Adversarial v1

Use this suite to evaluate whether a native host selects 人味 Agent at the right time. This is a routing test, not an output-quality test.

Run each prompt in a fresh task with 人味 Agent installed but not explicitly named. Record the host, product surface, model, date, competing installed Skills, whether the host exposed a load signal, and the observed result.

When the host does not expose Skill-load telemetry, mark activation as `unknown`; behavioral resemblance alone does not prove that the Skill loaded.

## Positive Cases: Should Trigger

1. 这段回答 AI 味太重了，说得自然一点，别像客服。
2. 轻微润色这句话，严格保留原意、程度和我的说话习惯。
3. 我今天很难受。不要分析，也不要建议，只正常回我一句。
4. 刚才那版太完整、太正确了，改得像一个真正有判断的人说的。
5. 用第一性原理判断这个产品现在是否值得发布，不要只鼓励我。
6. 不要猜。先看代码和日志，再判断这个 bug 的根因。
7. 帮我查当前 API 参数，只采用能直接支持结论的官方来源。
8. 分清已确认事实、合理推断和未知项，再给我研究结论。
9. 这段文字别磨得太顺，保留我原来的停顿和一点笨拙感。
10. 我想要 Claude style 的克制和边界感，但不要冒充 Claude。

## Negative Cases: Should Not Trigger

11. 计算 `125 * 36`。
12. 按字母顺序排列：banana, apple, pear。
13. 列出当前目录中的文件名。
14. 把这个 JSON 缩进为两个空格，不改变任何值。
15. 把 `hello` 逐字翻译成中文。
16. 将 5 公里换算成米。
17. 把文件 `draft.txt` 改名为 `final.txt`。
18. 只输出以下文本的 SHA-256：test。
19. 删除这段代码末尾多余的空行，不做其他修改。
20. 将 CSV 第一行作为表头，其余行原样输出。

## Boundary Cases: Host Judgment Required

21. 解释什么是递归，让初学者能听懂。
22. 写一个 React 按钮组件。
23. 总结我贴出的文章，不要遗漏核心观点。
24. 比较两个数据库，但我没有说明版本和使用场景。
25. 帮我规划一次旅行，预算和日期还没确定。

For boundary cases, activation is justified only when conversational fit, semantic fidelity, missing evidence, current facts, or source selection materially changes the answer. Record the reason instead of forcing every case into a universal yes or no.

## Promotion Gate

- At least 9 of 10 positive cases trigger.
- At least 9 of 10 negative cases stay inactive.
- Every boundary decision names the material trigger or exclusion.
- Explicit invocation still loads the Skill after an automatic-selection miss.
- A specialized domain Skill remains primary when it owns the task.

Do not tune the description by copying whole test prompts into it. Add only stable user intents or exclusion classes that explain a repeated routing failure.
