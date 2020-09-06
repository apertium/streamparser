#!/usr/bin/env python3
# coding=utf-8
"""
Usage: streamparser.py [FILE]

Consumes input from a file (first argument) or stdin, parsing and pretty printing the readings of lexical units found.
"""

__all__ = [
    'Knownness', 'known', 'unknown', 'biunknown', 'genunknown', 'LexicalUnit', 'SReading',
    'subreading_to_string', 'reading_to_string', 'mainpos', 'parse', 'parse_file',
]
__author__ = 'Sushain K. Cherivirala, Kevin Brubeck Unhammer'
__copyright__ = 'Copyright 2016--2018, Sushain K. Cherivirala, Kevin Brubeck Unhammer'
__credits__ = ['Sushain K. Cherivirala', 'Kevin Brubeck Unhammer']
__license__ = 'GPLv3+'
__status__ = 'Production'
__version__ = '5.0.2'

import fileinput
import functools
import itertools
import pprint
import re
import warnings
from collections import namedtuple

if False:
    from typing import Type, List, Tuple, Iterator, Iterable, Generator, Union  # noqa: F401


class Knownness:
    """Level of knowledge associated with a :class:`LexicalUnit`. \n
       Values: :class:`known`, :class:`unknown`, :class:`biunknown`, :class:`genunknown`
    """
    symbol = ''


class known(Knownness):  # noqa: N801
    pass


class unknown(Knownness):  # noqa: N801
    """Denoted by ``*``, analysis not available."""
    symbol = '*'


class biunknown(Knownness):  # noqa: N801
    """Denoted by ``@``, translation not available."""
    symbol = '@'


class genunknown(Knownness):  # noqa: N801
    """Denoted by ``#``, generated form not available."""
    symbol = '#'


def _symbol_to_knownness(symbol):  # type: (str) -> Type[Knownness]
    return {'*': unknown, '@': biunknown, '#': genunknown}.get(symbol, known)


SReading = namedtuple('SReading', ['baseform', 'tags'])
SReading.__doc__ = """A single subreading of an analysis of a token.

Attributes:
    baseform (str): The base form (lemma, lexical form, citation form) of the reading.
    tags (List[str]): The morphological tags associated with the reading.
"""


def subreading_to_string(sub):  # type: (SReading) -> str
    return sub.baseform + ''.join('<' + t + '>' for t in sub.tags)  # type: ignore


def reading_to_string(reading):  # type: (List[SReading]) -> str
    return '+'.join(subreading_to_string(sub) for sub in reading)


def mainpos(reading, ltr=False):  # type: (SReading, bool) -> str
    """Return the first part-of-speech tag of a reading. If there are
    several subreadings, by default give the first tag of the last
    subreading. If ltr=True, give the first tag of the first
    subreading, see
    http://beta.visl.sdu.dk/cg3/single/#sub-stream-apertium for more
    information.
    """
    if ltr:
        return reading[0].tags[0]  # type: ignore
    else:
        return reading[-1].tags[0]  # type: ignore


def _parse_tags(tag_str):  # type: (str) -> List[str]
    in_tag = False
    tags = []
    buf = ''
    stream = (c for c in tag_str)
    for c in stream:
        if not in_tag and c == '<':
            in_tag = True
            continue
        elif c == '\\':
            buf += c
            buf += next(stream)
        elif c == '>':
            tags.append(buf)
            buf = ''
            in_tag = False
        else:
            buf += c
    if buf != '':
        tags.append(buf)
    return tags


def _parse_subreading(reading):  # type: (str) -> List[Tuple[str, str]]
    in_lemma = True
    lemma = ''
    subs = []
    buf = ''
    stream = (c for c in reading)
    for c in stream:
        if c == '+':
            subs.append((lemma, buf))
            buf = ''
            lemma = ''
            in_lemma = True
            continue
        elif c == '\\':
            buf += c
            buf += next(stream)
        elif in_lemma and c == '<':
            in_lemma = False
            lemma = buf
            buf = ''
            buf += c
        else:
            buf += c
    if buf != '':
        if in_lemma:
            subs.append((lemma + buf, ''))
        else:
            subs.append((lemma, buf))
    return subs


