class readTopics():

    def __init__(self):
        self.lookupList = []
        self.lookupSet = []
        topicListFile = open("topicDictionary.txt", 'r+')
        topicList = topicListFile.readlines()
        for i, element in enumerate(topicList):
            self.lookupList.append(element.rstrip('\n'))
            self.lookupSet.append(element.rstrip('\n'))

    def generateMultiLabelArray(self, singleDocumentTopics, singleTopic):
        topicArray = []
        for item in singleDocumentTopics:
            if not singleTopic:
                if item in self.lookupList:
                    topicArray.append(item)
            else:
                if item == singleTopic:
                    topicArray.append(item)
            if item in self.lookupSet:
                self.lookupSet.remove(item)
        return(topicArray)

    def generateMultiLabelArrayTest(self, singleDocumentTopics):
        topicArray = []
        for item in singleDocumentTopics:
            topicArray.append(item)
        return(topicArray)
