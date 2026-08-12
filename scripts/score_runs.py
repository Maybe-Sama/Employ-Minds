#!/usr/bin/env python3
"""Summarize real A/B benchmark JSONL without inventing a magic aggregate score."""
from __future__ import annotations
import argparse, json, statistics
from collections import defaultdict
from pathlib import Path

REQUIRED = {"task_id","system","solved","false_completion","regression","critical_miss","reviewer_catches","input_tokens","output_tokens","wall_seconds"}

def load(path: Path):
    rows=[]
    for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        row=json.loads(line)
        missing=REQUIRED-row.keys()
        if missing: raise ValueError(f"line {n}: missing {sorted(missing)}")
        rows.append(row)
    return rows

def pct(n,d): return 0.0 if not d else 100*n/d

def main():
    p=argparse.ArgumentParser(); p.add_argument("results"); args=p.parse_args()
    groups=defaultdict(list)
    for row in load(Path(args.results)): groups[row["system"]].append(row)
    print("system\tn\tsolved%\tfalse_complete%\tregression%\tcritical_miss%\treviewer_catches\tmedian_tokens\tmedian_seconds")
    for system,rows in sorted(groups.items()):
        n=len(rows); tokens=[r["input_tokens"]+r["output_tokens"] for r in rows]
        print("\t".join(map(str,[system,n,f"{pct(sum(r['solved'] for r in rows),n):.1f}",f"{pct(sum(r['false_completion'] for r in rows),n):.1f}",f"{pct(sum(r['regression'] for r in rows),n):.1f}",f"{pct(sum(r['critical_miss'] for r in rows),n):.1f}",sum(r["reviewer_catches"] for r in rows),f"{statistics.median(tokens):.0f}",f"{statistics.median(r['wall_seconds'] for r in rows):.1f}"])))
    return 0

if __name__ == "__main__": raise SystemExit(main())
