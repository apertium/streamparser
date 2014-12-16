streamparser
============
Python library to parse [Apertium stream format](http://wiki.apertium.org/wiki/Apertium_stream_format), generating `LexicalUnit`s.

Usage
-----
### As a library
#### With string input
```python
>>> from streamparser import parse

>>> lexicalUnits = parse('^hypercholesterolemia/*hypercholesterolemia$\[\]\^\$[^ignoreme/yesreally$]^a\/s/a\/s<n><nt>$^vino/vino<n><m><sg>/venir<vblex><ifi><p3><sg>$.eefe^dímelo/decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><nt>/decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><m><sg>$')
>>> for lexicalUnit in lexicalUnits:
        print('%s (%s) → %s' % (lexicalUnit.wordform, lexicalUnit.knownness, lexicalUnit.readings))

hypercholesterolemia (Knownness.unknown) → []
a/s (Knownness.known) → [[Reading(baseform='a/s', tags={'n', 'nt'})]]
vino (Knownness.known) → [[Reading(baseform='vino', tags={'n', 'm', 'sg'})], [Reading(baseform='venir', tags={'ifi', 'vblex', 'p3', 'sg'})]]
dímelo (Knownness.known) → [[Reading(baseform='decir', tags={'vblex', 'imp', 'p2', 'sg'}), Reading(baseform='+me', tags={'p1', 'mf', 'enc', 'sg', 'prn'}), Reading(baseform='+lo', tags={'p3', 'enc', 'nt', 'prn'})], [Reading(baseform='decir', tags={'vblex', 'imp', 'p2', 'sg'}), Reading(baseform='+me', tags={'p1', 'mf', 'enc', 'sg', 'prn'}), Reading(baseform='+lo', tags={'p3', 'enc', 'm', 'prn', 'sg'})]]
```

#### With file input
```python
>>> from streamparser import parse_file

>>> lexicalUnits = parse_file(open('~/Downloads/analyzed.txt'))
>>> for lexicalUnit in lexicalUnits:
        print('%s (%s) → %s' % (lexicalUnit.wordform, lexicalUnit.knownness, lexicalUnit.readings))

Høgre (Knownness.known) → [[Reading(baseform='Høgre', tags={'np'})], [Reading(baseform='høgre', tags={'n', 'nt', 'sp'})], [Reading(baseform='høg', tags={'un', 'sint', 'sp', 'comp', 'adj'})], [Reading(baseform='høgre', tags={'f', 'n', 'ind', 'sg'})], [Reading(baseform='høgre', tags={'f', 'n', 'ind', 'sg'})], [Reading(baseform='høgre', tags={'sg', 'nt', 'ind', 'posi', 'adj'})], [Reading(baseform='høgre', tags={'mf', 'sg', 'ind', 'posi', 'adj'})], [Reading(baseform='høgre', tags={'un', 'ind', 'pl', 'posi', 'adj'})], [Reading(baseform='høgre', tags={'un', 'def', 'sp', 'posi', 'adj'})]]
kolonne (Knownness.known) → [[Reading(baseform='kolonne', tags={'m', 'n', 'ind', 'sg'})], [Reading(baseform='kolonne', tags={'m', 'n', 'ind', 'sg'})]]
Grunnprinsipp (Knownness.known) → [[Reading(baseform='grunnprinsipp', tags={'n', 'nt', 'ind', 'sg'})], [Reading(baseform='grunnprinsipp', tags={'n', 'nt', 'pl', 'ind'})], [Reading(baseform='grunnprinsipp', tags={'n', 'nt', 'ind', 'sg'})], [Reading(baseform='grunnprinsipp', tags={'n', 'nt', 'pl', 'ind'})]]
7 (Knownness.known) → [[Reading(baseform='7', tags={'qnt', 'pl', 'det'})]]
px (Knownness.unknown) → []
```

### From the terminal
#### With standard input
```bash
$ bzcat ~/corpora/nnclean2.txt.bz2 | apertium-deshtml | lt-proc -we /usr/share/apertium/apertium-nno/nno.automorf.bin | python3 streamparser.py
[[Reading(baseform='Høgre', tags={'np'})],
 [Reading(baseform='høgre', tags={'n', 'sp', 'nt'})],
 [Reading(baseform='høg', tags={'un', 'sp', 'adj', 'comp', 'sint'})],
 [Reading(baseform='høgre', tags={'n', 'f', 'ind', 'sg'})],
 [Reading(baseform='høgre', tags={'n', 'f', 'ind', 'sg'})],
 [Reading(baseform='høgre', tags={'posi', 'ind', 'adj', 'nt', 'sg'})],
 [Reading(baseform='høgre', tags={'posi', 'ind', 'adj', 'mf', 'sg'})],
 [Reading(baseform='høgre', tags={'posi', 'ind', 'adj', 'un', 'pl'})],
 [Reading(baseform='høgre', tags={'posi', 'def', 'sp', 'adj', 'un'})]]
[[Reading(baseform='kolonne', tags={'n', 'm', 'ind', 'sg'})],
 [Reading(baseform='kolonne', tags={'n', 'm', 'ind', 'sg'})]]
...
```

#### With file input
```bash
$ bzcat ~/corpora/nnclean2.txt.bz2 | apertium-deshtml | lt-proc -we /usr/share/apertium/apertium-nno/nno.automorf.bin > analyzed.txt
$ python3 streamparser.py analyzed.txt
[[Reading(baseform='Høgre', tags={'np'})],
 [Reading(baseform='høgre', tags={'n', 'sp', 'nt'})],
 [Reading(baseform='høg', tags={'un', 'sp', 'adj', 'comp', 'sint'})],
 [Reading(baseform='høgre', tags={'n', 'f', 'ind', 'sg'})],
 [Reading(baseform='høgre', tags={'n', 'f', 'ind', 'sg'})],
 [Reading(baseform='høgre', tags={'posi', 'ind', 'adj', 'nt', 'sg'})],
 [Reading(baseform='høgre', tags={'posi', 'ind', 'adj', 'mf', 'sg'})],
 [Reading(baseform='høgre', tags={'posi', 'ind', 'adj', 'un', 'pl'})],
 [Reading(baseform='høgre', tags={'posi', 'def', 'sp', 'adj', 'un'})]]
[[Reading(baseform='kolonne', tags={'n', 'm', 'ind', 'sg'})],
 [Reading(baseform='kolonne', tags={'n', 'm', 'ind', 'sg'})]]
...
```
