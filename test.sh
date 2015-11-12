#!/bin/bash

set -e -u

got=$(mktemp -t streamparser.XXXXXXXXXXX)
exp="$(dirname "$0")/test-expected"
trap 'rm -f "${got}"' EXIT

echo '[\^keep<escapes>\$] \^ \$ \/ \[ \] ^x\/y\^\$\<z\>å/A\$\^B<tag><tag2>/A\/S<tag>$' | python3 -c 'from streamparser import parse_file, readingToString
import sys
for blank, lu in parse_file(sys.stdin, withText=True):
    print("BLANK:"+blank+"\nLU:"+str(lu));print(lu.readings);print(lu.wordform)
' >"${got}"

diff -U0 "${got}" "${exp}"
