import sys
import numpy as np

class readTopics():

    def __init__(self):
        self.lookupList = []
        topicListFile = open("topicDictionary.txt", 'r+')
        topicList = topicListFile.readlines()
        for i, element in enumerate(topicList):
            self.lookupList.append(element.rstrip('\n'))

    def generateMultiLabelArray(self, singleDocumentTopics):
        topicArray = []
        for item in singleDocumentTopics:
            if item in self.lookupList:
                topicArray.append(item)
        return(topicArray)
