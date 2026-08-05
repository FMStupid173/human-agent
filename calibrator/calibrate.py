from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNS_ROOT = ROOT / "calibrator" / "runs"
RESPONSE_FIELDS = [
    "id",
    "split",
    "category",
    "prompt",
    "baseline_output",
    "candidate_output",
    "baseline_model",
    "baseline_fingerprint",
    "candidate_model",
    "candidate_fingerprint",
]
SCORE_FIELDS = [
    "useful",
    "response_act_fit",
    "interaction_contribution",
    "non_substitutability",
    "boundary_recognition",
    "proportion",
    "next_turn_fit",
    "semantic_fidelity",
    "evidence_hygiene",
    "source_fit",
    "verification",
]
SELECTION_FIELDS = [
    "useful",
    "response_act_fit",
    "interaction_contribution",
    "non_substitutability",
    "boundary_recognition",
    "proportion",
    "next_turn_fit",
]
SCORE_CSV_FIELDS = [
    "id",
    "split",
    "pass",
    *SCORE_FIELDS,
    "failure_tags",
    "hard_failure",
    "note",
]
GUARDRAIL_FIELDS = [
    "semantic_fidelity",
    "evidence_hygiene",
    "source_fit",
    "verification",
]
ALLOWED_PHASES = {"baseline", "candidate"}
GUARDRAIL_MARKERS = {
    "identity": ("claude", "identity", "身份", "假装", "声称"),
    "uncertainty": ("uncertain", "uncertainty", "evidence", "不确定", "证据"),
    "source-fit": ("source", "citation", "来源", "资料", "引用"),
    "semantic-fidelity": ("semantic", "meaning", "proposition", "语义", "原意"),
    "privacy": ("privacy", "private", "credential", "隐私", "私密", "凭据"),
    "project-causality": (
        "root cause",
        "reproduce",
        "baseline",
        "invariant",
        "根因",
        "复现",
        "不变量",
    ),
}
FORBIDDEN_CANDIDATE_PATTERNS = {
    "model identity claim": re.compile(
        r"(?i)\b(?:i am|i'm|pretend to be|act as)\s+(?:claude|chatgpt|gemini|deepseek)\b"
        r"|(?:我是|假装(?:自己)?是|扮演)(?:\s*)(?:Claude|ChatGPT|Gemini|DeepSeek)",
    ),
    "instruction override": re.compile(
        r"(?i)ignore\s+(?:all\s+)?(?:previous|prior|system)\s+instructions?"
        r"|忽略(?:此前|之前|系统|所有)?(?:的)?指令",
    ),
    "local user path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "credential material": re.compile(
        r"(?i)(?:sk-(?:ant-|proj-)?[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{30,}"
        r"|ghp_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)",
    ),
}


