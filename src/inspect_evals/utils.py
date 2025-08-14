import json
from pathlib import Path
from typing import Iterable, Dict, Any, List

def read_jsonl(path: str) -> List[Dict[str, Any]]:
    p = Path(path)
    lines = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            lines.append(json.loads(line))
    return lines

def write_jsonl(path: str, rows: Iterable[Dict[str, Any]]):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for obj in rows:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
