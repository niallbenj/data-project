import dataLoader
import readTopics
import numpy as np
from datetime import datetime
import csv
import string
import functions.notInTrainingList as notInTrainingList
import functions.returnJustBodiesAndTopics as returnJustBodiesAndTopics
import functions.printToSubmissionCSV as printToSubmissionCSV
import functions.optimizer as optimizer
import functions.classifyAndPredict as classifyAndPredict
import functions.calculateF1Score as calculateF1Score
import functions.makeAGuess as makeAGuess
import functions.staticValues as staticValues
import functions.basicInput as basicInput
import functions.createCorpus as createCorpus
import functions.important as important
import functions.storeBestResults as storeBestResults
import functions.includeSingleTopics as includeSingleTopics
import redis


def mainProcess(singleTopic, onlyOne):
    '''
         _____                  _
        |_   _|                | |
          | | _ __  _ __  _   _| |_
          | || '_ \| '_ \| | | | __|
         _| || | | | |_) | |_| | |_
         \___/_| |_| .__/ \__,_|\__|
                   | |
                   |_|
    '''

    np.set_printoptions(threshold=np.nan)
    inputs = basicInput.basic()
    (optimize, allTrainingData, jsonInRedis, latestFileNumber, includeSingles) = inputs

    '''
          _                     _
         | |                   | |
         | |     ___   __ _  __| |
         | |    / _ \ / _` |/ _` |
         | |___| (_) | (_| | (_| |
         \_____/\___/ \__,_|\__,_|
    '''
    dataToLoad = 'trainingData' if allTrainingData else 'subsetTraining'
    dbStore = 15 if allTrainingData else 14
    load = dataLoader.loadData(dataToLoad, 'TrainingData')
    topicDictionary = readTopics.readTopics()
    red = redis.Redis(host='localhost', port=6379, db=dbStore)

    initialTime = datetime.now()
    if jsonInRedis:
        if (red.exists('totalKeys')):
            print("---> Data will be read from Redis.")
        else:
            loadTime = datetime.now()
            load.getAllReports(red, jsonInRedis)
            text = "Loaded all Reports into Redis --->> "
            print(text + str(datetime.now() - loadTime))

    else:
        (justBodies, justTopics) = returnJustBodiesAndTopics(load, red,
                                                             jsonInRedis)

    '''
          ____
         / ___|___  _ __ _ __  _   _ ___
        | |   / _ \| '__| '_ \| | | / __|
        | |__| (_) | |  | |_) | |_| \__ \
         \____\___/|_|  | .__/ \__,_|___/
                        |_|
    '''

    print("Loading all Reports for TrainingData --->> " + str(initialTime))
    if jsonInRedis:
        fileStart = load.allJSONFiles[-latestFileNumber]
        numberOfKeys = int(red.get('totalKeys'))
        startingEntry = basicInput.fileThresholds(red, fileStart)
        output = createCorpus.createCorpusFromRedis(red, numberOfKeys,
                                                    startingEntry,
                                                    topicDictionary,
                                                    singleTopic,
                                                    singleClassify)
        (myLabelMatrix, corpus) = output
    else:
        output = createCorpus.createCorpusFromFile(justBodies, justTopics,
                                                   topicDictionary,
                                                   singleTopic,
                                                   singleClassify)
    (myLabelMatrix, corpus) = output

    text = "Loading all Reports for TestData --->> "
    print(text + str(datetime.now() - initialTime))
    predictData = dataLoader.loadData("testData", 'TestData')
    reportsToPredict = []
    reportNames = []
    topicsInResult = {}
    for reportToPredict in predictData.getAllReports(None, False):
        reportsToPredict.append(reportToPredict.bodyText)
        reportNames.append(reportToPredict.documentName)
        if optimize:
            t = topicDictionary.generateMultiLabelArray(reportToPredict.topics, singleTopic)
            topicsInResult[reportToPredict.documentName] = t

    '''
         _____ _               _  __
        /  __ \ |             (_)/ _|
        | /  \/ | __ _ ___ ___ _| |_ _   _
        | |   | |/ _` / __/ __| |  _| | | |
        | \__/\ | (_| \__ \__ \ | | | |_| |
         \____/_|\__,_|___/___/_|_|  \__, |
                                      __/ |
                                     |___/
    '''

    if (optimize):
        (bestLabels, num) = optimizer.optimizer(initialTime, myLabelMatrix,
                                                corpus, reportsToPredict,
                                                topicsInResult, optimize,
                                                classifyAndPredict,
                                                calculateF1Score,
                                                singleTopic)
        if (num == 0):
            return
        storeBestResults.store(redis, singleTopic, reportNames, bestLabels)
        return
    else:
        (minDf, maxDf, maxFeatures) = staticValues.static()
        classificationRes = classifyAndPredict.predict(maxDf, minDf,
                                                       maxFeatures,
                                                       initialTime,
                                                       myLabelMatrix,
                                                       corpus,
                                                       reportsToPredict,
                                                       topicsInResult,
                                                       optimize, None)
        (labelsPredicted, reportsToPredict) = classificationRes

    '''
         _____  _____  _   _
        /  __ \/  ___|| | | |
        | /  \/\ `--. | | | |
        | |     `--. \| | | |
        | \__/\/\__/ /\ \_/ /
         \____/\____/  \___/
    '''

    header = ['id'] + topicDictionary.lookupList
    notInTraining = notInTrainingList.notTrained()
    exclude = set(string.punctuation)
    with open('Results/Submission.csv', 'w', newline='') as outcsv:
        csvWriter = csv.writer(outcsv)
        csvWriter.writerow(header)

        count = 0
        for reportName, labels in zip(reportNames, labelsPredicted):
            myBodyText = makeAGuess.reshapeBodyText(reportsToPredict[count],
                                                    exclude)
            newLabels = makeAGuess.guess(labels, notInTraining, myBodyText)

            if includeSingles:
                labels = includeSingleTopics.include()

            printToSubmissionCSV.toCSV(csvWriter, reportName, newLabels,
                                       topicDictionary.lookupList)

        text = "CSV written / Run complete --->> "
        print(text + str(datetime.now() - initialTime))


if __name__ == '__main__':
    '''
    singleClassify = True for a binary single classification or empty
                   = False for normal classification process
    ignore = True then ignore the fact that sets already exist in redis
           = False only allow new entries in impList to be accessed
    improveOneTopic = True then target a specific label to include more
                           labels
                    = False then see above
    improveName = '' A string of the label to improve on
    '''
    singleClassify = True
    ignore = True
    improveOneTopic = False
    improveName = ''

    if singleClassify:
        if improveOneTopic:
            impList = [improveName]
        else:
            impList = important.important()
        red = redis.Redis(host='localhost', port=6379, db=7)
        for j, singleTopic in enumerate(impList):
            if (red.exists(singleTopic) and ignore):
                print(str(singleTopic) + " already exists!")
            else:
                mainProcess(singleTopic, singleClassify)
                text = "Completed ---->>>>>>>> " + str(j) + " / "
                print(text + str(len(impList)) + " : " + str(impList[j]))
    else:
        mainProcess(None, singleClassify)
