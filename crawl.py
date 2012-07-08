"""
	This is web crawler. It takes as input a root url, the maximum depth to be crawled and the total number of links to be 
	visited per page. The crawling starts from the root url. It follows a depth limited depth first search (DFS). The
	contents of pages successfully visited are stored for indexing. Also a matrix containing information
	regarding pages that links other pages are stored. We call this "Bit Matrix".
"""
from bs4 import BeautifulSoup
import urllib2
import os
import re
import codecs

visited = []
listed = []
listed = [] # to insert already found url so that they are inserted only into the uppermost node in the tree.

def save_big_matrix():
	file = open('big_matrix','w')
	for row in big_matrix:
		for element in row:
			file.write(str(element) + " ")
		file.write('\n')

def rewrite_big_matrix():
	index = []
	listedurls = []
	for url in listed:
		if url not in visited:
			print url , " " , listed.index(url)
			index.append(listed.index(url))
		else:
			listedurls.append(url)	
	index = sorted(index, reverse = True)
	for i in index:
		for row in big_matrix:
			print row
			row.pop(i)
	print big_matrix			
	print listedurls

def fill_big_matrix(page,urls):
	big_matrix.append([])
	position = visited.index(page)
	for i in range(len(listed)):
		big_matrix[position].append(0)
		
	for url in urls:
		if url in listed:
			big_matrix[position][listed.index(url)] = big_matrix[position][listed.index(url)] + 1
		else:
			listed.append(url)
			big_matrix[position].append(1)

def complete_big_matrix():
	size = len(big_matrix[-1])
	for row in big_matrix:
		diff = size - len(row) 
		for i in range(diff):
			row.append(0)
			
	print big_matrix
								
def write_text(text, n):
	file = codecs.open(str(n),'w','utf-8')
	file.write(text)
	file.close()

def write_visited_urls(visited):
	os.mkdir('visited_urls')
	os.chdir('visited_urls')
	file = open('visited-urls','w')
	for url in visited:
		file.write(url + '\n')
	file.close()	
	
def expand(page,max_n):
	urls = []
	try:
		request = urllib2.Request(page)
		request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
		response = urllib2.urlopen(request)
		
		"""
		urlfile = urllib2.urlopen(page)
		content = urlfile.read()"""
		soup = BeautifulSoup(response)
		text = soup.get_text()
		print 'visiting',page
		for url in soup.find_all('a',attrs={'href': re.compile("^http://")}):
			link = url['href']
			# add a link only if it is not previously found(so 'listed' lis) and not if it was only previously visited
			if link not in listed: 
				listed.append(link)
				urls.append(url['href'])
				print len(url), ' ', url['href']
			if len(urls) >= max_n:
				break
	except :
		print 'error visiting ', page
		return None, None

	return urls,text
	
def dfs(page,depth,max_n):	
	if depth == 0 or page == None:
		return		
	urls,text = expand(page,max_n)
	if page not in visited:
		visited.append(page)
		if not text == None:
			write_text(text,len(visited))
		print len(visited), page
		
	if urls == None:
		return
		
	for url in urls:
		if url not in visited:
			dfs(url,depth-1,max_n)
			
	return visited

page = str(raw_input('Enter root url::'))
depth = int(raw_input('Enter depth::'))
max_n = int(raw_input('Enter max_n::'))
os.mkdir('crawldata3')
os.chdir('crawldata3')

visited = dfs(page,depth,max_n)

"""for link in visited:
	print link.encode('ascii')"""
	
