import argparse
from inspect_evals.evaluator import load_config, run_eval
from inspect_evals.report import write_reports

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to eval_config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    res = run_eval(cfg)

    # Write reports
    results_path = f"{res['out_dir']}/results.jsonl"
    write_reports(results_path, res["out_dir"])
    print(f"\nWrote results to: {res['out_dir']}")

if __name__ == "__main__":
    main()
