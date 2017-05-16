import json
from os import listdir

class loadData():

    def __init__(self, directory, dataName):
        self.directory = directory
        self.allJSONFiles = sorted([files for files in listdir(directory)])
        self.allReports = []
        self.dataName = dataName

    def getAllReports(self, red, jsonInRedis):
        documentCount = 0
        for file in self.allJSONFiles:
            if jsonInRedis and self.directory == 'trainingData':
                print("---> Loading file into Redis - " + file)
            with open(self.directory + "/" + file, encoding='utf-8') as dataFile:
                data = json.load(dataFile)
                individualReport = data[self.dataName]
                for item in individualReport:
                    documentName = item
                    publishDate = individualReport[item]['webPublicationDate']
                    topics = individualReport[item]['topics']
                    bodyText = individualReport[item]['bodyText']
                    bodyText = bodyText.encode("ascii", "ignore")
                    if (jsonInRedis and self.directory == 'trainingData'):
                        mapDict = {}
                        for j, topic in enumerate(topics):
                            mapDict[j+1] = topic
                        if (mapDict != {}):
                            documentCount += 1
                            keyVal = 'body:' + str(documentCount)
                            topicVal = 'topics:' + str(documentCount)
                            red.set(name=keyVal, value=bodyText)
                            red.hmset(name=topicVal, mapping=mapDict)
                            red.incr(name='totalKeys', amount=1)
                    else:
                        report = singleDataReport(documentName, publishDate,
                                                  topics, bodyText)
                        self.allReports.append(report)

            if (jsonInRedis and self.directory == 'trainingData'):
                red.hset(name='fileStartPosition',
                         key=file,
                         value=documentCount)

        if not jsonInRedis:
            return(self.allReports)


class singleDataReport():
    def __init__(self, documentName, publishDate, topics, bodyText):
        self.topics = topics
        self.publishDate = publishDate
        self.bodyText = bodyText
        self.documentName = documentName
