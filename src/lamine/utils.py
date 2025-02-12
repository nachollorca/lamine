"""Contains utility clases and functions for the core modules."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable


def run_in_parallel(function: Callable, params_list: list[dict[str, Any]], max_workers: int = 10) -> list[Any]:
    """
    Executes a batch of calls of a function with different parameters in parallel using threading.

    Args:
        function (Callable): The function to be executed for each set of parameters.
        params_list (List[Dict[str, Any]]): A list of dictionaries, where each dictionary contains
            the keyword arguments for one call to `func`.
        max_threads (int): The maximum number of threads to use in the thread pool.

    Returns:
        List[Any]: A list containing the results of each function call, in the same order as the input parameters.

    Examples:
        >>> def add(a, b):
        ...     return a + b

        >>> params_list = [
        ...     {"a": 1, "b": 2},
        ...     {"a": 10, "b": 20},
        ...     {"a": 100, "b": 200}
        ... ]

        >>> run_in_parallel(add, params_list)
        [3, 30, 300]
    """
    results = [None] * len(params_list)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures_to_indices = {executor.submit(function, **params): index for index, params in enumerate(params_list)}
        for future in as_completed(futures_to_indices):
            index = futures_to_indices[future]
            results[index] = future.result()
    return results
