from bs4 import BeautifulSoup as bs
import urllib.request as url
import re
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import sent_tokenize
import heapq
import sys


link = sys.argv[1]
source = url.urlopen(link).read()
soup = bs(source, 'lxml')

text = ''
for para in soup.find_all('p'):
    text += para.text

text = re.sub(r'\[[0-9]*\]', ' ', text)
text = re.sub(r'\s+', ' ',text)
text_modified = text.lower()
text_modified = re.sub(r'\W', ' ', text_modified)
text_modified = re.sub(r'\d', ' ', text_modified)
text_modified = re.sub(r'\s+', ' ', text_modified)

sentences = sent_tokenize(text)
words = word_tokenize(text_modified)
stoplist = stopwords.words('english')


w2c = {}
for word in words:
    if word not in stoplist:
        if word not in w2c.keys():
            w2c[word] = 1
        else:
            w2c[word] += 1
            
for key in w2c:
    w2c[key] = w2c[key] / max(w2c.values())


sent2score = {}
for sentence in sentences:
    for word in word_tokenize(sentence.lower()):
        if word in w2c.keys():
            if len(sentence.split(' ')) < 25:
                if sentence not in sent2score.keys():
                    sent2score[sentence] = w2c[word]
                else:
                    sent2score[sentence] += w2c[word]


best_sent = heapq.nlargest(5, sent2score, key = sent2score.get)

for i in best_sent:
    print('----------------------------------------------------------------------------------------------------------')
    print(i)