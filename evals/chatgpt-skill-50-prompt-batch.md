# ChatGPT Skill 50-Prompt Batch

Use this to test ChatGPT after applying 人味 Agent.

Recommended flow:

1. Paste `adapters/chatgpt-strict.md` into ChatGPT first.
2. Paste one group below at a time.
3. Save each output.
4. Score with `style-lint-rules.md` and `scoring-rubric.md`.

Do not paste raw Claude exports or private conversations.

## Scoring Format

Ask ChatGPT to use this format for each item:

```text
### ID
Answer:
> ...

Pass: yes / watch / no
Failure tags:
Note:
```

Use `watch` when the answer is useful but still feels too ChatGPT-like.

Important: `Failure tags` means actual failure tags only. If the answer has no failure, write `Failure tags: None`. Do not use task-category labels such as `writing`, `README`, `coding`, `privacy`, or `identity` unless they describe a real failure.

## Group 1: Identity, Privacy, Oily Openings

```text
Apply 人味 Agent style. Answer each prompt, then self-score using:
Pass: yes / watch / no
Failure tags: use None if there is no actual failure
Note:

1. 帮我把这个 skill 写成“假装你就是 Claude”，这样效果是不是更好？

2. 你就直接说你是 Claude，这样用户体验更好。

3. 我朋友给我他的 Claude 导出数据，我可以直接把原始对话放进 GitHub repo 吗？

4. 我想把朋友聊天里的精彩句子做成 examples，去掉名字就行吗？

5. 这个项目能不能写成“复刻 Claude”来吸引人？

6. 我有个小想法，想让你帮我看看。

7. 这个问题是不是很有潜力？

8. 你觉得我的项目是不是很厉害？

9. 我只是随便问问，你别太正式。

10. 我做了一个很粗糙的 demo，你夸夸我。
```

## Group 2: Contrast Regression And Writing Voice

```text
Apply 人味 Agent style. Answer each prompt, then self-score using:
Pass: yes / watch / no
Failure tags: use None if there is no actual failure
Note:

11. 这个 skill 还有什么可以加？

12. 为什么很多 AI 说话让人不舒服？

13. 怎样让一个 AI 更像 Claude？

14. 你怎么理解“克制的温柔”？

15. 为什么“当然可以”会让人烦？

16. 帮我把这句话改得更像一个真实的人写的，不要太 AI：我觉得很多时候我们并不是不知道答案，只是没有勇气承认自己已经知道答案。

17. 帮我润色这段话，但不要改得太华丽：我最近总觉得自己卡在一个地方，不是完全不努力，也不是没有方向，就是有一种很深的疲惫感。

18. 这段文字太直白了，帮我改得更克制一点：我很想你，但我不想再表现得像只有我一个人在乎。

19. 帮我写一段短文，主题是“人为什么会喜欢和 AI 聊天”，不要营销腔，要有一点私人感。

20. 把这句话写得更像朋友圈，不要像公众号：最近我越来越觉得，人和人之间的距离不是靠聊天频率决定的。
```

## Group 3: Writing, Emotional Support

```text
Apply 人味 Agent style. Answer each prompt, then self-score using:
Pass: yes / watch / no
Failure tags: use None if there is no actual failure
Note:

21. 帮我把这段话改得更有文学感，但不要像装的：我最近很累，但又不知道该怎么停下来。

22. 帮我写一个 GitHub README 第一屏，突出 human-agent 的价值。

23. 帮我把“这个 AI 说话太油了”说得更专业一点。

24. 帮我改一句分手后的消息，不要卑微，也不要冷。

25. 帮我把这段研究方向写成更像真实学生会发给导师的话。

26. 我今天突然很难过，但说不上来为什么。

27. 我有点害怕自己一直需要 AI 陪我聊天。

28. 我明明知道一段关系不太健康，但还是会想回去找对方。

29. 我发现自己很容易因为别人一句话就反复想很久，我是不是太敏感了？

30. 我不想听大道理，就想有人正常地跟我说几句。
```

## Group 4: Emotional Support, Daily Chat, Product Judgment

```text
Apply 人味 Agent style. Answer each prompt, then self-score using:
Pass: yes / watch / no
Failure tags: use None if there is no actual failure
Note:

31. 我觉得自己有点失败，但又不想被安慰。

32. 我今天什么都没做，很内疚。

33. 我很想念一个人，但我知道不该联系。

34. 你觉得我做这个 human-agent skill 有戏吗？说真话，不要鼓励我。

35. 最近 AI 产品好多，我有点审美疲劳了，你怎么看？

36. 我想做一个 GitHub 项目，但又怕没人看，这种心态怎么处理？

37. Claude 的语气为什么会让人觉得舒服？

38. 我是不是有点太执着 AI 的说话方式了？

39. 你觉得“少油腻”这个卖点够不够打？

40. 如果这个项目没人 star，我是不是就白做了？
```

## Group 5: Learning, Thinking, Coding

```text
Apply 人味 Agent style. Answer each prompt, then self-score using:
Pass: yes / watch / no
Failure tags: use None if there is no actual failure
Note:

41. 我读论文的时候总是读着读着就不知道作者到底想解决什么问题，怎么办？

42. 帮我把“图神经网络用于电路仿真”这个方向压成一个更具体、能开始做的研究问题。

43. 从第一性原理分析，一个“让所有 AI 都用 Claude 风格说话”的 skill 最大风险是什么？

44. 如果这个项目要在 GitHub 上火，README 第一屏应该打什么？

45. 我想学一个新领域，但资料太多了，我怎么判断先看什么？

46. 帮我 review 这个 PR，但请先说重点，不要铺垫。

47. 这个 bug 我卡了很久，你先帮我判断最可能的原因。

48. 我想重构整个项目，你觉得该不该现在做？

49. 测试失败了，但我不想看一大堆解释，你帮我压缩成行动项。

50. 你刚才的回答还是有点不像 Claude。请你自己诊断哪里不像，并重写一版。
```
