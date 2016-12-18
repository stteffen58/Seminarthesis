from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

sys.path.append('SparseLSH-master/sparselsh/')

from lsh import LSH
from collections import defaultdict
from scipy.sparse import csr_matrix
from preprocessing import TFIDF
from preprocessing import HTMLPreprocessing

import numpy
import csv
import os
import uuid
import gzip
import warc

os.chdir('/home/eckel/')

''' load data '''
filenameIn = sys.argv[1]
datasetPath = 'dataset_id/'
max_files = int(sys.argv[2])
threshold = float(sys.argv[3])
doc_dict = {}
doc_uri = {}
doc_count = 0
print 'start preprocessing'
for i in range(0,max_files):
	print filenameIn+str(i)
	with gzip.open(datasetPath+filenameIn+str(i)+'.warc.gz', mode='rb') as gzf:
		for record in warc.WARCFile(fileobj=gzf):
			record_id = record['WARC-Record-ID']
			payload = record.payload.read()
			doc_uri[record_id] = record['WARC-Target-URI']
			text  = HTMLPreprocessing(payload).get_text()
			doc_dict[record_id] = text
			doc_count += 1

print 'create vectors'
tfidf = TFIDF(doc_dict)
vect_length = tfidf.vect_length # length of the input vector
num_hashtables = 1 # number of iterations
digest_length = 50
print 'perform lsh'
lsh = LSH(digest_length,vect_length,num_hashtables=num_hashtables)
for i,k in enumerate(tfidf._id_list):
    vect = tfidf.get_vector(i)
    lsh.index(vect,extra_data=tfidf._id_list[i])

''' Query documents '''
dedup = set()
keys = lsh.hash_tables[0].keys()
for key in keys:
	bucket = lsh.hash_tables[0].get_val(key)
	for query_object in bucket:
		candidates = lsh.query(query_object[0],distance_func='cosine')
		dedup.add(query_object[1])
		for c in candidates:
			candidate_key = c[0][1] # warc id is appended as extra data in lsh.index()
			if candidate_key == query_object[1]:
				continue
			candidate_distance = c[1]
			if float(candidate_distance) >= threshold:
				dedup.add(candidate_key)
			elif candidate_key in dedup:
				dedup.remove(candidate_key)

file = warc.open(filenameIn+'_dedup.warc.gz','wb')
numSingle = len(dedup)
for i in range(0,max_files):
	with gzip.open(datasetPath+filenameIn+str(i)+'.warc.gz', mode='rb') as gzf:
		for record in warc.WARCFile(fileobj=gzf):
			record_id = record['WARC-Record-ID']
			if record_id in dedup:
				payload = record.payload.read()
		    	file.write_record(warc.WARCRecord(payload=payload,headers=record.header))

print 'Total pages: ' + str(doc_count)
print 'Pages after deduplication: ' + str(numSingle)

file.close()

