import warc
import sys
import gzip
import os
os.chdir('/home/eckel/')
domain = str(sys.argv[1])

f = open('correspondences/'+domain+'_sim.txt','r')
warc_ids = set()

for line in f:
	s = line.split()
	warc_ids.add(s[0])
	warc_ids.add(s[1])
f.close()

filename = 'samples/'+domain+'_sample.warc.gz'
f = open('urls_extracted/'+domain+'urls.txt','w')
with gzip.open(filename, mode='rb') as gzf:
	for record in warc.WARCFile(fileobj=gzf):
		record_id = record['WARC-Record-ID']
		if record_id in warc_ids:
			print record_id
			uri = record['WARC-Target-URI']
			f.write(record_id + ' ' + uri + '\n')
f.close()
