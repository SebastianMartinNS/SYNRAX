"""Analyze benchmark traces for task 12508 — control vs codedna vs synrax_runtime."""
import json
from pathlib import Path

traces_dir = Path(r"c:\Users\adria\synrax\_reference\codedna\benchmark_agent\runs\or-deepseek-v3.2\session_traces")

files = {
    "control":        "bench_or-deepseek-v3.2_12508_control_20260323_223651_r0.json",
    "codedna":        "bench_or-deepseek-v3.2_12508_codedna_20260323_224120_r0.json",
    "synrax_runtime": "bench_or-deepseek-v3.2_12508_synrax_runtime_20260323_224441_r0.json",
}

for label, fname in files.items():
    t = json.loads((traces_dir / fname).read_text())
    m = t["metrics_read"]
    gt_set = set(t["ground_truth"])

    reads = [s for s in t["trace"] if s.get("tool") == "read_file"]
    read_files = [s["args"].get("path", "") for s in reads]

    noise_files = [f for f in read_files if f not in gt_set]
    hit_files = [f for f in read_files if f in gt_set]

    print(f"{'=' * 70}")
    print(f"  {label.upper()}")
    print(f"{'=' * 70}")
    print(f"  F1={m['f1']:.0%}  R={m['recall']:.0%}  P={m['precision']:.0%}")
    print(f"  Total reads: {len(reads)}  |  GT hit: {len(hit_files)}/{len(gt_set)}  |  Noise: {len(noise_files)} ({100*len(noise_files)/max(len(reads),1):.0f}%)")
    print(f"  Read order:")
    for i, f in enumerate(read_files, 1):
        marker = "GT" if f in gt_set else "NOISE"
        print(f"    {i:2d}. [{marker:5s}] {f}")

    # Also show all other tool calls
    greps = [s for s in t["trace"] if s.get("tool") == "grep"]
    lists = [s for s in t["trace"] if s.get("tool") == "list_files"]
    synrax = [s for s in t["trace"] if s.get("tool", "").startswith("query_")]
    print(f"  Other: {len(greps)} greps, {len(lists)} list_files, {len(synrax)} synrax queries")
    
    # Show missed GT files
    missed = gt_set - set(read_files)
    if missed:
        print(f"  MISSED GT: {', '.join(sorted(missed))}")
    print()
