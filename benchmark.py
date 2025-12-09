"""
benchmark.py

Compare read & write speed of CustomCsvReader/Writer vs Python stdlib csv.

Usage:
    python benchmark.py benchmark_data.csv --runs 5
"""

import argparse
import csv
import os
import statistics
import time
from custom_csv import CustomCsvReader, CustomCsvWriter


def time_reads_using_custom(path: str) -> (float, int):
    start = time.perf_counter()
    count = 0
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = CustomCsvReader(fh)
        for _ in reader:
            count += 1
    end = time.perf_counter()
    return end - start, count


def time_reads_using_stdlib(path: str) -> (float, int):
    start = time.perf_counter()
    count = 0
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        for _ in reader:
            count += 1
    end = time.perf_counter()
    return end - start, count


def time_write_custom(rows, tmp_path: str) -> float:
    start = time.perf_counter()
    with open(tmp_path, "w", encoding="utf-8", newline="") as fh:
        writer = CustomCsvWriter(fh)
        writer.writerows(rows)
    end = time.perf_counter()
    return end - start


def time_write_stdlib(rows, tmp_path: str) -> float:
    start = time.perf_counter()
    with open(tmp_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerows(rows)
    end = time.perf_counter()
    return end - start


def load_rows(path: str):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))


def run_benchmark(path: str, runs: int = 5, tmp_dir: str = "."):
    # Read benchmarks
    custom_times = []
    std_times = []
    counts = []
    for i in range(runs):
        t_c, c1 = time_reads_using_custom(path)
        t_s, c2 = time_reads_using_stdlib(path)
        if c1 != c2:
            raise RuntimeError(f"Row count mismatch: custom={c1}, stdlib={c2}")
        custom_times.append(t_c)
        std_times.append(t_s)
        counts.append(c1)

    # Load rows for write benchmarks once (using stdlib parser for canonical rows)
    rows = load_rows(path)

    custom_write_times = []
    std_write_times = []
    tmp_custom = os.path.join(tmp_dir, "tmp_custom_out.csv")
    tmp_std = os.path.join(tmp_dir, "tmp_std_out.csv")
    for i in range(runs):
        custom_write_times.append(time_write_custom(rows, tmp_custom))
        std_write_times.append(time_write_stdlib(rows, tmp_std))
        # remove to reduce caching effects
        try:
            os.remove(tmp_custom)
            os.remove(tmp_std)
        except OSError:
            pass

    # Report
    print("=== Read benchmark ===")
    print(f"Rows parsed: {counts[0]}")
    print(f"Custom reader: mean={statistics.mean(custom_times):.4f}s  stdev={statistics.stdev(custom_times):.4f}s")
    print(f"Stdlib reader: mean={statistics.mean(std_times):.4f}s  stdev={statistics.stdev(std_times):.4f}s")
    print()
    print("=== Write benchmark ===")
    print(f"Custom writer: mean={statistics.mean(custom_write_times):.4f}s  stdev={statistics.stdev(custom_write_times):.4f}s")
    print(f"Stdlib writer: mean={statistics.mean(std_write_times):.4f}s  stdev={statistics.stdev(std_write_times):.4f}s")
    print()
    # Throughput
    rows_count = counts[0]
    print("=== Throughput (rows/sec) ===")
    print(f"Custom read throughput: {rows_count / statistics.mean(custom_times):.1f} rows/sec")
    print(f"Stdlib read throughput: {rows_count / statistics.mean(std_times):.1f} rows/sec")
    print()
    print("=== Notes ===")
    print("- Stdlib csv is implemented in C and usually much faster.")
    print("- Custom parser is pure Python; optimizations may narrow gap.")
    print("- Run multiple times and on a quiet system for stable results.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="CSV path to benchmark (generate with generate_csv.py)")
    parser.add_argument("--runs", type=int, default=5, help="How many runs to average")
    parser.add_argument("--tmpdir", default=".", help="Directory for temporary output files")
    args = parser.parse_args()
    run_benchmark(args.path, runs=args.runs, tmp_dir=args.tmpdir)