class CalibrationError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CalibrationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CalibrationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CalibrationError(f"expected a JSON object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def project_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def manifest_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return path.name


def config_path(args: argparse.Namespace) -> Path:
    return Path(args.config).resolve()


def run_directory(config: dict[str, Any], override: str | None = None) -> Path:
    if override:
        return Path(override).resolve()
    name = str(config.get("run_name", "")).strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", name):
        raise CalibrationError("run_name must use letters, numbers, dot, underscore, or dash")
    return RUNS_ROOT / name


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_code_fence(text: str) -> str:
    match = re.search(r"```(?:text|markdown)?\s*\n(?P<body>.*?)\n```", text, flags=re.S | re.I)
    return match.group("body").strip() if match else text.strip()


def parse_prompts(path: Path, section_name: str = "") -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    active = not section_name
    found_section = not section_name
    category = "uncategorized"
    prompts: list[dict[str, str]] = []

    for line in lines:
        if line.startswith("## "):
            heading = line[3:].strip()
            if section_name and heading == section_name:
                active = True
                found_section = True
                continue
            if active and section_name:
                break
        if not active:
            continue
        if line.startswith("### "):
            category = line[4:].strip()
            continue
        match = re.match(r"^(\d+)\.\s+(.+)$", line)
        if match:
            prompts.append(
                {
                    "id": match.group(1),
                    "category": category,
                    "prompt": match.group(2).strip(),
                }
            )

    if not found_section:
        raise CalibrationError(f"section not found in {path}: {section_name}")
    if not prompts:
        raise CalibrationError(f"no numbered prompts found in {path}")
    ids = [item["id"] for item in prompts]
    if len(ids) != len(set(ids)):
        raise CalibrationError(f"duplicate prompt ids in {path}")
    return prompts


def exact_split_ids(
    prompts: list[dict[str, str]], seed: str, holdout_ratio: float
) -> set[str]:
    holdout_count = max(1, min(len(prompts) - 1, round(len(prompts) * holdout_ratio)))
    ranked = sorted(
        prompts,
        key=lambda item: hashlib.sha256(
            f"{seed}:{item['id']}".encode("utf-8")
        ).digest(),
    )
    return {item["id"] for item in ranked[:holdout_count]}


def ensure_both_splits(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["split"] for row in rows)
    if counts["train"] == 0 or counts["holdout"] == 0:
        raise CalibrationError("dataset split must contain at least one train and one holdout item")


def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return [
            {key: restore_csv_cell(value) for key, value in row.items()}
            for row in rows
        ]
    except FileNotFoundError as exc:
        raise CalibrationError(f"missing file: {path}") from exc


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(
            {
                key: protect_csv_cell(value) if isinstance(value, str) else value
                for key, value in row.items()
            }
            for row in rows
        )


def protect_csv_cell(value: str) -> str:
    if value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def restore_csv_cell(value: str | None) -> str:
    value = value or ""
    if value.startswith("'") and value[1:].lstrip().startswith(("=", "+", "-", "@")):
        return value[1:]
    return value


def require_phase(phase: str) -> None:
    if phase not in ALLOWED_PHASES:
        raise CalibrationError(f"phase must be one of: {', '.join(sorted(ALLOWED_PHASES))}")


def get_provider(config: dict[str, Any], key: str) -> dict[str, Any]:
    provider = config.get(key)
    if not isinstance(provider, dict):
        raise CalibrationError(f"config missing object: {key}")
    if provider.get("provider") != "deepseek":
        raise CalibrationError(f"only provider=deepseek is implemented for {key}")
    return provider


def api_key(provider: dict[str, Any]) -> str:
    env_name = str(provider.get("api_key_env", "DEEPSEEK_API_KEY"))
    value = os.environ.get(env_name, "")
    if not value:
        raise CalibrationError(f"environment variable {env_name} is not set")
    return value


def strip_json_fence(content: str) -> str:
    content = content.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", content, flags=re.S | re.I)
    return match.group(1).strip() if match else content


def deepseek_chat(
    provider: dict[str, Any],
    messages: list[dict[str, str]],
    *,
    json_mode: bool = False,
) -> tuple[str, dict[str, Any]]:
    base_url = str(provider.get("base_url", "https://api.deepseek.com")).rstrip("/")
    url = f"{base_url}/chat/completions"
    body: dict[str, Any] = {
        "model": provider["model"],
        "messages": messages,
        "stream": False,
        "temperature": provider.get("temperature", 0.0),
        "max_tokens": provider.get("max_tokens", 2048),
        "thinking": {"type": provider.get("thinking", "disabled")},
        "user_id": "human-agent-calibrator",
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}

    secret = api_key(provider)
    request = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/json",
            "User-Agent": "human-agent-calibrator/0.1",
        },
    )
    timeout = int(provider.get("timeout_seconds", 180))
    retries = int(provider.get("max_retries", 3))

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            message = payload["choices"][0]["message"]
            content = str(message.get("content") or "").strip()
            if not content:
                if attempt < retries:
                    time.sleep(min(2**attempt, 8))
                    continue
                raise CalibrationError("DeepSeek returned empty content")
            metadata = {
                "model": payload.get("model", provider.get("model", "")),
                "system_fingerprint": payload.get("system_fingerprint", ""),
                "usage": payload.get("usage", {}),
            }
            return content, metadata
        except urllib.error.HTTPError as exc:
            retryable = exc.code in {429, 500, 503}
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            detail = detail.replace(secret, "[REDACTED]")
            if retryable and attempt < retries:
                time.sleep(min(2**attempt, 8))
                continue
            raise CalibrationError(f"DeepSeek HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < retries:
                time.sleep(min(2**attempt, 8))
                continue
            raise CalibrationError(f"DeepSeek connection failed: {exc}") from exc
    raise CalibrationError("DeepSeek request failed after retries")


def adapter_text(config: dict[str, Any], phase: str, run_dir: Path) -> tuple[str, Path]:
    if phase == "candidate":
        path = run_dir / "candidate-adapter.md"
    else:
        path = project_path(str(config.get("adapter", "")))
    if not path.is_file():
        raise CalibrationError(f"adapter file not found: {path}")
    return extract_code_fence(path.read_text(encoding="utf-8")), path


def prepare(config: dict[str, Any], config_file: Path, run_dir: Path) -> None:
    if run_dir.exists() and any(run_dir.iterdir()):
        raise CalibrationError(f"run directory is not empty: {run_dir}")
    dataset = config.get("dataset", {})
    if not isinstance(dataset, dict):
        raise CalibrationError("config dataset must be an object")
    dataset_path = project_path(str(dataset.get("path", "")))
    adapter_path = project_path(str(config.get("adapter", "")))
    holdout_ratio = float(dataset.get("holdout_ratio", 0.3))
    if not 0.1 <= holdout_ratio <= 0.5:
        raise CalibrationError("holdout_ratio must be between 0.1 and 0.5")
    seed = str(dataset.get("seed", "human-agent-calibration-v1"))
    prompts = parse_prompts(dataset_path, str(dataset.get("section", "")))
    holdout_ids = exact_split_ids(prompts, seed, holdout_ratio)
    rows: list[dict[str, str]] = []
    for prompt in prompts:
        row = {field: "" for field in RESPONSE_FIELDS}
        row.update(prompt)
        row["split"] = "holdout" if prompt["id"] in holdout_ids else "train"
        rows.append(row)
    ensure_both_splits(rows)

    run_dir.mkdir(parents=True, exist_ok=True)
    write_csv(run_dir / "responses.csv", RESPONSE_FIELDS, rows)
    manifest = {
        "schema_version": 1,
        "created_at": utc_now(),
        "run_name": config["run_name"],
        "config_file": config_file.name,
        "dataset": {
            "path": manifest_path(dataset_path),
            "sha256": sha256_file(dataset_path),
            "prompt_count": len(rows),
            "train_count": sum(row["split"] == "train" for row in rows),
            "holdout_count": sum(row["split"] == "holdout" for row in rows),
            "seed": seed,
        },
        "adapter": {
            "path": manifest_path(adapter_path),
            "sha256": sha256_file(adapter_path),
        },
        "target": {
            "provider": config.get("target", {}).get("provider"),
            "model": config.get("target", {}).get("model"),
            "base_url": config.get("target", {}).get("base_url"),
        },
        "judge": {
            "provider": config.get("judge", {}).get("provider"),
            "model": config.get("judge", {}).get("model"),
            "base_url": config.get("judge", {}).get("base_url"),
        },
        "human_approval": "pending",
    }
    write_json(run_dir / "manifest.json", manifest)
    print(f"Prepared {len(rows)} prompts at {run_dir}")
    print(f"train={manifest['dataset']['train_count']} holdout={manifest['dataset']['holdout_count']}")


def run_outputs(
    config: dict[str, Any],
    run_dir: Path,
    phase: str,
    limit: int,
) -> None:
    require_phase(phase)
    provider = get_provider(config, "target")
    system_prompt, source_path = adapter_text(config, phase, run_dir)
    rows = read_csv(run_dir / "responses.csv")
    output_field = f"{phase}_output"
    model_field = f"{phase}_model"
    fingerprint_field = f"{phase}_fingerprint"
    completed = 0

    for row in rows:
        if row.get(output_field, "").strip():
            continue
        if limit and completed >= limit:
            break
        content, metadata = deepseek_chat(
            provider,
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": row["prompt"]},
            ],
        )
        row[output_field] = content
        row[model_field] = str(metadata.get("model", ""))
        row[fingerprint_field] = str(metadata.get("system_fingerprint", ""))
        completed += 1
        write_csv(run_dir / "responses.csv", RESPONSE_FIELDS, rows)
        print(f"{phase} {row['id']} complete")

    print(f"Generated {completed} {phase} output(s) using {source_path}")


