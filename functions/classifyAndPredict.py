from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from datetime import datetime


def predict(maxDf, minDf, maxFeatures, initialTime, myLabelMatrix, corpus,
            reportsToPredict, topicsInResult, optimize, calculateF1Score):
    provideOutput = True
    tf = TfidfVectorizer(input='content',
                         analyzer='word',
                         ngram_range=(1, 3),
                         max_df=maxDf,
                         min_df=minDf,
                         max_features=maxFeatures,
                         stop_words='english',
                         use_idf=True,
                         sublinear_tf=False,
                         lowercase=True)
    if provideOutput:
        print('Corpus generated --->> ' + str(datetime.now() - initialTime))
    tfidf_matrix = tf.fit_transform(corpus)

    if provideOutput:
        text = 'TFIDF matrix complete -->> '
        print(text + str(datetime.now() - initialTime))
    mlb = MultiLabelBinarizer()
    labeledTopics = mlb.fit_transform(myLabelMatrix)
    # try this?? SVC(kernel='linear')
    # SGDClassifier()
    classifier = OneVsRestClassifier(SVC(kernel='rbf')).fit(tfidf_matrix,
                                                            labeledTopics)

    if provideOutput:
        text = 'Classification complete --->> '
        print(text + str(datetime.now() - initialTime))
    reportToPredictMatrix = tf.transform(reportsToPredict)

    if provideOutput:
        text = 'Created prediction matrix --->> '
        print(text + str(datetime.now() - initialTime))

    y_pred = classifier.predict(reportToPredictMatrix)
    labelsPredicted = mlb.inverse_transform(y_pred)

    # Calculation of F1 score is disabled for now
    return(labelsPredicted, reportsToPredict)
