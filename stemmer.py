from nltk.stem import *
from nltk.corpus import stopwords
import re

def getWords(text):
    return re.compile('\w+').findall(text)

def stemWords(words):
    stemmer = SnowballStemmer("english");
    singles = [stemmer.stem(word) for word in words]
    return singles

def removeStopWords(words):
    stop = set(stopwords.words('english'))
    return ([i for i in words if i not in stop])



