#!/usr/bin/env python3
import json
import re

inputfilename = '05-api-output.json'
outputfilename = '05-magic-numbers.json'

inputfile = open(inputfilename)
data = json.load(inputfile)
inputfile.close()

print('Eingabeatei {0} enthält {1} Einträge.'.format(inputfilename, len(data)))
print()

results = {}
counts = {}

for record in data:
	recordId = re.findall(r'record_(.*)', record['id'])[0]
	fieldname = 'mediumimage'
	if fieldname in record:
		magicnumber = re.findall(r'.*kenom_viewer/data/(\d).*', record[fieldname])[0]
		results[recordId] = magicnumber
		if magicnumber not in counts:
			counts[magicnumber] = 0
		counts[magicnumber] += 1
	else:
		print('Datensatz {0} ohne Bild-URI im Feld {1}.'.format(recordId, fieldname))

print()
print('Schreibe {0} Zuordnungen in {1}'.format(len(results), outputfilename))
print()
print('Verteilung der magic numbers:')
print(counts)

with open(outputfilename, 'w') as f:
	json.dump(results, f, sort_keys=True, indent=4, separators=(',', ': '))
