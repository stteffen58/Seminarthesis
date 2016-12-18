import warc
import uuid
import sys
import os
import gzip
os.chdir('/home/eckel/')
''' Load and preprocess data '''

print 'preprocessing'
filenameIn = sys.argv[1]
max_range = int(sys.argv[2])
for i in range(0,max_range):
	print filenameIn+str(i)
	fw = warc.open('dataset_id/'+filenameIn+str(i)+'.warc.gz', 'wb')
	with gzip.open('dataset/'+filenameIn+'.com'+str(i)+'.warc.gz', mode='rb') as gzf:
		for record in warc.WARCFile(fileobj=gzf):
			record['WARC-Record-ID'] = str(uuid.uuid4())
			fw.write_record(warc.WARCRecord(payload=record.payload.read(), headers=record.header))
	fw.close()
