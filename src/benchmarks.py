from multiprocessing import Pool
from tqdm import tqdm

def pool_apply(numbers: list[int], algorithm, n_processes: int) -> list[int]:
    with Pool(processes=n_processes) as pool:
        return [pool.apply(algorithm, args=(n,)) for n in tqdm(numbers)]


def pool_apply_async(numbers: list[int], algorithm, n_processes: int) -> list[int]:
    with Pool(processes=n_processes) as pool:
        results = [pool.apply_async(algorithm, args=(n,)) for n in tqdm(numbers)]
        return [result.get() for result in tqdm(results)]


def pool_map(numbers: list[int], algorithm, n_processes: int) -> list[int]:
    with Pool(processes=n_processes) as pool:
        return pool.map(algorithm, tqdm(numbers))


def single_process_loop(numbers: list[int], algorithm, n_processes: int = None) -> list[int]:
    return [algorithm(n) for n in tqdm(numbers)]
