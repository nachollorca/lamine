from concurrent.futures import ThreadPoolExecutor, as_completed
from importlib import import_module
from time import time
from typing import Any, Callable

from .types import Answer, Message, Model


def get_answer(model: Model, conversation: list[Message], **kwargs) -> Answer:
    """
    Requests a response from a language model API for a single conversation.

    Args:
        model (Model): The language model to use for generating the response.
        conversation (list[Message]): A list of messages representing the conversation history.
        **kwargs: Additional keyword arguments like `temperature` or `top_p`.

    Returns:
        Answer: The response generated by the language model.
    """
    start = time()
    module = import_module(f"agilm.providers.{model.provider}")
    _get_answer = getattr(module, "get_answer")
    answer = _get_answer(model=model, conversation=conversation, **kwargs)
    answer.time = round(time() - start, 3)
    return answer


def _run_batch(
    function: Callable, params_list: list[dict[str, Any]], max_workers: int = 10
) -> list[Any]:
    """
    Executes a batch of calls of a function with different parameters in parallel using threading.

    Args:
        function (Callable): The function to be executed for each set of parameters.
        params_list (List[Dict[str, Any]]): A list of dictionaries, where each dictionary contains
            the keyword arguments for one call to `func`.
        max_threads (int): The maximum number of threads to use in the thread pool.

    Returns:
        List[Any]: A list containing the results of each function call, in the same order as the input parameters.
    """
    results = [None] * len(params_list)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures_to_indices = {
            executor.submit(function, **params): index
            for index, params in enumerate(params_list)
        }
        for future in as_completed(futures_to_indices):
            index = futures_to_indices[future]
            results[index] = future.result()
    return results


def get_answers(
    model: Model, conversations: list[list[Message]], **kwargs
) -> list[Answer]:
    """
    Request responses from a language model API for multiple conversations in parallel.

    Args:
        model (Model): The language model to use for generating the responses.
        conversations (list[list[Message]]): A list of conversations, where each conversation is a list of messages.
        **kwargs: Additional keyword arguments like `temperature` or `top_p`.

    Returns:
        list[Answer]: A list of responses generated by the language model for each conversation.
    """
    pass
