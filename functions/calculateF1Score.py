def F1(topicsInResult, labelsPredicted):
    averagef1 = 0.0
    for i, document in enumerate(topicsInResult):
        predictedLabels = labelsPredicted[i]
        trueP = 0
        falseP = 0
        falseN = 0
        predictedLength = len(predictedLabels)
        realLength = len(topicsInResult[document])
        if (predictedLength == 0) and (realLength == 0):
                f1Score = 1.0
        else:
            for item in predictedLabels:
                if (item in topicsInResult[document]):
                    trueP += 1
                else:
                    falseP += 1
            for item in topicsInResult[document]:
                if (item not in predictedLabels):
                    falseN += 1
            f1Score = (2.0*trueP)/(2.0*trueP + falseP + falseN)

        averagef1 = f1Score + averagef1

    totalf1 = (averagef1)/float(i+1)
    return(totalf1)
