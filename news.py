import re
from newsapi import NewsApiClient
from datetime import date
from bs4 import BeautifulSoup
from requests import get
import io
import nltk
import heapq

api = "8916083bfcea422fa2e4fa70f2e903c7"
url_list = []
date = date.today()
newsapi = NewsApiClient(api_key=api)
domains = ''

#summarizes an input text using natural language toolkit
def summarizer (text):
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    formatted_text = re.sub('[^a-zA-Z]', ' ', text)
    formatted_text = re.sub(r'\s+', ' ', formatted_text)

    sentence_list = nltk.sent_tokenize(text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

query = "hamilton"
#Gets news articles for a given search query
for i in range(1):
    all_articles = newsapi.get_everything(q=query,
                                          sources='bbc-news,the-verge',
                                          domains='bbc.co.uk,techcrunch.com',
                                          from_param='2020-01-10',
                                          to=date,
                                          language='en',
                                          sort_by='relevancy',
                                          page=i+1)["articles"]
    #writes the hyperlinks and the summary to a text file
    f = open("links.txt","a")
    for x in all_articles:
        url_list.append(x["url"])
        f.write(x["url"]+"\n")
    f.close()

counter = 0
#Using beautiful soup, get all the p tags from a given url. We use p tags because generally speaking sites use p tags for article content
#As we develop, we can make unique functions for each source so the data is cleaner
for x in url_list:
    text = ""
    f = open("newsclips/"+str(counter)+".txt","a", encoding="utf-8")
    response =get(x)
    soup = BeautifulSoup(response.text,'html.parser')
    page = soup.find_all('p')

    for x in page:
        text += x.getText() + "\n"

    out = summarizer(text)
    f.write(out)
    f.close()
    counter += 1


