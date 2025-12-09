"""
generate_csv.py

Generate a synthetic CSV file for benchmarking.
Usage:
    python generate_csv.py output.csv 10000 5
"""

import random
import sys
from custom_csv import CustomCsvWriter


def random_field(seed_idx: int) -> str:
    rnd = random.random()
    if rnd < 0.6:
        return f"val{seed_idx}"
    if rnd < 0.8:
        return f"multi,val{seed_idx}"
    if rnd < 0.9:
        return f'quote "val{seed_idx}"'
    return f"line1\nline2_{seed_idx}"


def generate(path: str, rows: int = 10000, cols: int = 5, seed: int = 42) -> None:
    random.seed(seed)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = CustomCsvWriter(fh)
        for i in range(rows):
            row = [random_field(i * cols + j) for j in range(cols)]
            writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_csv.py output.csv [rows] [cols]")
        sys.exit(1)
    out = sys.argv[1]
    rows = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    cols = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    generate(out, rows=rows, cols=cols)
    print(f"Generated {rows}x{cols} CSV at {out}")
