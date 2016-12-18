
import warc 
import gzip
import sys
import os

os.chdir('/home/eckel/')

amount_records = 0
domain = str(sys.argv[1])
max = int(sys.argv[2])
#for i in range(0,max):
#try:
for i in range(0,max):
	filename = 'dataset/'+domain+'.com'+str(i)+'.warc.gz'
	print filename
	with gzip.open(filename, mode='rb') as gzf:
		for record in warc.WARCFile(fileobj=gzf):	
			record.payload.read()
			amount_records += 1
#except:
#	print sys.exc_info()[1]
#	amount_records += 1
print amount_records
