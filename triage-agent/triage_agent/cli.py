import argparse
import os
from collections import Counter
from typing import List, Optional

from .pipeline import read_tickets, triage_all, write_results_csv
from .report import render_report


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="triage_agent", description="Rule-based support-ticket triage.")
    parser.add_argument("csv", help="input CSV of tickets")
    parser.add_argument("--out", default="out", help="output directory (default: out)")
    args = parser.parse_args(argv)

    results = triage_all(read_tickets(args.csv))
    os.makedirs(args.out, exist_ok=True)
    csv_path = os.path.join(args.out, "triaged.csv")
    report_path = os.path.join(args.out, "report.md")
    write_results_csv(results, csv_path)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(render_report(results, source=os.path.basename(args.csv)))

    urg = Counter(r.urgency for r in results)
    review = sum(r.needs_review for r in results)
    print(f"{len(results)} tickets triaged: P1={urg['P1']} P2={urg['P2']} P3={urg['P3']}, {review} need review")
    print(f"Wrote {csv_path} and {report_path}")
    return 0
