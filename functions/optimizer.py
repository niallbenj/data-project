import sys
import classifyAndPredict
import random


def optimizer(initialTime, myLabelMatrix, corpus, reportsToPredict,
              topicsInResult, debug):
    if (debug == 0):
        minDf = 0.00009
        maxDf = 0.99
        maxFeatures = 300000
        classificationRes = classifyAndPredict(maxDf, minDf, maxFeatures,
                                               initialTime, myLabelMatrix,
                                               corpus, reportsToPredict,
                                               topicsInResult, debug)
        (labelsPredicted, reportsToPredict) = classificationRes
        return(labelsPredicted, reportsToPredict)
    else:
        F = open("f1Results.txt", "a")
        F.write("minDf, maxDf, maxFeatures, numberOfFiles, f1Score \n")
        for i in range(30):
            for j in range(30):
                for x in range(30):
                    print("loading file " + str(x) + " /100")
                    numberOfFiles = 2
                    #
                    # Need to just increment these things!!
                    #
                    minDf = random.uniform(0.0, 0.1)
                    maxDf = random.uniform(0.8, 1.0)
                    maxFeatures = random.randint(25000, 70000)
                    classifyInput = (maxDf, minDf, maxFeatures, initialTime,
                                     myLabelMatrix, corpus, reportsToPredict,
                                     topicsInResult, debug)
                    classificationRes = classifyAndPredict(classifyInput)
                    (labelsPredicted, reportsToPredict, totalf1) = classificationRes
                    stringToWrite = str(minDf) + ", " + str(maxDf) + ", " +
                                    str(maxFeatures) + ", " +
                                    str(numberOfFiles) + str(totalf1) + "\n"
                    F.write(stringToWrite)

    sys.exit("Check results")
