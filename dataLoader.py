import json
from os import listdir
from os.path import isfile, join

class loadData():

    def __init__(self, directory, dataName):
        self.directory = directory
        self.allJSONFiles = [files for files in listdir(directory)]
        self.allReports = []
        self.dataName = dataName

    def getAllReports(self):
        for file in self.allJSONFiles:
            myFile = json.loads(open(self.directory + "/" + file).read())
            individualReport = myFile[self.dataName]
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
