from __future__ import division, unicode_literals
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from scipy.sparse import csr_matrix

from sklearn.feature_extraction.text import TfidfVectorizer as vectorizer
from sklearn.feature_extraction.text import HashingVectorizer as hashvectorizer
from bs4 import BeautifulSoup

class HTMLPreprocessing():
	def __init__(self,html_doc):
		self._html_doc = html_doc
		self._soup = BeautifulSoup(self._html_doc, 'html.parser')
		for script in self._soup(["script", "style"]):
			script.extract()
	
	def get_text(self):
         text = self._soup.get_text()
         '''lines = (line.strip() for line in text.splitlines())
         chunks = (phrase.strip() for line in lines for phrase in line.split(' '))
         return ' '.join(chunk for chunk in chunks if chunk)'''
         return text

class TFIDF():
    def __init__(self,doc_dict):
        #self._n_features = 100000
        self._tfidf_vectorizer = vectorizer(tokenizer=self.tokens,stop_words='english')
        self._doc_term_matr = self._tfidf_vectorizer.fit_transform(doc_dict.values())
        #self.vect_length = len(self._tfidf_vectorizer.vocabulary_)
        self.vect_length = self._doc_term_matr.shape[1]
        #self._vect_list = []
        self._id_list = []
        for i,k in enumerate(doc_dict):
            #self._vect_list.append(self._doc_term_matr[i])
            self._id_list.append(k)
        #doc_dict.clear() # release memory

    def tokens(self, x):
	return x.split()
	
    def get_vector(self, index):
        return self._doc_term_matr[index]#.toarray()[0]
    
