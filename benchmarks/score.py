"""
Polaris-Bench Scoring Script
Usage: python benchmarks/score.py --bench B01 --run-output LP01-B01/
Compares a Polaris run against known answers.
"""

import json, sys, argparse
from pathlib import Path

BENCH_DIR = Path(__file__).parent


def load_bench(bench_id: str) -> dict:
    """Load benchmark definition."""
    path = BENCH_DIR / f"{bench_id}_*.json"
    matches = list(BENCH_DIR.glob(f"{bench_id}_*.json"))
    if not matches:
        print(f"Benchmark {bench_id} not found")
        sys.exit(1)
    with open(matches[0], 'r', encoding='utf-8') as f:
        return json.load(f)


def score_run(bench: dict, run_dir: str = None) -> dict:
    """
    Score a Polaris run against the benchmark.
    If run_dir is None, print the benchmark's expected answer for manual review.
    """
    if run_dir is None:
        return {
            "bench_id": bench["id"],
            "mode": "dry_run",
            "expected_contradiction": f"{bench['contradiction']['proposition_A'][:60]}...",
            "expected_resolution": bench["ground_truth"]["resolution"][:120],
            "landmark_paper": bench["ground_truth"]["landmark_paper"],
            "scoring_rubric": bench["scoring"]
        }

    # TODO: Actual scoring against run output
    run_path = Path(run_dir)
    if not run_path.exists():
        return {"error": f"Run directory {run_dir} not found"}

    scores = {}
    # Check if closure report exists
    closure = run_path / "synthesis" / "closure_report.md"
    if closure.exists():
        scores["closure_exists"] = True

    # Basic scoring — expand as we collect runs
    return {
        "bench_id": bench["id"],
        "run_dir": str(run_path),
        "scores": scores,
        "total": "TBD — manual review needed"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polaris-Bench Scorer")
    parser.add_argument("--bench", required=True, help="Benchmark ID (e.g., B01)")
    parser.add_argument("--run", help="Path to Polaris run output directory")
    parser.add_argument("--list", action="store_true", help="List all available benchmarks")
    args = parser.parse_args()

    if args.list:
        for f in sorted(BENCH_DIR.glob("B*_*.json")):
            with open(f, 'r', encoding='utf-8') as fp:
                b = json.load(fp)
            print(f"  {b['id']}: {b['title']} ({b['domain']}, {b['difficulty']})")
        sys.exit(0)

    bench = load_bench(args.bench)

    if args.run:
        result = score_run(bench, args.run)
    else:
        result = score_run(bench)
        print(f"\n  Benchmark: {bench['id']} — {bench['title']}")
        print(f"  Domain: {bench['domain']} | Difficulty: {bench['difficulty']}")
        print(f"  Hidden assumption: {bench['what_selector_should_find']['hidden_assumption']}")
        print(f"  Ground truth: {bench['ground_truth']['resolution'][:200]}")
        print(f"  Key paper: {bench['ground_truth']['landmark_paper']}")
        print(f"\n  To score a run: python benchmarks/score.py --bench {bench['id']} --run <run_dir>")

    # Use ascii-safe output for Windows compatibility
    print(json.dumps(result, indent=2, ensure_ascii=True))
