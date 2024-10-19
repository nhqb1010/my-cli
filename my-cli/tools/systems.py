import platform
import subprocess
from pathlib import Path

from tools.constants import OSName
from tools.errors import CopyToClipboardException, FolderCreationExistException


def get_os_name() -> str:
    """
    Returns the name of the operating system.

    Returns:
        str: The name of the operating system. Possible values are "Windows", "Linux", "MacOS", or "Unknown".
    """

    system = platform.system()

    if system == "Windows":
        return OSName.WINDOWS.value
    elif system == "Linux":
        return OSName.LINUX.value
    elif system == "Darwin":
        return OSName.MACOS.value
    else:
        return OSName.UNKNOWN.value


def copy_to_clipboard(password: str, raise_exception: bool = False) -> None:
    """
    Copies the given password to the clipboard.

    Args:
        password (str): The password to be copied.
        raise_exception (bool, optional): Whether to raise an exception if the operating system is not supported. Defaults to False.

    Raises:
        Exception: If the operating system is not supported.

    Returns:
        None
    """
    try:
        os_name = get_os_name()

        if os_name == OSName.WINDOWS.value:
            subprocess.run("clip", text=True, input=password)
        elif os_name == OSName.LINUX.value or os_name == OSName.MACOS.value:
            subprocess.run("pbcopy", text=True, input=password)
        else:
            raise CopyToClipboardException("Operating system not supported for copy.")

        return True
    except Exception as e:
        if raise_exception:
            raise e

        return False


def create_folder_from_root_folder(folder_path: str) -> None:
    """
    Creates a folder if it does not exist.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        None
    """
    root_folder = Path(__file__).parent.parent.parent
    path = root_folder / folder_path

    # If exist raise error
    if path.exists() or path.is_dir():
        raise FolderCreationExistException(f"Folder already exists at {path}")

    Path(folder_path).mkdir(parents=True)