def load_prompt_file(relative: str) -> str:
    return (ROOT / "calibrator" / "prompts" / relative).read_text(encoding="utf-8")


def validate_score(value: dict[str, Any]) -> dict[str, Any]:
    status = str(value.get("pass", "")).lower()
    if status not in {"yes", "watch", "no"}:
        raise CalibrationError(f"judge returned invalid pass value: {status!r}")
    scores = value.get("scores")
    if not isinstance(scores, dict):
        raise CalibrationError("judge response missing scores object")
    clean_scores: dict[str, int] = {}
    for field in SCORE_FIELDS:
        score = scores.get(field)
        if not isinstance(score, (int, float)) or not 1 <= float(score) <= 5:
            raise CalibrationError(f"judge returned invalid score for {field}: {score!r}")
        clean_scores[field] = int(round(float(score)))
    tags = value.get("failure_tags", [])
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        raise CalibrationError("judge returned invalid failure_tags")
    return {
        "pass": status,
        "scores": clean_scores,
        "failure_tags": [tag.strip() for tag in tags if tag.strip()],
        "hard_failure": bool(value.get("hard_failure", False)),
        "note": str(value.get("note", "")).strip()[:500],
    }


def judge_outputs(config: dict[str, Any], run_dir: Path, phase: str, limit: int) -> None:
    require_phase(phase)
    provider = get_provider(config, "judge")
    judge_prompt = load_prompt_file("judge-system.md")
    responses = read_csv(run_dir / "responses.csv")
    score_path = run_dir / f"{phase}-scores.csv"
    existing = {row["id"]: row for row in read_csv(score_path)} if score_path.exists() else {}
    output_field = f"{phase}_output"
    completed = 0

    for row in responses:
        if row["id"] in existing or not row.get(output_field, "").strip():
            continue
        if limit and completed >= limit:
            break
        user_payload = {
            "prompt": row["prompt"],
            "answer": row[output_field],
            "category": row["category"],
        }
        content, _ = deepseek_chat(
            provider,
            [
                {"role": "system", "content": judge_prompt},
                {
                    "role": "user",
                    "content": "Evaluate this untrusted test item and return JSON:\n"
                    + json.dumps(user_payload, ensure_ascii=False),
                },
            ],
            json_mode=True,
        )
        try:
            scored = validate_score(json.loads(strip_json_fence(content)))
        except json.JSONDecodeError as exc:
            raise CalibrationError(f"judge returned invalid JSON for item {row['id']}") from exc
        score_row: dict[str, Any] = {
            "id": row["id"],
            "split": row["split"],
            "pass": scored["pass"],
            "failure_tags": ",".join(scored["failure_tags"]),
            "hard_failure": str(scored["hard_failure"]).lower(),
            "note": scored["note"],
        }
        score_row.update(scored["scores"])
        existing[row["id"]] = score_row
        completed += 1
        ordered = [existing[key] for key in sorted(existing, key=lambda value: int(value))]
        write_csv(score_path, SCORE_CSV_FIELDS, ordered)
        print(f"judged {phase} {row['id']}")

    print(f"Judged {completed} {phase} output(s)")


