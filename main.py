import dataLoader
import stemmer
import readTopics
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.sparse.csr import csr_matrix
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
import sys
import time

load = dataLoader.loadData("testData")
reports = load.getAllReports()
topicDictionary = readTopics.readTopics()

print(len(topicDictionary.lookupDictionary))
myLabelMatrix = []
labelstrings = []
corpus = []
reportToPredict = [reports[6].bodyText, reports[10].bodyText]
tf = TfidfVectorizer(input='content', analyzer='word', ngram_range=(1,1),
                     min_df = 0, sublinear_tf=True)
print ('initial time')
initialTime = time.time()
print (initialTime)
for report in reports:
    myLabelMatrix.append(topicDictionary.generateMultiLabelArray(report.topics))
    #wordsWithoutPunctuation = stemmer.getWords(report.bodyText)
    #stemmedWords = stemmer.stemWords(wordsWithoutPunctuation)
    #removedStopWords = stemmer.removeStopWords(stemmedWords)
    #corpus.append(removedStopWords)
    corpus.append(report.bodyText)

print ('end of loop')
print ((time.time()- initialTime )/60)
tfidf_matrix = tf.fit_transform(corpus)
reportToPredictMatrix = tf.transform(reportToPredict)
print('reportToPredictmatrix made')
print ((time.time()- initialTime )/60)
labeledTopics = MultiLabelBinarizer().fit_transform(myLabelMatrix)
print('created labeled topics')
print ((time.time()- initialTime )/60)
classifier = OneVsRestClassifier(SGDClassifier()).fit(tfidf_matrix, labeledTopics)
print('done classification')
y_pred = classifier.predict(reportToPredictMatrix)

print ((time.time()- initialTime )/60)
print("check result!")
print(y_pred)
