import sys
import numpy as np

class readTopics():

    def __init__(self):
        self.lookupDictionary = {}
        self.completeTopicList = []
	myFile = open("topicDictionary.txt", 'r+')
	topicList = myFile.readlines()
	    for i, element in enumerate(objects):
     		self.lookupDictionary[element.rstrip('\n')] = i
        return(self.lookupDictionary)

    def generateMultiLabelArray(self, singleDocumentTopics):
	for item in singleDocumentTopics:
	    topicArray.append(self.lookupDictionary[item])
        return(topicArray)
