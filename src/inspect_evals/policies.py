from dataclasses import dataclass
from typing import Any, Dict, List
from pathlib import Path
import yaml

@dataclass
class PolicyBundle:
    metadata: Dict[str, Any]
    pii: Dict[str, Any]
    harmful_content: Dict[str, Any]
    jailbreak: Dict[str, Any]

def load_policies(paths: List[str]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for p in paths:
        data = yaml.safe_load(Path(p).read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "name" not in data:
            continue
        merged[data["name"]] = data
    return merged
