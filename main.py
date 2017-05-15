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
import redis


#     _____                  _
#    |_   _|                | |
#      | | _ __  _ __  _   _| |_
#      | || '_ \| '_ \| | | | __|
#     _| || | | | |_) | |_| | |_
#     \___/_| |_| .__/ \__,_|\__|
#               | |
#               |_|

# debug = 0 to read from folder `trainingData`
#       = 1 to read from folder `debug`
# jsonInRedis = 0 useful for small cases where everything is read in
#                 (memory intensive)
#             = 1 to store everything in Redis and called one at a time,
#                 useful for loading in multiple `*.json` files
# startingEntry = x / 1547670 - which record to start classifying from
debug = False
jsonInRedis = True
startingEntry = 1350000
np.set_printoptions(threshold=np.nan)

#     _                     _
#    | |                   | |
#    | |     ___   __ _  __| |
#    | |    / _ \ / _` |/ _` |
#    | |___| (_) | (_| | (_| |
#    \_____/\___/ \__,_|\__,_|

dataToLoad = 'debug' if debug else 'trainingData'
dbStore = 14 if debug else 15
load = dataLoader.loadData(dataToLoad, 'TrainingData')
topicDictionary = readTopics.readTopics()
red = redis.Redis(host='localhost', port=6379, db=dbStore)

initialTime = datetime.now()
if (jsonInRedis):
    if (red.exists('totalKeys')):
        print("---> Data will be read from Redis.")
    else:
        load.getAllReports(red, jsonInRedis)
        print("Loading all Reports into Redis --->> " + str(initialTime))
        initialTime = datetime.now() - initialTime
else:
    (justBodies, justTopics) = returnJustBodiesAndTopics(load,
                                                         red,
                                                         jsonInRedis)

print("Loading all Reports for TrainingData --->> " + str(initialTime))
myLabelMatrix = []
corpus = []
if (jsonInRedis):
    numberOfKeys = int(red.get('totalKeys'))
    for i in range(startingEntry, numberOfKeys+1):
        bodyText = str(red.get(''.join(['body:' + str(i)])))
        bodyText = bodyText.decode("utf-8")
        topics = red.hgetall(''.join(['topics:' + str(i)]))
        holdOneArray = []
        for item in topics:
            holdOneArray.append(topics[item].decode("utf-8"))
        singleTopicArray = topicDictionary.generateMultiLabelArray(holdOneArray)
        if (singleTopicArray != []):
            myLabelMatrix.append(singleTopicArray)
            corpus.append(bodyText)
else:
    for i, report in enumerate(justBodies):
        singleTopicArray = topicDictionary.generateMultiLabelArray(justTopics[i])
        theNextBody = report
        if (singleTopicArray != []):
            myLabelMatrix.append(singleTopicArray)
            corpus.append(theNextBody)
        justBodies[i] = None
        justTopics[i] = None

print("Loading all Reports for TestData --->> " + str(datetime.now() - initialTime))
predictData = dataLoader.loadData("testData", 'TestData')
reportsToPredict = []
reportNames = []
topicsInResult = {}
for reportToPredict in predictData.getAllReports(None, False):
    reportsToPredict.append(reportToPredict.bodyText)
    reportNames.append(reportToPredict.documentName)
    if debug:
        t = topicDictionary.generateMultiLabelArrayTest(reportToPredict.topics)
        topicsInResult[reportToPredict.documentName] = t

#     _____ _               _  __
#    /  __ \ |             (_)/ _|
#    | /  \/ | __ _ ___ ___ _| |_ _   _
#    | |   | |/ _` / __/ __| |  _| | | |
#    | \__/\ | (_| \__ \__ \ | | | |_| |
#     \____/_|\__,_|___/___/_|_|  \__, |
#                                  __/ |
#                                 |___/

inputVar = (initialTime, myLabelMatrix, corpus, reportsToPredict,
            topicsInResult, debug, classifyAndPredict, calculateF1Score)
if (debug):
    optimizer.optimizer(inputVar)
else:
    (labelsPredicted, reportsToPredict) = optimizer.optimizer(inputVar)

#         __       _____  _____  _   _
#         \ \     /  __ \/  ___|| | | |
#     _____\ \    | /  \/\ `--. | | | |
#    |______> >   | |     `--. \| | | |
#          / /    | \__/\/\__/ /\ \_/ /
#         /_/      \____/\____/  \___/

header = ['id'] + topicDictionary.lookupList
notInTraining = notInTrainingList.notTrained()
exclude = set(string.punctuation)
with open('Results/Submission.csv', 'w', newline='') as outcsv:
    csvWriter = csv.writer(outcsv)
    csvWriter.writerow(header)

    count = 0
    for reportName, labels in zip(reportNames, labelsPredicted):
        myBodyText = makeAGuess.reshapeBodyText(reportsToPredict[count])
        newLabels = makeAGuess.guess(labels, notInTraining)
        if (jsonInRedis):
            red = redis.Redis(host='localhost', port=6379, db=16)

        count += 1

        printToSubmissionCSV.toCSV(csvWriter, reportName,
                                   labels, topicDictionary.lookupList)

print("CSV written / Run complete --->>" + str(datetime.now() - initialTime))
