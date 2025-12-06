# Compute-Intensive Benchmarking Suite (Python)

A modular, extensible benchmarking suite for comparing compute-heavy algorithms using Python Multiprocessing including:

+ Pool.apply
+ Pool.apply_async
+ Pool.map
+ Single-process execution

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
| `-benchmark`     | Benchmarking method (poolApply, poolApplyAsync, poolMap, singleProcessLoop) |
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

## Why `pool.apply()` is slow
`pool.apply()` is synchronous and blocking. 
It behaves like a normal function call and does not run tasks in parallel.

Execution model:

+ Submit task 1
+ Wait for task 1
+ Submit task 2
+ Wait for task 2
+ …

This makes .apply() significantly slower than a normal loop, because each call includes inter-process overhead.
Included for educational comparison.

## License

MIT