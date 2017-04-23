from nltk.stem import *
from nltk.corpus import stopwords
import re

def getWords(text):
    return re.compile('\w+').findall(text)

def stemWords(words):
    stemmer = SnowballStemmer("english", ignore_stopwords=True);
    singles = [stemmer.stem(word) for word in words]
    return singles

def removeStopWords(words):
    stop = set(stopwords.words('english'))
    print([i for i in words if i not in stop])



