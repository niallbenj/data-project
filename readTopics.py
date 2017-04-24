import sys
import numpy as np

class readTopics():

    def __init__(self):
        self.lookupDictionary = {}
        self.completeTopicList = []
        self.topicNotInTopicList = []
        myFile = open("topicDictionary.txt", 'r+')
        topicList = myFile.readlines()
        for i, element in enumerate(topicList):
            self.lookupDictionary[element.rstrip('\n')] = i

    def generateMultiLabelArray(self, singleDocumentTopics):
        topicArray = []
        for item in singleDocumentTopics:
            if item in self.lookupDictionary:
                topicArray.append(self.lookupDictionary[item])
            else:
                self.topicNotInTopicList.append(item)
        return(topicArray)
