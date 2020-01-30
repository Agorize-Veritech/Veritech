import re
import string
import csv
import pandas

def readFile():
	
	# extracted_text = pandas.read_csv('veritech-dataset/articles.csv', encoding='utf8')
	# print(extracted_text.info())
	# df = extracted_text[extracted_text['content']]
	# print(extracted_text.head())
	
	extracted_text = []
	line = 0
	with open('veritech-dataset/articles.csv', encoding='utf8') as file:
		read = csv.reader(file)
		for row in read:
			if line == 0:
				line += 1
				pass
			else:
				row[0] = rmRandomChars(row[0])
				row[2] = rmRandomChars(row[2])
				row[4] = cleanText(row[4])
				extracted_text.append(row)
				# temp = extracted_text[line-1].pop(4)
				# extracted_text[line-1].append(cleanText(temp))

	return extracted_text


def writeFile(extracted_text):
	with open('veritech-dataset/cleaned-articles.csv', 'w', encoding='utf8') as file:
		writer = csv.writer(file,lineterminator = '\n')
		for i in extracted_text:
			writer.writerow(i)


def rmRandomChars(text):
	text = ''.join([x for x in text if x.isascii()])

	return text


def cleanText(text):
	text = text.lower()
	text = re.sub('\[.*?\]', '', text)
	text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
	text = re.sub('\w*\d\w*', '', text)
	text = re.sub('[''""...‘’“”…]', '', text)
	text = re.sub('\n', '', text)

	text = rmRandomChars(text)

	return text

cleaned_data = readFile()
#print(cleaned_data)
writeFile(cleaned_data)
print("DATA EXTRACTED, CLEANED AND SAVED")