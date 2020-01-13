import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
#import spacy


#Scrape article
def getData(url):
	page = requests.get(url).text
	soup = BeautifulSoup(page, 'html.parser')
	text = [p.text for p in soup.find(class_="story-body__inner").find_all('p')]
	#print(url)
	return text


#Turn array into one string
def combineText(text):
	combined_text = ' '.join(text)
	return combined_text


#Clean text
def cleanText(text):

	text = text.lower()
	text = re.sub('\[.*?\]', '', text)
	text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
	text = re.sub('\w*\d\w*', '', text)
	text = re.sub('[''""...‘’“”…]', '', text)
	text = re.sub('\n', '', text)


	lemmatizer = WordNetLemmatizer()
	
	text_token = nltk.word_tokenize(text)
	text = ' '.join([lemmatizer.lemmatize(w) for w in text_token])

	### Figure out better lemmatizer (spaCy?)###
	# lemmatizer = spacy.load('en', disable=['parser','ner'])
	# text = lemmatizer(text)
	# text = " ".join ([token.lemma_ for token in text])
	return text



#################################################################
urls = ['https://www.bbc.com/news/world-us-canada-50663128']
sources = ['bbc']
political_stance = ['center']

articles = [getData(u) for u in urls]

#Save data
# for i, c in enumerate(sources):
# 	with open("articles/" + c + ".txt", "wb") as file:
# 		pickle.dump(articles[i], file)


#Load data
data = {}
for i, c in enumerate(sources):
	with open("articles/" + c + ".txt", "rb") as file:
		data[c] = pickle.load(file)


#Turn array into one string
data_combined = {key: [combineText(value)] for (key, value) in data.items()}


pd.set_option('max_colwidth',150)
#DataFrame - corpus
data_df = pd.DataFrame.from_dict(data_combined).transpose()
data_df.columns = ['article']
data_df = data_df.sort_index()
#print(data_df)


#Clean text
clean = lambda x: cleanText(x)

data_clean = pd.DataFrame(data_df.article.apply(clean))
#print(data_clean)

### SAVE DATAFRAME ###
# data_df['political stance'] = political_stance
# print(data_df)
# data_df.to_pickle("corpus.pkl")

cv = CountVectorizer(stop_words='english')

#Document Term Matrix
data_cv = cv.fit_transform(data_clean.article)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = data_clean.index
#print(data_dtm)

### SAVE DTM ###
# data_dtm.to_pickle("dtm.pkl")

# data_clean.to_pickle("data_clean.pkl")
# pickle.dump(cv, open("cv.pkl", "wb"))









