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
import functions.storeInRedis as storeInRedis
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
debug = 0
jsonInRedis = 0
np.set_printoptions(threshold=np.nan)

#     _                     _
#    | |                   | |
#    | |     ___   __ _  __| |
#    | |    / _ \ / _` |/ _` |
#    | |___| (_) | (_| | (_| |
#    \_____/\___/ \__,_|\__,_|

dataToLoad = 'debug' if debug == 1 else 'trainingData'
load = dataLoader.loadData(dataToLoad, 'TrainingData')

topicDictionary = readTopics.readTopics()
(justBodies, justTopics) = returnJustBodiesAndTopics(load)

initialTime = datetime.now()
print("Loading all Reports for TrainingData --->> " + str(initialTime))
myLabelMatrix = []
corpus = []
for i, report in enumerate(justBodies):
    singleTopicArray = topicDictionary.generateMultiLabelArray(justTopics[i])
    theNextBody = report
    if (singleTopicArray != []):
        myLabelMatrix.append(singleTopicArray)
        corpus.append(theNextBody)
        if debug == 1:
            pass
            # print(individualTopicArray)
    justBodies[i] = None
    justTopics[i] = None

initialTime = datetime.now()
print("Loading all Reports for TestData --->> " + str(initialTime))
predictData = dataLoader.loadData("testData", 'TestData')
reportsToPredict = []
reportNames = []
topicsInResult = {}
for reportToPredict in predictData.getAllReports():
    reportsToPredict.append(reportToPredict.bodyText)
    reportNames.append(reportToPredict.documentName)
    if debug == 1:
        t = topicDictionary.generateMultiLabelArrayTest(reportToPredict.topics)
        topicsInResult[reportToPredict.documentName] = t

# call the optimizer
# If optimizing then then don't return anything to write to file. Just exit
# and calculate F1 scores.
inputs = (initialTime, myLabelMatrix, corpus,
          reportsToPredict, topicsInResult, debug)
if (debug == 0):
    (reportNames, labelsPredicted, reportsToPredict) = optimizer(inputs)
else:
    optimizer(inputs)


# WRITE THE CSV
header = ['id'] + topicDictionary.lookupList
notInTraining = notInTrainingList()
exclude = set(string.punctuation)
with open('Results/Submission.csv', 'w', newline='') as outcsv:
    csvWriter = csv.writer(outcsv)
    csvWriter.writerow(header)

    count = 0
    for reportName, labels in zip(reportNames, labelsPredicted):
        newText = reportsToPredict[count]
        newText = newText.decode()
        newText = ''.join(ch for ch in newText if ch not in exclude)
        newText = newText.split()
        myBodyText = [str(x).lower() for x in newText]
        for newLabel in notInTraining:
            value = 0
            totalCount = 0
            if newLabel in labels:
                pass
            else:
                for item in notInTraining[newLabel]:
                    if item in myBodyText:
                        value = value + 1
                        totalCount = totalCount + myBodyText.count(item)
                if (value == len(notInTraining[newLabel])):
                    if (totalCount > 6):
                        labels = labels + (newLabel, )
        count += 1


        printToSubmissionCSV(csvWriter,
                             reportName,
                             labels,
                             topicDictionary.lookupList)

print(datetime.now() - initialTime)
