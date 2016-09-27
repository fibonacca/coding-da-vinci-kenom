#!/usr/bin/env python3
from __future__ import with_statement

import json

import xml.etree.ElementTree as ET

tree = ET.parse('02-result.xml')
root = tree.getroot()
missing = {}

def extractLocation(element):
	return element[0].text

def checkField(element, fieldName):
	field = element.find(fieldName)
	if field is None:
		print("Feld " + fieldName + " fehlt")
		if fieldName in missing:
			missing[fieldName] = missing[fieldName] + 1
		else:
			missing[fieldName] = 1
		return False
	return True


def isXmlRecordComplete(element):
	return checkField(element, 'title') and checkField(element, 'earliestDate') and checkField(element, 'material') and checkField(element, 'diameter') and checkField(element, 'weight') and checkField(element, 'location') and checkField(element, 'image-front-path') and checkField(element, 'image-back-path')


	return isComplete

records = [];
for xmlRecord in root:
	record = {}
	print("")
	print("---")
	record['uri'] = xmlRecord.find('uri').text
	print(record['uri'])
	
	if not isXmlRecordComplete(xmlRecord):
		print("UNVOLLSTÄNDIG")
	else:
		record['title'] = xmlRecord.findtext('title')
		record['date'] = xmlRecord.findtext('earliestDate')[0:4]
		record['material'] = xmlRecord.findtext('material') # evtl mehrere
		record['diameter'] = xmlRecord.findtext('diameter')
		record['weight'] = xmlRecord.findtext('weight')
		#record['orientation'] = xmlRecord.findtext('orientation')
		record['location'] = extractLocation(xmlRecord.findall('location'))
		record['front'] = xmlRecord.findtext('image-front-path')
		record['back'] = xmlRecord.findtext('image-back-path')
		if record['location'] != None:
			records += [record]
			print(json.dumps(record, sort_keys=True, indent=4, separators=(',', ': ')))
		else:
			print("Ohne Location")

print()
print()
print("Anzahl der erfolgreich überführten Records")
print(len(records))
print("")
print("Fehlende Felder:")
print(missing)
# Ergebnis: es fehlt sehr häufig etwas
# Anzahl der erfolgreich überführten Records
# 492
# Fehlende Felder:
# {'material': 12, 'weight': 11, 'image-back-path': 32, 'title': 30, 'location': 5145, 'diameter': 6787}

with open('03-result.json', 'w') as f:
	json.dump(records, f, sort_keys=True, indent=4, separators=(',', ': '))
