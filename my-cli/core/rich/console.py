from typing import Callable, Optional

from rich.console import Console
from rich import print as cli_print


console = Console()


def process_function_with_status(
    func: Callable,
    args: Optional[dict],
    loading_message: str,
    finished_messaged: Optional[str] = None,
):
    """
    Executes the given function with a loading message displayed in the console.

    Parameters:
        func (Callable): The function to be executed.
        args (Optional[dict]): The arguments to be passed to the function.
        loading_message (str): The loading message to be displayed.
        finished_messaged (Optional[str]): The optional message to be displayed after the function execution is finished.

    Returns:
        Any: The return value of the executed function.
    """

    with console.status(
        loading_message,
        spinner="aesthetic",
    ):
        return_data = func(**args) if args else func()

    if finished_messaged:
        cli_print(finished_messaged)

    return return_data
