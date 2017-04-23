from nltk.stem import *
import re

def getWords(text):
    return re.compile('\w+').findall(text)

def stemParagraph(paragraph):
    stemmer = PorterStemmer();
    singles = [stemmer.stem(word) for word in paragraph]
    print(singles)

