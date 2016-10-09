#!/usr/bin/env python3
import re
import json
import xml.etree.ElementTree as ET
import functools
import math

tree = ET.parse('01-result.xml')
root = tree.getroot()
recordStatistics = {}
missing = {}

def extractLocation(element):
	return element[0].text

def checkField(element, fieldName):
	field = element.find(fieldName)
	
	uri = element.findtext('uri')
	ownerID = re.sub('_kenom.*', '', re.sub('http://www.kenom.de/id/record_', '', uri))
	owner = ownerID + ' ' + element.findtext('recordOwner')
	if not owner in recordStatistics:
		recordStatistics[owner] = {'complete': 0}
	if not fieldName in recordStatistics[owner]:
		recordStatistics[owner][fieldName] = 0
	
	valueToAdd = 1

	typ = element.findtext(fieldName)
	if fieldName == 'type' and typ != 'Münze':
		valueToAdd = 0
		print('falscher Typ: ' + str(element.findtext(fieldName)))
	elif fieldName == 'complete':
		"""Sonderbehandlung für nicht existierendes 'complete' Feld, der reine Aufruf zählt einen hoch"""
		print('Vollständig')
	elif field is None:
		valueToAdd = 0
		print('fehldendes Feld: ' + fieldName)
	
	recordStatistics[owner][fieldName] = recordStatistics[owner][fieldName] + valueToAdd
		
	return valueToAdd == 1


def isXmlRecordComplete(element):
	"""Auf Relevanz prüfen und falls nicht relevant Prüfung abbrechen"""
	result = True
	result &= checkField(element, 'uri')
	result &= checkField(element, 'recordOwner')
	result &= checkField(element, 'type')
	
	if not result:
		return False
	
	"""Überprüfen mit Einfluß auf das Ergebnis"""
	result &= checkField(element, 'title')
	result &= checkField(element, 'earliestDate')
	result &= checkField(element, 'material')
	result &= checkField(element, 'diameter')
	result &= checkField(element, 'weight')
	result &= checkField(element, 'location')
	result &= checkField(element, 'imageFrontPath')
	result &= checkField(element, 'imageBackPath')
	
	if result:
		checkField(element, 'complete')
	
	"""Überprüfen ohne Einfluß auf das Ergebnis"""
	checkField(element, 'orientation')
	
	return result

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
		record['front'] = xmlRecord.findtext('imageFrontPath')
		record['back'] = xmlRecord.findtext('imageBackPath')
		record['owner'] = xmlRecord.findtext('recordOwner')

		records += [record]
		print(json.dumps(record, sort_keys=True, indent=4, separators=(',', ': ')))
		

def printRecordStatistics(stats):
	fields = ['uri', 'type', 'title', 'earliestDate', 'material', 'diameter', 'weight', 'orientation', 'location', 'imageFrontPath', 'imageBackPath', 'recordOwner']
	
	print('\t'.join(['owner'] + fields + ['complete', '%']))
	
	for owner in sorted(stats):
		row = stats[owner]
		values = []
		coinCount = row['type']
		for field in fields:
			value = 0
			if field in row:
				value = row[field]
			values += [str(value)]
		
		complete = row['complete']
		values = [owner] + values + [str(complete), str(math.floor(100 * complete / max(coinCount, 1)))]
		print('\t'.join(values))

print()
print()
print("Anzahl der erfolgreich überführten Records")
print(len(records))
print("")
print("Feldstatistik:")
printRecordStatistics(recordStatistics)


with open('03-result.json', 'w') as f:
	json.dump(records, f, sort_keys=True, indent=4, separators=(',', ': '))
