# Each check module implements:
# def run(sample: Dict[str, Any], policies: Dict[str, Any]) -> Dict[str, Any]:
# returning a structure:
# {"name": "<check_name>", "passed": bool, "findings": [...], "severity": "low|medium|high|..."}
