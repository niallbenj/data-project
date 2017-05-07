import dataLoader
import readTopics
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.sparse.csr import csr_matrix
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
import sys
from datetime import datetime
import csv

def PrintToSubmissionCSV(csvWriter, reportName, labelsInReport, allLabels):
    csvRow = [0] * len(allLabels)
    for label in labelsInReport:
        csvRow[allLabels.index(label)] = 1
    csvRow.insert(0, reportName)
    csvWriter.writerow(csvRow)

def GetBodyTextAndTopics(directory, jsonName):
    topicDictionary = readTopics.readTopics()
    topics = []
    bodyTexts = []
    dataLoad = dataLoader.dataLoader(directory, jsonName)
    for report in dataLoad.getAllReports():
        reducedTopics = topicDictionary.generateMultiLabelArray(report.topics)
        if reducedTopics:
            topics.append(reducedTopics)
            bodyTexts.append(report.bodyText)
    return(topics, bodyTexts)

def CreateClassifier(topics, bodyTexts, vectorizer, multiLabelBinarizer):
    tfidf_matrix = vectorizer.fit_transform(bodyTexts)
    print('tfidf matrix made')

    labeledTopics = multiLabelBinarizer.fit_transform(topics)
    print('created labeled topics')
    classifier = OneVsRestClassifier(SGDClassifier(n_jobs = 1)).fit(tfidf_matrix, labeledTopics)
    print('done classification')
    return classifier

def PredictTestData(vectorizer, classifier, mlb):
    predictData = dataLoader.dataLoader("testData", 'TestData')

    reportsToPredict = []
    reportNames = []
    for reportToPredict in predictData.getAllReports():
        reportsToPredict.append(reportToPredict.bodyText)
        reportNames.append(reportToPredict.documentName)

    reportToPredictMatrix = vectorizer.transform(reportsToPredict)
    print('reportToPredictmatrix made')

    y_pred = classifier.predict(reportToPredictMatrix)
    all_labels = mlb.inverse_transform(y_pred)

    print("check result!")

    topicDictionary = readTopics.readTopics()
    header = ['id'] + topicDictionary.lookupList
    with open('Results/Submission.csv', 'w', newline='') as outcsv:
        csvWriter = csv.writer(outcsv)

        csvWriter.writerow(header)

        for reportName, labels in zip(reportNames, all_labels):
            PrintToSubmissionCSV(csvWriter,
                                 reportName,
                                 labels,
                                 topicDictionary.lookupList)

def main():
    print ('initial time')
    initialTime = datetime.now()
    print (initialTime)

    vectorizer = TfidfVectorizer(input='content',
                         analyzer='word',
                         ngram_range=(1,3),
                         min_df = 0.00009,
                         max_features = 200000,
                         stop_words = 'english',
                         use_idf = True,
                         sublinear_tf=False)

    topics, bodyTexts = GetBodyTextAndTopics("trainingData", 'TrainingData')
    print ('Loaded all topics and bodyTexts')
    print (datetime.now() - initialTime )

    mlb = MultiLabelBinarizer()
    classifier = CreateClassifier(topics, bodyTexts, vectorizer, mlb)

    PredictTestData(vectorizer, classifier, mlb)

    print('Completed')
    print (datetime.now() - initialTime )

if __name__ == "__main__":
    main()
