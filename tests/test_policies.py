from inspect_evals.policies import load_policies

def test_load_policies():
    pols = load_policies([
        "policies/base_policy.yaml",
        "policies/pii.yaml",
        "policies/harmful_content.yaml",
        "policies/jailbreak.yaml",
    ])
    assert "pii" in pols and "harmful_content" in pols and "jailbreak" in pols