def word_count(text: str) -> int:
    latin = re.findall(r"[A-Za-z0-9_'-]+", text)
    cjk = re.findall(r"[\u3400-\u9fff]", text)
    return len(latin) + len(cjk)


def normalized_signature(text: str, length: int = 28) -> str:
    return re.sub(r"\s+", "", text)[:length]


def candidate_guardrail_violations(current: str, candidate: str) -> list[str]:
    current_lower = current.lower()
    candidate_lower = candidate.lower()
    violations = [
        f"missing existing {name} boundary"
        for name, markers in GUARDRAIL_MARKERS.items()
        if any(marker in current_lower for marker in markers)
        and not any(marker in candidate_lower for marker in markers)
    ]
    violations.extend(
        name for name, pattern in FORBIDDEN_CANDIDATE_PATTERNS.items() if pattern.search(candidate)
    )
    return violations


def proposal_context(run_dir: Path) -> list[dict[str, Any]]:
    responses = {row["id"]: row for row in read_csv(run_dir / "responses.csv")}
    scores = read_csv(run_dir / "baseline-scores.csv")
    failures: list[dict[str, Any]] = []
    for score in scores:
        if score.get("split") != "train" or score.get("pass") == "yes":
            continue
        response = responses[score["id"]]
        failures.append(
            {
                "id": score["id"],
                "category": response["category"],
                "prompt": response["prompt"],
                "answer": response["baseline_output"],
                "pass": score["pass"],
                "failure_tags": score["failure_tags"],
                "note": score["note"],
                "scores": {field: score[field] for field in SCORE_FIELDS},
            }
        )
    return failures


