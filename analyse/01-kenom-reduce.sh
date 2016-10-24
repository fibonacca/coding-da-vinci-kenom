#!/usr/bin/env sh
MERGED=01-merged.xml
RESULT=01-result.xml

# Zusammenfassen der einzelnen LIDO-Dateien in eine große XML Datei
# und Formatieren für bessere Menschenlesbarkeit.
( echo "<container>"; find lido -type f -print0 | xargs -0 cat | grep -v "<?xml"; echo "</container>" )\
    | xmllint --format -\
    > $MERGED

# Felder aus LIDO in ein flaches Dokument extrahieren.
saxon $MERGED 01-kenom-reduce.xsl > $RESULT
