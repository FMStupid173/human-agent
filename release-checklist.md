# v0.1 Preview Release Checklist

## Required Before Tagging

- [x] Core skill contains no Claude identity claim.
- [x] Raw private conversations and exports are excluded.
- [x] Dynamic structural validator passes after the response-selection rewrite.
- [x] Installed Codex skill matches the project skill byte for byte.
- [ ] Response-selection adversarial v1 passes its hard gates.
- [ ] Next-turn effects adversarial v1 is run privately before tagging.
- [ ] Project lifecycle adversarial v1 passes its hard gates on Codex.
- [ ] Blind A/B review is complete for any human-preference claim.
- [ ] Multi-turn treatment/control comparison is run privately before tagging.
- [ ] Focused regression clears its release gate.
- [x] Filled model outputs, personal ratings, and local run logs are excluded from the public repository.
- [x] README makes no claim from removed historical adapter scores.
- [x] Installation paths and adapter starting points are documented.
- [x] Codex, Claude Code, Gemini CLI, and Kimi Code native paths are separated from ChatGPT and Gemini web routes, Kimi Agent custom Skills, and Kimi standard-chat Presets.
- [x] ChatGPT Custom Instructions payload fits the 1,500-character Free/Go limit.
- [ ] Platform adapter adversarial v1 passes on each product surface claimed as verified.
- [x] Run a final archive privacy scan immediately before upload.
- [x] Inspect the GitHub release archive after extraction.
- [x] Local usernames and absolute user paths are absent from public files.
- [x] Common live-token, private-key, credential-assignment, account-ID, email, and phone patterns are absent.
- [x] `.gitignore` excludes environment files, credentials, archives, raw exports, databases, and JSONL corpora.
- [x] Public failure reports require a minimal redacted example.
- [x] Privacy and private security-reporting guidance are included.
- [x] Release packaging scans both the source tree and generated archive.
- [x] Calibration Copilot unit tests pass: 23 tests, including the platform-adapter suite parser.
- [x] Dynamic validator includes the new selection and calibration contracts and passes.
- [x] `calibrator/runs/` and `calibrator/config.local.json` are absent from the release archive.
- [x] Live DeepSeek smoke status is explicit: not run because no API key was available.
- [x] No adapter is described as calibrated without holdout results and a human approval record.

## Release Positioning

Use:

> A response-selection and reliability layer for context-sensitive AI behavior, semantic fidelity, source fit, and evidence-aware output.

Avoid:

- claiming to reproduce Claude internals;
- promising that every AI will sound identical;
- claiming perfect semantic preservation;
- presenting private or historical adapter scores as current cross-model proof;
- calling a model-judge result automatic proof of human preference;
- implying ChatGPT or Gemini web output generation is automated without an API integration;
- claiming a live DeepSeek calibration when only mocked tests were run;
- calling private conversation data a public training dataset.

## Calibration Gate

Before promoting a proposed adapter:

- keep the source adapter unchanged;
- generate or import baseline and candidate outputs;
- keep holdout prompts hidden from the proposer;
- require zero configured hard failures;
- reject composite or reliability-guardrail regressions;
- perform a blind, order-swapped human A/B review;
- record `human-approval.json` before claiming calibration.

## First Real-User Check

Ask each tester to use the adapter in their normal workflow for at least three tasks. Record actual use, not stated interest, in `evals/real-user-feedback-template.csv`.

The first release decision should use:

- successful installation;
- tasks actually completed;
- before/after preference;
- whether the user keeps the adapter enabled;
- concrete failure examples;
- willingness to recommend or open an issue.

Stars are a distribution signal, not the primary proof of recurring value.

## Repository Boundary

Initialize and publish the Git repository from this `human-agent-project` directory only. Its parent workspace contains private research artifacts and must never be added as the repository root.

Follow `docs/release-day.md` for the final packaging and launch sequence.
