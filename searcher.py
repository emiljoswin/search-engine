"""
	The users query is directly given to the whoosh library. It is a search library and returns pages based on their rank 
	using the Okapi BM25 ranking algorithm. This is not the only requirement of us since along with the content of the 
	webpages we also take into consideration the structure of internet. So the results of the search is obtained 
	and among them the pages are ordered on the basis of their pageranks. This will be the final result which will
	be provided to the user. The results are mapped back and appear as links to the respective pages.
"""

from whoosh.qparser import QueryParser
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh import index

#get the urls from the file filename
def geturls(filename):
	f = open(filename,'r')
	urls = []
	for line in f:
		urls.append(line)
	f.close()
	return urls
	
#get pager ranks from the file filename.	
def getpagerank(filename):
	pageranks = {}
	f = open(filename,'r')
	i = 5
	j = 1
	for line in f:
		if i == 0:
			pageranks[j] = line
			j = j + 1
		else:
			i = i - 1
	f.close()
	return pageranks
	
#the resutls are returned in the form of urlnumbers		
def getresult(query):
	res = []
	query = unicode(query)
	with myindex.searcher() as s:
		qp = QueryParser("content", myindex.schema)
		q = qp.parse(query)
		results = s.search(q)
		if len(results) == 0:
			print 'no results were found matching your query'
		
		for result in results:
			#~ print result['path'][59:]
			res.append(result['path'][59:])
			res[-1] = int(res[-1])
			
	return res

#'myindex' is the name of the index to which the contents of the files are stored.
myindex = index.open_dir('myindex')
#the page from where pagerank's are loaded. Output of an octave program			
filename = '/home/emil/workspace/python/project/fresh/crawl/crawldata5/visited_urls/pagerank'	
pageranksdict = getpagerank(filename)
#the page from where visited-urls is found
filename = '/home/emil/workspace/python/project/fresh/crawl/crawldata5/visited_urls/visited-urls'
urls = geturls(filename)
while True:
	query = str(raw_input('Enter the query:: '))
	#to retrieve the page no and corresponding pageranks of those
	#pages that appeared in the results list as the result of a query
	newdict = {}
	if query == '-1':
		break

	results = getresult(query)
	for result in results:
		newdict[result] = pageranksdict[result]
	
	#the dict keys are stored into the urllist in reverse order of
	#the values ie, the pagerank
	urllist = sorted(newdict,key = newdict.get,reverse = True)
	for i in urllist:
		print urls[i-1]
				
