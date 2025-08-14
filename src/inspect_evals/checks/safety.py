from typing import Dict, Any, List

def run(sample: Dict[str, Any], policies: Dict[str, Any]) -> Dict[str, Any]:
    pol = policies.get("harmful_content", {})
    cats = pol.get("categories", {})
    text = (sample.get("output") or "") + " " + (sample.get("prompt") or "")
    text_lower = text.lower()
    findings: List[Dict[str, Any]] = []
    max_severity = "info"
    severity_rank = ["info", "low", "medium", "high", "critical"]

    for cat, cfg in cats.items():
        kws = [k.lower() for k in cfg.get("keywords", [])]
        hit = any(k in text_lower for k in kws if k.strip())
        if hit:
            sev = cfg.get("severity", "low")
            findings.append({"category": cat, "severity": sev, "matched": True})
            if severity_rank.index(sev) > severity_rank.index(max_severity):
                max_severity = sev

    return {
        "name": "harmful_content",
        "passed": len(findings) == 0,
        "findings": findings,
        "severity": max_severity if findings else "info",
    }