class LexicalUnit:
    """A lexical unit consisting of a lemma and its readings.

    Attributes:
        lexical_unit (str): The lexical unit in Apertium stream format.
        wordform (str): The word form (surface form) of the lexical unit.
        wordbound_blank (str): The wordbound blank of the lexical unit.
        readings (List[List[:class:`SReading`]]): The analyses of the lexical unit with sublists containing all subreadings.
        knownness (:class:`Knownness`): The level of knowledge of the lexical unit.
    """

    def __init__(self, lexical_unit):  # type: (str) -> None
        self.lexical_unit = lexical_unit

        cohort = re.split(r'(?<!\\)/', lexical_unit)

        if "]]^" in cohort[0]:
            split_form = cohort[0].split("]]^")
            self.wordbound_blank = split_form[0] + "]]"
            self.wordform = split_form[1]
        else:
            self.wordbound_blank = ""
            self.wordform = cohort[0]

        readings = cohort[1:]

        if len(readings) == 1:
            self.knownness = _symbol_to_knownness(readings[0][:1])
        else:
            self.knownness = known

        self.readings = []  # type: List[List[SReading]]
        for reading in readings:
            if len(reading) < 1:
                warnings.warn('Empty readings for {}'.format(self.lexical_unit), RuntimeWarning)
            else:
                subreadings = []
                for subreading in _parse_subreading(reading):
                    baseform = subreading[0].lstrip('+')
                    tags = _parse_tags(subreading[1])
                    subreadings.append(SReading(baseform=baseform, tags=tags))

                self.readings.append(subreadings)

    def __repr__(self):  # type: () -> str
        return self.lexical_unit


@functools.singledispatch
def parse(stream, with_text=False):  # type: (Iterator[str], bool) -> Iterator[Union[Tuple[str, LexicalUnit], LexicalUnit]]
    """Generates lexical units from a character stream.

    Args:
        stream (Iterator[str]): A character stream containing lexical units, superblanks and other text.
        with_text (Optional[bool]): A boolean defining whether to output preceding text with each lexical unit.

    Yields:
        :class:`LexicalUnit`: The next lexical unit found in the character stream. (if `with_text` is False) \n
        *(str, LexicalUnit)* - The next lexical unit found in the character stream and the the text that seperated it from the
        prior unit in a tuple. (if with_text is True)
    """

    buffer = ''
    text_buffer = ''
    in_lexical_unit = False
    in_superblank = False

    for char in stream:
        if in_superblank:
            if char == ']':
                in_superblank = False
                text_buffer += char
            elif char == '\\':
                text_buffer += char
                text_buffer += next(stream)
            else:
                text_buffer += char
        elif in_lexical_unit:
            if char == '$':
                if with_text:
                    yield (text_buffer, LexicalUnit(buffer))
                else:
                    yield LexicalUnit(buffer)
                buffer = ''
                text_buffer = ''
                in_lexical_unit = False
            elif char == '\\':
                buffer += char
                buffer += next(stream)
            else:
                buffer += char
        else:
            if char == '[':
                next_char = next(stream)
                if next_char == '[':
                    buffer += "[[";
                    in_lexical_unit = True
                else:
                    in_superblank = True
                    text_buffer += char
                    if next_char == ']':
                        in_superblank = False
                        text_buffer += next_char
                    elif char == '\\':
                        text_buffer += next_char
                        text_buffer += next(stream)
                    else:
                        text_buffer += next_char
                
            elif char == '^':
                in_lexical_unit = True
            elif char == '\\':
                text_buffer += char
                text_buffer += next(stream)
            else:
                text_buffer += char


@parse.register(str)
def _parse_str(str, **kwargs):  # type: (str, dict) -> Iterator[Union[Tuple[str, LexicalUnit], LexicalUnit]]
    return parse(iter(str), **kwargs)


def parse_file(f, **kwargs):  # type: (Iterable, dict) -> Iterator[Union[Tuple[str, LexicalUnit], LexicalUnit]]
    """Generates lexical units from a file.

    Args:
        f (file): A file containing lexical units, superblanks and other text.

    Yields:
        :class:`LexicalUnit`: The next lexical unit found in the file.
    """

    return parse(itertools.chain.from_iterable(f), **kwargs)


def main():  # type: () -> None
    lexical_units = parse_file(fileinput.input())

    for lexical_unit in lexical_units:
        pprint.pprint(lexical_unit.readings, width=120)  # type: ignore


if __name__ == '__main__':
    main()

