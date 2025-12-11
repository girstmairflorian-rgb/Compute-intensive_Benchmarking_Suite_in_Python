from multiprocessing import Pool
from tqdm import tqdm
import math
from typing import Callable, Any


def pool_apply(numbers: list[int], algorithm: Callable, n_processes: int) -> list[Any]:
    with Pool(processes=n_processes) as pool:
        return [pool.apply(algorithm, args=(n,)) for n in tqdm(numbers)]


def pool_apply_async(numbers: list[int], algorithm: Callable, n_processes: int) -> list[Any]:
    with Pool(processes=n_processes) as pool:
        results = [pool.apply_async(algorithm, args=(n,)) for n in tqdm(numbers)]
        return [result.get() for result in tqdm(results)]


def pool_apply_async_chunked(numbers, algorithm: Callable, n_processes: int) -> list[Any]:
    total: int = len(numbers)
    chunk_size: int = auto_chunk_size(total)
    chunks = [numbers[i:i + chunk_size] for i in range(0, total, chunk_size)]

    with Pool(processes=n_processes) as pool:
        futures = [pool.apply_async(run_chunk, args=(chunk, algorithm)) for chunk in tqdm(chunks)]
        return [f.get() for f in tqdm(futures)]


def pool_map(numbers: list[int], algorithm: Callable, n_processes: int) -> list[Any]:
    total: int = len(numbers)
    chunk_size: int = auto_chunk_size(total)
    with Pool(processes=n_processes) as pool:
        return pool.map(algorithm, tqdm(numbers), chunksize=chunk_size)


def single_process_loop(numbers: list[int], algorithm: Callable, n_processes: int = None) -> list[Any]:
    return [algorithm(n) for n in tqdm(numbers)]


def auto_chunk_size(total_items: int, target_chunks=1000) -> int:
    """Compute an efficient chunk size."""
    if total_items <= 0:
        return 1

    chunk: int = math.ceil(total_items / target_chunks)

    if chunk < 1:
        chunk = 1
    if chunk > total_items:
        chunk = total_items

    return chunk


def run_chunk(chunk: Any, algorithm: Callable) -> list[int]:
    return [algorithm(n) for n in chunk]