"""	
	The contents of pages which were store are indexed using a library called whoosh. It uses the Okapi BM-25 algorithm.
	It rank matching documents according to their relevance to a given search query. The number of occurences 
	of words are given importance rather than their relative proximity.
"""
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh import index
from whoosh.qparser import QueryParser
import os,os.path
import codecs

schema = Schema(path=ID(unique=True,stored=True),content=TEXT)
dir = raw_input('Enter the index directory name:: ')
if not os.path.exists(dir):
	print 'creating dir', dir, '...'
	os.mkdir(dir)

myindex = index.create_in(dir,schema)
writer = myindex.writer()
doc_source_path = str(raw_input('enter the source of documents:: '))

print 'indexing....'
for file in os.listdir(doc_source_path):
	if file == 'visited_urls':
		continue
		
	file = doc_source_path + '/' + str(file)
	fileobj = codecs.open(file, 'r', 'utf-8')
	text = fileobj.read()
	writer.add_document(path = unicode(file),content = unicode(text))
	
writer.commit()
print 'done indexing'

