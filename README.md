streamparser
============
Python library to parse [Apertium stream format](http://wiki.apertium.org/wiki/Apertium_stream_format), generating `LexicalUnit`s.

Usage
-----
### As a library
    >>> from streamparser import parse

    >>> lexicalUnits = parse('\[\]\^\$[^ignoreme/yesreally$]^a\/s/a\/s<n><nt>$^vino/vino<n><m><sg>/venir<vblex><ifi><p3><sg>$.eefe^dímelo/decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><nt>/decir<vblex><imp><p2><sg>+me<prn><enc><p1><mf><sg>+lo<prn><enc><p3><m><sg>$')
    >>> for lexicalUnit in lexicalUnits:
            print('%s → %s' % (lexicalUnit.wordform, lexicalUnit.readings))

    a/s → [[Reading(baseform='a/s', tags={'nt', 'n'})]]
    vino → [[Reading(baseform='vino', tags={'sg', 'n', 'm'})], [Reading(baseform='venir', tags={'p3', 'sg', 'vblex', 'ifi'})]]
    dímelo → [[Reading(baseform='decir', tags={'sg', 'vblex', 'p2', 'imp'}), Reading(baseform='+me', tags={'p1', 'mf', 'prn', 'enc', 'sg'}), Reading(baseform='+lo', tags={'nt', 'prn', 'enc', 'p3'})], [Reading(baseform='decir', tags={'sg', 'vblex', 'p2', 'imp'}), Reading(baseform='+me', tags={'p1', 'mf', 'prn', 'enc', 'sg'}), Reading(baseform='+lo', tags={'m', 'sg', 'prn', 'enc', 'p3'})]]

### From the terminal
#### With standard input
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
#### With a file
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
  
