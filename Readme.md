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

Es bleiben 482 Münzen mit vollständigen Daten in der Datei [03-result.json](blob/master/03-result.json) übrig.

Es bleiben 9353 Münzen mit weniger Daten, die nur die Felder `back, front, owner, title, date, uri` enthalten – geeignet für das Memory Spiel – in der Datei [03-result-memory.json](blob/master/03-result-memory.json) übrig.

Die Auswertung in [03-result-feldstatistik.tsv](blob/master/03-result-feldstatistik.tsv) gibt Aufschluss darüber, welche Felder vermisst werden und wie die Lücken auf die verschiedenen Datenlieferanten verteilt sind.


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
