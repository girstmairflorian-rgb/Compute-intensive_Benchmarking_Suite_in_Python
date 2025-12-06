# Compute-Intensive Benchmarking Suite in Python

This project benchmarks different multiprocessing strategies in Python — including `pool.map`, `pool.apply`, 
`pool.apply_async`, and a single-process loop — using CPU-heavy algorithms such as prime checking. It provides a 
command-line interface for running tests with configurable algorithms, process counts, and input sizes, and includes 
progress bars and CSV output for deeper analysis.

The goal of the project is to explore how Python distributes compute-intensive workloads across multiple processes, 
how chunk sizes influence performance, and why certain strategies outperform others at scale.

## Features

+ Modular architecture (plug-in algorithms)
+ Multiple multiprocessing strategies
+ CLI interface using argparse
+ Consistent, comparable benchmark output
+ Easy to extend with new algorithms or benchmarking backends

## Usage

### Run a benchmark

`python src/main.py -algorithm primeChecker -benchmark poolMap -upperLimit 2000000 -numProcesses 4`

### Example Output

`primeChecker took 57.4905s for 2000000 numbers using poolMap`

## Command-line Arguments

| Argument         | Description                                                                                        |
|------------------|----------------------------------------------------------------------------------------------------|
| `-algorithm`     | Algorithm to benchmark (e.g., primeChecker)                                                        |
| `-benchmark`     | Benchmarking method (poolApply, poolApplyAsync, poolApplyAsyncChunked, poolMap, singleProcessLoop) |
| `-upperLimit`    | Range end for the benchmark (1…N)                                                                  |
| `-numProcesses`  | Number of worker processes                                                                         |

## Architecture
```
src/
  main.py               → CLI & orchestration
  benchmarks.py         → Multiprocessing strategies
  test_algorithms.py    → Computation functions (pluggable)
  results.csv           → permanent storage of the results
README.md
```

## Extending the project

### Add a new algorithm
```
# In test_algorithms.py
def fibonacci(n):
    ...
```
Then register it:
```
# In main.py
ALGORITHMS = {
    "primeChecker": check_if_prime,
    "fibonacci": fibonacci,
}
```
That's all — no other code changes required.

## Why `apply()` is slow
`apply()` is synchronous and blocking. 
It behaves like a normal function call and does not run tasks in parallel.
This makes `apply()` significantly slower than a normal loop, because each call includes inter-process overhead.

Included for educational comparison.

## `tqdm()` overhead
`tqdm()` adds a bit of overhead per iteration (~60ns / iteration). Worth it for the better experience.

## `apply_async()` and chunking
The default chunk size for `apply_async()` is effectively 1 because it is one task per submission.

To get around this, a manually set chunk size makes the algorithm way faster. The program automatically adjusts to the
upperLimit of the range and chooses between `apply_async()` and `apply_async_chunked()` accordingly.

## License

MIT