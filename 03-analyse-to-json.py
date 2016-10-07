#!/usr/bin/env python3
import re
import json
import xml.etree.ElementTree as ET

tree = ET.parse('02-result.xml')
root = tree.getroot()
recordStatistics = {}
missing = {}

def extractLocation(element):
	return element[0].text

def checkField(element, fieldName):
	field = element.find(fieldName)
	
	uri = element.findtext('uri')
	owner = element.findtext('record-owner') + ' ' + re.sub('_kenom.*', '', re.sub('http://www.kenom.de/id/record_', '', uri))
	if not owner in recordStatistics:
		recordStatistics[owner] = {}
	if not fieldName in recordStatistics[owner]:
		recordStatistics[owner][fieldName] = 0
	recordStatistics[owner][fieldName] = recordStatistics[owner][fieldName] + 1
	
	if field is None:
		print("Feld " + fieldName + " fehlt")
		if fieldName in missing:
			missing[fieldName] = missing[fieldName] + 1
		else:
			missing[fieldName] = 1
		return False
	return True


def isXmlRecordComplete(element):
	"""Überprüfen ohne Scheitern."""
	checkField(element, 'orientation')
	
	"""Restliche Felder überprüfen und ggf Scheiterungsgrund sein."""
	return checkField(element, 'uri') and checkField(element, 'title') and checkField(element, 'earliestDate') and checkField(element, 'material') and checkField(element, 'diameter') and checkField(element, 'weight') and checkField(element, 'location') and checkField(element, 'image-front-path') and checkField(element, 'image-back-path') and checkField(element, 'record-owner')


records = []

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
		record['owner'] = xmlRecord.findtext('record-owner')

		records += [record]
		print(json.dumps(record, sort_keys=True, indent=4, separators=(',', ': ')))
		

def printRecordStatistics(stats):
	fields = ['uri', 'title', 'earliestDate', 'material', 'diameter', 'weight', 'orientation', 'location', 'image-front-path', 'image-back-path', 'record-owner']
	
	print('\t'.join(['owner'] + fields))
	
	for owner in stats:
		row = stats[owner]
		values = [owner]
		for field in fields:
			if field in row:
				values += [str(row[field])]
			else:
				values += ['0']

		print('\t'.join(values))

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
print("")
print("Feldstatistik:")
printRecordStatistics(recordStatistics)


with open('03-result.json', 'w') as f:
	json.dump(records, f, sort_keys=True, indent=4, separators=(',', ': '))
