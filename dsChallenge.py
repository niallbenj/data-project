import json
from os import listdir
from os.path import isfile, join
import singleDataReport

class loadData():

    def __init__(self, direct):
        self.directory = direct
        self.allJSON = [files for files in listdir(direct)]
        self.allReports = []

    def returnData(self):
        for singleFile in self.allJSON:
            myFile = json.loads(open(self.directory + "/" + singleFile).read())
            entries = myFile['TrainingData']
            for item in entries:
                publishDate = entries[item]['webPublicationDate'] 
                topics = entries[item]['topics']
                bodyText = entries[item]['bodyText']
                report = singleDataReport.singleDataReport(publishDate, topics, bodyText)
                self.allReports.append(report)
        return self.allReports
        


load = loadData("testData")
result = load.returnData()
for report in result:
    print report.bodyText
