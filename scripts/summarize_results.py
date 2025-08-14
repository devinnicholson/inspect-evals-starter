import argparse
from inspect_evals.report import write_reports

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, help="Path to results.jsonl")
    parser.add_argument("--out", required=True, help="Directory to write summary")
    args = parser.parse_args()

    write_reports(args.results, args.out)
    print(f"Wrote summary to {args.out}")

if __name__ == "__main__":
    main()
