from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

sys.path.append('SparseLSH-master/sparselsh/')

from lsh import LSH
from preprocessing import TFIDF
from collections import defaultdict
import warc
import time
import gzip
import preprocessing as pre
import os

os.chdir('/home/eckel/')
domain = str(sys.argv[1])
log = ''
''' Load and preprocess data '''
log += str(time.asctime( time.localtime(time.time())))+'\n'
print time.asctime( time.localtime(time.time()))
log += 'preprocessing\n'
print 'preprocessing'
filename = 'samples/'+domain+'_sample.warc.gz'
doc_dict = {} 
record_count = 0 
with gzip.open(filename, mode='rb') as gzf:
	for record in warc.WARCFile(fileobj=gzf):
		record_id = record['WARC-Record-ID']
		payload = record.payload.read()
		text = pre.HTMLPreprocessing(payload).get_text()
		if text.strip():
			doc_dict[record_id] = text
			record_count+=1

log += "amount warc records: " + str(record_count) + '\n'
print "amount warc records: " + str(record_count)

log += str(time.asctime( time.localtime(time.time()))) + '\n'
print time.asctime( time.localtime(time.time()))

''' Transform each document into tfidf and index documents '''
log += 'create tfidf vectors of documents\n'
print 'create tfidf vectors of documents'
tfidf = TFIDF(doc_dict)

''' Perform lsh '''
print time.asctime(time.localtime(time.time()))
digest_length = int(sys.argv[2])
vect_length = tfidf.vect_length
num_hashtables = 1
log += 'perform lsh with hash-length: ' + str(digest_length) + ', vect-length: ' + str(vect_length) + ', num-hashtables: ' + str(num_hashtables) + '\n'
print 'perform lsh with hash-length: ' + str(digest_length) + ', vect-length: ' + str(vect_length) + ', num-hashtables: ' + str(num_hashtables)
r = {"dict":None}
lsh = LSH(digest_length,vect_length,storage_config=r,num_hashtables=num_hashtables)
for i,k in enumerate(tfidf._id_list):
    vect = tfidf.get_vector(i)
    lsh.index(vect,extra_data=tfidf._id_list[i])

''' Query documents '''
log += str(time.asctime( time.localtime(time.time()))) + '\n'
log += 'query documents\n'
print time.asctime( time.localtime(time.time()))
print 'Query documents'
distance_func = "cosine"

corr = set()

for i,key in enumerate(tfidf._id_list):
	query_object = tfidf.get_vector(i)
	candidates = lsh.query(query_object,distance_func=distance_func)
	for c in candidates:
		candidate_key = c[0][1] # warc id is appended as extra data in lsh.index()
		candidate_distance = c[1]
		if str(key) < str(candidate_key):
			candidate = (key,candidate_key,candidate_distance)
			corr.add(candidate)

corr_list = list(corr)
corr_list = sorted(corr_list,key=lambda x:x[2])

f = open('correspondences/'+domain+'_sim.txt','w')
for t in corr_list:
	f.write(t[0] + ' ' + t[1] + ' ' + str(t[2]) + '\n')
f.close()
print time.asctime(time.localtime(time.time()))
log += str(time.asctime( time.localtime(time.time()))) + '\n'
log += 'finish\n'
f_log = open(domain+'_log.txt','w')
f_log.write(log)
f_log.close()
