# streamparser

Python library to parse [Apertium stream format](http://wiki.apertium.org/wiki/Apertium_stream_format), generating `LexicalUnit`s.

[![Build Status](https://travis-ci.org/apertium/streamparser.svg)](https://travis-ci.org/apertium/streamparser)
[![Coverage Status](https://coveralls.io/repos/github/apertium/streamparser/badge.svg?branch=master)](https://coveralls.io/github/apertium/streamparser?branch=master)

## Usage

### As a library

#### With string input

```python
>>> from streamparser import parse
>>> lexical_units = parse('^hypercholesterolemia/*hypercholesterolemia$\[\]\^\$[^ignoreme/yesreally$]^a\/s/a\/s<n><nt>$^vino/vino<n><m><sg>/venir<vblex><ifi><p3><sg>$.eefe^dímelo/decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><nt>/decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><m><sg>$')
>>> for lexical_unit in lexical_units:
        print('%s (%s) → %s' % (lexical_unit.wordform, lexical_unit.knownness, lexical_unit.readings))
```

    hypercholesterolemia (<class 'streamparser.unknown'>) → [[SReading(baseform='*hypercholesterolemia', tags=[])]]
    a\/s (<class 'streamparser.known'>) → [[SReading(baseform='a\\/s', tags=['n', 'nt'])]]
    vino (<class 'streamparser.known'>) → [[SReading(baseform='vino', tags=['n', 'm', 'sg'])], [SReading(baseform='venir', tags=['vblex', 'ifi', 'p3', 'sg'])]]
    dímelo (<class 'streamparser.known'>) → [[SReading(baseform='decir', tags=['vblex', 'imp', 'p2', 'sg']), SReading(baseform='me', tags=['prn', 'enc', 'p1', 'mf', 'sg']), SReading(baseform='lo', tags=['prn', 'enc', 'p3', 'nt'])], [SReading(baseform='decir', tags=['vblex', 'imp', 'p2', 'sg']), SReading(baseform='me', tags=['prn', 'enc', 'p1', 'mf', 'sg']), SReading(baseform='lo', tags=['prn', 'enc', 'p3', 'm', 'sg'])]]

#### With file input

```python
>>> from streamparser import parse_file
>>> lexical_units = parse_file(open('~/Downloads/analyzed.txt'))
>>> for lexical_unit in lexical_units:
        print('%s (%s) → %s' % (lexical_unit.wordform, lexical_unit.knownness, lexical_unit.readings))
```

    Høgre (<class 'streamparser.known'>) → [[SReading(baseform='Høgre', tags=['np'])], [SReading(baseform='høgre', tags=['n', 'nt', 'sp'])], [SReading(baseform='høg', tags=['un', 'sint', 'sp', 'comp', 'adj'])], [SReading(baseform='høgre', tags=['f', 'n', 'ind', 'sg'])], [SReading(baseform='høgre', tags=['f', 'n', 'ind', 'sg'])], [SReading(baseform='høgre', tags=['sg', 'nt', 'ind', 'posi', 'adj'])], [SReading(baseform='høgre', tags=['mf', 'sg', 'ind', 'posi', 'adj'])], [SReading(baseform='høgre', tags=['un', 'ind', 'pl', 'posi', 'adj'])], [SReading(baseform='høgre', tags=['un', 'def', 'sp', 'posi', 'adj'])]]
    kolonne (<class 'streamparser.known'>) → [[SReading(baseform='kolonne', tags=['m', 'n', 'ind', 'sg'])], [SReading(baseform='kolonne', tags=['m', 'n', 'ind', 'sg'])]]
    Grunnprinsipp (<class 'streamparser.known'>) → [[SReading(baseform='grunnprinsipp', tags=['n', 'nt', 'ind', 'sg'])], S[Reading(baseform='grunnprinsipp', tags=['n', 'nt', 'pl', 'ind'])], [SReading(baseform='grunnprinsipp', tags=['n', 'nt', 'ind', 'sg'])], [SReading(baseform='grunnprinsipp', tags=['n', 'nt', 'pl', 'ind'])]]
    7 (<class 'streamparser.known'>) → [[SReading(baseform='7', tags=['qnt', 'pl', 'det'])]]
    px (<class 'streamparser.unknown'>) → []

### From the terminal

#### With standard input

```bash
$ bzcat ~/corpora/nnclean2.txt.bz2 | apertium-deshtml | lt-proc -we /usr/share/apertium/apertium-nno/nno.automorf.bin | python3 streamparser.py
[[SReading(baseform='Høgre', tags=['np'])],
 [SReading(baseform='høgre', tags=['n', 'sp', 'nt'])],
 [SReading(baseform='høg', tags=['un', 'sp', 'adj', 'comp', 'sint'])],
 [SReading(baseform='høgre', tags=['n', 'f', 'ind', 'sg'])],
 [SReading(baseform='høgre', tags=['n', 'f', 'ind', 'sg'])],
 [SReading(baseform='høgre', tags=['posi', 'ind', 'adj', 'nt', 'sg'])],
 [SReading(baseform='høgre', tags=['posi', 'ind', 'adj', 'mf', 'sg'])],
 [SReading(baseform='høgre', tags=['posi', 'ind', 'adj', 'un', 'pl'])],
 [SReading(baseform='høgre', tags=['posi', 'def', 'sp', 'adj', 'un'])]]
[[SReading(baseform='kolonne', tags=['n', 'm', 'ind', 'sg'])],
 [SReading(baseform='kolonne', tags=['n', 'm', 'ind', 'sg'])]]
...
```

#### With file input in terminal

```bash
$ bzcat ~/corpora/nnclean2.txt.bz2 | apertium-deshtml | lt-proc -we /usr/share/apertium/apertium-nno/nno.automorf.bin > analyzed.txt
$ python3 streamparser.py analyzed.txt
[[SReading(baseform='Høgre', tags=['np'])],
 [SReading(baseform='høgre', tags=['n', 'sp', 'nt'])],
 [SReading(baseform='høg', tags=['un', 'sp', 'adj', 'comp', 'sint'])],
 [SReading(baseform='høgre', tags=['n', 'f', 'ind', 'sg'])],
 [SReading(baseform='høgre', tags=['n', 'f', 'ind', 'sg'])],
 [SReading(baseform='høgre', tags=['posi', 'ind', 'adj', 'nt', 'sg'])],
 [SReading(baseform='høgre', tags=['posi', 'ind', 'adj', 'mf', 'sg'])],
 [SReading(baseform='høgre', tags=['posi', 'ind', 'adj', 'un', 'pl'])],
 [SReading(baseform='høgre', tags=['posi', 'def', 'sp', 'adj', 'un'])]]
[[SReading(baseform='kolonne', tags=['n', 'm', 'ind', 'sg'])],
 [SReading(baseform='kolonne', tags=['n', 'm', 'ind', 'sg'])]]
...
```
