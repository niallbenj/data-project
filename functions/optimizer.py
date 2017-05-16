

def optimizer(initialTime, myLabelMatrix, corpus, reportsToPredict,
              topicsInResult, optimize, classifyAndPredict, calculateF1Score,
              singleTopic):
    bestScore = -1000000
    variables = valuesToIncrement()
    loops = variables[0]
    startingMinDf = variables[1]
    startingMaxDf = variables[3]
    startingMaxFeatures = variables[5]
    minDf = startingMinDf
    maxDf = startingMaxDf
    maxFeatures = startingMaxFeatures

    # Begin looping over results..
    print("\n" + "Results for ---> " + str(singleTopic) + " <---")
    print("minDf, maxDf, maxFeatures, singleClassifyCount")
    for i in range(loops):
        minDf += variables[2]
        maxDf = startingMaxDf
        maxFeatures = startingMaxFeatures
        for j in range(loops):
            maxDf += variables[4]
            maxFeatures = startingMaxFeatures
            for k in range(loops):
                maxFeatures += variables[6]
                out = singleLoop(maxDf, minDf, maxFeatures, initialTime,
                                 myLabelMatrix, corpus, reportsToPredict,
                                 topicsInResult, optimize, calculateF1Score,
                                 classifyAndPredict, singleTopic)
                (singleClassifyCount, labelsPredicted) = out
                text = printOutput(minDf, maxDf, maxFeatures,
                                   singleClassifyCount)
                print(text)
                (bestLabels, bestScore) = checkClosest(singleClassifyCount,
                                                       singleTopic,
                                                       labelsPredicted,
                                                       bestScore)
    return(bestLabels, singleClassifyCount)


def singleLoop(maxDf, minDf, maxFeatures, initialTime, myLabelMatrix, corpus,
               reportsToPredict, topicsInResult, optimize, calculateF1Score,
               classifyAndPredict, singleTopic):
    classificationRes = classifyAndPredict.predict(maxDf, minDf, maxFeatures,
                                                   initialTime, myLabelMatrix,
                                                   corpus, reportsToPredict,
                                                   topicsInResult, optimize,
                                                   calculateF1Score)
    (labelsPredicted, reportsToPredict) = classificationRes
    singleClassifyCount = 0
    for labels in labelsPredicted:
        checkLabel = list(labels)
        if singleTopic in checkLabel:
            singleClassifyCount += 1
    return(singleClassifyCount, labelsPredicted)


def valuesToIncrement():
    loops = 1
    minDfRangeLo = 0.0
    minDfRangeHi = 0.0
    maxDfRangeLo = 1.0
    maxDfRangeHi = 1.0
    maxFeaturesLo = 60000
    maxFeaturesHi = 60000

    minDfInc = (minDfRangeHi - minDfRangeLo)/float(loops)
    maxDfInc = (maxDfRangeHi - maxDfRangeLo)/float(loops)
    maxFeaturesInc = int((maxFeaturesHi - maxFeaturesLo)/float(loops))
    return(loops, minDfRangeLo - minDfInc, minDfInc,
           maxDfRangeLo - maxDfInc, maxDfInc,
           maxFeaturesLo - maxFeaturesInc, maxFeaturesInc)


def printOutput(minDf, maxDf, maxFeatures, singleClassifyCount):
    text = ''
    text += str(minDf) + ", "
    text += str(maxDf) + ", "
    text += str(maxFeatures) + ", "
    text += str(singleClassifyCount)
    return(text)


def checkClosest(singleClassifyCount, singleTopic, labelsPredicted, bestScore):
    closest = listOfGuesses(singleTopic)
    if (abs(closest - singleClassifyCount) < abs(closest - bestScore)):
        bestScore = singleClassifyCount
        bestLabels = labelsPredicted
    return(bestLabels, bestScore)


def listOfGuesses(singleTopic):
    bigList = {'afghanistan': 422,
               'aid': 161,
               'arabandmiddleeastprotests': 270,
               'criminaljustice': 256,
               'defence': 174,
               'ebola': 460,
               'economy': 712,
               'egypt': 233,
               'france': 523,
               'germany': 346,
               'hacking': 129,
               'humanrights': 554,
               'immigration': 529,
               'india': 320,
               'iraq': 648,
               'isis': 805,
               'israel': 443,
               'libya': 179,
               'localgovernment': 173,
               'london': 1011,
               'metropolitanpolice': 141,
               'military': 369,
               'naturaldisasters': 228,
               'nuclearweapons': 141,
               'police': 561,
               'protest': 464,
               'religion': 859,
               'russia': 520,
               'surveillance': 193,
               'southafrica': 217,
               'syria': 388,
               'terrorism': 195,
               'transport': 379,
               'uksecurity': 323,
               'unitednations': 336,
               'ukcrime': 847}

    # Still do analysis on topics that arent the top hits
    # - this could be for fine tuning down the line
    if singleTopic not in bigList:
        return(0)
    else:
        return(bigList[singleTopic])
