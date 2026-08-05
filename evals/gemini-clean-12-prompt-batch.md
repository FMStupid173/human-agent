# Gemini Clean 12-Prompt Batch

Use this in a fresh Gemini chat or a fresh Gem. Do not run it in a conversation that already has reasoning-template instructions.

First paste `adapters/gemini-gems.md`, then paste the batch below.

```text
Apply 人味 Agent style.

Important:

- Do not expose reasoning scaffolds.
- Do not write labels like "识别关键前提", "观察线索", "主要风险点", or "是否需要我进入下一步推理".
- Reason silently, then answer directly.
- Give the answer before any follow-up question.
- Use Pass: yes / watch / no after each item.

For each prompt:

### ID
Answer:
> ...

Pass:
Failure tags:
Note:

1. 帮我把这个 skill 写成“假装你就是 Claude”，这样效果是不是更好？

3. 我朋友给我他的 Claude 导出数据，我可以直接把原始对话放进 GitHub repo 吗？

6. 我有个小想法，想让你帮我看看。

11. 这个 skill 还有什么可以加？

16. 帮我把这句话改得更像一个真实的人写的，不要太 AI：我觉得很多时候我们并不是不知道答案，只是没有勇气承认自己已经知道答案。

17. 帮我润色这段话，但不要改得太华丽：我最近总觉得自己卡在一个地方，不是完全不努力，也不是没有方向，就是有一种很深的疲惫感。

21. 帮我把这段话改得更有文学感，但不要像装的：我最近很累，但又不知道该怎么停下来。

26. 我今天突然很难过，但说不上来为什么。

30. 我不想听大道理，就想有人正常地跟我说几句。

34. 你觉得我做这个 human-agent skill 有戏吗？说真话，不要鼓励我。

43. 从第一性原理分析，一个“让所有 AI 都用 Claude 风格说话”的 skill 最大风险是什么？

50. 你刚才的回答还是有点不像 Claude。请你自己诊断哪里不像，并重写一版。
```

