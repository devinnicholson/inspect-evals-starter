# inspect-evals-starter-with-policies

A minimal, batteries-included starter kit for evaluating LLM outputs against
**policy rules** (PII, harmful content, jailbreak patterns, etc.). This project
provides a simple evaluator, YAML-based policies, and a markdown/CSV report.

**Why this exists**

- Quick-start an internal eval harness without heavy dependencies.
- Keep policies in version-controlled YAML.
- Produce repeatable, diffable results for CI or ad-hoc checks.

## Quickstart

```bash
# 1) Create a virtual env (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the sample eval
python scripts/run_eval.py --config configs/eval_config.yaml
```

The run will generate outputs under `out/` and print a summary. Open the
markdown report in `out/`.

## Project layout

```text
inspect-evals-starter-with-policies/
├─ configs/
│  └─ eval_config.yaml
├─ data/
│  └─ samples/
│     ├─ prompts.jsonl
│     └─ outputs.jsonl
├─ policies/
│  ├─ base_policy.yaml
│  ├─ pii.yaml
│  ├─ harmful_content.yaml
│  └─ jailbreak.yaml
├─ scripts/
│  ├─ run_eval.py
│  └─ summarize_results.py
├─ src/inspect_evals/
│  ├─ __init__.py
│  ├─ datasets.py
│  ├─ evaluator.py
│  ├─ policies.py
│  ├─ report.py
│  ├─ utils.py
│  └─ checks/
│     ├─ __init__.py
│     ├─ pii.py
│     ├─ safety.py
│     └─ jailbreaks.py
├─ tests/
│  ├─ test_evaluator.py
│  └─ test_policies.py
├─ requirements.txt
├─ pyproject.toml
├─ VERSION.txt
├─ LICENSE
└─ .gitignore
```

## Configuration

`configs/eval_config.yaml` controls which dataset and checks to run, and where
to write results. Policies are defined under `policies/*.yaml` and are loaded by
`src/inspect_evals/policies.py`.

### Adding a new policy or check

1. Create a new YAML under `policies/` with your rules.
2. Create a new checker in `src/inspect_evals/checks/` that implements
   `run(sample, policies)`.
3. Add the checker key to `checks:` in `configs/eval_config.yaml`.

## Extending datasets

Put your prompts and model responses in JSONL files (`data/your-dataset/`). Each
line should be a JSON object:

```json
{
  "id": "uuid-or-string",
  "prompt": "Your prompt",
  "output": "Model response text"
}
```

Update paths in `configs/eval_config.yaml` and rerun.

## License

MIT. See `LICENSE`.
