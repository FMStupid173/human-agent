# Public Source Notes

These notes summarize public materials that informed 人味 Agent's rubric and human-cadence layer.

They are not claims about Claude's private implementation.

## Anthropic: Claude's Character

Useful takeaways:

- Character can be treated as a behavior layer, not a brand identity.
- Good assistant behavior includes truthfulness without unkindness, curiosity, open-mindedness, and avoiding both overconfidence and excessive caution.
- The model should not simply mirror the user's views or pretend to be objective and infallible.
- Character traits should behave like nudges, not rigid rules.
- Human review still matters when adjusting traits.

Source: https://www.anthropic.com/news/claude-character

## Constitutional AI

Useful takeaways:

- Written principles can steer behavior.
- Critique -> revision loops are a practical way to improve output.
- Harmlessness should not collapse into evasiveness.
- A good refusal should still engage with the user and explain the boundary.

Source: https://arxiv.org/abs/2212.08073

## Claude Styles

Useful takeaways:

- Style is context-dependent: concise, formal, explanatory, and custom styles serve different needs.
- User-provided writing samples can define a preferred voice.
- A useful style system should support tone and structure, not just word choice.

Source: https://claude.com/blog/styles

## 人味 Agent Interpretation

For this project, the transferable method is:

1. Define traits as behavioral standards.
2. Create adversarial prompts for likely failures.
3. Score outputs by paired preference and concrete failure tags.
4. Revise the skill with small, testable rules.
5. Keep identity claims out of the system.

The current human-cadence layer is based on this loop: test, notice the failure, name the failure, add one small rule, test again.

## Benchmark Mapping

The reusable benchmark maps to these public-method ideas:

- Character traits as nudges: 人味 Agent should push toward restraint, judgment, and honesty without forcing a fake persona.
- Balance confidence: avoid both fake certainty and useless hedging.
- Useful refusal: when evidence is missing, refuse the false claim and still give a next step.
- Style as context fit: writing, emotional support, product judgment, and research prompts need different answer shapes.
- Iteration: each watch item becomes a named failure tag and one small rule update.

Useful watch tags include:

- `performative-toughness`: the answer replaces blandness with staged sharpness.
- `portable-emotion`: the answer uses a comforting line that could fit almost any sad prompt.

These tags keep the project aligned with a principle-based method rather than drifting into one-off taste complaints.

## Implemented Modules

The public-method ideas now map to concrete files:

- Character traits as nudges -> `skill/references/trait-layer.md`
- Critique and revision -> `skill/references/critique-revision-loop.md`
- Style as context fit -> `modes/` and `adapters/`
- Reliability under missing evidence -> `skill/references/rigor-layer.md`
- Source fit and research targeting -> `skill/references/source-fit-layer.md`
- Human cadence -> `skill/references/human-cadence-layer.md`
- Reusable benchmark prompts -> `evals/`

This keeps the project portable: it borrows public design principles, not private model identity.

## Source Fit Method Signals

Mature research/search assistants share a pattern:

- break the question into targeted searches
- prefer primary or official sources for factual claims
- check whether the cited source directly supports the claim
- handle recency for unstable facts
- synthesize across sources instead of summarizing the first result
- name missing evidence instead of filling the gap

Useful public references:

- OpenAI Deep Research: multi-step browsing, analysis, synthesis, and cited outputs for complex tasks.
- Perplexity Search/API docs: search quality depends on targeted queries, filtering, and retrieving relevant ranked sources.
- Evidence-review methods: source selection, screening, extraction, and quality assessment matter as much as summary quality.
- AI search audit literature: citations can be present but still misrepresent sources, so claim-to-source fidelity must be checked.

人味 Agent turns these into a practical rule: choose the evidence type before writing the answer.
