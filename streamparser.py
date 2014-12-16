#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Usage: streamparser.py [FILE]

Consumes input from a file (first argument) or stdin, parsing and pretty printing the readings of lexical units found.
"""

import re, pprint, sys, itertools, fileinput
from enum import Enum
from collections import namedtuple


Knownness = Enum('Knownness', 'known unknown biunknown genunknown')
Knownness.__doc__ = """Level of knowledge associated with a lexical unit.
    Values:
        known
        unknown: Denoted by '*', analysis not available.
        biunknown: Denoted by '@', translation not available.
        genunknown: Denoted by '#', generated form not available.
"""


Reading = namedtuple('Reading', ['baseform', 'tags'])
Reading.__doc__ = """A single analysis of a token.
    Fields:
        baseform (str): The base form (lemma, lexical form, citation form) of the reading.
        tags (set of str): The morphological tags associated with the reading.
"""


class LexicalUnit:
    """A lexical unit consisting of a lemma and its readings.

    Attributes:
        lexicalUnit (str): The lexical unit in Apertium stream format.
        wordform (str): The word form (surface form) of the lexical unit.
        readings (list of list of Reading): The analyses of the lexical unit with sublists containing all subreadings.
        knownness (Knownness): The level of knowledge of the lexical unit.
    """

    def __init__(self, lexicalUnit):
        self.lexicalUnit = lexicalUnit

        cohort = re.split(r'(?<!\\)/', lexicalUnit)
        self.wordform = cohort[0].replace(r'\/', '/')
        readings = cohort[1:]

        self.readings = []
        for reading in readings:
            reading = reading.replace(r'\/', '/')
            if readings[0][0] not in '*#@':
                self.knownness = Knownness.known
                subreadings = []

                subreadingParts = re.findall(r'([^<]+)((?:<[^>]+>)+)', reading)
                for subreading in subreadingParts:
                    baseform = subreading[0]
                    tags = set(re.findall(r'<([^>]+)>', subreading[1]))

                    subreadings.append(Reading(baseform=baseform, tags=tags))

                self.readings.append(subreadings)
            else:
                self.knownness = {'*': Knownness.unknown, '@': Knownness.biunknown, '#': Knownness.genunknown}[readings[0][0]]

    def __repr__(self):
        return self.lexicalUnit


def parse(stream):
    """Generates lexical units from a character stream.

    Args:
        stream (iterable): A character stream containing lexical units, superblanks and other text.

    Yields:
        LexicalUnit: The next lexical unit found in the character stream.
    """

    buffer = ''
    inLexicalUnit = False
    inSuperblank = False
    escaping = False

    for char in stream:
        if char == '\\' and not inLexicalUnit:
            escaping = True
            continue

        if inSuperblank:
            if char == ']' and not escaping:
                inSuperblank = False
        elif inLexicalUnit:
            if char == '$' and not escaping:
                yield LexicalUnit(buffer)
                buffer = ''
                inLexicalUnit = False
            else:
                buffer += char
        else:
            if char == '[' and not escaping:
                inSuperblank = True
            elif char == '^' and not escaping:
                inLexicalUnit = True

        escaping = False


def parse_file(f):
    """Generates lexical units from a file.

    Args:
        f (file): A file containing lexical units, superblanks and other text.

    Yields:
        LexicalUnit: The next lexical unit found in the file.
    """

    return parse(itertools.chain.from_iterable(f))


if __name__ == '__main__':
    lexicalUnits = parse_file(fileinput.input())

    for lexicalUnit in lexicalUnits:
        pprint.pprint(lexicalUnit.readings, width=120)