def propose(config: dict[str, Any], run_dir: Path) -> None:
    provider = get_provider(config, "judge")
    failures = proposal_context(run_dir)
    if not failures:
        raise CalibrationError("no watch/fail training items available for proposal")
    current_text, current_path = adapter_text(config, "baseline", run_dir)
    max_words = int(config.get("thresholds", {}).get("max_adapter_words", 900))
    payload = {
        "current_adapter": current_text,
        "training_failures": failures,
        "word_budget": max_words,
    }
    content, _ = deepseek_chat(
        provider,
        [
            {"role": "system", "content": load_prompt_file("propose-system.md")},
            {
                "role": "user",
                "content": "Propose a candidate adapter and return JSON:\n"
                + json.dumps(payload, ensure_ascii=False),
            },
        ],
        json_mode=True,
    )
    try:
        value = json.loads(strip_json_fence(content))
    except json.JSONDecodeError as exc:
        raise CalibrationError("proposer returned invalid JSON") from exc
    candidate = str(value.get("candidate_adapter", "")).strip()
    if not candidate:
        raise CalibrationError("proposer returned an empty candidate_adapter")
    words = word_count(candidate)
    if words > max_words:
        raise CalibrationError(f"candidate word budget exceeded: {words} > {max_words}")

    benchmark_rows = read_csv(run_dir / "responses.csv")
    normalized_candidate = re.sub(r"\s+", "", candidate)
    leaked = [
        row["id"]
        for row in benchmark_rows
        if normalized_signature(row["prompt"]) in normalized_candidate
    ]
    if leaked:
        raise CalibrationError(f"candidate contains benchmark prompt signatures: {', '.join(leaked)}")
    guardrail_violations = candidate_guardrail_violations(current_text, candidate)
    if guardrail_violations:
        raise CalibrationError(
            "candidate failed deterministic guardrails: " + "; ".join(guardrail_violations)
        )

    candidate_path = run_dir / "candidate-adapter.md"
    candidate_path.write_text(candidate + "\n", encoding="utf-8")
    diff = "".join(
        difflib.unified_diff(
            current_text.splitlines(keepends=True),
            candidate.splitlines(keepends=True),
            fromfile=str(current_path),
            tofile=str(candidate_path),
        )
    )
    (run_dir / "candidate-adapter.diff").write_text(diff, encoding="utf-8")
    write_json(
        run_dir / "proposal.json",
        {
            "created_at": utc_now(),
            "training_failure_count": len(failures),
            "candidate_word_count": words,
            "changes": value.get("changes", []),
            "risks": value.get("risks", []),
            "training_failure_tags_addressed": value.get("training_failure_tags_addressed", []),
            "promotion_status": "unvalidated",
        },
    )
    print(f"Candidate written to {candidate_path}")
    print("Holdout content was not included in the proposal payload")


