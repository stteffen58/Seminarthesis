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
import gzip
import warc

os.chdir('/home/eckel/')

''' load data '''
filenameIn = sys.argv[1]
datasetPath = 'samples/'
threshold = float(sys.argv[2])
doc_dict = {}
doc_uri = {}
doc_count = 0
print 'start preprocessing'
with gzip.open(datasetPath+filenameIn+'_sample.warc.gz', mode='rb') as gzf:
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
digest_length = 0
print 'perform lsh'
lsh = LSH(digest_length,vect_length,num_hashtables=num_hashtables)
for i,k in enumerate(tfidf._id_list):
    vect = tfidf.get_vector(i)
    lsh.index(vect,extra_data=tfidf._id_list[i])

''' Query documents '''
dedup = set()
keys = lsh.hash_tables[0].keys()
i=0
for key in keys:
	bucket = lsh.hash_tables[0].get_val(key)
	for query_object in bucket:
		candidates = lsh.query(query_object[0],distance_func='cosine')
		for c in candidates:
			candidate_key = c[0][1] # warc id is appended as extra data in lsh.index()
			if candidate_key == query_object[1]:
				continue
			if str(query_object[1]) <= str(candidate_key):
				candidate_distance = c[1]
				if float(candidate_distance) >= threshold:
					dedup.add((query_object[1],candidate_key,candidate_distance,'false'))
				else:
					dedup.add((query_object[1],candidate_key,candidate_distance,'true'))
			sys.stdout.write("\rDoing thing %i" % i)
			sys.stdout.flush()
			i+=1

print 'sort and write to file'
l = list(dedup)
l = sorted(l,key=lambda x:x[2])
with open('goldstandard/'+filenameIn,'w') as f:
	for e in l:
		f.write(str(e[0]) + ' ' + str(e[1]) + ' ' + str(e[2]) + ' ' + str(e[3]) + '\n')
	f.flush()
print 'finish'


