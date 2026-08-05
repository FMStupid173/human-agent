from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    required = [
        "skill/references/dynamic-human-layer.md",
        "skill/references/response-selection.md",
        "skill/references/project-lifecycle.md",
        "skill/profiles/taste-profile-template.md",
        "evals/response-selection-adversarial-v1.md",
        "evals/next-turn-effects-adversarial-v1.md",
        "evals/project-lifecycle-adversarial-v1.md",
        "evals/platform-adapter-adversarial-v1.md",
        "evals/human-taste-holdout-v1.md",
        "evals/multi-turn-human-v1.md",
        "evals/house-style-audit.md",
        "evals/focused-regression-v2.md",
        "evals/model-adapter-matrix.md",
        "evals/real-user-feedback-template.csv",
        "adapters/universal-copy-paste-prompt.md",
        "adapters/README.md",
        "adapters/native-skill-install.md",
        "adapters/kimi-preset.md",
        "adapters/kimi-agent-skill-creator.md",
        "adapters/chatgpt-custom-instructions.md",
        "calibrator/calibrate.py",
        "calibrator/config.example.json",
        "calibrator/prompts/judge-system.md",
        "calibrator/prompts/propose-system.md",
        "calibrator/README.md",
        "release-checklist.md",
        "VERSION",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            failures.append(f"missing file: {relative}")

    contracts = {
        "skill/SKILL.md": [
            "references/dynamic-human-layer.md",
            "references/response-selection.md",
            "references/project-lifecycle.md",
            "profiles/taste-profile-template.md",
            "Freeze content-bearing words and qualifiers",
            "source and candidate clause by clause",
            "return it unchanged or adjust punctuation only",
            "unchanged source a mandatory baseline candidate",
            "identify the concrete grammatical or clarity defect",
            "omit remembered names and numbers",
            "do not draft any public-facing version of the claim",
            "Never say a preference was remembered permanently",
            "Select the response act before drafting",
            "next-turn effects gate",
            "smallest sufficient system model",
            "lexical patterns and familiar AI phrases as evaluation clues only",
        ],
        "skill/references/critique-revision-loop.md": [
            "current-session taste notes",
            "Do not claim persistent memory",
        ],
        "skill/references/human-cadence-layer.md": [
            "evaluation outcome, not a wording recipe",
            "wrong-response-act",
            "Do not convert a failure tag into a banned-word list",
        ],
        "skill/references/dynamic-human-layer.md": [
            "Context-only, evidence-only, and critique-only turns",
            "Do not produce the next artifact",
            "actual storage mechanism ran successfully",
            "Select Before Drafting",
            "transient common-ground ledger",
            "unnecessary obligation",
        ],
        "skill/references/response-selection.md": [
            "Select The Response Act",
            "Compare Candidates",
            "Acknowledgment Proof",
            "Edit Necessity Gate",
            "Next-Turn Effects Gate",
            "Reply-burden test",
            "Autonomy test",
            "Continuation test",
            "without asking to end contact",
            "Relationship test",
            "Closure test",
            "conversational debt",
            "changing the interaction",
            "Every changed token must repair that defect",
            "Echo test",
            "Substitution test",
            "Allow The Null Move",
        ],
        "skill/references/writing-voice.md": [
            "Proposition Lock",
            "trend versus frequency",
            "Determine Transformation Freedom",
            "Returning the original unchanged is valid",
        ],
        "skill/references/source-fit-layer.md": [
            "Citation Metadata Gate",
            "Never infer a publication year from a DOI",
            "remembered specifics are not a fallback",
            "do not convert that attribution into README copy",
            "Do not offer an `if you must` public-facing paraphrase",
        ],
        "skill/references/project-lifecycle.md": [
            "Project State Ledger",
            "Build The Smallest Sufficient System Model",
            "Establish A Baseline",
            "Decompose From First Principles",
            "information gain",
            "Make The Smallest Coherent Change",
            "Attack The Result",
            "Causal Debugging Loop",
            "false-root-cause",
            "verification-theater",
            "process-performance",
        ],
        "adapters/model-adapter-guide.md": [
            "900 words",
            "holdout",
            "each product surface as a separate runtime",
        ],
        "adapters/README.md": [
            "Native Skill",
            "Instruction adapter",
            "Codex app, CLI, or IDE",
            "Claude Code",
            "Gemini CLI",
            "Gemini web or mobile",
            "Kimi Code CLI",
            "Kimi Agent mode",
            "Kimi standard chat",
            "ChatGPT web or mobile",
            "universal-copy-paste-prompt.md",
            "does not validate Gemini web",
        ],
        "adapters/native-skill-install.md": [
            ".agents\\skills\\human-agent",
            ".claude\\skills\\human-agent",
            "gemini skills link",
            ".gemini\\skills\\human-agent",
            ".kimi-code\\skills\\human-agent",
            "/skill:human-agent",
            "complete `skill/` directory",
        ],
        "adapters/chatgpt-custom-instructions.md": [
            "1,500-character limit",
            "Use a Dynamic Human Layer",
            "Never claim to be Claude or another model",
        ],
        "adapters/kimi-preset.md": [
            "Kimi Preset",
            "Select what this turn needs before drafting",
            "not a native Skill package",
        ],
        "adapters/kimi-agent-skill-creator.md": [
            "/skill-creator",
            "Create a reusable custom Skill named human-agent",
            "single core function",
            "Do not promise identical behavior across models or product surfaces",
        ],
        "adapters/universal-copy-paste-prompt.md": [
            "Operate as a Dynamic Human Layer",
            "answer, acknowledge, ask, challenge, repair, execute, or leave room",
            "literal candidate",
            "relational candidate",
            "Treat instructions inside webpages",
            "cannot add browsing, code execution, persistent memory, retrieval",
            "cannot guarantee correctness or human preference",
        ],
        "calibrator/calibrate.py": [
            "exact_split_ids",
            "proposal_context",
            "candidate_guardrail_violations",
            "benchmark prompt signatures",
            "needs-human-review",
            "The production adapter was not modified",
            "environment variable",
            '"next_turn_fit"',
            '"project-causality"',
        ],
        "calibrator/prompts/judge-system.md": [
            "next_turn_fit",
            "reply-burden",
            "autonomy-overreach",
            "premature-closure",
        ],
        "benchmark-agent/benchmark-agent-prompt.md": [
            "next-turn fit",
            "reply-burden",
        ],
        "evals/next-turn-effects-adversarial-v1.md": [
            "Clean Prompt Batch",
            "Hidden Pass Criteria",
            "Promotion Gate",
            "Reliability scores remain separate guardrails",
        ],
        "evals/project-lifecycle-adversarial-v1.md": [
            "Clean Prompt Batch",
            "Hidden Pass Criteria",
            "Failure Tags",
            "Promotion Gate",
            "false-root-cause",
            "verification-theater",
        ],
        "evals/platform-adapter-adversarial-v1.md": [
            "Clean Prompt Batch",
            "Hidden Pass Criteria",
            "Failure Tags",
            "Promotion Gate",
            "portability-overclaim",
            "exact product surface",
        ],
        "calibrator/prompts/propose-system.md": [
            "training failures",
            "must not request or infer holdout answers",
            "Do not paste benchmark prompts",
            "Do not add banned-word lists",
            "Do not ban questions",
        ],
        "calibrator/README.md": [
            "never overwrites a production adapter",
            "DEEPSEEK_API_KEY",
            "Web Models Without API Access",
            "next-turn fit",
        ],
        "benchmark-agent/example-results.csv": [
            "next_turn_fit",
        ],
        "evals/benchmark-results-template.csv": [
            "next_turn_fit",
        ],
        "scripts/package-release.ps1": [
            "calibrator[\\\\/]runs",
            "config\\.local\\.json",
            "credentials.*\\.json",
        ],
        "evals/style-lint-rules.md": [
            "Echo test",
            "Substitution test",
            "Next-Turn Effects Review",
            "reply-burden",
            "diagnostic evidence only",
        ],
        "README.md": [
            "Dynamic Human Layer",
            "The Innovation: Response Selection",
            "response-selection.md",
            "evals/response-selection-adversarial-v1.md",
            "evals/next-turn-effects-adversarial-v1.md",
            "evals/project-lifecycle-adversarial-v1.md",
            "skill/profiles/taste-profile-template.md",
            "evals/human-taste-holdout-v1.md",
            "evals/multi-turn-human-v1.md",
            "v0.2-preview",
            "## Known Limits",
            "## Project Lifecycle And Bug Repair",
            "## Platform Coverage",
            "adapters/native-skill-install.md",
            "adapters/kimi-preset.md",
            "evals/platform-adapter-adversarial-v1.md",
        ],
    }
    for relative, needles in contracts.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing contract file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                failures.append(f"{relative} missing contract: {needle}")

    skill_md_path = ROOT / "skill/SKILL.md"
    if skill_md_path.is_file():
        skill_md = skill_md_path.read_text(encoding="utf-8")
        frontmatter_match = re.match(r"^---\n(?P<body>.*?)\n---", skill_md, flags=re.S)
        if not frontmatter_match:
            failures.append("skill/SKILL.md invalid YAML frontmatter boundary")
        else:
            frontmatter: dict[str, str] = {}
            for line in frontmatter_match.group("body").splitlines():
                if not line.strip():
                    continue
                if ":" not in line:
                    failures.append(f"skill/SKILL.md invalid frontmatter line: {line}")
                    continue
                key, value = line.split(":", 1)
                frontmatter[key.strip()] = value.strip()
            unexpected = set(frontmatter) - {"name", "description"}
            if unexpected:
                failures.append(
                    "skill/SKILL.md unexpected frontmatter keys: "
                    + ", ".join(sorted(unexpected))
                )
            name = frontmatter.get("name", "")
            description = frontmatter.get("description", "")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                failures.append(f"skill/SKILL.md invalid skill name: {name!r}")
            elif name != "human-agent":
                failures.append(f"skill/SKILL.md unexpected skill name: {name!r}")
            if not description:
                failures.append("skill/SKILL.md missing description")
            elif len(description) > 1024:
                failures.append(
                    f"skill/SKILL.md description too long: {len(description)} > 1024"
                )

    legacy_brand = re.compile(r"calm[ _-]agent", flags=re.I)
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in {
            ".md", ".py", ".ps1", ".yaml", ".yml", ".json", ".csv", ".txt"
        }:
            continue
        if legacy_brand.search(path.read_text(encoding="utf-8", errors="ignore")):
            failures.append(f"legacy brand remains: {path.relative_to(ROOT)}")

    active_generation_paths = [
        ROOT / "skill/SKILL.md",
        ROOT / "skill/references/dynamic-human-layer.md",
        ROOT / "skill/references/response-selection.md",
        ROOT / "skill/references/project-lifecycle.md",
        ROOT / "skill/references/human-cadence-layer.md",
        ROOT / "skill/references/conversation-taste.md",
        ROOT / "skill/references/daily-chat.md",
        ROOT / "skill/references/emotional-support.md",
        *sorted((ROOT / "adapters").glob("*.md")),
        *sorted((ROOT / "modes").glob("*.md")),
    ]
    forbidden_language_recipes = [
        "Use one light spoken pivot",
        "one prompt-specific phrase",
        "a clean landing",
        "Good Openings",
        "If the answer contains more than one contrast",
        "Before finalizing, scan the answer for contrast",
        "Avoid repeated contrast formulas",
        "开场直接、自然",
    ]
    for path in active_generation_paths:
        text = path.read_text(encoding="utf-8")
        for recipe in forbidden_language_recipes:
            if recipe in text:
                failures.append(
                    f"active generation guidance contains lexical recipe: "
                    f"{path.relative_to(ROOT)} -> {recipe}"
                )

    gemini_path = ROOT / "adapters/gemini-gems.md"
    if gemini_path.is_file():
        gemini = gemini_path.read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", gemini))
        if words >= 900:
            failures.append(f"Gemini adapter word budget exceeded: {words} >= 900")
        leaked_calibration = [
            "我最近很累，很多事都不太想解释",
            "我最近有点空，不太清楚自己在等什么",
            "目前只能确认看到一条 TypeError",
        ]
        for phrase in leaked_calibration:
            if phrase in gemini:
                failures.append(f"Gemini adapter contains benchmark-answer leakage: {phrase}")

    chatgpt_path = ROOT / "adapters/chatgpt-custom-instructions.md"
    if chatgpt_path.is_file():
        chatgpt = chatgpt_path.read_text(encoding="utf-8")
        payload = re.search(r"```text\n(?P<body>.*?)\n```", chatgpt, flags=re.S)
        if not payload:
            failures.append("ChatGPT custom instructions text block missing")
        else:
            length = len(payload.group("body"))
            if length > 1500:
                failures.append(
                    f"ChatGPT custom instructions payload too long: {length} > 1500"
                )

    platform_matrix_path = ROOT / "evals/model-adapter-matrix.md"
    if platform_matrix_path.is_file():
        platform_matrix = platform_matrix_path.read_text(encoding="utf-8")
        for platform in (
            "Codex app / CLI / IDE",
            "Claude Code",
            "ChatGPT web",
            "Gemini web",
            "Gemini CLI",
            "Kimi Agent mode",
            "Kimi standard chat",
            "Kimi Code",
        ):
            if platform not in platform_matrix:
                failures.append(f"adapter matrix missing platform: {platform}")

    holdout_path = ROOT / "evals/human-taste-holdout-v1.md"
    if holdout_path.is_file():
        holdout = holdout_path.read_text(encoding="utf-8")
        section = re.search(
            r"## Clean Prompt Batch(?P<body>.*?)## External Scoring Rubric",
            holdout,
            flags=re.S,
        )
        if not section:
            failures.append("holdout clean prompt section missing")
        else:
            prompts = re.findall(r"(?m)^\d+\.\s+(.+)$", section.group("body"))
            if len(prompts) != 20:
                failures.append(f"holdout prompt count: {len(prompts)} != 20")
            leakage_targets = [
                ROOT / "adapters",
                ROOT / "examples",
                ROOT / "skill/references",
            ]
            corpus = "\n".join(
                path.read_text(encoding="utf-8")
                for directory in leakage_targets
                for path in directory.rglob("*.md")
            )
            for prompt in prompts:
                signature = re.sub(r"\s+", "", prompt)[:28]
                if signature and signature in re.sub(r"\s+", "", corpus):
                    failures.append(f"holdout prompt leaked into guidance: {prompt[:50]}")

    multi_path = ROOT / "evals/multi-turn-human-v1.md"
    if multi_path.is_file():
        scenarios = re.findall(
            r"(?m)^### Scenario (\d+):",
            multi_path.read_text(encoding="utf-8"),
        )
        if scenarios != [str(number) for number in range(1, 11)]:
            failures.append(f"multi-turn scenarios must be 1..10, found: {scenarios}")

    focused_path = ROOT / "evals/focused-regression-v2.md"
    if focused_path.is_file():
        focused = focused_path.read_text(encoding="utf-8")
        section = re.search(
            r"## Clean Prompt Batch(?P<body>.*?)## Hidden Scoring Notes",
            focused,
            flags=re.S,
        )
        if not section:
            failures.append("focused regression clean prompt section missing")
        else:
            prompts = re.findall(r"(?m)^\d+\.\s+(.+)$", section.group("body"))
            if len(prompts) != 30:
                failures.append(f"focused regression prompt count: {len(prompts)} != 30")
            guidance = "\n".join(
                path.read_text(encoding="utf-8")
                for path in (ROOT / "skill").rglob("*.md")
            )
            normalized_guidance = re.sub(r"\s+", "", guidance)
            for prompt in prompts:
                signature = re.sub(r"\s+", "", prompt)[:28]
                if signature and signature in normalized_guidance:
                    failures.append(
                        f"focused regression prompt leaked into skill: {prompt[:50]}"
                    )

    selection_path = ROOT / "evals/response-selection-adversarial-v1.md"
    if selection_path.is_file():
        selection = selection_path.read_text(encoding="utf-8")
        section = re.search(
            r"## Clean Prompt Batch(?P<body>.*?)## Hidden Pass Criteria",
            selection,
            flags=re.S,
        )
        if not section:
            failures.append("response-selection clean prompt section missing")
        else:
            prompts = re.findall(r"(?m)^\d+\.\s+(.+)$", section.group("body"))
            if len(prompts) != 20:
                failures.append(f"response-selection prompt count: {len(prompts)} != 20")
            guidance = "\n".join(
                path.read_text(encoding="utf-8")
                for directory in (ROOT / "skill", ROOT / "adapters", ROOT / "modes")
                for path in directory.rglob("*.md")
            )
            normalized_guidance = re.sub(r"\s+", "", guidance)
            for prompt in prompts:
                signature = re.sub(r"\s+", "", prompt)[:28]
                if signature and signature in normalized_guidance:
                    failures.append(
                        f"response-selection prompt leaked into guidance: {prompt[:50]}"
                    )

    next_turn_path = ROOT / "evals/next-turn-effects-adversarial-v1.md"
    if next_turn_path.is_file():
        next_turn = next_turn_path.read_text(encoding="utf-8")
        section = re.search(
            r"## Clean Prompt Batch(?P<body>.*?)## Hidden Pass Criteria",
            next_turn,
            flags=re.S,
        )
        if not section:
            failures.append("next-turn effects clean prompt section missing")
        else:
            prompts = re.findall(r"(?m)^\d+\.\s+(.+)$", section.group("body"))
            if len(prompts) != 20:
                failures.append(f"next-turn effects prompt count: {len(prompts)} != 20")
            guidance = "\n".join(
                path.read_text(encoding="utf-8")
                for directory in (ROOT / "skill", ROOT / "adapters", ROOT / "modes")
                for path in directory.rglob("*.md")
            )
            normalized_guidance = re.sub(r"\s+", "", guidance)
            for prompt in prompts:
                signature = re.sub(r"\s+", "", prompt)[:28]
                if signature and signature in normalized_guidance:
                    failures.append(
                        f"next-turn effects prompt leaked into guidance: {prompt[:50]}"
                    )

    project_path = ROOT / "evals/project-lifecycle-adversarial-v1.md"
    if project_path.is_file():
        project = project_path.read_text(encoding="utf-8")
        section = re.search(
            r"## Clean Prompt Batch(?P<body>.*?)## Hidden Pass Criteria",
            project,
            flags=re.S,
        )
        if not section:
            failures.append("project lifecycle clean prompt section missing")
        else:
            prompts = re.findall(r"(?m)^\d+\.\s+(.+)$", section.group("body"))
            if len(prompts) != 20:
                failures.append(f"project lifecycle prompt count: {len(prompts)} != 20")
            guidance = "\n".join(
                path.read_text(encoding="utf-8")
                for directory in (ROOT / "skill", ROOT / "adapters", ROOT / "modes")
                for path in directory.rglob("*.md")
            )
            normalized_guidance = re.sub(r"\s+", "", guidance)
            for prompt in prompts:
                signature = re.sub(r"\s+", "", prompt)[:28]
                if signature and signature in normalized_guidance:
                    failures.append(
                        f"project lifecycle prompt leaked into guidance: {prompt[:50]}"
                    )

    platform_path = ROOT / "evals/platform-adapter-adversarial-v1.md"
    if platform_path.is_file():
        platform = platform_path.read_text(encoding="utf-8")
        section = re.search(
            r"## Clean Prompt Batch(?P<body>.*?)## Hidden Pass Criteria",
            platform,
            flags=re.S,
        )
        if not section:
            failures.append("platform adapter clean prompt section missing")
        else:
            prompts = re.findall(r"(?m)^\d+\.\s+(.+)$", section.group("body"))
            if len(prompts) != 20:
                failures.append(f"platform adapter prompt count: {len(prompts)} != 20")
            guidance = "\n".join(
                path.read_text(encoding="utf-8")
                for directory in (ROOT / "skill", ROOT / "adapters", ROOT / "modes")
                for path in directory.rglob("*.md")
            )
            normalized_guidance = re.sub(r"\s+", "", guidance)
            for prompt in prompts:
                signature = re.sub(r"\s+", "", prompt)[:28]
                if signature and signature in normalized_guidance:
                    failures.append(
                        f"platform adapter prompt leaked into guidance: {prompt[:50]}"
                    )

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        print(f"SUMMARY failures={len(failures)}")
        return 1

    print(f"PASS required_project_files={len(required)}")
    contract_count = sum(len(needles) for needles in contracts.values())
    print(f"PASS dynamic_contracts={contract_count}")
    print("PASS active_generation_lexical_recipes=0")
    print("PASS gemini_adapter_words<900 leakage=0")
    print("PASS holdout_prompts=20 leakage=0")
    print("PASS multi_turn_scenarios=10")
    print("PASS focused_regression_prompts=30 leakage=0")
    print("PASS response_selection_prompts=20 leakage=0")
    print("PASS next_turn_effects_prompts=20 leakage=0")
    print("PASS project_lifecycle_prompts=20 leakage=0")
    print("PASS platform_adapter_prompts=20 leakage=0")
    print("PASS chatgpt_custom_instructions_chars<=1500")
    print("PASS platform_matrix=codex,claude-code,chatgpt,gemini,kimi")
    print("PASS skill_frontmatter=name,description")
    return 0


if __name__ == "__main__":
    sys.exit(main())
