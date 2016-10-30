#!/usr/bin/env python3
import json
import re

memoryfilename = '03-result-memory.json'
magicnumberfilename = '05-magic-numbers.json'
outputfilename = '06-result-memory.json'

inputfile = open(memoryfilename)
memorydata = json.load(inputfile)
inputfile.close()
print('Eingabeatei {0} enthält {1} Einträge.'.format(memoryfilename, len(memorydata)))

inputfile = open(magicnumberfilename)
magicnumberdata = json.load(inputfile)
inputfile.close()
print('Eingabeatei {0} enthält {1} Einträge.'.format(magicnumberfilename, len(magicnumberdata)))

results = []

for record in memorydata:
	'''ID aus Bild-URI extrahieren'''
	recordId = recordId = re.findall(r'record_(.*)_media.*', record['back'])[0]

	if recordId in magicnumberdata:
		results.append({
			'id': recordId,
			'uri': record['uri'],
			'title': record['title'],
			'year': record['date'],
			'magic': magicnumberdata[recordId],
			'owner': record['owner']
		})
	else:
		print('Keine magic number für ID {0} bekannt. Datensatz verwerfen.'.format(recordId))


print('Schreibe {0} Einträge in {1}'.format(len(results), outputfilename))

with open(outputfilename, 'w') as f:
	json.dump(results, f, sort_keys=True, indent=4, separators=(',', ': '))
