# Compute-Intensive Benchmarking Suite (Python)

A modular, extensible benchmarking suite for comparing compute-heavy algorithms using Python `multiprocessing` including:

+ `apply()`
+ `apply_async()`
+ `map()`
+ Single-process execution (i.e. a `for`-loop)

This project allows you to benchmark any algorithm simply by registering it in the ALGORITHMS dictionary.
Currently implemented: a prime-checking function.

## Features

+ Modular architecture (plug-in algorithms)
+ Multiple multiprocessing strategies
+ CLI interface using argparse
+ Consistent, comparable benchmark output
+ Easy to extend with new algorithms or benchmarking backends

## Usage

### Run a benchmark

`python main.py -algorithm primeChecker -benchmark poolMap -upperLimit 2000000 -numProcesses 4`

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
This adds a bit of overhead per iteration (~60ns / iteration). Worth it for the better experience.

## `apply_async()` and chunking
The default chunk size for `apply_async()` is effectively 1 because it is one task per submission.

To get around this, a manually set chunk size makes the algorithm way faster. The program automatically adjusts to the
upperLimit of the range and chooses between `apply_async()` and `apply_async_chunked()` accordingly.

## License

MIT