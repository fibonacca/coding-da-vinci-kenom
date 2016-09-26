#CdV Kenom Analyse

Analyse der Metadaten zu Münzen aus dem [Kenom Projekt](http://www.kenom.de), die im Rahmen von [Coding da Vinci](https://codingdavinci.de) Nord (2016) bereitstanden.


### Ausgangslage & Zielsetzung

Die Metadaten zu gut 25000 Münzen und Geldscheinen liegen als einzelne LIDO-Dateien vor. Die leicht verständlichen Felder sollen aus dem Format extrahiert werden, um sie in [einfachen Spielen](https://hackdash.org/projects/57dd5e93d9284f016c047460) zu nutzen.
Die Ideen reichen dabei von ja/nein-Entscheidungen auf einzelnen Datenfelden über Memory mit den zugehörigen Bilddaten zu einem Quartett.


### Extraktion interessanter Felder

Die 25000 LIDO Dateien im Ordner »lido« werden zunächst zu einer großen XML Datei zusammengefügt und schön formatiert, damit sie schneller bearbeitbar und besser betrachtbar sind.

Eine XSL-Transformation liest anschließend die interessanten Felder aus den Daten. Die Felder wurden dazu »nach Augenmaß« ermittelt.

Ca 300MB XML insgesamt.

xmllint benötigt knapp 1,5GB RAM für das Formatieren. Die Ein- und Ausgabedateien sind nicht Teil des Repositories.

saxon benötigt etwa 2GB RAM für die XSL Transformation, xsltproc knapp 2,5GB.