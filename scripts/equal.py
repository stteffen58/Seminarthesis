from __future__ import division, unicode_literals
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from bs4 import BeautifulSoup

import gzip
import warc
import os
import re

os.chdir('/home/eckel')

def remove_space(text):
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split(' '))
	joined = ' '.join(chunk for chunk in chunks if chunk)
	return re.sub(r'\W+','',joined)

domain = (sys.argv[1])
filename = 'samples/'+domain+'_sample.warc.gz'
doc_dict = {}
count = 0
print 'load' 
if not os.path.exists('cache/'+domain+'_cached.txt'):
	with gzip.open(filename, mode='rb') as gzf:
		cache = open('cache/'+domain+'_cached.txt','w')
		for record in warc.WARCFile(fileobj=gzf):
			record_id = record['WARC-Record-ID']
			text = record.payload.read()
			soup = BeautifulSoup(text, 'html.parser')
			for script in soup(["script", "style"]):
				script.extract()
			text_split = remove_space(soup.get_text()).split()
			text_split.sort
			text = ' '.join(text_split)
			doc_dict[record_id] = text
			cache.write(record_id+'\n')
			cache.write(text+'\n')
		cache.close()
else:
	cache = open('cache/'+domain+'_cached.txt','r')
	while True:
		record_id = cache.readline().strip()
		if not record_id:
			break
		text = cache.readline().strip()
		doc_dict[record_id] = text
	cache.close() 

print 'check'		
with open('correspondences/'+domain+'_sim.txt','r') as f:
	for i,line in enumerate(f):
		tokens = line.split()
		doc1 = doc_dict[tokens[0]]
		doc2 = doc_dict[tokens[1]]
		if i == 128:
			s = open('test.txt','w')
			s.write(doc_dict[tokens[0]]+'\n\n'+ doc_dict[tokens[1]])
			s.close()
		if doc1 == doc2:
			print 'line: ' + str(i)
