from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from .utils import read_jsonl

def _bool_to_mark(b: bool) -> str:
    return "✅" if b else "❌"

def write_reports(results_path: str, out_dir: str):
    rows = read_jsonl(results_path)
    df = pd.DataFrame(rows)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # CSV
    csv_path = out / "results.csv"
    df.to_csv(csv_path, index=False)

    # Markdown
    md_lines: List[str] = []
    md_lines.append("# Eval Report\n")
    md_lines.append("| id | pii | harmful | jailbreak |")
    md_lines.append("|---:|:---:|:-------:|:---------:|")

    for r in rows:
        md_lines.append(
            f"| {r['id']} | {_bool_to_mark(r.get('pii_passed', True))} | "
            f"{_bool_to_mark(r.get('harmful_content_passed', True))} | "
            f"{_bool_to_mark(r.get('jailbreak_passed', True))} |"
        )

    (out / "report.md").write_text("\n".join(md_lines), encoding="utf-8")

    return {"csv": str(csv_path), "md": str(out / "report.md")}
