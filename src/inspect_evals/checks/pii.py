import regex as re
from typing import Dict, Any, List

def run(sample: Dict[str, Any], policies: Dict[str, Any]) -> Dict[str, Any]:
    pol = policies.get("pii", {})
    rules = pol.get("rules", [])
    text = (sample.get("output") or "") + " " + (sample.get("prompt") or "")
    findings: List[Dict[str, Any]] = []
    max_severity = "info"
    severity_rank = ["info", "low", "medium", "high", "critical"]

    for r in rules:
        if r.get("type") == "regex" and r.get("pattern"):
            try:
                pat = re.compile(r["pattern"])
                if pat.search(text):
                    findings.append({
                        "rule_id": r.get("id"),
                        "description": r.get("description"),
                        "severity": r.get("severity", "low"),
                    })
                    if severity_rank.index(r.get("severity", "low")) > severity_rank.index(max_severity):
                        max_severity = r.get("severity", "low")
            except Exception:
                continue

    return {
        "name": "pii",
        "passed": len(findings) == 0,
        "findings": findings,
        "severity": max_severity if findings else "info",
    }
