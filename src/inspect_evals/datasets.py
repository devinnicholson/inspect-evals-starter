from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from .utils import read_jsonl

@dataclass
class Dataset:
    samples: List[Dict[str, Any]]

def load_dataset(prompts_path: str, outputs_path: Optional[str] = None) -> Dataset:
    prompts = {row["id"]: row for row in read_jsonl(prompts_path)}
    outputs = {}
    if outputs_path:
        outputs = {row["id"]: row for row in read_jsonl(outputs_path)}

    samples = []
    for sid, p in prompts.items():
        sample = {"id": sid, "prompt": p.get("prompt", "")}
        if sid in outputs:
            sample["output"] = outputs[sid].get("output", "")
        else:
            sample["output"] = ""
        samples.append(sample)
    return Dataset(samples=samples)
