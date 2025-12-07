from time import perf_counter
import csv
import argparse
from pathlib import Path
import test_algorithms
import benchmarks

# Setup clean directory structure for the output to results.csv
ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)
RESULTS_FILE = RESULTS_DIR / "results.csv"

ALGORITHMS = {
    "primeChecker": test_algorithms.check_if_prime,
    "fibonacci": test_algorithms.fibonacci,
}

BENCHMARKS = {
    "poolApply": benchmarks.pool_apply,
    "poolApplyAsync": benchmarks.pool_apply_async,
    "poolApplyAsyncChunked": benchmarks.pool_apply_async_chunked,
    "poolMap": benchmarks.pool_map,
    "singleProcessLoop": benchmarks.single_process_loop,
}

def parse_args():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument(
        "-algorithm",
        choices=list(ALGORITHMS.keys()),
        required=True,
        help="Algorithm to benchmark"
    )

    parser.add_argument(
        "-benchmark",
        choices=list(BENCHMARKS.keys()),
        required=True,
        help="Benchmarking method to use"
    )

    parser.add_argument(
        "-upperLimit",
        type=int,
        default=10_000,
        help="Range end for the benchmark"
    )

    parser.add_argument(
        "-numProcesses",
        type=int,
        default=4,
        help="Number of worker processes"
    )
    return parser.parse_known_args()

if __name__ == "__main__":
    args, unknown = parse_args()
    algorithm = ALGORITHMS[args.algorithm]
    benchmark_func = BENCHMARKS[args.benchmark]

    numbers: list[int] = list(range(1, args.upperLimit + 1))
    num_processes = args.numProcesses

    for arg in unknown:
        print(f'"{arg}" is not a valid parameter. It will be skipped.')

    # Auto-detect upperLimit to choose between poolApplyAsyncChunked and poolApplyAsync
    if args.benchmark == "poolApplyAsync" and args.upperLimit > 200_000:
        args.benchmark = "poolApplyAsyncChunked"
        benchmark_func = benchmarks.pool_apply_async_chunked
        print("Auto-selected chunked async version for large input.")

    start = perf_counter()
    result = benchmark_func(numbers, algorithm, args.numProcesses)
    end = perf_counter()

    elapsedTime = round((end - start), 5)

    print(f"Calculating {args.algorithm} using {args.benchmark} with {args.numProcesses} processes for {args.upperLimit} numbers took {elapsedTime}s")

    with RESULTS_FILE.open("a", encoding="utf-8") as printFile:
        file_writer = csv.writer(printFile, delimiter=",", lineterminator="\n")
        file_writer.writerow([args.algorithm, args.benchmark, args.numProcesses, str(args.upperLimit), str(elapsedTime)])