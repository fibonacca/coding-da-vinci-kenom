#CdV Kenom Analyse

Analyse der Metadaten zu Münzen aus dem [Kenom Projekt](http://www.kenom.de), die im Rahmen von [Coding da Vinci](https://codingdavinci.de) Nord (2016) bereitstanden.


### Ausgangslage & Zielsetzung

Die Metadaten zu gut 25000 Münzen und Geldscheinen liegen als einzelne LIDO-Dateien vor. Die leicht verständlichen Felder sollen aus dem Format extrahiert werden, um sie in [einfachen Spielen](https://hackdash.org/projects/57dd5e93d9284f016c047460) zu nutzen.
Die Ideen reichen dabei von ja/nein-Entscheidungen auf einzelnen Datenfelden über Memory mit den zugehörigen Bilddaten zu einem Quartett.


### 01-kenom-reduce.sh: Extraktion interessanter Felder

Die 25000 LIDO Dateien im Ordner »lido« werden zunächst zu einer großen XML Datei zusammengefügt und schön formatiert, damit sie schneller bearbeitbar und besser betrachtbar sind.

Eine XSL-Transformation liest anschließend die interessanten Felder aus den Daten. Die Felder wurden dazu »nach Augenmaß« ermittelt.

Ca 300MB XML insgesamt.

xmllint benötigt knapp 1,5GB RAM für das Formatieren. Die Ein- und Ausgabedateien sind nicht Teil des Repositories.

saxon benötigt etwa 2GB RAM für die XSL Transformation, xsltproc knapp 2,5GB.


### Objekttypen

Es gibt Datensätze für vier Objektarten, davon gut 12500 Münzen.

```
╰─ grep "<type>" 01-result.xml | sort | uniq -c
3613     <type>Banknote</type>
3043     <type>Medaille</type>
12521     <type>Münze</type>
5678     <type>Münzfund</type>
```

### 03-analyse-to-json.py: Vollständige Datensätze finden und als JSON exportieren

Dieses Skript wandelt die XML Daten in das JSON Format um. Dabei werden nur die Datensätze behalten, für die alle Felder des Zielformats gefüllt werden können.

Es bleiben 482 Münzen mit vollständigen Daten in der Datei [03-result.json](blob/master/analyse/03-result.json) übrig.

Es bleiben 9353 Münzen mit weniger Daten, die nur die Felder `back, front, owner, title, date, uri` enthalten – geeignet für das Memory Spiel – in der Datei [03-result-memory.json](blob/master/analyse/03-result-memory.json) übrig.

Die Auswertung in [03-result-feldstatistik.tsv](blob/master/analyse/03-result-feldstatistik.tsv) gibt Aufschluss darüber, welche Felder vermisst werden und wie die Lücken auf die verschiedenen Datenlieferanten verteilt sind.

### 04-extract-years.py: Jahreszahlstatistik

Einen Eindruck bekommen, [wie die Münzen über die Jahrhunderte verteilt sind](blob/master/analyse/04-results-years.tsv): Es gibt nicht zu jedem Jahrhundert gleichviele Münzen und viele sehr alte.


### 05-extract-magic-numbers.py

Da die geplante IIIF Schnittstelle für Bilder noch nicht umgesetzt ist und die Bild URLs vom Format

```
http://www.kenom.de/content/?action=image&sourcepath=file:///opt/digiverso/kenom_viewer/data/3/media/record_DE-MUS-805518_kenom_47075/record_DE-MUS-805518_kenom_47075_vs.jpg&width=600&height=500&rotate=0&resolution=72&ignoreWatermark=true
```

eine nicht-konstante und nicht offensichtlich vorhersagbare »magic number« im Abschnitt »data/_3_/media« enthalten, führt dies zu gelegentlich nicht ladbaren Bildern (Probieren vermittelt auch den Eindruck, dass der Bild-Server irreführende Statuscodes – 200 und leere Antwort, wenn die magic number »falsch« ist – liefert und dass teilweise mehrere Zahlen ein Ergebnis liefern.)

Dieser Bearbeitungsschritt nutzt eine KENOM API, um Metadaten aus den Bild-URIs aller Datensätzen, die Suchergebnisse für das Wort Münze sind, die magic number zu extrahieren. Abruf, [Pretty-Printing](https://jmhodges.github.io/jsonpp/) und Speicherung der Daten erfolgte mit

```
curl "http://www.kenom.de/api?action=query&q=Münze" | jsonpp > 05-api-output.json
```

Das Ergebnis ist eine Map mit ID → magic number Zuordnung und die Zählung:

```
{'1': 5205, '2': 3028, '3': 4404}
```


### 06-merge-data.py

Führt die Daten aus den Schritten 3 und 5 zusammen und reduziert die Größe der Ausgabedatei.

Das JSON der Ergebnisdatei ist nun knapp 3&nbsp;MB groß. Mit gzip Komprimierung schrumpft sie auf knapp 120&nbsp;KB.


### Weitere Schritte und Ideen

* Extrahierte GND URLs für Orte auflösen und Koordinaten extrahieren
* Prüfen, ob sich die Masse nicht für etliche Münzen noch extrahieren lässt. Sie scheint teilweise im Freitext aber nicht als Daten abgelegt zu sein. Z.B. record_DE-MUS-059418_kenom_163474.xml

        <lido:objectMeasurementsWrap>
          <lido:objectMeasurementsSet>
            <lido:displayObjectMeasurements>Durchmesser: ca, 18,5 mm
          Gewicht: 0,415 g</lido:displayObjectMeasurements>
            <lido:objectMeasurements>
              <lido:measurementsSet>
                <lido:measurementType xml:lang="en">weight</lido:measurementType>
                <lido:measurementType>Gewicht</lido:measurementType>
                <lido:measurementUnit>g</lido:measurementUnit>
                <lido:measurementValue>0.415</lido:measurementValue>
              </lido:measurementsSet>
            </lido:objectMeasurements>
          </lido:objectMeasurementsSet>
        </lido:objectMeasurementsWrap>
