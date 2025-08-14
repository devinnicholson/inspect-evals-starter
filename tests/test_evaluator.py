from inspect_evals.evaluator import load_config, run_eval

def test_run_eval(tmp_path):
    cfg = load_config("configs/eval_config.yaml")
    cfg.out_dir = str(tmp_path / "out")
    res = run_eval(cfg)
    assert "rows" in res and len(res["rows"]) >= 1
