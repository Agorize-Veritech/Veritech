import requests
import json
from bs4 import BeautifulSoup

url = ('https://newsapi.org/v2/everything?'
       'sources=cnn&'
       'from=2019-12-24&'
       'language=en&'
       'apiKey=8916083bfcea422fa2e4fa70f2e903c7')

response = requests.get(url)
data = response.json()

# print (response.json())
# print(data['articles'])

def scrape(url):
	response = requests.get(url).text
	#print(response.text[:1000])
	soup = BeautifulSoup(response, 'html.parser')
	text = [p.text for p in soup.find_all('p')]
	# text = [soup.get_text()]
	print(text)

for i in (data['articles']):
	scrape(i['url'])
	print (i['url'])





