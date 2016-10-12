#!/usr/bin/env python3
import json

import re
import xml.etree.ElementTree as ET
import functools
import math
from enum import Enum

inputfile = open('03-result-memory.json')
data = json.load(inputfile)
inputfile.close()

results = {}

for record in data:
	year = int(record['date'])
	century = year // 100
	if century not in results:
		results[century] = 0
	results[century] += 1

outputfile = open('04-results-years.tsv', 'w')
outputfile.write('Jahrhundert\tAnzahl\n')
for century in sorted(results):
	outputfile.write(str(century) + '\t' + str(results[century]) + '\n')
outputfile.close()
