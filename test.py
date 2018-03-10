#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from streamparser import parse, SReading, known


class TestParse(unittest.TestCase):
    s = '[\^keep<escapes>\$] \^ \$ \/ \[ \] ^x\/y\^\$\<z\>å/A\$\^B<tag><tag2>/A\/S<tag><#1-\>2>$'

    def test_parse(self):
        lexical_units = list(parse(self.s))
        self.assertEqual(len(lexical_units), 1)
        lexical_unit = lexical_units[0]
        self.assertEqual(str(lexical_unit), 'x\/y\^\$\<z\>å/A\$\^B<tag><tag2>/A\/S<tag><#1-\>2>')
        readings = lexical_unit.readings
        self.assertListEqual(readings, [[SReading(baseform='A\\$\\^B', tags=['tag', 'tag2'])], [SReading(baseform='A\\/S', tags=['tag', '#1-\\>2'])]])
        self.assertEqual(lexical_unit.wordform, 'x\/y\^\$\<z\>å')
        self.assertEqual(lexical_unit.knownness, known)

    def test_parse_with_text(self):
        lexical_units_with_blanks = list(parse(self.s, with_text=True))
        self.assertEqual(len(lexical_units_with_blanks), 1)
        blank, _lexical_unit = lexical_units_with_blanks[0]
        self.assertEqual(blank, '[\^keep<escapes>\$] \^ \$ \/ \[ \] ')

    def test_parse_file(self):
        pass


if __name__ == '__main__':
    unittest.main()
