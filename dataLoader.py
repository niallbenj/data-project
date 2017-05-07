import json
from os import listdir
from os.path import isfile, join

class dataLoader():

    def __init__(self, directory, dataName):
        self.directory = directory
        self.allJSONFiles = [files for files in listdir(directory)]
        self.allReports = []
        self.dataName = dataName

    def getAllReports(self):
        for file in self.allJSONFiles:
            with open(self.directory + "/" + file) as data_file:
                data = json.load(data_file)
                individualReport = data[self.dataName]
                for item in individualReport:
                    documentName = item
                    publishDate = individualReport[item]['webPublicationDate']
                    topics = individualReport[item]['topics']
                    bodyText = individualReport[item]['bodyText']
                    report = singleDataReport(documentName, publishDate, topics, bodyText)
                    self.allReports.append(report)
        return self.allReports

class singleDataReport():
    def __init__(self, documentName, publishDate, topics, bodyText):
        self.publishDate = publishDate
        self.topics = topics
        self.bodyText = bodyText
        self.documentName = documentName
