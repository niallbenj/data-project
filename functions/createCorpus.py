def createCorpusFromRedis(red, numberOfKeys, startingEntry, topicDictionary,
                          singleTopic, singleClassify):
    myLabelMatrix = []
    corpus = []
    for i in range(startingEntry, numberOfKeys+1):
        bodyText = str(red.get('body:' + str(i)))
        topics = red.hgetall('topics:' + str(i))
        holdOneArray = []
        for item in topics:
            holdOneArray.append(topics[item].decode("utf-8"))
        singleTopicArray = topicDictionary.generateMultiLabelArray(holdOneArray,
                                                                   singleTopic)
        if (singleTopicArray != [] or singleClassify):
            if (singleTopicArray == []):
                singleTopicArray = ['blank']
            myLabelMatrix.append(singleTopicArray)
            corpus.append(bodyText)
    return(myLabelMatrix, corpus)


def createCorpusFromFile(justBodies, justTopics, topicDictionary, singleTopic,
                         singleClassify):
    myLabelMatrix = []
    corpus = []
    for i, report in enumerate(justBodies):
        singleTopicArray = topicDictionary.generateMultiLabelArray(justTopics[i], singleTopic)
        theNextBody = report
        if (singleTopicArray != [] or singleClassify):
            if (singleTopicArray == []):
                singleTopicArray = ['blank']
            myLabelMatrix.append(singleTopicArray)
            corpus.append(theNextBody)
        justBodies[i] = None
        justTopics[i] = None
    return(myLabelMatrix, corpus)
