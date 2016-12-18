from bs4 import BeautifulSoup

import re
import warc
import gzip
import os
import sys
os.chdir('/home/eckel/')

def extract_href(text):
	bs = BeautifulSoup(text,'html.parser')
	hrefs = []
	for a in bs.find_all('a', href=True):
		url = a['href']
		i = url.find('?')
		if i == -1:
			hrefs.append(url)
		else:
			hrefs.append(url[0:i])
	hrefs.sort()
	return ' '.join(hrefs)

def concatenate(bs):
	if isinstance(bs, list):
		for tag in bs:
			for script in tag(["script", "style"]):
				script.extract()
		text = ' '.join(c.get_text() for c in bs)
	else:
		for script in bs(["script", "style"]):
			script.extract()
		text = bs.get_text()
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split(' '))
	joined = ' '.join(chunk for chunk in chunks if chunk)
	cleaned = re.sub(r'\W+', ' ', joined).split()
	cleaned.sort()
	return ' '.join(cleaned)

def remove_space(text,id):
	bs = BeautifulSoup(text,'html.parser')
	anchor1 =  "productListForm"
	text = ''
	if bs.find("div", {"id": anchor1}):
		bs = bs.find("div", {"id": anchor1})
		text = concatenate(bs)
	else:
		print 'tag not found!'
		print id
		text = concatenate(bs)
	return text
	
def compare_content(doc0,doc1):
	doc0_split = doc0.split()
	doc1_split = doc1.split()
	for i,word in enumerate(doc0_split):
		try:
			if word != doc1_split[i]:
				return str(doc0_split[i-10:i+10]) + ',' + str(doc1_split[i-10:i+10])
		except IndexError:
			return 'IndexError'
	return 'Euqal!'
	
def compare_hrefs(doc0,doc1):
	doc0_split = doc0.split()
	doc1_split = doc1.split()
	for i,word in enumerate(doc0_split):
		try:
			if word != doc1_split[i]:
				return str(doc0_split[i]) + ',' + str(doc1_split[i])
		except IndexError:
			return 'IndexError'
	return 'href euqal!'

domain = sys.argv[1]

corpus_file = 'samples/'+domain+'_sample.warc.gz'
gzf =  gzip.open(corpus_file, mode='rb')
doc_dict_content = {}
doc_dict_hrefs = {}
for record in  warc.WARCFile(fileobj=gzf):
	content = record.payload.read()
	doc_dict_content[record['WARC-Record-ID']] = remove_space(content,record['WARC-Record-ID'])
	doc_dict_hrefs[record['WARC-Record-ID']] = extract_href(content)

corrs_file = 'correspondences/'+domain+'_sim.txt'
label_file = 'labels/'+domain+'_label.txt'
corrs = open(corrs_file,'r')
labels = open(label_file,'w')

doc0 = ''
doc1 = ''
for i,line in enumerate(corrs):
	corr = line.split()
	if corr[2] == '0.0':
		labels.write(corr[0] + ' ' + corr[1] + ' ' + corr[2] + ' ' + 'tp' + '\n')
		continue
	for id in doc_dict_content:
		if id == corr[0]:
			doc0 = doc_dict_content[id]
			href0 = doc_dict_hrefs[id] 
		elif id == corr[1]:
			doc1 = doc_dict_content[id]
			href1 = doc_dict_hrefs[id] 
		elif doc0 and doc1:
			result_content = compare_content(doc0,doc1)
			result_hrefs = compare_hrefs(href0,href1)
			print str(i) + ' ' + corr[0] +  ' ' + corr[1] + ' ' + corr[2]
			print result_content
			print result_hrefs
			v = raw_input("tp or fp? ")
			labels.write(corr[0] + ' ' + corr[1] + ' ' + corr[2] + ' ' + v + '\n')
			doc0 = ''
			doc1 = ''
			gzf.close()
			break
corrs.close()
labels.close()
