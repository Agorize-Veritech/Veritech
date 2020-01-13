from bs4 import BeautifulSoup
from requests import get
from googlesearch import search

NUM_QUERIES = 20

## Isolate headline from different providers with different class names ##
#CP24									class="articleHeadline" 	
#Global News 							class="l-article__title"   
#Hamilton News, Hamilton Spectator 		class="ar-title"
#CBC									class="detailHeadline"
#The Star 								class="article-headline"
#National Post							class="headline"
##########################################################################

## Find headlines from articles ##
def scrape(url):
	response = get(url).text
	#print(response.text[:1000])
	soup = BeautifulSoup(response, 'html.parser')
	text = [p.text for p in soup.find_all('p')]
	print(text)


## Get sites based on query ##
def searchQuery(query):
	for i in search(query, tld="co.in", num=NUM_QUERIES, stop=NUM_QUERIES, pause=2):
		#if '/news' in i:
 		# print(i)
 		scrape(i)


query = input("What would you like to know about?")
searchQuery(query)
#url = 'https://www.thestar.com/news/canada/2019/11/27/hamilton-failed-its-citizens-by-not-reporting-sewage-spill-environment-minister-says.html'

#scrape(url)