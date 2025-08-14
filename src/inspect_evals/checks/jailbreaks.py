from typing import Dict, Any, List

def run(sample: Dict[str, Any], policies: Dict[str, Any]) -> Dict[str, Any]:
    pol = policies.get("jailbreak", {})
    pats = pol.get("patterns", [])
    text = (sample.get("output") or "") + " " + (sample.get("prompt") or "")
    text_lower = text.lower()
    findings: List[Dict[str, Any]] = []

    for p in pats:
        subs = [s.lower() for s in p.get("substrings", [])]
        if any(s in text_lower for s in subs if s.strip()):
            findings.append({
                "pattern_id": p.get("id"),
                "description": p.get("description"),
                "severity": p.get("severity", "low"),
            })

    return {
        "name": "jailbreak",
        "passed": len(findings) == 0,
        "findings": findings,
        "severity": max((f.get("severity", "low") for f in findings), default="info"),
    }
