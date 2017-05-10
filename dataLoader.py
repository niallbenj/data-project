import json
from os import listdir
from os.path import isfile, join

<<<<<<< HEAD

class loadData():
=======
class dataLoader():
>>>>>>> 4e9c87b35e823bec78e2e02b54313aa2f2dac3e8

    def __init__(self, directory, dataName):
        self.directory = directory
        self.allJSONFiles = [files for files in listdir(directory)]
        self.allReports = []
        self.dataName = dataName

    def getAllReports(self):
        for file in self.allJSONFiles:
<<<<<<< HEAD
            with open(self.directory + "/" + file, encoding='utf-8') as data_file:
=======
            with open(self.directory + "/" + file) as data_file:
>>>>>>> 4e9c87b35e823bec78e2e02b54313aa2f2dac3e8
                data = json.load(data_file)
                individualReport = data[self.dataName]
                for item in individualReport:
                    documentName = item
                    publishDate = individualReport[item]['webPublicationDate']
                    topics = individualReport[item]['topics']
                    bodyText = individualReport[item]['bodyText']
<<<<<<< HEAD
                    bodyText = bodyText.encode("ascii", "ignore")
                    report = singleDataReport(documentName, publishDate, topics, bodyText)
                    self.allReports.append(report)
        return(self.allReports)

=======
                    report = singleDataReport(documentName, publishDate, topics, bodyText)
                    self.allReports.append(report)
        return self.allReports
>>>>>>> 4e9c87b35e823bec78e2e02b54313aa2f2dac3e8

class singleDataReport():
    def __init__(self, documentName, publishDate, topics, bodyText):
        self.topics = topics
        self.publishDate = publishDate
        self.bodyText = bodyText
        self.documentName = documentName
