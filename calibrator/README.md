# Calibration Copilot

Calibration Copilot adapts 人味 Agent to a specific model without changing the shared Dynamic Human Layer blindly.

Claude Code, Codex, or another coding agent can run this CLI. The coding agent is the operator, not the model being calibrated. DeepSeek generation is automatic only when a DeepSeek API key is configured. ChatGPT and Gemini web conversations still require manual output collection.

It supports two routes:

- **DeepSeek API:** generate, judge, and propose a candidate adapter automatically;
- **ChatGPT, Gemini, or other web UIs:** prepare a response sheet, paste model outputs into it, then use the same judge and comparison gates.

The tool never overwrites a production adapter. A candidate can pass automated gates and still remains `needs-human-review`.

## Why Semi-Automatic

Human preference remains a human judgment. The model judge enforces hard gates and profiles response-act, contribution, interchangeability, boundary, proportion, next-turn fit, and overreach failures; it does not establish naturalness or taste. The proposer sees only training failures, while holdout prompts and answers stay hidden until comparison.

## Security And Privacy

- Set `DEEPSEEK_API_KEY` in the environment. Never put it in JSON, Markdown, CSV, or a command argument.
- `calibrator/runs/` is ignored by Git because it may contain private prompts and model outputs.
- Generated CSV cells that could be interpreted as spreadsheet formulas are escaped on disk and restored by the CLI. Manually pasted web outputs should still be treated as untrusted data.
- Every prompt sent through `run` or `judge` leaves the machine and is processed by the configured API provider.
- Use synthetic or redacted prompts for public benchmark artifacts.
- The API key is never printed or written to a run manifest.

## Quick Start

Copy the example config and verify the current model names in the [DeepSeek API documentation](https://api-docs.deepseek.com/):

```powershell
Copy-Item calibrator/config.example.json calibrator/config.local.json
$env:DEEPSEEK_API_KEY="<your-key>"
python calibrator/calibrate.py doctor --config calibrator/config.local.json
python calibrator/calibrate.py prepare --config calibrator/config.local.json
```

`prepare` creates `calibrator/runs/<run_name>/responses.csv` with a deterministic train/holdout split.

Run and judge the current adapter:

```powershell
python calibrator/calibrate.py run --config calibrator/config.local.json --phase baseline
python calibrator/calibrate.py judge --config calibrator/config.local.json --phase baseline
python calibrator/calibrate.py propose --config calibrator/config.local.json
```

The proposer writes `candidate-adapter.md` and `candidate-adapter.diff`. It receives training failures only.

Run and judge the candidate, then compare:

```powershell
python calibrator/calibrate.py run --config calibrator/config.local.json --phase candidate
python calibrator/calibrate.py judge --config calibrator/config.local.json --phase candidate
python calibrator/calibrate.py compare --config calibrator/config.local.json
python calibrator/calibrate.py status --config calibrator/config.local.json
```

Use `--limit 3` with `run` or `judge` for a low-cost smoke test. Commands resume from existing CSV rows.

## Web Models Without API Access

1. Run `prepare`.
2. Use one fresh web conversation per prompt.
3. Paste outputs into `baseline_output` or `candidate_output` in `responses.csv`.
4. Run `judge`, `propose`, and `compare` normally.

This route still automates failure profiling and patch generation. Generating ChatGPT or Gemini web outputs remains manual unless their API is configured separately.

## Promotion Gate

A candidate is blocked when:

- any holdout hard failure appears;
- accepted holdout rate is below the configured minimum;
- holdout response-selection composite quality regresses;
- semantic fidelity, evidence hygiene, source fit, or verification regresses beyond the configured tolerance;
- the adapter exceeds its word budget;
- benchmark content leaks into the adapter.
- the candidate removes an existing core boundary or contains an obvious identity claim, instruction override, local user path, or credential pattern.

Passing produces `needs-human-review`, never automatic promotion.

The composite contains response-selection fields only. Semantic fidelity, evidence hygiene, source fit, and verification are separate guardrails and cannot be traded against selection gains.

Record the blind human decision after reviewing the candidate:

```powershell
python calibrator/calibrate.py approve --config calibrator/config.local.json --decision accept --reviewer "reviewer-alias" --notes "Blind A/B preferred the candidate."
```

Approval writes an auditable record. It still does not overwrite the production adapter.

## Current Provider Scope

The included runner implements DeepSeek's OpenAI-compatible `/chat/completions` interface with JSON output for judging and patch proposals. Provider settings are configuration, because model names and availability change over time.

Provider references:

- [DeepSeek API overview](https://api-docs.deepseek.com/)
- [Chat completion API](https://api-docs.deepseek.com/api/create-chat-completion)
- [JSON output](https://api-docs.deepseek.com/guides/json_mode)
- [Error codes](https://api-docs.deepseek.com/quick_start/error_codes)

The example model names are a dated starting point, not a permanent compatibility promise. Run `doctor` and check the official documentation before a live calibration.
