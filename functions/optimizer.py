import sys
import random


def optimizer(initialTime, myLabelMatrix, corpus, reportsToPredict,
              topicsInResult, debug, classifyAndPredict, calculateF1Score):
    if not debug:
        minDf = 0.00009
        maxDf = 0.99
        maxFeatures = 60000
        classificationRes = classifyAndPredict.predict(maxDf, minDf, maxFeatures,
                                               initialTime, myLabelMatrix,
                                               corpus, reportsToPredict,
                                               topicsInResult, debug,
                                               None)
        (labelsPredicted, reportsToPredict) = classificationRes
        return(labelsPredicted, reportsToPredict)
    else:
        F = open("f1Results.txt", "a")
        F.write("minDf, maxDf, maxFeatures, numberOfFiles, f1Score \n")
        variables = valuesToIncrement()
        loops = variables[0]
        minDf = variables[1]
        maxDf = variables[3]
        maxFeatures = variables[5]
        for i in range(loops):
            minDf += variables[2]
            for j in range(loops):
                maxDf += variables[4]
                for x in range(loops):
                    maxFeatures += variables[6]
                    print("loading file " + str(x) + " / " + str(loops))
                    numberOfFiles = 2
                    classifyInput = (maxDf, minDf, maxFeatures, initialTime,
                                     myLabelMatrix, corpus, reportsToPredict,
                                     topicsInResult, debug, calculateF1Score)
                    classificationRes = classifyAndPredict.predict(classifyInput)
                    (labelsPredicted, reportsToPredict, totalf1) = classificationRes
                    stringToWrite = str(minDf) + ", " + str(maxDf) + ", " + str(maxFeatures) + ", " + str(numberOfFiles) + str(totalf1) + "\n"
                    F.write(stringToWrite)

    sys.exit("Check results")


def valuesToIncrement():
    loops = 30
    minDfRangeLo = 0.0
    minDfRangeHi = 0.1
    maxDfRangeLo = 0.8
    maxDfRangeHi = 1.0
    maxFeaturesLo = 25000
    maxFeaturesHi = 70000

    minDfInc = (minDfRangeHi - minDfRangeLo)/float(loops)
    maxDfInc = (maxDfRangeHi - maxDfRangeLo)/float(loops)
    maxFeaturesInc = int((maxFeaturesHi - maxFeaturesLo)/float(loops))
    return(loops, minDfRangeLo - minDfInc, minDfInc
           maxDfRangeLo - maxDfInc, maxDfInc,
           maxFeaturesLo - maxFeaturesInc, maxFeaturesInc)
