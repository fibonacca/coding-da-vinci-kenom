#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import re

tree = ET.parse('01-result.xml')

records = tree.findall('.//record')

for record in records:
	uri = record.findtext('uri')
	ownerID = re.sub('_kenom.*', '', re.sub('http://www.kenom.de/id/record_', '', uri))
	front = record.findtext('imageFrontPath')
	back = record.findtext('imageBackPath')
	
	if front != None and back != None:
		for magicnumber in range(1, 5):
			url = ('http://www.kenom.de/content/?' 
				+ 'action=image&width=300&height=300&resolution=72&rotate=0&'
				+ 'sourcepath=file:///opt/digiverso/kenom_viewer/data/'
				+ str(magicnumber)
				+ '/media/'
				+ front.replace('_media', ''))
			print('Fetching: ' + url)

print(imagepaths)