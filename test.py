#!/usr/bin/env python3
# coding=utf-8

import contextlib
import io
import tempfile
import unittest
import unittest.mock
import warnings

import streamparser
from streamparser import (
    parse, parse_file, SReading, known, unknown, mainpos,
    reading_to_string, subreading_to_string,
)


class Test(unittest.TestCase):
    s1 = r'[\^keep<escapes>\$] \^ \$ \/ \[ \] ^x\/y\^\$\<z\>å/A\$\^B<tag><tag2>/A\/S<tag><#1-\>2>$'
    s2 = '^hypercholesterolemia/*hypercholesterolemia$'
    s3 = '$^vino/vino<n><m><sg>/venir<vblex><ifi><p3><sg>$'
    s4 = '^dímelo/decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><nt>/decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><m><sg>$'

    def test_parse(self):
        lexical_units = list(parse(self.s1))
        self.assertEqual(len(lexical_units), 1)
        lexical_unit = lexical_units[0]
        self.assertEqual(str(lexical_unit), r'x\/y\^\$\<z\>å/A\$\^B<tag><tag2>/A\/S<tag><#1-\>2>')
        readings = lexical_unit.readings
        self.assertListEqual(readings, [[SReading(baseform='A\\$\\^B', tags=['tag', 'tag2'])], [SReading(baseform='A\\/S', tags=['tag', '#1-\\>2'])]])
        self.assertEqual(lexical_unit.wordform, r'x\/y\^\$\<z\>å')
        self.assertEqual(lexical_unit.knownness, known)

    def test_parse_with_text(self):
        lexical_units_with_blanks = list(parse(self.s1, with_text=True))
        self.assertEqual(len(lexical_units_with_blanks), 1)
        blank, _lexical_unit = lexical_units_with_blanks[0]
        self.assertEqual(blank, r'[\^keep<escapes>\$] \^ \$ \/ \[ \] ')

    def test_parse_unknown(self):
        lexical_units = list(parse(self.s2))
        self.assertEqual(len(lexical_units), 1)
        self.assertEqual(lexical_units[0].knownness, unknown)

    def test_parse_file(self):
        with tempfile.TemporaryFile(mode='w+') as fp:
            fp.write(self.s3)
            fp.seek(0)
            lexical_units = list(parse_file(fp))
            self.assertEqual(len(lexical_units), 1)
            self.assertEqual(lexical_units[0].wordform, 'vino')

    @unittest.mock.patch.object(streamparser, 'fileinput')
    def test_module(self, fileinput):
        fileinput.input = lambda: self.s3
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            streamparser.main()
            self.assertEqual(output.getvalue(), "[[SReading(baseform='vino', tags=['n', 'm', 'sg'])], [SReading(baseform='venir', tags=['vblex', 'ifi', 'p3', 'sg'])]]\n")

    def test_parse_subreadings(self):
        lexical_units = list(parse(self.s4))
        self.assertEqual(len(lexical_units), 1)
        self.assertListEqual(
            lexical_units[0].readings,
            [
                [
                    SReading(baseform='decir', tags=['vblex', 'imp', 'p2', 'sg']),
                    SReading(baseform='me', tags=['prn', 'enc', 'p1', 'mf', 'sg']),
                    SReading(baseform='lo', tags=['prn', 'enc', 'p3', 'nt']),
                ],
                [
                    SReading(baseform='decir', tags=['vblex', 'imp', 'p2', 'sg']),
                    SReading(baseform='me', tags=['prn', 'enc', 'p1', 'mf', 'sg']),
                    SReading(baseform='lo', tags=['prn', 'enc', 'p3', 'm', 'sg']),
                ],
            ],
        )

    def test_mainpos(self):
        lexical_units = list(parse(self.s4))
        self.assertEqual(len(lexical_units), 1)
        pos = mainpos(lexical_units[0].readings[0])
        self.assertEqual(pos, 'prn')

    def test_mainpos_ltr(self):
        lexical_units = list(parse(self.s4))
        self.assertEqual(len(lexical_units), 1)
        pos = mainpos(lexical_units[0].readings[0], ltr=True)
        self.assertEqual(pos, 'vblex')

    def test_reading_to_string(self):
        lexical_units = list(parse(self.s4))
        self.assertEqual(len(lexical_units), 1)
        self.assertEqual(reading_to_string(lexical_units[0].readings[0]), 'decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><nt>')

    def test_subreading_to_string(self):
        lexical_units = list(parse(self.s4))
        self.assertEqual(len(lexical_units), 1)
        self.assertEqual(subreading_to_string(lexical_units[0].readings[0][0]), 'decir<vblex><imp><p2><sg>')

    def test_empty_readings(self):
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter('always')
            next(parse('^foo/$'))
            self.assertEqual(len(caught_warnings), 1)
            self.assertTrue(issubclass(caught_warnings[0].category, RuntimeWarning))
            self.assertIn('Empty readings', str(caught_warnings[0].message))


if __name__ == '__main__':
    unittest.main()
