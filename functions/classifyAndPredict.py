from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from datetime import datetime


def predict(maxDf, minDf, maxFeatures, initialTime, myLabelMatrix,
                       corpus, reportsToPredict, topicsInResult, debug,
                       calculateF1Score):
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

    print('Corpus generated --->> ' +
          str(datetime.now() - initialTime))
    tfidf_matrix = tf.fit_transform(corpus)

    print('TFIDF matrix complete -->> ' +
          str(datetime.now() - initialTime))
    mlb = MultiLabelBinarizer()
    labeledTopics = mlb.fit_transform(myLabelMatrix)
    classifier = OneVsRestClassifier(SGDClassifier()).fit(tfidf_matrix,
                                                          labeledTopics)

    print('Classification complete --->> ' +
          str(datetime.now() - initialTime))
    reportToPredictMatrix = tf.transform(reportsToPredict)
    print('Created prediction matrix --->> ' +
          str(datetime.now() - initialTime))

    y_pred = classifier.predict(reportToPredictMatrix)
    labelsPredicted = mlb.inverse_transform(y_pred)

    if debug:
        totalf1 = calculateF1Score.F1(topicsInResult, labelsPredicted)
        print('F1 Score --->> ' + str(totalf1))
        print("check result! --->> " + str(datetime.now() - initialTime))
        return(labelsPredicted, reportsToPredict, totalf1)
    else:
        return(labelsPredicted, reportsToPredict)
