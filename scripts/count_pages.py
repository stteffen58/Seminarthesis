'''
script for counting what kind of pages are contained in sample, e.g. products, errors, other (like disclaimers)
'''

import sys
import os
import gzip
import warc
from bs4 import BeautifulSoup
os.chdir('/home/eckel')

filename = 'samples/'+sys.argv[1]+'_sample.warc.gz'
l_product = []
l_search = []
l_other = []

with gzip.open(filename, mode='rb') as gzf:
	products = 0
	search = 0
	other = 0
	for record in warc.WARCFile(fileobj=gzf):
		bs = BeautifulSoup(record.payload.read(),'html.parser')
		anchor1 = "mainContent"
		anchor2 = "search-results"
		if bs.find("section", {"id": anchor1}):
			products += 1
			l_product.append(record['WARC-Record-ID'])
		elif bs.find("div", {"id": anchor2}):
			search += 1
			l_search.append(record['WARC-Record-ID'])
		else:
			other += 1
			l_other.append(record['WARC-Record-ID'])

f = open('log','w')
f.write('amount search ' + str(search) + '\n')
f.write(' '.join(l_search))
f.write('\n')
f.write('amount products ' + str(products) + '\n')
f.write(' '.join(l_product))
f.write('\n')
f.write('amount others ' + str(other) + '\n')
f.write(' '.join(l_other))
f.write('\n')
f.close()

