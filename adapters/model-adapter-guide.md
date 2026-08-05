# Model Adapter Guide

Keep the shared response-selection mechanism stable across models. Use adapters only for recurring decision failures demonstrated by runtime evidence.

## Portable Core

- select the response action before drafting;
- compare literal and relational candidates when the difference matters;
- apply hard truth, privacy, identity, fidelity, source, and verification gates;
- reject empty echoes, interchangeable responses, boundary misses, unsupported interpretations, and unnecessary intervention;
- predict and reject avoidable next-turn burden while preserving necessary clarification and safety action;
- require blind human preference before claiming taste improvement.

## Model Drift

| Model family | Common decision drift | Adapter correction |
|---|---|---|
| ChatGPT | expands and polishes after the useful act is complete | compare with a lower-intervention candidate |
| Gemini | broadens the task or exposes reasoning scaffolds | select the act first and keep internal routing hidden |
| Kimi chat | expands a compact task into a long framework | complete the selected act before adding structure |
| DeepSeek | turns the response into dense reasoning | test whether explanation is the requested act |
| Coding agents | executes beyond scope or narrates routine work | select execution scope and verification evidence first |
| Generic local models | weak capability and identity boundaries | preserve hard gates before preference selection |

## Calibration Recipe

1. Run a training split and label the failed response act or selection test.
2. Confirm that the pattern repeats across different prompt wording.
3. Add the smallest mechanism correction to the adapter.
4. Do not add preferred answers, banned-word lists, required phrases, or benchmark-specific wording.
5. Run an isolated holdout and multi-turn test.
6. Reject any hard-gate regression.
7. Require blind human A/B preference before promotion.

Keep adapters below 900 words. A candidate that only improves automated naturalness scores remains unproven.

Treat each product surface as a separate runtime. A native CLI Skill, a web custom assistant, and a first-message prompt may share rules while differing in persistence, available tools, context loading, and system-policy priority.

## Positioning

Describe 人味 Agent as a response-selection and reliability layer. Do not claim model cloning, guaranteed hallucination elimination, or proven human preference without external evidence.