def score_number(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise CalibrationError(f"invalid numeric score: {value!r}") from exc


def score_metrics(rows: list[dict[str, str]], split: str) -> dict[str, Any]:
    selected = [row for row in rows if row.get("split") == split]
    if not selected:
        raise CalibrationError(f"no scored rows for split: {split}")
    pass_counts = Counter(row.get("pass", "") for row in selected)
    averages = {
        field: round(sum(score_number(row[field]) for row in selected) / len(selected), 3)
        for field in SCORE_FIELDS
    }
    composite = round(
        sum(averages[field] for field in SELECTION_FIELDS) / len(SELECTION_FIELDS),
        3,
    )
    hard_failures = sum(row.get("hard_failure", "").lower() == "true" for row in selected)
    return {
        "count": len(selected),
        "pass_counts": dict(pass_counts),
        "pass_rate": round(pass_counts["yes"] / len(selected), 3),
        "accepted_rate": round(
            (pass_counts["yes"] + pass_counts["watch"]) / len(selected), 3
        ),
        "hard_failures": hard_failures,
        "averages": averages,
        "composite": composite,
    }


def compare(config: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    baseline = read_csv(run_dir / "baseline-scores.csv")
    candidate = read_csv(run_dir / "candidate-scores.csv")
    baseline_ids = {row["id"] for row in baseline}
    candidate_ids = {row["id"] for row in candidate}
    if baseline_ids != candidate_ids:
        raise CalibrationError("baseline and candidate score files must contain the same ids")
    baseline_splits = {row["id"]: row.get("split") for row in baseline}
    candidate_splits = {row["id"]: row.get("split") for row in candidate}
    if baseline_splits != candidate_splits:
        raise CalibrationError("baseline and candidate score files must use the same splits")

    base_holdout = score_metrics(baseline, "holdout")
    candidate_holdout = score_metrics(candidate, "holdout")
    base_train = score_metrics(baseline, "train")
    candidate_train = score_metrics(candidate, "train")
    thresholds = config.get("thresholds", {})
    max_hard = int(thresholds.get("max_hard_failures", 0))
    min_pass = float(thresholds.get("min_holdout_pass_rate", 0.7))
    min_accepted = float(thresholds.get("min_holdout_accepted_rate", 0.85))
    min_delta = float(thresholds.get("min_holdout_composite_delta", 0.0))
    max_regression = float(thresholds.get("max_guardrail_regression", 0.0))
    reasons: list[str] = []

    if candidate_holdout["hard_failures"] > max_hard:
        reasons.append(
            f"holdout hard failures {candidate_holdout['hard_failures']} > {max_hard}"
        )
    if candidate_holdout["pass_rate"] < min_pass:
        reasons.append(
            f"holdout pass rate {candidate_holdout['pass_rate']} < {min_pass}"
        )
    if candidate_holdout["accepted_rate"] < min_accepted:
        reasons.append(
            f"holdout accepted rate {candidate_holdout['accepted_rate']} < {min_accepted}"
        )
    composite_delta = round(candidate_holdout["composite"] - base_holdout["composite"], 3)
    if composite_delta < min_delta:
        reasons.append(f"holdout composite delta {composite_delta} < {min_delta}")
    guardrail_deltas: dict[str, float] = {}
    for field in GUARDRAIL_FIELDS:
        delta = round(
            candidate_holdout["averages"][field] - base_holdout["averages"][field],
            3,
        )
        guardrail_deltas[field] = delta
        if delta < -max_regression:
            reasons.append(f"{field} regression {delta} < {-max_regression}")

    automated_gate = "blocked" if reasons else "passed"
    result = {
        "created_at": utc_now(),
        "automated_gate": automated_gate,
        "promotion_status": "blocked" if reasons else "needs-human-review",
        "reasons": reasons,
        "holdout_composite_delta": composite_delta,
        "holdout_guardrail_deltas": guardrail_deltas,
        "baseline": {"train": base_train, "holdout": base_holdout},
        "candidate": {"train": candidate_train, "holdout": candidate_holdout},
        "human_review_required": True,
    }
    write_json(run_dir / "comparison.json", result)
    lines = [
        "# Calibration Comparison",
        "",
        f"Automated gate: **{automated_gate}**",
        f"Promotion status: **{result['promotion_status']}**",
        f"Holdout composite delta: `{composite_delta}`",
        "",
        "## Guardrail Deltas",
        "",
    ]
    lines.extend(f"- {field}: `{delta}`" for field, delta in guardrail_deltas.items())
    lines.extend(["", "## Blocking Reasons", ""])
    if reasons:
        lines.extend(f"- {reason}" for reason in reasons)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Human Review",
            "",
            "Run a blind, order-swapped A/B preference review before changing the production adapter.",
        ]
    )
    (run_dir / "comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def status(run_dir: Path) -> None:
    rows = read_csv(run_dir / "responses.csv")
    summary: dict[str, Any] = {
        "prompts": len(rows),
        "train": sum(row.get("split") == "train" for row in rows),
        "holdout": sum(row.get("split") == "holdout" for row in rows),
        "baseline_outputs": sum(bool(row.get("baseline_output", "").strip()) for row in rows),
        "candidate_outputs": sum(bool(row.get("candidate_output", "").strip()) for row in rows),
        "baseline_scores": len(read_csv(run_dir / "baseline-scores.csv"))
        if (run_dir / "baseline-scores.csv").exists()
        else 0,
        "candidate_scores": len(read_csv(run_dir / "candidate-scores.csv"))
        if (run_dir / "candidate-scores.csv").exists()
        else 0,
        "candidate_adapter": (run_dir / "candidate-adapter.md").exists(),
        "comparison": (run_dir / "comparison.json").exists(),
        "human_approval": (run_dir / "human-approval.json").exists(),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def approve(
    run_dir: Path,
    decision: str,
    reviewer: str,
    notes: str,
) -> None:
    comparison = read_json(run_dir / "comparison.json")
    if decision == "accept" and comparison.get("automated_gate") != "passed":
        raise CalibrationError("cannot accept a candidate blocked by the automated gate")
    candidate_path = run_dir / "candidate-adapter.md"
    if not candidate_path.is_file():
        raise CalibrationError("candidate-adapter.md is required before human approval")
    record = {
        "created_at": utc_now(),
        "decision": decision,
        "reviewer": reviewer.strip() or "anonymous-human-reviewer",
        "notes": notes.strip(),
        "comparison_sha256": sha256_file(run_dir / "comparison.json"),
        "candidate_adapter_sha256": sha256_file(candidate_path),
        "automatic_promotion": False,
    }
    write_json(run_dir / "human-approval.json", record)
    manifest_path = run_dir / "manifest.json"
    manifest = read_json(manifest_path)
    manifest["human_approval"] = decision
    write_json(manifest_path, manifest)
    print(f"Recorded human decision: {decision}")
    print("The production adapter was not modified")


def doctor(config: dict[str, Any]) -> int:
    checks: list[tuple[str, bool, str]] = []
    dataset = project_path(str(config.get("dataset", {}).get("path", "")))
    adapter = project_path(str(config.get("adapter", "")))
    checks.append(("dataset", dataset.is_file(), str(dataset)))
    checks.append(("adapter", adapter.is_file(), str(adapter)))
    for key in ("target", "judge"):
        provider = config.get(key, {})
        env_name = str(provider.get("api_key_env", "DEEPSEEK_API_KEY"))
        checks.append((f"{key} provider", provider.get("provider") == "deepseek", str(provider.get("provider"))))
        checks.append((f"{key} model", bool(provider.get("model")), str(provider.get("model"))))
        checks.append((f"{key} API key", bool(os.environ.get(env_name)), f"environment:{env_name}"))
    failed = False
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
        failed = failed or not ok
    print("NOTE API keys are checked for presence only and are never printed")
    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="人味 Agent cross-model Calibration Copilot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def common(name: str) -> argparse.ArgumentParser:
        sub = subparsers.add_parser(name)
        sub.add_argument("--config", required=True)
        sub.add_argument("--run-dir", default="")
        return sub

    common("doctor")
    common("prepare")
    run_parser = common("run")
    run_parser.add_argument("--phase", choices=sorted(ALLOWED_PHASES), required=True)
    run_parser.add_argument("--limit", type=int, default=0)
    judge_parser = common("judge")
    judge_parser.add_argument("--phase", choices=sorted(ALLOWED_PHASES), required=True)
    judge_parser.add_argument("--limit", type=int, default=0)
    common("propose")
    common("compare")
    common("status")
    approve_parser = common("approve")
    approve_parser.add_argument("--decision", choices=["accept", "reject"], required=True)
    approve_parser.add_argument("--reviewer", default="")
    approve_parser.add_argument("--notes", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        config_file = config_path(args)
        config = read_json(config_file)
        run_dir = run_directory(config, args.run_dir or None)
        if args.command == "doctor":
            return doctor(config)
        if args.command == "prepare":
            prepare(config, config_file, run_dir)
        elif args.command == "run":
            run_outputs(config, run_dir, args.phase, args.limit)
        elif args.command == "judge":
            judge_outputs(config, run_dir, args.phase, args.limit)
        elif args.command == "propose":
            propose(config, run_dir)
        elif args.command == "compare":
            compare(config, run_dir)
        elif args.command == "status":
            status(run_dir)
        elif args.command == "approve":
            approve(run_dir, args.decision, args.reviewer, args.notes)
        return 0
    except CalibrationError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
