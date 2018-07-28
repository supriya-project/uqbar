"""
Tools for string manipulation.
"""

import textwrap
import unidecode  # type: ignore
from typing import Generator


def delimit_words(string: str) -> Generator[str, None, None]:
    """
    Delimit a string at word boundaries.
    """
    # TODO: Reimplement this
    wordlike_characters = ('<', '>', '!')
    current_word = ''
    for i, character in enumerate(string):
        if (
            not character.isalpha() and
            not character.isdigit() and
            character not in wordlike_characters
            ):
            if current_word:
                yield current_word
                current_word = ''
        elif not current_word:
            current_word += character
        elif character.isupper():
            if current_word[-1].isupper():
                current_word += character
            else:
                yield current_word
                current_word = character
        elif character.islower():
            if current_word[-1].isalpha():
                current_word += character
            else:
                yield current_word
                current_word = character
        elif character.isdigit():
            if current_word[-1].isdigit():
                current_word += character
            else:
                yield current_word
                current_word = character
        elif character in wordlike_characters:
            if current_word[-1] in wordlike_characters:
                current_word += character
            else:
                yield current_word
                current_word = character
    if current_word:
        yield current_word


def normalize(string: str) -> str:
    """
    Normalizes whitespace.

    Strips leading and trailing blank lines, dedents, and removes trailing
    whitespace from the result.
    """
    string = string.replace('\t', '    ')
    lines = string.split('\n')
    while lines and (not lines[0] or lines[0].isspace()):
        lines.pop(0)
    while lines and (not lines[-1] or lines[-1].isspace()):
        lines.pop()
    for i, line in enumerate(lines):
        lines[i] = line.rstrip()
    string = '\n'.join(lines)
    string = textwrap.dedent(string)
    return string


def to_dash_case(string: str) -> str:
    """
    Convert a string to dash-delimited words.

    ::

        >>> import uqbar.strings
        >>> string = 'Tô Đặc Biệt Xe Lửa'
        >>> print(uqbar.strings.to_dash_case(string))
        to-dac-biet-xe-lua

    ::

        >>> string = 'alpha.beta.gamma'
        >>> print(uqbar.strings.to_dash_case(string))
        alpha-beta-gamma

    """
    string = unidecode.unidecode(string)
    words = (_.lower() for _ in delimit_words(string))
    string = '-'.join(words)
    return string


def to_snake_case(string: str) -> str:
    """
    Convert a string to underscore-delimited words.

    ::

        >>> import uqbar.strings
        >>> string = 'Tô Đặc Biệt Xe Lửa'
        >>> print(uqbar.strings.to_snake_case(string))
        to_dac_biet_xe_lua

    ::

        >>> string = 'alpha.beta.gamma'
        >>> print(uqbar.strings.to_snake_case(string))
        alpha_beta_gamma

    """
    string = unidecode.unidecode(string)
    words = (_.lower() for _ in delimit_words(string))
    string = '_'.join(words)
    return string
