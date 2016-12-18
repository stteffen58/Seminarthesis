from __future__ import division, unicode_literals
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import warc
import random
import uuid
import gzip

domain = str(sys.argv[1])
max = int(sys.argv[2])
per_warc = 100/max
filename_sample = '../'+domain+'_sample.warc.gz'

for i in range(0,max):
	count = 0
#	filename = '../dataset/'+domain+'.com'+str(i)+'.warc.gz'
	filename = '../samples/'+domain+'_sample.warc.gz'
	print 'Load'+filename
	try:
		with gzip.open(filename,'rb') as gfz:
			''' Load file '''
			contents = [(warc.WARCRecord(payload=record.payload.read(),headers=record.header)) for record in warc.WARCFile(fileobj=gfz)]
			l = len(contents)
	except:
		continue	
	
	''' select records randomly '''
	print 'select'
	f_sample = warc.open(filename_sample,'a')
	while count < per_warc:
		rand = random.randint(0,l-1)
		sys.stdout.write("\rRecord count %i" % count)
		sys.stdout.flush()
		r = contents[rand]
		#pre = preprocessing.HTMLPreprocessing(r.payload)
		payload = r.payload
		r['Content-Length'] = str(len(payload))
		r['WARC-Record-ID'] = str(uuid.uuid4())
		f_sample.write_record(warc.WARCRecord(payload=payload,headers=r.header))
		count += 1
	print '\n'
	f_sample.close()
	
