# CSV-parser-from-scratch-in-python
# Custom CSV Parser From Scratch in Python

This project implements a **Custom CSV Reader and Writer** completely from scratch using pure Python.  
It is built as part of a Data Engineering task (GPP), focusing on understanding CSV parsing mechanics, file I/O, buffering, quoting rules, and performance benchmarking.

The custom parser supports:
- Comma-separated fields  
- Quoted fields `"..."`  
- Escaped quotes `""` inside quoted fields  
- Embedded newlines in quoted fields  
- Streaming line-by-line parsing (does not load entire file into memory)  
- Writer-side quoting and escaping  
- Benchmarking against Python’s built-in `csv` module  

All functionality has been implemented and validated using automated tests.

---

## 📦 Project Structure

```
CSV-parser-from-scratch-in-python/
│
├── custom_csv.py           # Custom CSV Reader & Writer (core implementation)
├── tests.py                # Automated tests comparing with stdlib csv
├── generate_csv.py         # Synthetic dataset generator (10k x 5)
├── benchmark.py            # Performance benchmarking script
├── benchmark_data.csv      # Generated dataset (ignored if large)
├── requirements.txt        # External dependencies (none)
└── README.md               # Documentation (this file)
```

---

#  Features

### ✔ Custom CSV Reader
Implements:
- Proper comma parsing  
- Quote handling  
- Escaped quotes (`""`)  
- Embedded newline support  
- Works as an iterator (`__iter__`, `__next__`)  
- Streaming (does not read whole file at once)

### Custom CSV Writer
Automatically:
- Quotes fields containing comma/quote/newline  
- Escapes inner quotes  
- Produces valid CSV readable by any standard CSV library  

### Benchmarking System
Compares:
- Custom reader vs stdlib `csv.reader`  
- Custom writer vs stdlib `csv.writer`  

Using a 10,000-row dataset with varied content:
- Plain values  
- Commas  
- Quotes  
- Multiline fields  

---

# Installation

This project uses **only the Python standard library**.

`requirements.txt`:

```
# No external dependencies. Project uses only Python standard library.
```

---

# Usage

## Running the Custom Reader/Writer Demo

```
python custom_csv.py
```

Expected output:

```
ROW: ['a', 'b,1', 'line\nbreak', 'He said "Hi" ', 'x']
ROW: ['one', 'two', 'three']
```

---

## Running Tests

```
python tests.py
```

Expected last line:

```
All tests passed.
```

---

## Generate Benchmark Dataset (10k x 5)

```
python generate_csv.py benchmark_data.csv 10000 5
```

---

## Run Benchmark

```
python benchmark.py benchmark_data.csv --runs 5
```

---

# Benchmark Results (Your Actual Run)

Dataset: 10,000 rows × 5 columns  
Runs: 5

### **Read Performance**
| System | Mean Time | Stdev |
|-------|-----------|--------|
| **Custom Reader** | **0.0921 s** | 0.0136 s |
| **Stdlib Reader** | **0.0157 s** | 0.0071 s |

### **Write Performance**
| System | Mean Time | Stdev |
|--------|------------|--------|
| **Custom Writer** | **0.0434 s** | 0.0046 s |
| **Stdlib Writer** | **0.0145 s** | 0.0033 s |

### **Throughput (Rows/sec)**
| System | Rows/sec |
|--------|-----------|
| **Custom Reader** | 108,594 rows/sec |
| **Stdlib Reader** | 637,098 rows/sec |

---

# Benchmark Analysis

The Python `csv` module is implemented in optimized C, while the custom parser is pure Python.  
As expected:

- The **stdlib CSV reader** is ≈ **6× faster** than the custom reader.
- The **stdlib CSV writer** is ≈ **3× faster** than the custom writer.
- The results are stable across runs (low standard deviation).

Despite being slower, the custom implementation correctly handles:
- Complex quoting rules  
- Escaped quotes  
- Multiline fields  
- Streaming parsing  

This demonstrates a complete understanding of low-level CSV parsing mechanics.