"""
Utilities for manipulating strings.
"""

import textwrap
import unicodedata


def delimit_words(string):
    wordlike_characters = ('<', '>', '!')
    current_word = ''
    for character in string:
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


def normalize(string):
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


def strip_diacritics(string):
    string = unicodedata.normalize('NFKD', string)
    string = string.encode('ascii', 'ignore')
    return string.decode()


def to_dash_case(string):
    string = strip_diacritics(string)
    words = delimit_words(string)
    words = (_.lower() for _ in words)
    string = '-'.join(words)
    return string


def to_snake_case(string):
    string = strip_diacritics(string)
    words = delimit_words(string)
    words = (_.lower() for _ in words)
    string = '_'.join(words)
    return string
