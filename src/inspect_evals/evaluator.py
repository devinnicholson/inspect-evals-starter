from dataclasses import dataclass
from typing import Dict, Any, List
from pathlib import Path
import yaml
from rich.console import Console
from rich.table import Table

from .datasets import load_dataset
from .policies import load_policies
from .utils import write_jsonl

from .checks import pii as check_pii
from .checks import safety as check_safety
from .checks import jailbreaks as check_jailbreaks

CHECKERS = {
    "pii": check_pii.run,
    "harmful_content": check_safety.run,
    "jailbreak": check_jailbreaks.run,
}

console = Console()

@dataclass
class EvalConfig:
    prompts_path: str
    outputs_path: str
    checks: List[str]
    policy_files: List[str]
    out_dir: str

def load_config(path: str) -> EvalConfig:
    cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    ds = cfg.get("dataset", {})
    return EvalConfig(
        prompts_path=ds.get("prompts_path"),
        outputs_path=ds.get("outputs_path"),
        checks=list(cfg.get("checks", [])),
        policy_files=list(cfg.get("policy_files", [])),
        out_dir=cfg.get("out_dir", "out/run"),
    )

def run_eval(cfg: EvalConfig) -> Dict[str, Any]:
    dataset = load_dataset(cfg.prompts_path, cfg.outputs_path)
    policies = load_policies(cfg.policy_files)
    out_dir = Path(cfg.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, Any]] = []
    for sample in dataset.samples:
        sample_row = {"id": sample["id"], "prompt": sample.get("prompt", ""), "output": sample.get("output", "")}
        for ck in cfg.checks:
            fn = CHECKERS.get(ck)
            if not fn:
                continue
            res = fn(sample, policies)
            sample_row[f"{ck}_passed"] = res["passed"]
            sample_row[f"{ck}_severity"] = res.get("severity", "info")
            sample_row[f"{ck}_findings"] = res.get("findings", [])
        rows.append(sample_row)

    write_jsonl(str(out_dir / "results.jsonl"), rows)

    # Simple console summary
    table = Table(title="Eval Summary")
    table.add_column("ID", justify="right", style="bold")
    for ck in cfg.checks:
        table.add_column(f"{ck} ✓/✗")
    for r in rows:
        values = [r["id"]]
        for ck in cfg.checks:
            values.append("✓" if r.get(f"{ck}_passed") else "✗")
        table.add_row(*values)
    console.print(table)

    return {"rows": rows, "out_dir": str(out_dir)}
