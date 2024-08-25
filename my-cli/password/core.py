import string
import secrets
from typing import Optional

from .errors import InvalidPasswordLengthException, InvalidPasswordOptionsException

LOWERCASE_LETTERS = string.ascii_lowercase
UPPERCASE_LETTERS = string.ascii_uppercase
DIGITS = string.digits
SAFE_PUNCTUATION = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"


def shuffle_string(string: str) -> str:
    """
    Shuffles the characters in the given string and returns the shuffled string.

    Args:
        string (str): The input string to be shuffled.

    Returns:
        str: The shuffled string.

    """
    string_list = list(string)
    secrets.SystemRandom().shuffle(string_list)
    return "".join(string_list)


def generate_random_letters(
    length: int,
    with_lowercase: Optional[bool] = True,
    with_uppercase: Optional[bool] = True,
) -> str:
    """
    Generate a random string of letters.

    Args:
        length (int): The length of the random string.
        with_lowercase (bool, optional): Whether to include lowercase letters. Defaults to True.
        with_uppercase (bool, optional): Whether to include uppercase letters. Defaults to True.

    Returns:
        str: The generated random string of letters.
    """
    half_length = length // 2

    # Generate letters
    if with_lowercase and with_uppercase:
        lower_case = "".join(
            secrets.choice(LOWERCASE_LETTERS) for _ in range(half_length)
        )
        upper_case = "".join(
            secrets.choice(UPPERCASE_LETTERS) for _ in range(length - half_length)
        )
        random_string = lower_case + upper_case

    elif with_lowercase:
        random_string = "".join(
            secrets.choice(LOWERCASE_LETTERS) for _ in range(length)
        )

    elif with_uppercase:
        random_string = "".join(
            secrets.choice(UPPERCASE_LETTERS) for _ in range(length)
        )

    return shuffle_string(random_string)


def replace_random_characters(
    original_string: str,
    replacement_choices: str,
    replace_first_character: bool = False,
    exclusion_indexes: set[int] = None,
) -> tuple[str, set[int]]:
    """
    Replaces random characters in the original string with characters from the replacement choices.

    Args:
        original_string (str): The original string to modify.
        replacement_choices (str): The characters to choose from for replacement.
        replace_first_character (bool, optional): Whether to replace the first character or not. Defaults to False.
        exclusion_indexes (set[int], optional): Set of indexes to exclude from replacement. Defaults to None.

    Returns:
        tuple[str, set[int]]: A tuple containing the modified string and the set of indexes that were replaced.
    """

    length = len(original_string)
    half_length = length // 2
    indexes = (
        list(range(0, length)) if replace_first_character else list(range(1, length))
    )

    # Find reasonable replacement length
    replacement_length = min(half_length // 3, 7)
    if length < 10 or replacement_length < 2:
        replacement_length = 2

    # Find possible indexes for replacement
    possible_indexes = list(
        set(indexes).difference(exclusion_indexes)
        if exclusion_indexes
        else set(indexes)
    )
    replacement_indexes = {
        secrets.choice(possible_indexes) for _ in range(replacement_length)
    }

    # Replace characters randomly
    original_string = list(original_string)
    for index in replacement_indexes:
        original_string[index] = secrets.choice(replacement_choices)

    original_string = "".join(original_string)

    return original_string, replacement_indexes


def generate_safe_token(length: Optional[int] = 14) -> str:
    return secrets.token_urlsafe(length)


def generate_password(
    length: Optional[int] = 14,
    with_number: Optional[bool] = True,
    with_lowercase: Optional[bool] = True,
    with_uppercase: Optional[bool] = True,
    with_special: Optional[bool] = True,
) -> str:
    # Ensure at least there are letters
    if not with_lowercase and not with_uppercase:
        raise InvalidPasswordOptionsException()

    options = {
        "with_number": with_number,
        "with_lowercase": with_lowercase,
        "with_uppercase": with_uppercase,
        "with_special": with_special,
    }

    # Ensure valid password length
    if length < 5:
        raise InvalidPasswordLengthException()

    if sum(options.values()) > 2 and length < 10:
        chosen_options = list(filter(lambda key: options[key], options.keys()))
        raise InvalidPasswordLengthException(
            message=f"Password length is too short for the chosen options: {chosen_options}"
        )

    # Generate letters
    password = generate_random_letters(
        length=length,
        with_lowercase=with_lowercase,
        with_uppercase=with_uppercase,
    )

    # Generate numbers
    digits_indexes = None
    if with_number:
        password, digits_indexes = replace_random_characters(
            original_string=password,
            replacement_choices=DIGITS,
        )

    # Generate special characters
    if with_special:
        password, _ = replace_random_characters(
            original_string=password,
            replacement_choices=SAFE_PUNCTUATION,
            exclusion_indexes=digits_indexes,
        )

    return password
