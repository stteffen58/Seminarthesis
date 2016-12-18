import warc
import uuid
import os
os.chdir('/home/eckel/')

f = warc.open("samples/overstock_sample.warc.gz", "rb")
fw = warc.open("overstock_test.warc.gz", "wb")
count = 0
for record in f:
	if record['WARC-Record-ID'] == '2dd726fe-5f11-43c3-a02c-47860e668cac' or record['WARC-Record-ID'] == '4b3e1e5f-9ac3-4619-b784-a093a1d1ac0d':
		payload = record.payload.read()
		record_header = record.header
		fw.write_record(warc.WARCRecord(payload=payload,headers=record.header))
		fw.write_record(warc.WARCRecord(payload=payload,headers=record.header))
		fw.write_record(warc.WARCRecord(payload=payload,headers=record.header))
		fw.write_record(warc.WARCRecord(payload=payload,headers=record.header))
	#elif count < 2:
	#	payload = record.payload.read()
        #       record_header = record.header
	#	fw.write_record(warc.WARCRecord(payload=payload,headers=record.header))
	#	count += 1
f.close()
fw.close()
